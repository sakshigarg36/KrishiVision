export function requireAuth(_req, res, next) {
  return res.status(501).json({ error: 'Authentication is not configured' });
}
