# 🛵 FreshMart Grocery Delivery App (FastAPI)

## 🚀 Project Overview

FreshMart is a backend API system built using FastAPI that simulates a real-world grocery delivery application.
It allows users to browse grocery items, manage cart operations, and place delivery orders with different slots.

This project demonstrates core backend development concepts including REST APIs, data validation, CRUD operations, and advanced querying features.

---

## 🎯 Features Implemented

### ✅ Day 1: Basic APIs

* Home route
* Get all grocery items
* Get item by ID
* Orders listing
* Items summary (stock + category breakdown)

### ✅ Day 2–3: POST APIs & Validation

* Order creation with Pydantic validation
* Field constraints and error handling
* Helper functions:

  * `find_item()`
  * `calculate_total()`
* Bulk order discount logic

### ✅ Day 4: CRUD Operations

* Add new item
* Update item details
* Delete item (with validations)
* Duplicate item prevention

### ✅ Day 5: Cart Workflow

* Add items to cart
* View cart with subtotal and total
* Checkout system (multi-order creation)
* Cart clearing after checkout

### ✅ Day 6: Advanced APIs

* Search items (name + category)
* Sort items
* Pagination
* Order search, sorting, and pagination
* Combined browsing (filter + search + sort + paginate)

---

## 🛠️ Tech Stack

* Python 🐍
* FastAPI ⚡
* Uvicorn 🚀
* Pydantic (Data Validation)

---

## 📁 Project Structure

```
grocery_app/
│
├── main.py              # Main FastAPI application
├── requirements.txt    # Dependencies
├── README.md           # Project documentation
└── screenshots/        # API screenshots (Q1–Q20)
```

---

## ▶️ How to Run the Project

### 1️⃣ Install Dependencies

```
pip install fastapi uvicorn
```

### 2️⃣ Run the Server

```
uvicorn main:app --reload
```

### 3️⃣ Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## 📸 API Testing

All endpoints are tested using Swagger UI.

Screenshots for each task (Q1–Q20) are included in the `screenshots` folder:

* Q1: Home route
* Q2: Get items
* Q3: Get item by ID
* ...
* Q20: Combined browsing API

---

## 📌 Sample Functionalities

* 🛒 Add items to cart and checkout
* 📦 Place single and bulk orders
* 🔍 Search and filter items
* 📊 View item summary and stock details
* 📄 Paginate large datasets

---

## ⚠️ Validation Rules

* Quantity must be between 1–50
* Customer name minimum length: 2
* Delivery address minimum length: 10
* Duplicate items are not allowed

---

## 🎓 Learning Outcomes

* Built a complete FastAPI backend from scratch
* Learned API design and route structuring
* Implemented real-world workflows (Cart → Order → Delivery)
* Applied search, sorting, and pagination techniques
* Improved debugging and testing skills using Swagger

---

## 🔗 Future Improvements

* Add database (MongoDB / MySQL)
* Implement user authentication (JWT)
* Build frontend using React
* Add payment integration

---

## 🙌 Acknowledgment

This project was developed as part of FastAPI training at **Innomatics Research Labs**.

---

## 📎 Submission Links

* 🔗 GitHub Repository: *(Add your link here)*
* 🔗 LinkedIn Post: *(Add your link here)*

---

## 📢 Hashtags

#FastAPI #Python #BackendDevelopment #API #WebDevelopment
