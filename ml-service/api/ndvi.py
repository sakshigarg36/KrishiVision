
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import numpy as np

from services.ndvi_service import compute_ndvi

router = APIRouter()


class NDVIRequest(BaseModel):
    red: list[list[float]] = Field(..., min_length=1)
    near_infrared: list[list[float]] = Field(..., min_length=1)


@router.post("/compute")
def calculate_ndvi(request: NDVIRequest):
    try:
        red = np.asarray(request.red, dtype=np.float32)
        nir = np.asarray(request.near_infrared, dtype=np.float32)

        if red.ndim != 2 or nir.ndim != 2:
            raise HTTPException(
                status_code=422,
                detail="Red and NIR must be two-dimensional arrays."
            )

        if red.shape != nir.shape:
            raise HTTPException(
                status_code=422,
                detail="Red and NIR arrays must have the same shape."
            )

        if red.size == 0:
            raise HTTPException(
                status_code=422,
                detail="Input arrays cannot be empty."
            )

        if not np.isfinite(red).all() or not np.isfinite(nir).all():
            raise HTTPException(
                status_code=422,
                detail="Input arrays contain invalid numeric values."
            )

        if np.any(red < 0) or np.any(nir < 0):
            raise HTTPException(
                status_code=422,
                detail="Red and NIR reflectance values cannot be negative."
            )

        ndvi = compute_ndvi(red, nir)
        ndvi = np.clip(ndvi, -1.0, 1.0)

        zones = np.zeros(ndvi.shape, dtype=np.uint8)
        zones[(ndvi >= 0.0) & (ndvi < 0.2)] = 1
        zones[(ndvi >= 0.2) & (ndvi < 0.4)] = 2
        zones[(ndvi >= 0.4) & (ndvi < 0.6)] = 3
        zones[(ndvi >= 0.6) & (ndvi <= 1.0)] = 4

        return {
            "status": "success",
            "height": int(ndvi.shape[0]),
            "width": int(ndvi.shape[1]),
            "ndvi": ndvi.tolist(),
            "health_zones": zones.tolist(),
            "statistics": {
                "min": float(ndvi.min()),
                "max": float(ndvi.max()),
                "mean": float(ndvi.mean())
            },
            "zone_classes": [
                int(value) for value in np.unique(zones)
            ]
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"NDVI calculation failed: {str(exc)}"
        )
