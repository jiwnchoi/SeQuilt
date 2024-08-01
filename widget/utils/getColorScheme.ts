import { hsl, schemeCategory10 } from "d3";

export default function getColorScheme(size: number) {
  if (size < 1) return [];

  const schemeLightCategory10 = schemeCategory10.map(color => hsl(color).brighter(0.8).toString());
  const schemeDarkCategory10 = schemeCategory10.map(color => hsl(color).darker().toString());
  const extended_scheme = [...schemeCategory10, ...schemeLightCategory10, ...schemeDarkCategory10];
  return extended_scheme.slice(0, size);
}
