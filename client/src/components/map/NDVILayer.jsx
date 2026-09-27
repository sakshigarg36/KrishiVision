export default function NDVILayer({ enabled = false }) {
  return <div aria-live="polite">{enabled ? 'NDVI imagery source not configured.' : 'NDVI layer off'}</div>;
}
