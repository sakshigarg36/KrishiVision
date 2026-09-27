export default function Loader({ label = 'Loading' }) {
  return <div role="status" aria-live="polite">{label}...</div>;
}
