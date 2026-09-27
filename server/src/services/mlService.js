const baseUrl = process.env.ML_SERVICE_URL || 'http://localhost:8000';
export async function checkMlService() {
  const response = await fetch(`${baseUrl}/health`);
  if (!response.ok) throw new Error(`ML service unavailable (${response.status})`);
  return response.json();
}
