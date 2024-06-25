import type { IWidgetModel } from "@/model";
import type { RenderProps } from "@anywidget/types";
import { html, render } from "lit-html";
import SeqeuenceView from "./view/Sequence";
import { Legend } from "./view";

function renderWidget({ model, el }: RenderProps<IWidgetModel>) {
	const widget = document.createElement("div");
	widget.id = "widget";
	const sequenceView = new SeqeuenceView(800, 400);
	const legendView = new Legend();

	model.on("change:sequences", () => {
		sequenceView._render(model.get("sequences"), model.get("labels"));
	});

	render(
		html`
        <div id="sequences-view" style="background-color: transparent;">
          ${legendView.render(model.get("labels"))}
          ${sequenceView.render(model.get("sequences"), model.get("labels"))}
        </div>`,
		widget,
	);
	el.appendChild(widget);
}

export default { render: renderWidget };
