import { pool } from '../config/db.js';
import { requestMlAnalysis } from '../services/mlService.js';
import { evaluateAlerts } from '../services/alertService.js';



export async function createAnalysis(req, res, next) {
    let analysisId;

    try {
        const { field_id, analysis_type, input_data } = req.body;
        const uploadedFile = req.file;

        if (!field_id || !analysis_type) {
            return res.status(400).json({
                error: 'field_id and analysis_type are required'
            });
        }

        const allowedTypes = [
            'NDVI',
            'SEGMENTATION',
            'DISEASE',
            'YIELD'
        ];

        if (!allowedTypes.includes(analysis_type)) {
            return res.status(400).json({
                error: 'Invalid analysis_type. FULL_ANALYSIS is not supported yet.'
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

        if (analysis_type === 'DISEASE') {
            if (!uploadedFile) {
                return res.status(400).json({
                    error: 'A crop image file is required for disease detection'
                });
            }

            if (!uploadedFile.mimetype?.startsWith('image/')) {
                return res.status(400).json({
                    error: 'Please upload a valid image file'
                });
            }
        }

        const [insertResult] = await pool.execute(
            `INSERT INTO analyses
             (field_id, analysis_type, status, input_data)
             VALUES (?, ?, 'PENDING', ?)`,
            [
                field_id,
                analysis_type,
                input_data != null ? JSON.stringify(input_data) : null
            ]
        );

        analysisId = insertResult.insertId;

        await pool.execute(
            "UPDATE analyses SET status = 'PROCESSING' WHERE id = ?",
            [analysisId]
        );

        let mlResult;

        try {
            mlResult = await requestMlAnalysis({
                analysis_type,
                input_data: input_data ?? {},
                file: uploadedFile
            });
        } catch (mlError) {
            await pool.execute(
                "UPDATE analyses SET status = 'FAILED' WHERE id = ?",
                [analysisId]
            );

            const [analyses] = await pool.execute(
                'SELECT * FROM analyses WHERE id = ?',
                [analysisId]
            );

           console.error(
    `ML analysis failed for analysis ${analysisId}:`,
    mlError
);

return res.status(502).json({
    error: 'ML analysis failed',
    analysis: analyses[0]
});
        }

        const numericValue =
            analysis_type === 'NDVI' &&
            typeof mlResult.mean_ndvi === 'number' &&
            Number.isFinite(mlResult.mean_ndvi)
                ? mlResult.mean_ndvi
                : null;

        const [resultInsert] = await pool.execute(
            `INSERT INTO results
             (analysis_id, result_type, result_data, numeric_value)
             VALUES (?, ?, ?, ?)`,
            [
                analysisId,
                analysis_type,
                JSON.stringify(mlResult),
                numericValue
            ]
        );

        await pool.execute(
            `UPDATE analyses
             SET status = 'COMPLETED',
                 completed_at = CURRENT_TIMESTAMP
             WHERE id = ?`,
            [analysisId]
        );

        if (analysis_type === 'NDVI') {
            try {
                await evaluateAlerts(analysisId);
            } catch (alertError) {
                console.error(
                    `Alert evaluation failed for analysis ${analysisId}:`,
                    alertError.message
                );
            }
        }

        const [results] = await pool.execute(
            'SELECT * FROM results WHERE id = ?',
            [resultInsert.insertId]
        );

        const [analyses] = await pool.execute(
            'SELECT * FROM analyses WHERE id = ?',
            [analysisId]
        );

        return res.status(201).json({
            message: 'Analysis completed successfully',
            analysis: analyses[0],
            result: results[0]
        });

    } catch (error) {
        if (analysisId !== undefined) {
            try {
                await pool.execute(
                    "UPDATE analyses SET status = 'FAILED' WHERE id = ?",
                    [analysisId]
                );
            } catch {
                // Preserve the original error if status update also fails.
            }
        }

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
    'YIELD'
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
