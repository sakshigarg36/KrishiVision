from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/")
def segment_field() -> None:
    raise HTTPException(status_code=501, detail="Segmentation weights are not installed")
