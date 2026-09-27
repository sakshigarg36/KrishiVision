import { Router } from 'express';
import { notImplemented } from '../controllers/analysisController.js';
const router = Router();
router.route('/').get(notImplemented).post(notImplemented);
export default router;
