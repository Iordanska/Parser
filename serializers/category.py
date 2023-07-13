def category_serializer(category) -> dict:
    return {
        "id": str(category["_id"]),
        "category_id": category["category_id"],
        "name": category["name"],
        "link": category["link"],
    }


def categories_serializer(categories) -> list:
    return [category_serializer(category) for category in categories]
