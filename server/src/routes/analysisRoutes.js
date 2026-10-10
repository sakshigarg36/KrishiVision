import { Router } from 'express';

import {
    createAnalysis,
    getAnalyses,
    getAnalysisById,
    updateAnalysis,
    deleteAnalysis
} from '../controllers/analysisController.js';

const router = Router();

// Create analysis / Get all analyses
router.route('/')
    .get(getAnalyses)
    .post(createAnalysis);

// Get / Update / Delete single analysis
router.route('/:id')
    .get(getAnalysisById)
    .put(updateAnalysis)
    .delete(deleteAnalysis);

export default router;
