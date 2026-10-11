# AgriVision X — Satellite & NDVI Pipeline

## 1. Satellite Data Source

The project uses Sentinel-2 satellite imagery obtained through the
Copernicus Data Space Ecosystem / Copernicus Browser.

Selected product:

- Mission: Sentinel-2
- Product: Level-2A (L2A)
- Instrument: MSI (MultiSpectral Instrument)
- Area of Interest: Selected agricultural field polygon
- Location: Meerut, Uttar Pradesh, India

## 2. Required Spectral Bands

The NDVI pipeline uses two Sentinel-2 bands:

| Band | Name | Purpose | Resolution |
|------|------|---------|------------|
| B04 | Red | Red reflectance | 10 m |
| B08 | NIR | Near Infrared reflectance | 10 m |

B04 is used as the Red input and B08 as the Near Infrared input.

## 3. Input Data Format

The satellite band data will be processed as raster/GeoTIFF data.

Expected inputs:

datasets/
└── sentinel2/
    └── YYYY-MM-DD/
        ├── B04_red.tif
        └── B08_nir.tif

Example:

datasets/
└── sentinel2/
    └── 2026-09-30/
        ├── B04_red.tif
        └── B08_nir.tif

## 4. Preprocessing Approach

The preprocessing pipeline will:

1. Load Sentinel-2 B04 and B08 raster files.
2. Read the first raster band using Rasterio.
3. Convert raster values to float32.
4. Verify that Red and NIR rasters have matching dimensions.
5. Preserve the spatial metadata/profile of the input raster.
6. Handle zero denominators during NDVI calculation.
7. Clip NDVI values to the range -1 to 1.
8. Save the resulting NDVI as a single-band GeoTIFF.

## 5. NDVI Calculation

NDVI is calculated using:

NDVI = (NIR - Red) / (NIR + Red)

Where:

Red = Sentinel-2 B04

NIR = Sentinel-2 B08

## 6. Health Zone Classification

The initial prototype uses the following NDVI ranges:

0.0 <= NDVI < 0.2  → Zone 1
0.2 <= NDVI < 0.4  → Zone 2
0.4 <= NDVI < 0.6  → Zone 3
0.6 <= NDVI <= 1.0 → Zone 4

Values below 0 are retained in the NDVI raster and remain unclassified
in the initial health-zone prototype.

## 7. Output Format

The pipeline will generate:

ndvi.tif

and

health_zones.tif

Both outputs retain raster/spatial metadata required for later GIS
visualization and backend integration.

## 8. Project Integration

The satellite pipeline will provide outputs to the ML/backend layer.

Planned flow:

Copernicus Sentinel-2 L2A
        ↓
B04 Red + B08 NIR
        ↓
Preprocessing
        ↓
NDVI Calculation
        ↓
Health Zone Classification
        ↓
NDVI Raster + Health Zone Raster
        ↓
Backend API
        ↓
React/GIS Dashboard

## 9. Current Development Status

Day 1:
- Sentinel-2 data source finalized.
- Sentinel-2 Level-2A selected.
- B04 Red band finalized.
- B08 NIR band finalized.
- GeoTIFF/raster format finalized.
- Initial preprocessing approach defined.
- NDVI pipeline prototype created and tested using synthetic GeoTIFF data.

Day 2:
- Download/use real Sentinel-2 B04 and B08 data.
- Implement real satellite image loading.
- Implement preprocessing and band extraction.

Day 3:
- Generate NDVI raster from real satellite data.
- Generate health zones.