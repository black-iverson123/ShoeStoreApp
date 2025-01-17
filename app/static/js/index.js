function buyProduct(productId) {
    const quantityInput = document.getElementById(`quantity-${productId}`);
    const sizeInput = document.getElementById(`size-${productId}`);
    const quantity = parseInt(quantityInput.value, 10);
    const size = parseInt(sizeInput.value, 10)

    if (isNaN(quantity && size) || (quantity && size) < 1) {
        alert("Please enter a valid quantity and size.");
        return;
    }

    fetch('/add_to_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken() // Include CSRF token if CSRF protection is enabled
        },
        body: JSON.stringify({ product_id: productId, quantity: quantity, size:size })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Failed to add product to cart.');
    })
    .then(data => {
        const flashContainer = document.getElementById('flash-container');
        if (flashContainer) {
            flashContainer.innerHTML = ''; // Clear old messages
            data.flash_messages.forEach(flash => {
                const alertDiv = document.createElement('div');
                alertDiv.className = `alert alert-${flash.category} alert-dismissible fade show`;
                alertDiv.role = 'alert';
                alertDiv.innerHTML = `
                    ${flash.message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                `;
                flashContainer.appendChild(alertDiv);
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while adding the product to the cart.');
    });
}


// Helper function to retrieve CSRF token (if CSRF protection is enabled in Flask)
function getCSRFToken() {
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    return csrfMeta ? csrfMeta.getAttribute('content') : '';
}


function newUser() {
    alert("Kindly log in to your account to make a purchase !!!")
}

function toggleForm() {
    const form = document.getElementById('popupForm');
    // Toggle visibility: if it's hidden, show it; if it's shown, hide it
    if (form.style.display === "block") {
        form.style.display = "none";
    } else {
        form.style.display = "block";
    }
}

function comingSoon() {
    alert("Payment feature to be integrated soon!!!")
}
