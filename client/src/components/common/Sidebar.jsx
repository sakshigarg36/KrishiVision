import { NavLink } from 'react-router-dom';

const links = [
  ['Overview', '/'], ['Fields', '/fields'], ['Analysis', '/analysis'],
  ['Disease detection', '/disease-detection'], ['Yield prediction', '/yield-prediction'], ['Alerts', '/alerts'],
];

export default function Sidebar() {
  return <aside className="sidebar"><p className="brand">AgriVision X</p><nav className="nav-links" aria-label="Main navigation">{links.map(([label, to]) => <NavLink key={to} to={to} end={to === '/'}>{label}</NavLink>)}</nav></aside>;
}
