import type { ILabel, ISequlet } from "@/model/event";
import { scaleLinear, scaleOrdinal, schemeCategory10 } from "d3";

function getRescaledSequlets(
  sequlets: ISequlet[],
  legend: ILabel[],
  width: number,
  height: number,
  margin = { top: 10, right: 10, bottom: 10, left: 10 },
) {
  const maxX = Math.max(...sequlets.flatMap(s => s.rects.map(r => r.x + r.width)));
  const maxY = Math.max(...sequlets.flatMap(s => s.rects.map(r => r.y + r.height)));

  const x = scaleLinear([margin.left, width - margin.right]).domain([0, maxX]);
  const y = scaleLinear([margin.top, height - margin.bottom]).domain([0, maxY]);
  const color = scaleOrdinal(schemeCategory10).domain(legend.map(label => label.value.toString()));

  return sequlets.map(sequlet => ({
    id: sequlet.id,
    rects: sequlet.rects.map(rect => ({
      ...rect,
      color: color(rect.value.toString()),
      x: x(rect.x),
      y: y(rect.y),
      width: x(rect.width + rect.x) - x(rect.x),
      height: y(rect.height + rect.y) - y(rect.y),
    })),
  }));
}

export default getRescaledSequlets;
