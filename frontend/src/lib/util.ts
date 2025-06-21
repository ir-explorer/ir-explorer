export function toHumanReadable(n: number): string {
  if (n < 1000) return n.toString();
  if (n > 1000000000000) return "> 1T";

  const suffixes = ["", "k", "M", "B"];
  const i = Math.floor(Math.log(n) / Math.log(1000));
  return Math.round(n / Math.pow(1000, i)) + suffixes[i];
}
