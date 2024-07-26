import type { IWidget } from "@/model";
import { getRescaledSequlets } from "@/utils";
import { Legend, Sequence } from "@/view";
import type { RenderProps } from "@anywidget/types";
import { html, render } from "lit-html";

function renderWidget({ model, el }: RenderProps<IWidget>) {
	const widget = document.createElement("div");
	widget.id = "widget";

	const sequenceView = new Sequence(model.get("width"), model.get("height"));
	const legendView = new Legend();
	const sequlets = getRescaledSequlets(
		model.get("sequlets"),
		model.get("labels"),
		model.get("width"),
		model.get("height"),
	);

	render(
		html`
      ${legendView.render(model.get("labels"))}
      <div id="sequenceView" style="padding:10px;">
        ${sequenceView.render(sequlets, model.get("labels"))}
      </div>
    `,
		widget,
	);
	el.appendChild(widget);
}

export default { render: renderWidget };
