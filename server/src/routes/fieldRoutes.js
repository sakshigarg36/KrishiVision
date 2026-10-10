import { Router } from 'express';
import {
    createField,
    getFields,
    getFieldById,
    updateField,
    deleteField
} from '../controllers/fieldController.js';

const router = Router();

router.route('/')
    .get(getFields)
    .post(createField);
router.route('/:id')
    .get(getFieldById)
    .put(updateField)
    .delete(deleteField);

export default router;