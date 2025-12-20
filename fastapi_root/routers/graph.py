from fastapi import APIRouter, HTTPException
from utils.db_utils import get_graph_data

router = APIRouter(prefix="/api/graph", tags=["Graph"])

@router.get("/data")
async def get_graph(limit: int = 100):
    try:
        data = get_graph_data(limit)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
