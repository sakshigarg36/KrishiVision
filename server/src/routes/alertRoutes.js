import { Router } from 'express';

import {
    createAlert,
    getAlerts,
    getAlertById,
    updateAlert,
    deleteAlert
} from '../controllers/alertController.js';

const router = Router();

// Create alert / Get all alerts
router.route('/')
    .get(getAlerts)
    .post(createAlert);

// Get / Update / Delete single alert
router.route('/:id')
    .get(getAlertById)
    .put(updateAlert)
    .delete(deleteAlert);

export default router;
