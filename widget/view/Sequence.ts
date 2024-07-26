import type { ILabel } from "@/model";
import { ISequlet } from "@/model/event";
import { getOutline } from "@/utils";
import { create } from "d3";

class Sequence {
	svg: d3.Selection<SVGSVGElement, undefined, null, undefined>;

	constructor(width: number, height: number) {
		this.svg = create("svg").attr("viewBox", [0, 0, width, height].join(" "));
	}

	_render(sequlets: ISequlet[], labels: ILabel[]) {
		if (sequlets.length === 0 || labels.length === 0) {
			return;
		}

		// Draw rects
		this.svg
			.selectAll("rect")
			.data(sequlets.flatMap((sequlet) => sequlet.rects))
			.join("rect")
			.attr("x", (d) => d.x)
			.attr("y", (d) => d.y)
			.attr("width", (d) => d.width)
			.attr("height", (d) => d.height)
			.attr("fill", (d) => d.color ?? "black");

		this.svg
			.selectAll("path")
			.data(sequlets)
			.join("path")
			.attr("d", (d) => getOutline(d.rects))
			.attr("fill", "none")
			.attr("stroke", "#333333")
			.attr("stroke-width", "3");

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
	}
	render(sequlets: ISequlet[], labels: ILabel[]) {
		this._render(sequlets, labels);
		return this.svg.node();
	}
}

export default Sequence;
