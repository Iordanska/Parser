def stream_serializer(stream) -> dict:
    return {
        "id": str(stream["_id"]),
        "stream_id": stream["id"],
        "user_id": stream["user_id"],
        "user_login": stream["user_login"],
        "game_id": stream["game_id"],
        "game_name": stream["game_name"],
        "title": stream["title"],
        "tags": stream["tags"],
        "viewer_count": stream["viewer_count"],
        "started_at": stream["started_at"],
        "language": stream["language"],
        "thumbnail_url": stream["thumbnail_url"],
    }


def streams_serializer(streams) -> list:
    return [stream_serializer(stream) for stream in streams]
