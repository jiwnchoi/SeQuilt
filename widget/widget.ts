import type { IWidgetModel } from "@/model";
import type { RenderProps } from "@anywidget/types";
import { html, render } from "lit-html";
import SeqeuenceView from "./view/Sequence";

function renderWidget({ model, el }: RenderProps<IWidgetModel>) {
	const widget = document.createElement("div");
	const sequenceView = new SeqeuenceView(800, 300);
	model.on("change:ids", () => {
		console.log("changed");
		sequenceView.render(model.get("ids"), model.get("feature_ids"));
	});
	model.on("change:feature_ids", () => {
		// render legend
		// render view
	});
	sequenceView.render(model.get("ids"), model.get("feature_ids"));
	render(html`<div id="sequences-view">${sequenceView.node()}</div>`, widget);
	el.appendChild(widget);
}

export default { render: renderWidget };
