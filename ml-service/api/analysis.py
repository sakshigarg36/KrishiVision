from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import numpy as np

from services.ndvi_service import compute_ndvi
from services.segmentation_service import segment

router = APIRouter()


class AnalysisRequest(BaseModel):
    red: list[list[float]] = Field(..., min_length=1)
    near_infrared: list[list[float]] = Field(..., min_length=1)


@router.post("/process")
def process_analysis(request: AnalysisRequest):
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

        if red.shape != (256, 256):
            raise HTTPException(
                status_code=422,
                detail="Input tile must be 256x256 pixels."
            )

        if not np.isfinite(red).all() or not np.isfinite(nir).all():
            raise HTTPException(
                status_code=422,
                detail="Input contains invalid numeric values."
            )

        if np.any(red < 0) or np.any(nir < 0):
            raise HTTPException(
                status_code=422,
                detail="Red and NIR values cannot be negative."
            )

        # NDVI calculation
        ndvi = compute_ndvi(red, nir)
        ndvi = np.clip(ndvi, -1.0, 1.0).astype(np.float32)

        # Health-zone classification
        health_zones = np.zeros(ndvi.shape, dtype=np.uint8)

        health_zones[(ndvi >= 0.0) & (ndvi < 0.2)] = 1
        health_zones[(ndvi >= 0.2) & (ndvi < 0.4)] = 2
        health_zones[(ndvi >= 0.4) & (ndvi < 0.6)] = 3
        health_zones[(ndvi >= 0.6) & (ndvi <= 1.0)] = 4

        # U-Net segmentation
        segmentation_result = segment(ndvi)
        segmentation_mask = segmentation_result["mask"]

        return {
            "status": "success",
            "image": {
                "height": 256,
                "width": 256,
                "resolution": "10m"
            },
            "ndvi": {
                "min": float(ndvi.min()),
                "max": float(ndvi.max()),
                "mean": float(ndvi.mean())
            },
            "health_zones": {
                "classes": [
                    int(value) for value in np.unique(health_zones)
                ],
            },
            "segmentation": {
                "model": segmentation_result["model"],
                "classes": segmentation_result["classes"],
            }
        }

    except HTTPException:
        raise

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc)
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(exc)}"
        )