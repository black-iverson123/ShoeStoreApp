from app import app, db
from app.models import User, Products

@app.shell_context_processor
def make_shell_context():
    """This allows direct interaction with database and
       models in the flask shell

    Returns:
        _type_: db, User and Products variables
    """
    return {'db': db, 'User':User, 'Products':Products}


if __name__ == "__main__":
    app.app_context().push()
    db.create_all()
    app.run(debug=True)