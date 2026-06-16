const apiHost =
  import.meta.env.VITE_API_HOST ||
  window.location.hostname ||
  "localhost";

const apiPort =
  import.meta.env.VITE_API_PORT ||
  "5050";

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  `http://${apiHost}:${apiPort}/api`;
