from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/predict")
def predict_yield() -> None:
    raise HTTPException(status_code=501, detail="Yield model weights are not installed")
