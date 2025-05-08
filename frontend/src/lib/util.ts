export function toHumanReadable(n: number): string {
  if (n < 100) return "< 100";

  const suffixes = ["", "k", "M", "B"];
  const i = Math.floor(Math.log(n) / Math.log(1000));
  return Math.round(n / Math.pow(1000, i)) + suffixes[i];
}
