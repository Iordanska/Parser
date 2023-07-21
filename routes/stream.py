from fastapi import APIRouter, Depends

from DAOs.stream import StreamDAO, get_stream_dao

router = APIRouter()


@router.get("/", response_description="List all streams")
async def list_streams(dao: StreamDAO = Depends(get_stream_dao)):
    streams = dao.get_streams()
    return {"streams": streams}
