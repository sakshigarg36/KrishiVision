export default function HealthCard({ status = 'No analysis available' }) {
  return <section><h2>Crop health</h2><p>{status}</p></section>;
}
