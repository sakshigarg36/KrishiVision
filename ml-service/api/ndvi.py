
import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import numpy as np

from services.ndvi_service import compute_ndvi

router = APIRouter()


class NDVIRequest(BaseModel):
    red: list[list[float]] = Field(..., min_length=1)
    near_infrared: list[list[float]] = Field(..., min_length=1)


@router.post("/compute")
def compute_ndvi_endpoint(request: NDVIRequest):
    try:
        red = np.asarray(request.red, dtype=np.float32)
        nir = np.asarray(request.near_infrared, dtype=np.float32)

        if red.ndim != 2 or nir.ndim != 2:
            raise ValueError("Red and NIR must be 2D arrays.")

        if red.shape != nir.shape:
            raise ValueError("Red and NIR arrays must have the same dimensions.")

        if red.size == 0:
            raise ValueError("Input arrays cannot be empty.")

        if not np.isfinite(red).all() or not np.isfinite(nir).all():
            raise ValueError("Band values must be finite numbers.")

        if np.any(red < 0) or np.any(nir < 0):
            raise ValueError("Reflectance values cannot be negative.")

        ndvi = np.clip(compute_ndvi(red, nir), -1.0, 1.0)

        mean_ndvi = float(np.mean(ndvi))

        zones = np.zeros(ndvi.shape, dtype=np.uint8)
        zones[(ndvi >= 0.0) & (ndvi < 0.2)] = 1
        zones[(ndvi >= 0.2) & (ndvi < 0.4)] = 2
        zones[(ndvi >= 0.4) & (ndvi < 0.6)] = 3
        zones[(ndvi >= 0.6) & (ndvi <= 1.0)] = 4

        return {
            "analysis_type": "NDVI",
            "status": "success",
            "mean_ndvi": round(mean_ndvi, 4),
            "min_ndvi": round(float(np.min(ndvi)), 4),
            "max_ndvi": round(float(np.max(ndvi)), 4),
            "ndvi": ndvi.tolist(),
            "health_status": (
                "Healthy" if mean_ndvi >= 0.3 else "Potential stress"
            ),
            "health_zones": zones.tolist(),
            "statistics": {
                "min": float(np.min(ndvi)),
                "max": float(np.max(ndvi)),
                "mean": mean_ndvi
            },
            "zone_classes": [
                int(value) for value in np.unique(zones)
            ],
            "note": "Demonstration calculation using supplied band values; not verified satellite imagery."
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
        
