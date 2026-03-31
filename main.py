from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

# -------------------------
# DATA (Q2)
# -------------------------
items = [
    {"id": 1, "name": "Tomato", "price": 30, "unit": "kg", "category": "Vegetable", "in_stock": True},
    {"id": 2, "name": "Apple", "price": 120, "unit": "kg", "category": "Fruit", "in_stock": True},
    {"id": 3, "name": "Milk", "price": 50, "unit": "litre", "category": "Dairy", "in_stock": True},
    {"id": 4, "name": "Rice", "price": 60, "unit": "kg", "category": "Grain", "in_stock": True},
    {"id": 5, "name": "Eggs", "price": 70, "unit": "dozen", "category": "Dairy", "in_stock": False},
    {"id": 6, "name": "Potato", "price": 25, "unit": "kg", "category": "Vegetable", "in_stock": True}
]

orders = []
order_counter = 1
cart = []

# -------------------------
# Q1 HOME
# -------------------------
@app.get("/")
def home():
    return {"message": "Welcome to FreshMart Grocery"}

# -------------------------
# Q2 GET ITEMS
# -------------------------
@app.get("/items")
def get_items():
    return {
        "items": items,
        "total": len(items),
        "in_stock_count": sum(1 for i in items if i["in_stock"])
    }

# -------------------------
# Q5 SUMMARY (IMPORTANT ABOVE ID ROUTE)
# -------------------------
@app.get("/items/summary")
def summary():
    categories = {}
    for i in items:
        categories[i["category"]] = categories.get(i["category"], 0) + 1

    return {
        "total": len(items),
        "in_stock": sum(1 for i in items if i["in_stock"]),
        "out_of_stock": sum(1 for i in items if not i["in_stock"]),
        "categories": categories
    }

# -------------------------
# Q3 GET ITEM BY ID
# -------------------------
@app.get("/items/{item_id}")
def get_item(item_id: int):
    for i in items:
        if i["id"] == item_id:
            return i
    raise HTTPException(status_code=404, detail="Item not found")

# -------------------------
# Q4 GET ORDERS
# -------------------------
@app.get("/orders")
def get_orders():
    return {"orders": orders, "total": len(orders)}

# -------------------------
# Q6 MODEL
# -------------------------
class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=50)
    delivery_address: str = Field(..., min_length=10)
    delivery_slot: str = "Morning"
    bulk_order: bool = False

# -------------------------
# Q7 HELPERS
# -------------------------
def find_item(item_id):
    for i in items:
        if i["id"] == item_id:
            return i
    return None

def calculate_total(price, quantity, slot, bulk):
    total = price * quantity
    original = total

    if bulk and quantity >= 10:
        total *= 0.92  # 8% discount

    delivery = 40 if slot == "Morning" else 60 if slot == "Evening" else 0

    return {
        "original": original,
        "final": total + delivery
    }

# -------------------------
# Q8 + Q9 POST ORDER
# -------------------------
@app.post("/orders")
def create_order(order: OrderRequest):
    global order_counter

    item = find_item(order.item_id)
    if not item:
        raise HTTPException(404, "Item not found")

    if not item["in_stock"]:
        raise HTTPException(400, "Item out of stock")

    cost = calculate_total(item["price"], order.quantity, order.delivery_slot, order.bulk_order)

    new_order = {
        "order_id": order_counter,
        "customer": order.customer_name,
        "item": item["name"],
        "quantity": order.quantity,
        "total_cost": cost,
        "status": "confirmed"
    }

    orders.append(new_order)
    order_counter += 1

    return new_order

# -------------------------
# Q10 FILTER
# -------------------------
@app.get("/items/filter")
def filter_items(category: Optional[str] = None,
                 max_price: Optional[int] = None,
                 unit: Optional[str] = None,
                 in_stock: Optional[bool] = None):

    result = items

    if category is not None:
        result = [i for i in result if i["category"] == category]

    if max_price is not None:
        result = [i for i in result if i["price"] <= max_price]

    if unit is not None:
        result = [i for i in result if i["unit"] == unit]

    if in_stock is not None:
        result = [i for i in result if i["in_stock"] == in_stock]

    return {"results": result}

# -------------------------
# Q11 CREATE ITEM
# -------------------------
class NewItem(BaseModel):
    name: str
    price: int
    unit: str
    category: str
    in_stock: bool = True

@app.post("/items", status_code=201)
def add_item(item: NewItem):
    for i in items:
        if i["name"].lower() == item.name.lower():
            raise HTTPException(400, "Duplicate item")

    new = item.dict()
    new["id"] = len(items) + 1
    items.append(new)
    return new

# -------------------------
# Q12 UPDATE ITEM
# -------------------------
@app.put("/items/{item_id}")
def update_item(item_id: int, price: Optional[int] = None, in_stock: Optional[bool] = None):
    for i in items:
        if i["id"] == item_id:
            if price is not None:
                i["price"] = price
            if in_stock is not None:
                i["in_stock"] = in_stock
            return i
    raise HTTPException(404, "Item not found")

# -------------------------
# Q13 DELETE ITEM
# -------------------------
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for i in items:
        if i["id"] == item_id:
            items.remove(i)
            return {"message": "Deleted"}
    raise HTTPException(404, "Item not found")

# -------------------------
# Q14 CART
# -------------------------
@app.post("/cart/add")
def add_cart(item_id: int, quantity: int = 1):
    item = find_item(item_id)

    if not item or not item["in_stock"]:
        raise HTTPException(400, "Invalid item")

    for c in cart:
        if c["item_id"] == item_id:
            c["quantity"] += quantity
            return {"cart": cart}

    cart.append({"item_id": item_id, "quantity": quantity})
    return {"cart": cart}

@app.get("/cart")
def view_cart():
    total = 0
    details = []

    for c in cart:
        item = find_item(c["item_id"])
        subtotal = item["price"] * c["quantity"]
        total += subtotal

        details.append({
            "item": item["name"],
            "qty": c["quantity"],
            "subtotal": subtotal
        })

    return {"cart": details, "total": total}

# -------------------------
# Q15 CHECKOUT
# -------------------------
class Checkout(BaseModel):
    customer_name: str
    delivery_address: str
    delivery_slot: str

@app.post("/cart/checkout", status_code=201)
def checkout(data: Checkout):
    global order_counter

    if not cart:
        raise HTTPException(400, "Cart empty")

    result = []
    grand = 0

    for c in cart:
        item = find_item(c["item_id"])
        cost = item["price"] * c["quantity"]
        grand += cost

        result.append({
            "order_id": order_counter,
            "item": item["name"],
            "total": cost
        })

        order_counter += 1

    cart.clear()

    return {"orders": result, "grand_total": grand}

# -------------------------
# Q16 SEARCH
# -------------------------
@app.get("/items/search")
def search(keyword: str):
    res = [i for i in items if keyword.lower() in i["name"].lower() or keyword.lower() in i["category"].lower()]
    return {"results": res, "total": len(res)}

# -------------------------
# Q17 SORT
# -------------------------
@app.get("/items/sort")
def sort_items(sort_by: str = "price"):
    return {"sorted": sorted(items, key=lambda x: x[sort_by])}

# -------------------------
# Q18 PAGINATION
# -------------------------
@app.get("/items/page")
def paginate(page: int = 1, limit: int = 4):
    start = (page - 1) * limit
    end = start + limit
    return {
        "page": page,
        "data": items[start:end]
    }

# -------------------------
# Q19 ORDER SEARCH + SORT + PAGE
# -------------------------
@app.get("/orders/search")
def order_search(name: str):
    return [o for o in orders if name.lower() in o["customer"].lower()]

@app.get("/orders/sort")
def order_sort():
    return sorted(orders, key=lambda x: x["total_cost"]["final"])

@app.get("/orders/page")
def order_page(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    return orders[start:start+limit]

# -------------------------
# Q20 COMBINED
# -------------------------
@app.get("/items/browse")
def browse(keyword: Optional[str] = None,
           category: Optional[str] = None,
           in_stock: Optional[bool] = None,
           page: int = 1,
           limit: int = 3):

    res = items

    if keyword:
        res = [i for i in res if keyword.lower() in i["name"].lower()]

    if category:
        res = [i for i in res if i["category"] == category]

    if in_stock is not None:
        res = [i for i in res if i["in_stock"] == in_stock]

    start = (page - 1) * limit
    return res[start:start+limit]