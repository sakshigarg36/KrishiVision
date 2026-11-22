
from fastapi import APIRouter, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import logging
from services.disease_service import classify
logger = logging.getLogger(__name__)
router = APIRouter()
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB

@router.post("/detect")
async def detect_disease(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid image file."
        )

    try:
        image_bytes = await file.read(MAX_IMAGE_SIZE + 1)

        if len(image_bytes) > MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="Image file must be 10 MB or smaller."
            )

        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty."
            )

        image = Image.open(BytesIO(image_bytes))
        result = classify(image)

        return {
            "success": True,
            "message": "Disease detection completed successfully",
            "data": result
        }

    except UnidentifiedImageError:
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted image file."
        )

    except HTTPException:
        raise

    except Exception:
        logger.exception("Disease detection failed")
        raise HTTPException(
            status_code=500,
            detail="Disease detection failed. Please try again later."
        )

    finally:
        await file.close()
