import { Router } from 'express';
import { notImplemented } from '../controllers/fieldController.js';
const router = Router();
router.route('/').get(notImplemented).post(notImplemented);
router.route('/:id').get(notImplemented).put(notImplemented).delete(notImplemented);
export default router;
