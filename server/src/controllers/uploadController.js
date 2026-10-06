import { pool } from '../config/db.js';
import fs from 'fs';

export async function uploadFieldData(req, res, next) {
    try {
        const { field_id } = req.body;

        if (!field_id) {
            if (req.file) {
                fs.unlinkSync(req.file.path);
            }

            return res.status(400).json({
                error: 'field_id is required'
            });
        }

        const [fields] = await pool.execute(
            'SELECT id FROM fields WHERE id = ?',
            [field_id]
        );

        if (fields.length === 0) {
            if (req.file) {
                fs.unlinkSync(req.file.path);
            }

            return res.status(404).json({
                error: 'Field not found'
            });
        }

        if (!req.file) {
            return res.status(400).json({
                error: 'File is required'
            });
        }

        const [result] = await pool.execute(
            `INSERT INTO uploads
            (field_id, original_name, stored_name, file_path, mime_type, file_size)
            VALUES (?, ?, ?, ?, ?, ?)`,
            [
                field_id,
                req.file.originalname,
                req.file.filename,
                req.file.path,
                req.file.mimetype,
                req.file.size
            ]
        );

        const [rows] = await pool.execute(
            'SELECT * FROM uploads WHERE id = ?',
            [result.insertId]
        );

        res.status(201).json({
            message: 'File uploaded successfully',
            upload: rows[0]
        });

    } catch (error) {
        if (req.file && fs.existsSync(req.file.path)) {
            fs.unlinkSync(req.file.path);
        }

        next(error);
    }
}

export async function getUploadsByField(req, res, next) {
    try {
        const { fieldId } = req.params;

        const [rows] = await pool.execute(
            `SELECT * FROM uploads
             WHERE field_id = ?
             ORDER BY created_at DESC`,
            [fieldId]
        );

        res.status(200).json({
            count: rows.length,
            uploads: rows
        });

    } catch (error) {
        next(error);
    }
}
