import requests

from category.schema import Category


def parse_categories():
    url = "https://www.lamoda.by/?json=1"
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }
    response = requests.get(url, headers=headers)

    data = response.json()["payload"]["seo"]["footer"]["sections"]
    main_cats = {}

    for section in data[0:3]:
        if section["sections"]:
            for links in section["sections"]:
                for link in links["links"]:
                    id = link["link"].split("/")[2]
                    main_cats.setdefault(
                        id,
                        {
                            "main_cat": section["title"],
                            "cat": link["title"],
                            "link": link["link"],
                        },
                    )

    # all_cats = {}
    #
    # for key, value in main_cats.items():
    #     url = f"https://www.lamoda.by/{key}?json=1"
    #     main_cat = value['main_cat']
    #     headers = {"Accept": "*/*", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    #     response = requests.get(url, headers=headers)
    #     data = response.json()["payload"]["popular_categories"]
    #     if data:
    #         for item in data:
    #             all_cats.setdefault(item['url'], {'main_cat': main_cat, 'cat': item['title']})

    data_list = []
    for key, value in main_cats.items():
        data_list.append(
            Category(
                category_id=key,
                name=value["main_cat"] + " " + value["cat"],
                link=value["link"],
            )
        )

    return data_list
