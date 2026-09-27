export default function Modal({ open, title, onClose, children }) {
  if (!open) return null;
  return <div role="presentation" onClick={onClose}><section role="dialog" aria-modal="true" aria-label={title} onClick={(event) => event.stopPropagation()}><header><h2>{title}</h2><button type="button" onClick={onClose} aria-label="Close">Close</button></header>{children}</section></div>;
}
