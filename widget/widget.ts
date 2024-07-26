import type { IWidget } from "@/model";
import type { RenderProps } from "@anywidget/types";
import { html, render } from "lit-html";

function renderWidget({ model, el }: RenderProps<IWidget>) {
	const widget = document.createElement("div");
	widget.id = "widget";
	console.log(model);
	// const width = model.get("width");
	// const height = model.get("height");

	// const sequenceView = new Sequence(model);
	// const legendView = new Legend();

	// model.on("change:rects", () => {
	// 	sequenceView._render(model);
	// });
	// model.on("change:grid", () => {
	// 	sequenceView._render(model);
	// });

	// render(
	// 	html`
	//       <div id="sequences-view" style="background-color: transparent;">
	//         ${legendView.render(model.get("labels"))}
	//         ${sequenceView.render(model)}
	//       </div>`,
	// 	widget,
	// );
	render(html`<div>Hello W123123orld1d</div>`, widget);
	el.appendChild(widget);
}

export default { render: renderWidget };
