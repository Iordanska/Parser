import requests
from fastapi import HTTPException

from config.base_settings import settings
from schemas.stream import Stream


def parse_streams(game_id: str | None = None, user_login: str | None = None):
    params = {"first": 10}

    if game_id:
        params["game_id"] = game_id
    elif user_login:
        params["user_login"] = user_login

    url = "https://api.twitch.tv/helix/streams"
    headers = {
        "Accept": "*/*",
        "Authorization": settings.AUTH_TOKEN,
        "Client-Id": settings.CLIENT_ID,
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 400:
        raise HTTPException(
            status_code=400,
            detail=response.data,
        )
        return

    streams = response.json()

    if not streams["data"]:
        raise HTTPException(status_code=400, detail="The query data doesn't exist.")
    return

    data_list = []

    for stream in streams["data"]:
        data_list.append(
            Stream(
                stream_id=stream["id"],
                user_id=stream["user_id"],
                user_login=stream["user_login"],
                game_id=stream["game_id"],
                game_name=stream["game_name"],
                title=stream["title"],
                tags=stream["tags"],
                viewer_count=stream["viewer_count"],
                started_at=stream["started_at"],
                language=stream["language"],
                thumbnail_url=stream["thumbnail_url"],
            )
        )

    return data_list
