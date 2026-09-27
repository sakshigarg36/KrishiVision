export default function FarmMap({ children }) {
  return <section aria-label="Farm map" className="farm-map">{children ?? <p className="placeholder">Map provider and field geometry are not configured.</p>}</section>;
}
