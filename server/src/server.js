import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import authRoutes from './routes/authRoutes.js';
import fieldRoutes from './routes/fieldRoutes.js';
import analysisRoutes from './routes/analysisRoutes.js';
import diseaseRoutes from './routes/diseaseRoutes.js';
import yieldRoutes from './routes/yieldRoutes.js';
import alertRoutes from './routes/alertRoutes.js';
import { errorHandler, notFound } from './middleware/errorMiddleware.js';
import { testDatabaseConnection } from './config/db.js';
import resultRoutes from './routes/resultRoutes.js';
import uploadRoutes from './routes/uploadRoutes.js';

const app = express();
app.use(cors());
app.use(express.json({ limit: '1mb' }));
app.get('/api/health', (_req, res) => res.json({ status: 'ok' }));
app.use('/api/auth', authRoutes);
app.use('/api/fields', fieldRoutes);
app.use('/api/analysis', analysisRoutes);
app.use('/api/disease', diseaseRoutes);
app.use('/api/yield', yieldRoutes);
app.use('/api/alerts', alertRoutes);
app.use('/api/results', resultRoutes);
app.use('/api/uploads', uploadRoutes);
app.use(notFound);
app.use(errorHandler);


const port = Number(process.env.PORT || 5000);
app.listen(port, async () => {
    console.log(`AgriVision API listening on port ${port}`);

    await testDatabaseConnection();
});
