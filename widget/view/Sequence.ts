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
		const sequenceLength = model.get("n_length");
		const numSequences = model.get("n_sequences");
		if (rects.length === 0 || labels.length === 0) {
			return;
		}

		const x = d3.scaleLinear([0, this.width]).domain([0, sequenceLength]);
		const y = d3.scaleLinear([0, this.height]).domain([0, numSequences]);

		const color = d3
			.scaleOrdinal(d3.schemeCategory10)
			.domain(labels.map((label) => label.id.toString()));

		this.svg
			.selectAll("rect")
			.data(rects)
			.join("rect")
			.attr("fill", (d: IRectModel) => color(d.id.toString()))
			// .transition() Column으로 Groupby 한다음에 Column 별로 Transition 적용되게 변경
			.attr("x", (d) => x(d.x))
			.attr("y", (d) => y(d.y_start))
			.attr("width", x(1) - x(0))
			.attr("height", (d) => y(d.y_end + 1) - y(d.y_start));
	}

	render(model: AnyModel<IWidgetModel>) {
		this._render(model);
		return this.svg.node();
	}
}

export default Sequence;
