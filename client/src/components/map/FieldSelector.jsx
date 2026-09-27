export default function FieldSelector({ fields = [], value = '', onChange }) {
  return <label>Field <select value={value} onChange={(event) => onChange?.(event.target.value)}><option value="">Select a field</option>{fields.map((field) => <option key={field.id} value={field.id}>{field.name}</option>)}</select></label>;
}
