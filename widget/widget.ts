import type { IWidgetModel } from "@/model";
import { Legend, Sequence } from "@/view";
import type { RenderProps } from "@anywidget/types";
import { html, render } from "lit-html";

function renderWidget({ model, el }: RenderProps<IWidgetModel>) {
	const widget = document.createElement("div");
	widget.id = "widget";

	const width = model.get("width");
	const height = model.get("height");

	const sequenceView = new Sequence(width, height);
	const legendView = new Legend();

	model.on("change:rects", () => {
		sequenceView._render(model);
	});

	render(
		html`
        <div id="sequences-view" style="background-color: transparent;">
          ${legendView.render(model.get("labels"))}
          ${sequenceView.render(model)}
        </div>`,
		widget,
	);
	el.appendChild(widget);
}

export default { render: renderWidget };
