import { Router } from 'express';
import multer from 'multer';
import path from 'path';
import fs from 'fs';

import {
    uploadFieldData,
    getUploadsByField
} from '../controllers/uploadController.js';

const router = Router();

const uploadDirectory = path.resolve('uploads');

if (!fs.existsSync(uploadDirectory)) {
    fs.mkdirSync(uploadDirectory, { recursive: true });
}

const storage = multer.diskStorage({
    destination: (_req, _file, cb) => {
        cb(null, uploadDirectory);
    },

    filename: (_req, file, cb) => {
        const extension = path.extname(file.originalname);
        const uniqueName = `${Date.now()}-${Math.round(Math.random() * 1e9)}${extension}`;

        cb(null, uniqueName);
    }
});

const upload = multer({
    storage,
    limits: {
        fileSize: 50 * 1024 * 1024
    }
});

router.post('/', upload.single('file'), uploadFieldData);

router.get('/field/:fieldId', getUploadsByField);

export default router;
