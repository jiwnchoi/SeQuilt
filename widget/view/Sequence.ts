import type { ILabelModel, TSequenceModel } from "@/model";
import * as d3 from "d3";

class SequenceView {
	svg: d3.Selection<SVGSVGElement, undefined, null, undefined>;
	width: number;
	height: number;

	constructor(width: number, height: number) {
		this.svg = d3.create("svg").attr("viewBox", [0, 0, width, height]);
		this.width = width;
		this.height = height;
	}

	render(sequences: TSequenceModel[], labels: ILabelModel[]) {
		if (sequences.length === 0 || labels.length === 0) {
			return;
		}

		const windowLength = sequences[0].length;

		const x = d3.scaleLinear().domain([0, windowLength]).range([0, this.width]);
		const y = d3
			.scaleLinear()
			.domain([0, sequences.length])
			.range([0, this.height]);

		this.svg
			.selectAll("g")
			.data(sequences)
			.join("g")
			.attr("transform", (_, i) => `translate(0, ${y(i)})`)
			// .attr("stroke", "#F2F2F2")
			.selectAll("rect")
			.data((d) => d)
			.join("rect")
			.attr("x", (_, i) => x(i))
			.attr("y", 0)
			.attr("width", x(1) - x(0))
			.attr("height", y(1) - y(0))
			// .attr("stroke", "#F2F2F2")
			// .attr("stroke-width", 0.1)
			.attr("fill", (d) =>
				labels.map((l) => l.id).includes(d)
					? d3.schemeCategory10[labels.findIndex((l) => l.id === d)]
					: "transparent",
			)
			.attr("class", "cell");

		return this.svg.node();
	}
}

export default SequenceView;
