
const addButtons = document.querySelectorAll(".add-btnn");

const cartItems = document.getElementById("cart-items");
const mobileCart = document.getElementById("mobile-cart");

const dateTime =document.getElementById("date-time");

const subtotalElement = document.getElementById("subtotal");
const taxElement = document.getElementById("tax");
const grandTotalElement = document.getElementById("grand-total");

const clearCartBtn = document.getElementById("clear-cart-btn");
const generateBillBtn = document.getElementById("generate-bill");

const receiptModal = document.getElementById("receipt-modal");
const receiptItems = document.getElementById("receipt-items");
const receiptSubtotal = document.getElementById("receipt-subtotal");
const receiptTax = document.getElementById("receipt-tax");
const receiptGrandTotal = document.getElementById("receipt-grandtotal");
const closeReceiptBtn = document.getElementById("close-receipt-btn");

let cart = JSON.parse(localStorage.getItem("cart")) || [];

function saveCart() {
    localStorage.setItem("cart", JSON.stringify(cart));
}

addButtons.forEach(button => {  //event listener

    button.addEventListener("click", () => {

        const name = button.dataset.name;
        const category = button.dataset.category;
        const price = parseFloat(button.dataset.price);

        addToCart(name, category, price);

    });

});

clearCartBtn.addEventListener("click", () => {
    cart = [];
    localStorage.removeItem("cart");
    displayCart();
});

generateBillBtn.addEventListener("click", () => {
    saveOrder();
});

closeReceiptBtn.addEventListener("click", () => {
    receiptModal.style.display = "none";
});

function addToCart(name, category, price){
    const existingItem = cart.find(item => item.name === name);
    if(existingItem){
        existingItem.quantity += 1;
    }
    else{
        cart.unshift({      //push to diplay in ascending and unshift to descending
            name: name,
            category: category,
            price: price,
            quantity: 1
        });
    }

    displayCart();
    saveCart();
}

function displayCart(){
    cartItems.innerHTML = "";
    mobileCart.innerHTML = "";
    if(cart.length === 0){  
    cartItems.innerHTML = `

        <tr>
            <td colspan="5" class="empty-cart">
                Your cart is empty
            </td>
        </tr>

    `;
    mobileCart.innerHTML = `<div class="empty-cart">Your cart is empty</div>`;

    subtotalElement.innerText = "₹0.00";
    taxElement.innerText = "₹0.00";
    grandTotalElement.innerText = "₹0.00";
    return;
}

    let subtotal = 0;

    cart.forEach(item => {
        const itemTotal = item.price * item.quantity;
        subtotal += itemTotal;

        cartItems.innerHTML += `

            <tr>
                <td>${item.name}</td>
                <td>
                <div class="qty-box">
                <button onclick="decreaseQty('${item.name}')">-</button>
                <span>${item.quantity}</span>
                <button onclick="increaseQty('${item.name}')">+</button>
                </div>
                </td>
                <td>₹${item.price}</td>
                <td>₹${itemTotal}</td>
                <td>
                <button class="remove-btn" onclick="if(confirm('Are you sure you want to remove this menu item from billing?')) removeItem('${item.name}')">
                    X
                </button>
                </td>
            </tr>

        `;
        mobileCart.innerHTML += `
        <div class="mobile-cart-card">
            <h3>${item.name}</h3>
            <p><strong>Price :</strong> ₹${item.price}</p>
            <div class="mobile-qty">
                <span><strong>Quantity</strong></span>
                <div class="qty-box">
                    <button onclick="decreaseQty('${item.name}')">-</button>
                    <span>${item.quantity}</span>
                    <button onclick="increaseQty('${item.name}')">+</button>
                </div>
            </div>
            <p><strong>Total :</strong> ₹${item.price * item.quantity}</p>
            <button class="remove-btn" onclick="if(confirm('Are you sure?')) removeItem('${item.name}')"> Remove </button>
        </div>
    `;
    });


    const tax = subtotal * 0.05;
    const grandTotal = subtotal + tax;
    subtotalElement.innerText = `₹${subtotal.toFixed(2)}`;
    taxElement.innerText = `₹${tax.toFixed(2)}`;
    grandTotalElement.innerText = `₹${grandTotal.toFixed(2)}`;

}

function removeItem(name){
    cart = cart.filter(item => item.name !== name);
    displayCart();
    saveCart();
}

function increaseQty(name){
    const item = cart.find(item => item.name === name);
    item.quantity += 1;
    displayCart();
    saveCart();

}

function decreaseQty(name){
    const item = cart.find(item => item.name === name);
    if(item.quantity > 1){
        item.quantity -= 1;
    }
    else{
        removeItem(name);
    }

    displayCart();
    saveCart();

}

function saveOrder(){
    if(cart.length === 0){
        alert("Cart is empty");
        return;
    }

    fetch("/save-order", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            cart: cart,
            subtotal: subtotalElement.innerText.replace("₹",""),
            tax: taxElement.innerText.replace("₹",""),
            grandTotal: grandTotalElement.innerText.replace("₹","")
        })

    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        showReceipt();
        cart = [];
        localStorage.removeItem("cart");
        displayCart();
    });

}

function updateDateTime(){

    const now = new Date();
    const options = {
        day: "2-digit",
        month: "short",
        year: "numeric"
    };

    const date =now.toLocaleDateString("en-IN", options);
    const time =now.toLocaleTimeString("en-IN", {hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: true});
    dateTime.innerText =`${date} | ${time}`;
}
updateDateTime();
setInterval(updateDateTime, 1000);

function showReceipt(){
    const now = new Date();
    const date = now.toLocaleDateString();
    const time = now.toLocaleTimeString();

    document.getElementById("receipt-date").innerText = "Date: " + date;
    document.getElementById("receipt-time").innerText = "Time: " + time;

    receiptItems.innerHTML = "";
    cart.forEach(item => {
        receiptItems.innerHTML += `
            <tr>
                <td>${item.name}</td>
                <td>${item.quantity}</td>
                <td>₹${item.price * item.quantity}</td>
            </tr>
        `;
    });
    receiptSubtotal.innerText = subtotalElement.innerText;
    receiptTax.innerText = taxElement.innerText;
    receiptGrandTotal.innerText = grandTotalElement.innerText;

    receiptModal.style.display = "flex";
}

document.getElementById("print-bill-btn").addEventListener("click", function() {
    window.print();
});

displayCart();
window.addEventListener("resize", displayCart);