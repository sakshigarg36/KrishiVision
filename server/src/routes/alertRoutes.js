import { Router } from 'express';
import { notImplemented } from '../controllers/alertController.js';
const router = Router();
router.route('/').get(notImplemented).post(notImplemented);
export default router;
