import { pool } from '../config/db.js';

const allowedAlertTypes = [
    'CROP_STRESS',
    'DISEASE',
    'YIELD',
    'GENERAL'
];

const allowedSeverities = [
    'LOW',
    'MEDIUM',
    'HIGH',
    'CRITICAL'
];

export async function createAlert(req, res, next) {
    try {
        const {
            field_id,
            analysis_id,
            alert_type,
            severity,
            message,
            is_read
        } = req.body;

        if (!field_id || !alert_type || !message) {
            return res.status(400).json({
                error: 'field_id, alert_type and message are required'
            });
        }

        if (!allowedAlertTypes.includes(alert_type)) {
            return res.status(400).json({
                error: 'Invalid alert_type'
            });
        }

        if (severity !== undefined && !allowedSeverities.includes(severity)) {
            return res.status(400).json({
                error: 'Invalid severity'
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

        if (analysis_id !== undefined && analysis_id !== null) {
            const [analyses] = await pool.execute(
                'SELECT id FROM analyses WHERE id = ?',
                [analysis_id]
            );

            if (analyses.length === 0) {
                return res.status(404).json({
                    error: 'Analysis not found'
                });
            }
        }

        const [result] = await pool.execute(
            `INSERT INTO alerts
            (field_id, analysis_id, alert_type, severity, message, is_read)
            VALUES (?, ?, ?, ?, ?, ?)`,
            [
                field_id,
                analysis_id ?? null,
                alert_type,
                severity || 'MEDIUM',
                message,
                is_read ?? false
            ]
        );

        const [rows] = await pool.execute(
            'SELECT * FROM alerts WHERE id = ?',
            [result.insertId]
        );

        res.status(201).json({
            message: 'Alert created successfully',
            alert: rows[0]
        });

    } catch (error) {
        next(error);
    }
}

export async function getAlerts(req, res, next) {
    try {
        const { field_id, analysis_id, is_read } = req.query;

        let query = 'SELECT * FROM alerts';
        const conditions = [];
        const params = [];

        if (field_id) {
            conditions.push('field_id = ?');
            params.push(field_id);
        }

        if (analysis_id) {
            conditions.push('analysis_id = ?');
            params.push(analysis_id);
        }

        if (is_read !== undefined) {
            conditions.push('is_read = ?');
            params.push(is_read === 'true' ? 1 : 0);
        }

        if (conditions.length > 0) {
            query += ' WHERE ' + conditions.join(' AND ');
        }

        query += ' ORDER BY created_at DESC';

        const [rows] = await pool.execute(query, params);

        res.status(200).json({
            count: rows.length,
            alerts: rows
        });

    } catch (error) {
        next(error);
    }
}

export async function getAlertById(req, res, next) {
    try {
        const { id } = req.params;

        const [rows] = await pool.execute(
            'SELECT * FROM alerts WHERE id = ?',
            [id]
        );

        if (rows.length === 0) {
            return res.status(404).json({
                error: 'Alert not found'
            });
        }

        res.status(200).json({
            alert: rows[0]
        });

    } catch (error) {
        next(error);
    }
}

export async function updateAlert(req, res, next) {
    try {
        const { id } = req.params;

        const {
            alert_type,
            severity,
            message,
            is_read
        } = req.body;

        if (alert_type !== undefined && !allowedAlertTypes.includes(alert_type)) {
            return res.status(400).json({
                error: 'Invalid alert_type'
            });
        }

        if (severity !== undefined && !allowedSeverities.includes(severity)) {
            return res.status(400).json({
                error: 'Invalid severity'
            });
        }

        if (is_read !== undefined && typeof is_read !== 'boolean') {
            return res.status(400).json({
                error: 'is_read must be a boolean'
            });
        }

        const [existing] = await pool.execute(
            'SELECT * FROM alerts WHERE id = ?',
            [id]
        );

        if (existing.length === 0) {
            return res.status(404).json({
                error: 'Alert not found'
            });
        }

        const current = existing[0];

        const [result] = await pool.execute(
            `UPDATE alerts
             SET alert_type = ?,
                 severity = ?,
                 message = ?,
                 is_read = ?
             WHERE id = ?`,
            [
                alert_type !== undefined ? alert_type : current.alert_type,
                severity !== undefined ? severity : current.severity,
                message !== undefined ? message : current.message,
                is_read !== undefined ? is_read : current.is_read,
                id
            ]
        );

        const [rows] = await pool.execute(
            'SELECT * FROM alerts WHERE id = ?',
            [id]
        );

        res.status(200).json({
            message: 'Alert updated successfully',
            alert: rows[0]
        });

    } catch (error) {
        next(error);
    }
}

export async function deleteAlert(req, res, next) {
    try {
        const { id } = req.params;

        const [result] = await pool.execute(
            'DELETE FROM alerts WHERE id = ?',
            [id]
        );

        if (result.affectedRows === 0) {
            return res.status(404).json({
                error: 'Alert not found'
            });
        }

        res.status(200).json({
            message: 'Alert deleted successfully'
        });

    } catch (error) {
        next(error);
    }
}
