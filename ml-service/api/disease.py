from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/detect")
def detect_disease() -> None:
    raise HTTPException(status_code=501, detail="Disease model weights are not installed")
