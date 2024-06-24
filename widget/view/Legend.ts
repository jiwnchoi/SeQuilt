import type { ILabelModel } from "@/model";
import { schemeCategory10 } from "d3";
import { html, render } from "lit-html";
import { repeat } from "lit-html/directives/repeat.js";
import { styleMap } from "lit-html/directives/style-map.js";

const ulStyle = {
	listStyleType: "none",
	padding: "0",
	display: "flex",
	flexDirection: "row",
	gap: "8px",
};

const liStyle = {
	display: "flex",
	alignItems: "center",
	gap: "4px",
};

const spanStyle = (size: number, bgColor: string) => ({
	display: "inline-block",
	width: `${size}px`,
	height: `${size}px`,
	backgroundColor: bgColor,
});

class Legend {
	container: HTMLElement;

	constructor() {
		this.container = document.createElement("div");
	}

	render(labels: ILabelModel[]) {
		const colorScale = schemeCategory10;
		const size = 10;

		render(
			html`
      <ul style=${styleMap(ulStyle)}>
        ${repeat(
					labels,
					(label) => `label-${label.id}`,
					(label, index) => html`
          <li style=${styleMap(liStyle)}>
            <div style="${styleMap(spanStyle(size, colorScale[index]))}"></div>
            ${label.token}
            
          </li>
        `,
				)}
      </ul>
    `,
			this.container,
		);
		return this.container;
	}
}

export default Legend;
