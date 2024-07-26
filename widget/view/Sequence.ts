import type { IWidget } from "@/model";
import { getOutline } from "@/utils";
import { AnyModel } from "@anywidget/types";
import * as d3 from "d3";
// import { html, svg } from "lit-html";
// import { repeat } from "lit-html/directives/repeat.js";

class Sequence {
	svg: d3.Selection<SVGSVGElement, undefined, null, undefined>;
	model: AnyModel<IWidget>;

	constructor(model: AnyModel<IWidget>) {
		this.model = model;
		this.svg = d3
			.create("svg")
			.attr(
				"viewBox",
				[0, 0, model.get("width"), model.get("height")].join(" "),
			);
	}

	_render() {
		const sequlets = this.model.get("sequlets");
		const labels = this.model.get("labels");

		if (sequlets.length === 0 || labels.length === 0) {
			return;
		}

		const x = d3
			.scaleLinear([0, this.model.get("width")])
			.domain([0, this.model.get("canvasWidth")]);

		const y = d3
			.scaleLinear([0, this.model.get("height")])
			.domain([0, this.model.get("canvasHeight")]);

		const color = d3
			.scaleOrdinal(d3.schemeCategory10)
			.domain(labels.map((label) => label.value.toString()));

		// Sequlet Grouping
		const sequletGroups = this.svg
			.selectAll("g")
			.data(sequlets)
			.join("g")
			.attr("class", (d) => `sequlet-${d.id}`);

		// Draw Rects
		// 추후에 Gradient로 변경 가능
		sequletGroups
			.selectAll("rect")
			.data((d) => d.rects)
			.join("rect")
			.attr("fill", (d) => color(d.value.toString()))
			.attr("x", (d) => x(d.x))
			.attr("y", (d) => y(d.y))
			.attr("width", (d) => x(d.width))
			.attr("height", (d) => y(d.height));

		// Draw Paths
		sequletGroups
			.selectAll("path")
			.data((d) => getOutline(d.rects))
			.join("path")
			.attr("d", (d) => d)
			.attr("fill", "none")
			.attr("stroke", "black")
			.attr("stroke-width", 0.3);

		if (this.model.get("grid")) {
			// Grid lines for x-axis
			this.svg
				.selectAll("line.verticalGrid")
				.data(d3.range(0, this.model.get("canvasWidth") + 1))
				.join("line")
				.attr("class", "verticalGrid")
				.attr("x1", (d) => x(d))
				.attr("x2", (d) => x(d))
				.attr("y1", y(0))
				.attr("y2", y(this.model.get("canvasHeight")))
				.attr("stroke", "black")
				.attr("stroke-width", 0.2);

			// Grid lines for y-axis
			this.svg
				.selectAll("line.horizontalGrid")
				.data(d3.range(0, this.model.get("canvasHeight") + 1))
				.join("line")
				.attr("class", "horizontalGrid")
				.attr("x1", x(0))
				.attr("x2", x(this.model.get("canvasWidth")))
				.attr("y1", (d) => y(d))
				.attr("y2", (d) => y(d + 1))
				.attr("stroke", "black")
				.attr("stroke-width", 0.2);
		} else {
			this.svg.selectAll("line.verticalGrid").remove();
			this.svg.selectAll("line.horizontalGrid").remove();
		}
	}
	render() {
		this._render();
		return this.svg.node();
	}
}

export default Sequence;
