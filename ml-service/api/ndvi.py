
import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.ndvi_service import compute_ndvi

router = APIRouter()


class NDVIRequest(BaseModel):
    red: list[list[float]] = Field(..., min_length=1)
    near_infrared: list[list[float]] = Field(..., min_length=1)


@router.post("/compute")
def compute_ndvi_endpoint(request: NDVIRequest):
    try:
        red = np.asarray(request.red, dtype=float)
        near_infrared = np.asarray(request.near_infrared, dtype=float)

        if red.ndim != 2 or near_infrared.ndim != 2:
            raise ValueError("Red and near-infrared bands must be 2D arrays")
        if red.shape != near_infrared.shape:
           raise ValueError(
                "Red and near-infrared bands must have the same dimensions."
            )

        if not np.isfinite(red).all() or not np.isfinite(near_infrared).all():
            raise ValueError("Band values must be finite numbers")

        ndvi = compute_ndvi(red, near_infrared)

        return {
            "analysis_type": "NDVI",
            "mean_ndvi": round(float(np.mean(ndvi)), 4),
            "min_ndvi": round(float(np.min(ndvi)), 4),
            "max_ndvi": round(float(np.max(ndvi)), 4),
            "ndvi": ndvi.tolist(),
            "health_status": (
                "Healthy" if float(np.mean(ndvi)) >= 0.3
                else "Potential stress"
            ),
            "note": "Demonstration calculation using supplied band values; not verified satellite imagery."
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
