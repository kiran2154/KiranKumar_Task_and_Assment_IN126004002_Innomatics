from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()                   
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]
class Product(BaseModel):
    name: str
    price: int
    category: str
    in_stock: bool

@app.get("/")
def home():
    return {"message": "FastAPI Product API Running"}

# GET ALL PRODUCTS
@app.get("/products")
def get_products():
    return {"products": products, "total": len(products)}

# POST ADD PRODUCT
@app.post("/products")
def add_product(product: Product):
    for p in products:
        if p["name"].lower() == product.name.lower():
            raise HTTPException(status_code=400, detail="Product already exists")
    new_id = max(p["id"] for p in products) + 1
    new_product = {
        "id": new_id,
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "in_stock": product.in_stock
    }
    products.append(new_product)
    return {
        "message": "Product added",
        "product": new_product
    }
    
# PUT UPDATE PRODUCT
@app.put("/products/{product_id}")
def update_product(product_id: int, price: int = None, in_stock: bool = None):
    for product in products:
        if product["id"] == product_id:
            if price is not None:
                product["price"] = price
            if in_stock is not None:
                product["in_stock"] = in_stock
            return product
    raise HTTPException(status_code=404, detail="Product not found")

# DELETE PRODUCT
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return {"message": f"Product '{product['name']}' deleted"}
    raise HTTPException(status_code=404, detail="Product not found")

# INVENTORY AUDIT
@app.get("/products/audit")
def audit_products():
    total_products = len(products)
    in_stock_products = [p for p in products if p["in_stock"]]
    out_of_stock = [p["name"] for p in products if not p["in_stock"]]
    total_stock_value = sum(p["price"] for p in in_stock_products) * 10
    most_expensive = max(products, key=lambda x: x["price"])
    return {
        "total_products": total_products,
        "in_stock_count": len(in_stock_products),
        "out_of_stock_names": out_of_stock,
        "total_stock_value": total_stock_value,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        }
    }

# CATEGORY DISCOUNT
@app.put("/products/discount/apply")
def apply_discount(category: str, discount_percent: int):
    updated_products = []
    for product in products:
        if product["category"].lower() == category.lower():
            new_price = int(product["price"] * (1 - discount_percent / 100))
            product["price"] = new_price
            updated_products.append({
                "name": product["name"],
                "new_price": new_price
            })
    if not updated_products:
        return {"message": "No products found in this category"}
    return {
        "updated_count": len(updated_products),
        "products": updated_products
    }

# GET SINGLE PRODUCT
@app.get("/products/{product_id}")
def get_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(status_code=404, detail="Product not found")
