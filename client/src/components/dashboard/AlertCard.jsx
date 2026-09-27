export default function AlertCard({ alert }) {
  return <section><h2>Alerts</h2><p>{alert ?? 'No alerts available'}</p></section>;
}
