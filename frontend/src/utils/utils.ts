export function SplitFileNames(arr: string[]) {
  return arr.map((value: string) => {
    // Normalize to forward slashes
    const normalized = value.replace(/\\/g, "/");

    return {
      // Grab filename without extension
      name: normalized.split("/").pop()?.split(".")[0] ?? "",
      // Grab everything after "images"
      image_path: normalized.split("images").pop() ?? "",
    };
  });
}
