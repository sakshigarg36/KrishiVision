export default function FieldMarker({ label }) {
  return <button type="button" aria-label={label ?? 'Field marker'} title={label}>Field</button>;
}
