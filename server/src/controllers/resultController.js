import { pool } from '../config/db.js';

export async function createResult(req, res, next) {
    try {
        const {
            analysis_id,
            result_type,
            result_data,
            numeric_value,
            output_path
        } = req.body;

        if (!analysis_id || !result_type) {
            return res.status(400).json({
                error: 'analysis_id and result_type are required'
            });
        }

        const allowedTypes = [
            'NDVI',
            'SEGMENTATION',
            'DISEASE',
            'YIELD'
        ];

        if (!allowedTypes.includes(result_type)) {
            return res.status(400).json({
                error: 'Invalid result_type'
            });
        }

        // Check whether the analysis exists
        const [analyses] = await pool.execute(
            'SELECT id FROM analyses WHERE id = ?',
            [analysis_id]
        );

        if (analyses.length === 0) {
            return res.status(404).json({
                error: 'Analysis not found'
            });
        }

        // Store the result
        const [result] = await pool.execute(
            `INSERT INTO results
            (analysis_id, result_type, result_data, numeric_value, output_path)
            VALUES (?, ?, ?, ?, ?)`,
            [
                analysis_id,
                result_type,
                result_data ? JSON.stringify(result_data) : null,
                numeric_value ?? null,
                output_path || null
            ]
        );

        // Mark analysis as completed
        await pool.execute(
            `UPDATE analyses
             SET status = 'COMPLETED',
                 completed_at = CURRENT_TIMESTAMP
             WHERE id = ?`,
            [analysis_id]
        );

        // Get created result
        const [rows] = await pool.execute(
            'SELECT * FROM results WHERE id = ?',
            [result.insertId]
        );

        res.status(201).json({
            message: 'Result created successfully',
            result: rows[0]
        });

    } catch (error) {
        next(error);
    }
}


export async function getResultsByAnalysis(req, res, next) {
    try {
        const { analysisId } = req.params;

        const [rows] = await pool.execute(
            `SELECT * FROM results
             WHERE analysis_id = ?
             ORDER BY created_at DESC`,
            [analysisId]
        );

        res.status(200).json({
            count: rows.length,
            results: rows
        });

    } catch (error) {
        next(error);
    }
}