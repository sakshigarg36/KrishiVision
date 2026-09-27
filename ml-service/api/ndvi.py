from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/compute")
def compute_ndvi() -> None:
    raise HTTPException(status_code=501, detail="Provide validated red and near-infrared imagery to enable NDVI processing")
