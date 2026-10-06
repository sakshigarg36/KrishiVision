import { pool } from '../config/db.js';

export async function createField(req, res, next) {
    try {
        const {
            user_id,
            name,
            crop_type,
            area,
            latitude,
            longitude,
            soil_type,
            boundary
        } = req.body;

        if (!user_id || !name) {
            return res.status(400).json({
                error: 'user_id and name are required'
            });
        }

        const [result] = await pool.execute(
            `INSERT INTO fields
            (user_id, name, crop_type, area, latitude, longitude, soil_type, boundary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
            [
                user_id,
                name,
                crop_type || null,
                area || null,
                latitude || null,
                longitude || null,
                soil_type || null,
                boundary ? JSON.stringify(boundary) : null
            ]
        );

        const [rows] = await pool.execute(
            'SELECT * FROM fields WHERE id = ?',
            [result.insertId]
        );

        res.status(201).json({
            message: 'Field created successfully',
            field: rows[0]
        });
    } catch (error) {
        next(error);
    }
}

export async function getFields(req, res, next) {
    try {
        const userId = req.query.user_id;

        let query = 'SELECT * FROM fields';
        let params = [];

        if (userId) {
            query += ' WHERE user_id = ?';
            params.push(userId);
        }

        query += ' ORDER BY created_at DESC';

        const [rows] = await pool.execute(query, params);

        res.status(200).json({
            count: rows.length,
            fields: rows
        });
    } catch (error) {
        next(error);
    }
}
export async function getFieldById(req, res, next) {
    try {
        const { id } = req.params;

        const [rows] = await pool.execute(
            'SELECT * FROM fields WHERE id = ?',
            [id]
        );

        if (rows.length === 0) {
            return res.status(404).json({
                error: 'Field not found'
            });
        }

        res.status(200).json({
            field: rows[0]
        });
    } catch (error) {
        next(error);
    }
}
export async function updateField(req, res, next) {
    try {
        const { id } = req.params;

        const {
            name,
            crop_type,
            area,
            latitude,
            longitude,
            soil_type,
            boundary
        } = req.body;

        const [result] = await pool.execute(
            `UPDATE fields
             SET name = ?,
                 crop_type = ?,
                 area = ?,
                 latitude = ?,
                 longitude = ?,
                 soil_type = ?,
                 boundary = ?
             WHERE id = ?`,
            [
                name,
                crop_type || null,
                area || null,
                latitude || null,
                longitude || null,
                soil_type || null,
                boundary ? JSON.stringify(boundary) : null,
                id
            ]
        );

        if (result.affectedRows === 0) {
            return res.status(404).json({
                error: 'Field not found'
            });
        }

        const [rows] = await pool.execute(
            'SELECT * FROM fields WHERE id = ?',
            [id]
        );

        res.status(200).json({
            message: 'Field updated successfully',
            field: rows[0]
        });
    } catch (error) {
        next(error);
    }
}
export async function deleteField(req, res, next) {
    try {
        const { id } = req.params;

        const [result] = await pool.execute(
            'DELETE FROM fields WHERE id = ?',
            [id]
        );

        if (result.affectedRows === 0) {
            return res.status(404).json({
                error: 'Field not found'
            });
        }

        res.status(200).json({
            message: 'Field deleted successfully'
        });
    } catch (error) {
        next(error);
    }
}