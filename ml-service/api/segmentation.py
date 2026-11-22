from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import numpy as np

from services.segmentation_service import segment

router = APIRouter()


class SegmentationRequest(BaseModel):
    ndvi: list[list[float]] = Field(
        ...,
        min_length=1,
        description="2D NDVI array"
    )


@router.post("/")
def segment_field(request: SegmentationRequest):
    try:
        ndvi_array = np.asarray(request.ndvi, dtype=np.float32)

        if ndvi_array.ndim != 2:
            raise HTTPException(
                status_code=422,
                detail="NDVI must be a two-dimensional array."
            )

        if ndvi_array.shape[0] != ndvi_array.shape[1]:
            raise HTTPException(
                status_code=422,
                detail="NDVI must be a square tile."
            )

        if ndvi_array.shape[0] != 256:
            raise HTTPException(
                status_code=422,
                detail="NDVI tile must be 256x256 pixels."
            )

        if not np.isfinite(ndvi_array).all():
            raise HTTPException(
                status_code=422,
                detail="NDVI contains invalid numeric values."
            )

        if np.any(ndvi_array < -1) or np.any(ndvi_array > 1):
            raise HTTPException(
                status_code=422,
                detail="NDVI values must be between -1 and 1."
            )

        result = segment(ndvi_array)
        mask = result.pop("mask")

        return {
            "status": "success",
            **result,
            "mask": mask.tolist()
        }

    except HTTPException:
        raise
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Segmentation failed: {str(exc)}"
        )