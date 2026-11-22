
const baseUrl = (
    process.env.ML_SERVICE_URL || 'http://localhost:8000'
).replace(/\/+$/, '');

const analysisEndpoints = {
    NDVI: '/ndvi/compute',
    SEGMENTATION: '/segmentation/',
    DISEASE: '/disease/detect',
    YIELD: '/yield/predict',
};

export async function checkMlService() {
    const response = await fetch(`${baseUrl}/health`);

    if (!response.ok) {
        throw new Error(`ML service unavailable (${response.status})`);
    }

    return response.json();
}

export async function requestMlAnalysis(analysis) {
    const endpoint = analysisEndpoints[analysis.analysis_type];

    if (!endpoint) {
        throw new Error(
            `Unsupported analysis type: ${analysis.analysis_type}`
        );
    }

    let body;
    const headers = {};

    if (analysis.analysis_type === 'DISEASE') {
        if (!analysis.file) {
            throw new Error('Disease image file is required');
        }

        const formData = new FormData();

        const imageBlob = new Blob(
            [analysis.file.buffer],
            { type: analysis.file.mimetype }
        );

        formData.append(
            'file',
            imageBlob,
            analysis.file.originalname
        );

        body = formData;
    } else {
        headers['Content-Type'] = 'application/json';
        body = JSON.stringify(analysis.input_data ?? {});
    }

    const response = await fetch(`${baseUrl}${endpoint}`, {
        method: 'POST',
        headers,
        body,
        signal: AbortSignal.timeout(60000),
    });

    const responseData = await response.json().catch(() => ({}));

    if (!response.ok) {
        const detail =
            responseData.detail ||
            responseData.error ||
            `ML service failed (${response.status})`;

        throw new Error(detail);
    }

    return responseData;
}
