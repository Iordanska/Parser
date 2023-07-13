from datetime import datetime

import requests
from user_agent import generate_user_agent

from schemas.category import Category
from schemas.product import Product


def parse_categories():
    url = "https://www.lamoda.by/?json=1"
    headers = {
        "Accept": "*/*",
        "User-Agent": generate_user_agent(),
    }
    response = requests.get(url, headers=headers)

    data = response.json()["payload"]["seo"]["footer"]["sections"]
    main_categories = {}

    for section in data[0:3]:
        if section["sections"]:
            for links in section["sections"]:
                for link in links["links"]:
                    id = link["link"].split("/")[2]
                    main_categories.setdefault(
                        id,
                        {
                            "main_category": section["title"],
                            "category": link["title"],
                            "link": link["link"],
                        },
                    )

    all_categories = {}

    for key, value in main_categories.items():
        url = f"https://www.lamoda.by/{value['link']}?json=1"
        main_category = value["main_category"]
        headers = {"Accept": "*/*", "User-Agent": generate_user_agent()}
        response = requests.get(url, headers=headers)
        data = response.json()["payload"]["popular_categories"]

        if data:
            for item in data:
                id = item["url"].split("/")[2]
                all_categories.setdefault(
                    id,
                    {
                        "main_category": main_category,
                        "category": item["title"],
                        "link": item["url"],
                    },
                )

    data_list = []

    for key, value in all_categories.items():
        data_list.append(
            Category(
                category_id=key,
                name=value["main_category"] + " " + value["category"],
                link=value["link"],
            )
        )

    return data_list


def parse_category(category):
    json_data = get_product_from_category(category)

    data_list = get_data_from_json(json_data)
    return data_list


def get_product_from_category(category):
    url = f"https://www.lamoda.by{category}?json=1"
    headers = {
        "Accept": "*/*",
        "User-Agent": generate_user_agent(),
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    data = data["payload"]["products"]
    return data


def get_data_from_json(json_data):
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
