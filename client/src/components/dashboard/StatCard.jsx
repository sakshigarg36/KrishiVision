export default function StatCard({ label, value = '—' }) {
  return <section aria-label={label}><p>{label}</p><strong>{value}</strong></section>;
}
