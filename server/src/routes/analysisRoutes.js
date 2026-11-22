import { Router } from 'express';
import { upload } from '../middleware/uploadMiddleware.js';

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

// Disease detection with image upload
router.post('/disease', upload.single('file'), createAnalysis);

// Get / Update / Delete single analysis
router.route('/:id')
    .get(getAnalysisById)
    .put(updateAnalysis)
    .delete(deleteAnalysis);

export default router;
