
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.yield_service import predict
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class YieldPredictionRequest(BaseModel):
    Region: str
    Crop: str
    Season: str
    Year: int = Field(ge=1900, le=2100)
    Temperature: float
    Rainfall: float = Field(ge=0)
    Humidity: float = Field(ge=0, le=100)
    pH: float = Field(ge=0, le=14)
    Nitrogen: float = Field(ge=0)
    Phosphorus: float = Field(ge=0)
    Potassium: float = Field(ge=0)
    Fertilizer: float = Field(ge=0)
    Pesticide: float = Field(ge=0)
    soil_type: str = Field(alias="Soil Type")


@router.post("/predict")
def predict_yield(request: YieldPredictionRequest):
    try:
        features = request.model_dump(by_alias=True)
        predicted_yield = predict(features)

        return {
            "success": True,
            "prediction": {
                "crop": request.Crop,
                "region": request.Region,
                "season": request.Season,
                "predicted_yield": predicted_yield,
                "unit": "as defined by training dataset"
            }
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
    except Exception:
        logger.exception("Yield prediction failed")
        raise HTTPException(
            status_code=500,
            detail="Yield prediction failed. Please try again later."
        )
