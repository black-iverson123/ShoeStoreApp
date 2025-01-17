from app import app, db
from flask import render_template, redirect, url_for, request, flash, jsonify, session, get_flashed_messages
from app.forms import Register, Login, Contact, Stocks
from app.models import User, Messages, Products
from flask_login import login_user, logout_user, login_required, current_user
import base64

@app.route("/", methods=['GET', 'POST'])
def home():
    """View function that queries the database using Products model
        and populates fields dynamically using jinja template, also
        uses flask current user authentication to determine user status.     

    Returns:
        _type_(html page): returns index.html which contains homepage
    """
    products = Products.query.all()
    #converting saved binary file to Base64
    for product in products:
        if product.image:
            product.image_base64 = base64.b64encode(product.image).decode('utf-8')
        else:
            product.image_base64 = None
    return render_template("index.html", products=products)

@app.route('/register', methods=['GET','POST'])
def register():
    """View function that returns an account creation page and redirects
        on successful action and send user informative messages, then redireects
        user to login page

    Returns:
        _type_(login): This is the redirected view function
        __type__(html page): returns a register.html page intilally
    """
    form = Register()
    if form.validate_on_submit():
        user = User(username=form.username.data, contact=form.contact.data,
                    email=form.email.data, contact_address=form.contact_address.data)
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully", "success")
        
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """View function handles user authentication and sesssion handling
       before letting user enjoy full app capabilities

    Returns:
        _type_(home): view function returned after a successful autentication
        _type_(html page): renders index.html page
    """
    form = Login(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Bad login Credentials!!!", "danger")
            return redirect(url_for('login'))
        
        
        login_user(user)
        session['name'] = user.username
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """View function to logout current user from the platform

    Returns:
        _type_(login): returns login view function
    """
    logout_user()
    return redirect(url_for('login'))
    

@app.route('/contact-us', methods=['GET', 'POST'])
def contact():
    """View function that renders a contact form and saves to database

    Returns:
        _type(home)_: returns view function for homepage
        _type_(html page): returns contact.html page
    """
    form = Contact()
    if form.validate_on_submit():
        message = Messages(name=form.name.data, email=
                           form.email.data, message=form.message.data)
        db.session.add(message)
        db.session.commit()
        
        flash("Your message has been sent!!!", "success")
        
        return redirect(url_for('home'))
    
    return render_template('contact.html', form=form)

@app.route('/about-us', methods=['GET'])
def about():
    """View funtion returns the about of web app 

    Returns:
        _type_(html page): renders about.html
    """
    return render_template('about.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """View function for users to create and upload products, and displays
        products created and owned by current user. images stored in database 
        as binary are retrieved and encode to base64 before rendering

    Returns:
        _type_(dashboard): returns itself
        _type_(html page): returns dashboard.html as a page
    """
    form = Stocks()
    if form.validate_on_submit():
        image = form.image.data
        product = Products(
            product_name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            description=form.description.data,
            image=image.read(),
            created_by=current_user.id
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('dashboard'))

    # Fetch all products for the current user
    products = Products.query.filter_by(created_by=current_user.id).all()

    # Convert image to base64 for each product
    for product in products:
        if product.image:
            product.image_base64 = base64.b64encode(product.image).decode('utf-8')
        else:
            product.image_base64 = None

    return render_template('dashboard.html', form=form, products=products)


@app.route('/cart', methods=["GET", "POST"])
@login_required
def cart():
    """View function that handles users selected list of products, then
        performs a sum calculation before passing variables 

    Returns:
        _type_(html page): returns htmlpage with variables
    """
    cart_items = session['cart']
    total_price = sum(product['price'] * product['quantity'] for product in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)
    
@app.route('/add_to_cart', methods=["POST"])
@login_required
def add_to_cart():
    """View function is responsible revieving json data serviced by
        ajax code from client-side then checks for validity giving appropriate
        responses where needed(messages returned json style). if values are 
        acceptable queries products table in database, decodes images checks if 
        query returns none before next action to add cart selections to session
        managed by server side. 

    Returns:
        _type_(json): dictionary datatype used to exchange information to ajax code
    """
    data = request.get_json()
    #print(f"Received data: {data}") #viewing recieved data 
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    size = data.get('size')

    if not product_id or not quantity or not size:
        #print("Invalid input") #viewung server error
        flash("Invalid input provided!", "danger")
        return jsonify({
            "message": "Invalid input",
            "flash_messages": [{"category": "danger", "message": "Invalid input provided!"}]
        }), 400

    product = Products.query.get(product_id)
    # converting image to base64
    product.image = base64.b64encode(product.image).decode('utf-8')
    print(f"Image base64: {product.image}")  # Ensure the image is base64 encoded

    if not product:
        print(f"Product with ID {product_id} not found.")  # Log missing product
        flash("Product not found.", "danger")
        return jsonify({
            "message": "No product found",
            "flash_messages": [{"category": "danger", "message": "Product not found."}]
        }), 404

    cart = session.get('cart', [])
    quantity = int(quantity)
    for item in cart:
        if item['id'] == product.id:
            item['quantity'] += quantity
            flash(f"Updated quantity for {product.product_name}.", "info")
            break
    else:
        cart.append({
            'id': product.id,
            'name': product.product_name,
            'price': product.price,
            'quantity': quantity,
            'image_base64': product.image,
            'size': size
        })
        flash(f"{product.product_name} added to cart!", "success")

    session['cart'] = cart

    flash_messages = [{"category": category, "message": message} for category, message in get_flashed_messages(with_categories=True)]
    #print(flash_messages)  # view flashed messages

    return jsonify({
        "message": f"{product.product_name} has been added to cart",
        "flash_messages": flash_messages
    }), 200

@app.route('/remove_from_cart<int:product_id>', methods=["GET","POST"])
def remove_from_cart(product_id):
    """View function responsible for deletion of cart object in user session

    Args:
        product_id (int): This is the product id in the products table of the database

    Returns:
        _type_(cart): returns cart view function
    """
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['id'] != product_id]
        session.modified = True
        flash(f'Product removed', "success")
    return redirect(url_for('cart'))