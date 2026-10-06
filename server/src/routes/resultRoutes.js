import { Router } from 'express';

import {
    createResult,
    getResultsByAnalysis
} from '../controllers/resultController.js';

const router = Router();

// Create a result for an analysis
router.route('/')
    .post(createResult);

// Get all results for an analysis
router.route('/analysis/:analysisId')
    .get(getResultsByAnalysis);

export default router;