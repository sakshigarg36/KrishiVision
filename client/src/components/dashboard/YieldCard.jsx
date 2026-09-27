export default function YieldCard({ estimate = null }) {
  return <section><h2>Yield outlook</h2><p>{estimate ?? 'No estimate available'}</p></section>;
}
