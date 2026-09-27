import { Navigate, Route, Routes } from 'react-router-dom';
import Navbar from './components/common/Navbar.jsx';
import Sidebar from './components/common/Sidebar.jsx';
import Login from './pages/Login.jsx';
import Register from './pages/Register.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Fields from './pages/Fields.jsx';
import FieldDetails from './pages/FieldDetails.jsx';
import Analysis from './pages/Analysis.jsx';
import DiseaseDetection from './pages/DiseaseDetection.jsx';
import YieldPrediction from './pages/YieldPrediction.jsx';
import Alerts from './pages/Alerts.jsx';

const pages = [
  ['/', Dashboard], ['/fields', Fields], ['/fields/:id', FieldDetails],
  ['/analysis', Analysis], ['/disease-detection', DiseaseDetection],
  ['/yield-prediction', YieldPrediction], ['/alerts', Alerts],
];

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="*" element={(
        <div className="app-shell">
          <Sidebar />
          <div className="app-main">
            <Navbar />
            <main className="page-content">
              <Routes>
                {pages.map(([path, Page]) => <Route key={path} path={path} element={<Page />} />)}
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </main>
          </div>
        </div>
      )} />
    </Routes>
  );
}
