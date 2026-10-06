import { pool } from '../config/db.js';

export async function createAnalysis(req, res, next) {
    try {
        const {
            field_id,
            analysis_type,
            input_data
        } = req.body;

        if (!field_id || !analysis_type) {
            return res.status(400).json({
                error: 'field_id and analysis_type are required'
            });
        }

        const allowedTypes = [
            'NDVI',
            'SEGMENTATION',
            'DISEASE',
            'YIELD',
            'FULL_ANALYSIS'
        ];

        if (!allowedTypes.includes(analysis_type)) {
            return res.status(400).json({
                error: 'Invalid analysis_type'
            });
        }

        const [fields] = await pool.execute(
            'SELECT id FROM fields WHERE id = ?',
            [field_id]
        );

        if (fields.length === 0) {
            return res.status(404).json({
                error: 'Field not found'
            });
        }

        const [result] = await pool.execute(
            `INSERT INTO analyses
            (field_id, analysis_type, status, input_data)
            VALUES (?, ?, 'PENDING', ?)`,
            [
                field_id,
                analysis_type,
                input_data ? JSON.stringify(input_data) : null
            ]
        );

        const [rows] = await pool.execute(
            'SELECT * FROM analyses WHERE id = ?',
            [result.insertId]
        );

        res.status(201).json({
            message: 'Analysis request created successfully',
            analysis: rows[0]
        });

    } catch (error) {
        next(error);
    }
}

export async function getAnalyses(req, res, next) {
    try {
        const fieldId = req.query.field_id;

        let query = 'SELECT * FROM analyses';
        const params = [];

        if (fieldId) {
            query += ' WHERE field_id = ?';
            params.push(fieldId);
        }

        query += ' ORDER BY requested_at DESC';

        const [rows] = await pool.execute(query, params);

        res.status(200).json({
            count: rows.length,
            analyses: rows
        });

    } catch (error) {
        next(error);
    }
}

export async function getAnalysisById(req, res, next) {
    try {
        const { id } = req.params;

        const [rows] = await pool.execute(
            'SELECT * FROM analyses WHERE id = ?',
            [id]
        );

        if (rows.length === 0) {
            return res.status(404).json({
                error: 'Analysis not found'
            });
        }

        res.status(200).json({
            analysis: rows[0]
        });

    } catch (error) {
        next(error);
    }
}

export async function updateAnalysis(req, res, next) {
    try {
        const { id } = req.params;

        const {
            analysis_type,
            status,
            input_data,
            completed_at
        } = req.body;

        const allowedTypes = [
            'NDVI',
            'SEGMENTATION',
            'DISEASE',
            'YIELD',
            'FULL_ANALYSIS'
        ];

        const allowedStatuses = [
            'PENDING',
            'PROCESSING',
            'COMPLETED',
            'FAILED'
        ];

        if (analysis_type !== undefined && !allowedTypes.includes(analysis_type)) {
            return res.status(400).json({
                error: 'Invalid analysis_type'
            });
        }

        if (status !== undefined && !allowedStatuses.includes(status)) {
            return res.status(400).json({
                error: 'Invalid status'
            });
        }

        const [existing] = await pool.execute(
            'SELECT * FROM analyses WHERE id = ?',
            [id]
        );

        if (existing.length === 0) {
            return res.status(404).json({
                error: 'Analysis not found'
            });
        }

        const current = existing[0];

        const [result] = await pool.execute(
            `UPDATE analyses
             SET analysis_type = ?,
                 status = ?,
                 input_data = ?,
                 completed_at = ?
             WHERE id = ?`,
            [
                analysis_type !== undefined ? analysis_type : current.analysis_type,
                status !== undefined ? status : current.status,
                input_data !== undefined
                    ? JSON.stringify(input_data)
                    : current.input_data,
                completed_at !== undefined ? completed_at : current.completed_at,
                id
            ]
        );

        const [rows] = await pool.execute(
            'SELECT * FROM analyses WHERE id = ?',
            [id]
        );

        res.status(200).json({
            message: 'Analysis updated successfully',
            analysis: rows[0]
        });

    } catch (error) {
        next(error);
    }
}

export async function deleteAnalysis(req, res, next) {
    try {
        const { id } = req.params;

        const [result] = await pool.execute(
            'DELETE FROM analyses WHERE id = ?',
            [id]
        );

        if (result.affectedRows === 0) {
            return res.status(404).json({
                error: 'Analysis not found'
            });
        }

        res.status(200).json({
            message: 'Analysis deleted successfully'
        });

    } catch (error) {
        next(error);
    }
}
