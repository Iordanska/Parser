def product_serializer(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "categories": product["categories"],
        "brand": product["brand"],
        "brand_id": product["brand_id"],
        "sku": product["sku"],
        "price": product["price"],
        "old_price": product["old_price"],
        "discount": product["discount"],
        "color": product["color"],
        "image_links": product["image_links"],
        "url": product["url"],
        "rating": product["rating"],
        "reviews": product["reviews"],
        "created_at": product["created_at"],
    }


def products_serializer(products) -> list:
    return [product_serializer(product) for product in products]
