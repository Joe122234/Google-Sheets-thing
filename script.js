let revenueData = [];
let expenseData = [];
let products = [
    { name: "Product A", count: 10 },
    { name: "Product B", count: 15 },
    { name: "Product C", count: 20 }
    // Add more products as needed
];

// Load data from localStorage if available
if (localStorage.getItem('revenueData')) {
    revenueData = JSON.parse(localStorage.getItem('revenueData'));
    updateTable();
    calculateTotals();
}

if (localStorage.getItem('expenseData')) {
    expenseData = JSON.parse(localStorage.getItem('expenseData'));
    updateTable();
    calculateTotals();
}

// Populate product dropdown
let productDropdown = document.getElementById("product");
products.forEach(product => {
    let option = document.createElement("option");
    option.value = product.name;
    option.textContent = product.name;
    productDropdown.appendChild(option);
});

function addRevenue() {
    let product = document.getElementById("product").value.trim();
    let quantity = parseInt(document.getElementById("quantity").value.trim(), 10);
    let price = parseFloat(document.getElementById("price").value.trim());

    if (product && quantity && price) {
        let date = new Date().toISOString().slice(0, 10);
        let totalRevenue = quantity * price;
        
        revenueData.push({ date, category: "Revenue", description: product, amount: totalRevenue });
        saveData();
        updateTable();
        calculateTotals();
        clearFields();
        updateProductCount(product, -quantity); // Update product count
    } else {
        alert("Please fill out all fields correctly.");
    }
}

function addExpense() {
    let expenseType = document.getElementById("expense_type").value.trim();
    let description = document.getElementById("description").value.trim();
    let amount = parseFloat(document.getElementById("amount").value.trim());

    if (expenseType && description && amount) {
        let date = new Date().toISOString().slice(0, 10);
        
        expenseData.push({ date, category: "Expense", description, amount });
        saveData();
        updateTable();
        calculateTotals();
        clearFields();
    } else {
        alert("Please fill out all fields correctly.");
    }
}

function updateTable() {
    let tableBody = document.getElementById("dataBody");
    tableBody.innerHTML = "";

    let allData = [...revenueData, ...expenseData];

    allData.forEach((item, index) => {
        let row = `<tr>
            <td>${item.date}</td>
            <td>${item.category}</td>
            <td>${item.description}</td>
            <td>$${item.amount.toFixed(2)}</td>
            <td><button onclick="deleteRow(${index})">Delete</button></td>
        </tr>`;
        tableBody.innerHTML += row;
    });
}

function deleteRow(index) {
    let allData = [...revenueData, ...expenseData];
    allData.splice(index, 1);
    
    // Separate revenue and expense data
    revenueData = allData.filter(item => item.category === "Revenue");
    expenseData = allData.filter(item => item.category === "Expense");
    
    saveData();
    updateTable();
    calculateTotals();
}

function deleteAllRows() {
    revenueData = [];
    expenseData = [];
    saveData();
    updateTable();
    calculateTotals();
}

function calculateTotals() {
    // Calculate total revenue
    let totalRevenue = revenueData.reduce((acc, curr) => acc + curr.amount, 0);
    document.getElementById("totalRevenue").textContent = `Total Revenue: $${totalRevenue.toFixed(2)}`;

    // Calculate total expenses
    let totalExpense = expenseData.reduce((acc, curr) => acc + curr.amount, 0);
    document.getElementById("totalExpense").textContent = `Total Expenses: $${totalExpense.toFixed(2)}`;

    // Calculate total profit
    let profit = totalRevenue - totalExpense;
    document.getElementById("totalProfit").textContent = `Total Profit: $${profit.toFixed(2)}`;
}

function saveData() {
    localStorage.setItem('revenueData', JSON.stringify(revenueData));
    localStorage.setItem('expenseData', JSON.stringify(expenseData));
}

function clearFields() {
    document.getElementById("product").value = "";
    document.getElementById("quantity").value = "";
    document.getElementById("price").value = "";
    document.getElementById("expense_type").value = "";
    document.getElementById("description").value = "";
    document.getElementById("amount").value = "";
}

// Function to update product count (simulated)
function updateProductCount(productName, quantity) {
    let product = products.find(p => p.name === productName);
    if (product) {
        product.count += quantity;
        updateProductPage(); // Update product page display
    }
}

// Update product page display
function updateProductPage() {
    let productsContainer = document.createElement("div");
    productsContainer.classList.add("container");
    productsContainer.innerHTML = "<h2>Products</h2>";

    products.forEach(product => {
        let productDiv = document.createElement("div");
        productDiv.classList.add("product-item");
        productDiv.innerHTML = `
            <p>${product.name}: ${product.count}</p>
        `;
        productsContainer.appendChild(productDiv);
    });

    // Replace existing container with updated productsContainer
    let mainContainer = document.querySelector("main");
    mainContainer.innerHTML = "";
    mainContainer.appendChild(productsContainer);
}
