from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "price": 1000, "category": "electronics", "in_stock": True},
    {"id": 2, "name": "Mouse", "price": 20, "category": "electronics", "in_stock": True},
    {"id": 3, "name": "Keyboard", "price": 50, "category": "electronics", "in_stock": True},
    {"id": 4, "name": "Monitor", "price": 200, "category": "electronics", "in_stock": True},
    {"id": 5, "name": "Laptop Stand", "price": 30, "category": "accessories", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 120, "category": "electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 80, "category": "electronics", "in_stock": True}
]

@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }
    
@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):
    filtered_products = []

    for product in products:
        if product["category"].lower() == category_name.lower():
            filtered_products.append(product)

    if len(filtered_products) == 0:
        return {"error": "No products found in this category"}

    return {
        "products": filtered_products,
        "total": len(filtered_products)
    }

@app.get("/products/instock")
def get_instock_products():
    in_stock_products = []

    for product in products:
        if product["in_stock"] == True:
            in_stock_products.append(product)

    return {
        "in_stock_products": in_stock_products,
        "count": len(in_stock_products)
    }
    
@app.get("/store/summary")
def get_store_summary():

    total_products = len(products)

    in_stock_count = len([p for p in products if p["in_stock"]])
    
    out_of_stock_count = total_products - in_stock_count

    categories = list(set([p["category"] for p in products]))

    return {
        "store_name": "My E-commerce Store",
        "total_products": total_products,
        "in_stock": in_stock_count,
        "out_of_stock": out_of_stock_count,
        "categories": categories
    }
    
@app.get("/products/search/{keyword}")
def search_products(keyword: str):

    matched_products = []

    for product in products:
        if keyword.lower() in product["name"].lower():
            matched_products.append(product)

    if len(matched_products) == 0:
        return {"message": "No products matched your search"}

    return {
        "matched_products": matched_products,
        "count": len(matched_products)
    }
    
@app.get("/products/deals")
def get_best_and_premium_products():

    cheapest_product = min(products, key=lambda p: p["price"])
    most_expensive_product = max(products, key=lambda p: p["price"])

    return {
        "best_deal": cheapest_product,
        "premium_pick": most_expensive_product
    }
