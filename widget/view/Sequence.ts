import type { IRect, ISequlet } from "@/model/event";
import { getOutline } from "@/services";
import { type BaseType, type Selection, create } from "d3";

const DURATION = 150;

class Sequence {
  svg: Selection<SVGSVGElement, undefined, null, undefined>;
  rects: Selection<SVGRectElement | BaseType, IRect, SVGElement, undefined>;
  paths: Selection<SVGPathElement | BaseType, ISequlet, SVGElement, undefined>;
  selected: ISequlet | undefined;
  bg: Selection<SVGRectElement, undefined, null, undefined>;

  g_rects: Selection<SVGGElement, undefined, null, undefined>;
  g_paths: Selection<SVGGElement, undefined, null, undefined>;

  constructor(width: number, height: number) {
    this.svg = create("svg").attr("viewBox", [0, 0, width, height].join(" "));
    this.selected = undefined;

    // add transparent background to svg
    this.bg = this.svg
      .append("rect")
      .attr("id", "sequenceBg")
      .attr("width", width)
      .attr("height", height)
      .attr("fill", "transparent")
      .on("click", () => {
        this.rects.transition().duration(DURATION).attr("opacity", 1);
        this.paths.transition().duration(DURATION).attr("opacity", 1);
        this.selected = undefined;
      });

    this.g_rects = this.svg.append("g");
    this.g_paths = this.svg.append("g");

    this.rects = this.g_rects.selectAll("rect");
    this.paths = this.g_paths.selectAll("path");
  }

  _renderRects(sequlets: ISequlet[]) {
    this.rects = this.g_rects
      .selectAll("rect")
      .data(sequlets.flatMap(sequlet => sequlet.rects))
      .join("rect")
      .attr("x", d => d.x)
      .attr("y", d => d.y)
      .attr("width", d => d.width)
      .attr("height", d => d.height)
      .attr("fill", d => d.color ?? "black");
  }

  _renderPaths(sequlets: ISequlet[]) {
    this.paths = this.g_paths
      .selectAll("path")
      .data(sequlets)
      .join("path")
      .attr("d", d => getOutline(d.rects))
      .attr("fill", "transparent")
      .attr("stroke", "#333333")
      .attr("stroke-width", "1.5");

    this._addSequletClickEvent();
  }

  _addSequletClickEvent() {
    this.paths.on("click", (_, d) => {
      if (this.selected && this.selected === d) {
        this.rects.transition().duration(DURATION).attr("opacity", 1);
        this.paths.transition().duration(DURATION).attr("opacity", 1);
        this.selected = undefined;
      } else {
        this.rects
          .transition()
          .duration(DURATION)
          .attr("opacity", rect => (d.rects.includes(rect) ? 1 : 0.1));
        this.paths
          .transition()
          .duration(DURATION)
          .attr("opacity", path => (path === d ? 1 : 0.1));
        this.selected = d;
      }
    });
  }

  render(sequlets: ISequlet[]) {
    if (sequlets.length) {
      this._renderRects(sequlets);
      this._renderPaths(sequlets);
    }

    return this.svg.node();
  }
}

export default Sequence;

// if (this.model.get("grid")) {
// 	// Grid lines for x-axis
// 	this.svg
// 		.selectAll("line.verticalGrid")
// 		.data(range(0, this.model.get("canvasWidth") + 1))
// 		.join("line")
// 		.attr("class", "verticalGrid")
// 		.attr("x1", (d) => x(d))
// 		.attr("x2", (d) => x(d))
// 		.attr("y1", y(0))
// 		.attr("y2", y(this.model.get("canvasHeight")))
// 		.attr("stroke", "black")
// 		.attr("stroke-width", 0.2);

// 	// Grid lines for y-axis
// 	this.svg
// 		.selectAll("line.horizontalGrid")
// 		.data(range(0, this.model.get("canvasHeight") + 1))
// 		.join("line")
// 		.attr("class", "horizontalGrid")
// 		.attr("x1", x(0))
// 		.attr("x2", x(this.model.get("canvasWidth")))
// 		.attr("y1", (d) => y(d))
// 		.attr("y2", (d) => y(d + 1))
// 		.attr("stroke", "black")
// 		.attr("stroke-width", 0.2);
// } else {
// 	this.svg.selectAll("line.verticalGrid").remove();
// 	this.svg.selectAll("line.horizontalGrid").remove();
// }
