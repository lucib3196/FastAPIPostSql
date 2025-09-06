export const API_URL = (import.meta.env.VITE_API_URL ?? "").replace(/\/$/, "");

export const imageUrl = (path: string) => {
  try {
    return `${API_URL}${path.startsWith("/") ? "" : "/"}${path}`;
  } catch (error) {
    console.log(error);
    console.log(API_URL,path)
  }
};
