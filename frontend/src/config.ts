export const API_URL = (import.meta.env.VITE_API_URL ?? "").replace(/\/$/, "");

export const imageUrl = (path: string) =>
  `${API_URL}${path.startsWith("/") ? "" : "/"}${path}`;
