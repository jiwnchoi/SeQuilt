import type { IWidget } from "@/model";
import { getRescaledSequlets } from "@/utils";
import { Legend, Sequence } from "@/view";
import type { RenderProps } from "@anywidget/types";
import { html, render } from "lit-html";

function renderWidget({ model, el }: RenderProps<IWidget>) {
	const widget = document.createElement("div");

	const width = model.get("width");
	const height = model.get("height");

	const sequenceView = new Sequence(width, height);
	const legendView = new Legend();

	model.on("change:labels", (_, labels) => {
		legendView.render(labels);
	});

	model.on("change:sequlets", (_, sequlets) => {
		sequenceView.render(
			getRescaledSequlets(sequlets, model.get("labels"), width, height),
		);
	});

	render(
		html`
      ${legendView.render(model.get("labels"))}
      <div id="sequenceView" style="padding:10px;">
        ${sequenceView.render(
					getRescaledSequlets(
						model.get("sequlets"),
						model.get("labels"),
						width,
						height,
					),
				)}
      </div>
    `,
		widget,
	);
	el.appendChild(widget);
}

export default { render: renderWidget };
