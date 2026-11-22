import { pool } from '../config/db.js';

const NDVI_STRESS_THRESHOLD = 0.30;

export async function evaluateAlerts(analysisId) {
    if (!analysisId) {
        throw new Error('analysisId is required');
    }

    // Find the analysis and its NDVI result
    const [rows] = await pool.execute(
        `SELECT
            a.id AS analysis_id,
            a.field_id,
            r.numeric_value
         FROM analyses a
         JOIN results r ON r.analysis_id = a.id
         WHERE a.id = ?
           AND r.result_type = 'NDVI'
           AND r.numeric_value IS NOT NULL
         ORDER BY r.created_at DESC
         LIMIT 1`,
        [analysisId]
    );

    if (rows.length === 0) {
        return {
            created: false,
            message: 'No NDVI result found for this analysis'
        };
    }

    const analysis = rows[0];
    const ndvi = Number(analysis.numeric_value);

    if (ndvi >= NDVI_STRESS_THRESHOLD) {
        return {
            created: false,
            message: 'No crop-stress alert generated',
            ndvi
        };
    }

    // Avoid creating a duplicate alert for the same analysis
    const [existing] = await pool.execute(
        `SELECT id FROM alerts
         WHERE analysis_id = ?
           AND alert_type = 'CROP_STRESS'
         LIMIT 1`,
        [analysisId]
    );

    if (existing.length > 0) {
        return {
            created: false,
            message: 'Crop-stress alert already exists',
            alert_id: existing[0].id
        };
    }

    const [result] = await pool.execute(
        `INSERT INTO alerts
         (field_id, analysis_id, alert_type, severity, message)
         VALUES (?, ?, 'CROP_STRESS', 'HIGH', ?)`,
        [
            analysis.field_id,
            analysisId,
            `Potential crop stress detected. NDVI value: ${ndvi.toFixed(2)}`
        ]
    );

    return {
        created: true,
        alert_id: result.insertId,
        ndvi
    };
}