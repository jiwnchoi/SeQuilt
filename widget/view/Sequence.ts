import type { IRectModel, IWidgetModel } from "@/model";
import { AnyModel } from "@anywidget/types";
import * as d3 from "d3";
// import { html, svg } from "lit-html";
// import { repeat } from "lit-html/directives/repeat.js";

class Sequence {
	svg: d3.Selection<SVGSVGElement, undefined, null, undefined>;
	width: number;
	height: number;

	constructor(width: number, height: number) {
		this.svg = d3.create("svg").attr("viewBox", [0, 0, width, height]);
		this.width = width;
		this.height = height;
	}

	_render(model: AnyModel<IWidgetModel>) {
		const rects = model.get("rects");
		const labels = model.get("labels");
		// const sequenceLength = model.get("n_length");
		const numSequences = model.get("n_sequences");
		const grid = model.get("grid");

		if (rects.length === 0 || labels.length === 0) {
			return;
		}

		const showColumns = [...new Set(rects.map((rect) => rect.x))];

		function changeColumn(rect: IRectModel) {
			const column = showColumns.indexOf(rect.x);
			return { ...rect, x: column };
		}

		const x = d3.scaleLinear([0, this.width]).domain([0, showColumns.length]);
		const y = d3.scaleLinear([0, this.height]).domain([0, numSequences]);

		const color = d3
			.scaleOrdinal(d3.schemeCategory10)
			.domain(labels.map((label) => label.id.toString()));

		this.svg
			.selectAll("rect")
			.data(rects.map(changeColumn))
			.join("rect")
			.attr("fill", (d: IRectModel) => color(d.id.toString()))
			// .transition() Column으로 Groupby 한다음에 Column 별로 Transition 적용되게 변경
			.attr("x", (d) => x(d.x))
			.attr("y", (d) => y(d.y_start))
			.attr("width", x(1) - x(0))
			.attr("height", (d) => y(d.y_end + 1) - y(d.y_start));

		if (grid) {
			// Grid lines for x-axis
			this.svg
				.selectAll("line.verticalGrid")
				.data(d3.range(0, showColumns.length + 1))
				.join("line")
				.attr("class", "verticalGrid")
				.attr("x1", (d) => x(d))
				.attr("x2", (d) => x(d))
				.attr("y1", y(0))
				.attr("y2", y(numSequences))
				.attr("stroke", "black")
				.attr("stroke-width", 0.2);

			// Grid lines for y-axis
			this.svg
				.selectAll("line.horizontalGrid")
				.data(d3.range(0, numSequences + 1))
				.join("line")
				.attr("class", "horizontalGrid")
				.attr("x1", x(0))
				.attr("x2", x(showColumns.length))
				.attr("y1", (d) => y(d))
				.attr("y2", (d) => y(d + 1))
				.attr("stroke", "black")
				.attr("stroke-width", 0.2);
		} else {
			this.svg.selectAll("line.verticalGrid").remove();
			this.svg.selectAll("line.horizontalGrid").remove();
		}
	}
	render(model: AnyModel<IWidgetModel>) {
		this._render(model);
		return this.svg.node();
	}
}

export default Sequence;
