import { useParams } from 'react-router-dom';
export default function FieldDetails() { const { id } = useParams(); return <><h1>Field details</h1><p className="placeholder">Field {id} is not loaded. Connect the field API to view its data.</p></>; }
