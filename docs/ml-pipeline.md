# ML pipeline

Expected stages are source ingestion, band/image validation, preprocessing, inference, and result persistence through the API. Keep input metadata (sensor, acquisition time, coordinate reference system, crop/cultivar, and units) alongside each asset.

`services/ndvi_service.py` implements the normalized difference vegetation index for matching red and near-infrared arrays. Segmentation, disease classification, and yield prediction deliberately raise `NotImplementedError` until their architectures, preprocessing contracts, evaluation results, and trained artifacts are provided. Never present placeholder responses as model predictions.

Place development datasets under `ml-service/datasets/` and deployable weights under `ml-service/trained_models/`; both directories are ignored by Git apart from their `.gitkeep` markers. The architecture mentions `.pth`, `.h5`, and `.json` artifacts as expected formats, not included files.
