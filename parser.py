from datetime import datetime

import requests

from product.schema import Product


def parse_category(category):
    json_data = get_product_from_category(category)
    data_list = get_data_from_json(json_data)
    return data_list


def get_product_from_category(category):
    url = f"https://www.lamoda.by{category}?json=1"
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    data = data["payload"]["products"]
    return data


def get_data_from_json(json_data, quantity):
    data_list = []

    for product in json_data:
        rating = product.get("rating", None)
        average_rating = None
        reviews_count = None

        if rating:
            average_rating = rating["average_rating"]
            reviews_count = rating["reviews_count"]

        data_list.append(
            Product(
                name=product["name"],
                categories=product["category_leaves_denormalized"],
                brand=product["brand"]["name"],
                brand_id=product["brand"]["id"],
                sku=product["sku"],
                price=product["price_amount"],
                old_price=product.get("old_price_amount", None),
                discount=product.get("discount", None),
                color=product.get("color_family", None),
                image_links=product["gallery"],
                url="https://www.lamoda.by/p/" + str(product["sku"]),
                rating=average_rating,
                reviews=reviews_count,
                created_at=datetime.now(),
            )
        )

    return data_list
