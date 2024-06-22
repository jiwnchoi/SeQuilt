import type { ILabelModel } from "@/model";
import { schemeCategory10 } from "d3";
import { html, render } from "lit-html";
import { repeat } from "lit-html/directives/repeat.js";

class Legend {
	container: HTMLElement;

	constructor() {
		this.container = document.createElement("div");
	}

	render(labels: ILabelModel[]) {
		const colorScale = schemeCategory10;
		const size = 10;

		const legendTemplate = html`
      <ul style="list-style-type: none; padding: 0; display: flex; flex-direction: row; gap: 8px;">
        ${repeat(
					labels,
					(label) => label.id,
					(label, index) => html`
          <li style="display: flex; align-items: center; gap: 4px;">
            <span style="display: inline-block; width: ${size}px; height: ${size}px; background-color: ${colorScale[index % colorScale.length]};"></span>
            ${label.token}
          </li>
        `,
				)}
      </ul>
    `;

		render(legendTemplate, this.container);
		return this.container;
	}
}

export default Legend;
