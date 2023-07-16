from typing import List

from pydantic import BaseModel


class Stream(BaseModel):
    stream_id: str
    user_id: str
    user_login: str
    game_id: str
    game_name: str
    title: str
    tags: List[str]
    viewer_count: int
    started_at: str
    language: str
    thumbnail_url: str
