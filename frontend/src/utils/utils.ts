export function SplitFileNames(arr: string[]) {
  return arr.map((value: string) => ({
    name: value.split("\\").pop()?.split(".")[0] ?? "",
    image_path: value.split("images").pop(),
  }));
}
