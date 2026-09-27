import StatCard from '../components/dashboard/StatCard.jsx';
import HealthCard from '../components/dashboard/HealthCard.jsx';
import YieldCard from '../components/dashboard/YieldCard.jsx';
import AlertCard from '../components/dashboard/AlertCard.jsx';

export default function Dashboard() {
  return <><h1>Farm overview</h1><p className="placeholder">Connect a farm to begin monitoring.</p><div className="dashboard-grid"><StatCard label="Fields" /><StatCard label="Area monitored" /><HealthCard /><YieldCard /><AlertCard /></div></>;
}
