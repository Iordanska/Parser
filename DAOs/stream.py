from fastapi import Depends
from pymongo.collection import Collection

from config.db import get_stream_collection
from schemas.stream import Stream
from serializers.stream import streams_serializer


class StreamDAO:
    def __init__(self, collection: Collection):
        self.collection = collection

    def get_streams(self):
        streams = streams_serializer(self.collection.find())
        return streams

    def create_stream(self, stream: Stream):
        stream = self.collection.insert_one(stream)
        stream_id = str(stream.inserted_id)
        return stream_id


def get_stream_dao(collection: Collection = Depends(get_stream_collection)):
    return StreamDAO(collection)
