import uvicorn

from fastapi import FastAPI, HTTPException

app = FastAPI()

sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}
products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]



@app.get("/product/{product_id}")
async def get_product(product_id: int) -> dict:
    product = [product for product in products if product["product_id"] == product_id]
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product[0]

@app.get("/products/search")
async def get_products(keyword: str, category: str = None, limit: int = 10) -> list[dict]:
    results = []
    for product in products:
        if keyword.lower() in product["name"].lower():
            if category:
                if product["category"].lower() != category.lower():
                    continue
                results.append(product)
    return results[:limit]



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)