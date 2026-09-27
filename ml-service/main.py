from fastapi import FastAPI

from api.disease import router as disease_router
from api.ndvi import router as ndvi_router
from api.segmentation import router as segmentation_router
from api.yield_prediction import router as yield_router

app = FastAPI(title="AgriVision ML Service", version="0.1.0")
app.include_router(ndvi_router, prefix="/ndvi", tags=["ndvi"])
app.include_router(segmentation_router, prefix="/segmentation", tags=["segmentation"])
app.include_router(disease_router, prefix="/disease", tags=["disease"])
app.include_router(yield_router, prefix="/yield", tags=["yield"])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
