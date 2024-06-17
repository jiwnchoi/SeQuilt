import type { RenderProps } from "@anywidget/types"
import "./widget.css"

/* Specifies attributes defined with traitlets in ../src/seq/__init__.py */
interface WidgetModel {
  value: number
  /* Add your own */
}

function render({ model, el }: RenderProps<WidgetModel>) {
  let btn = document.createElement("button")
  btn.innerHTML = `count231 is ${model.get("value")}`
  btn.addEventListener("click", () => {
    model.set("value", model.get("value") + 1)
    model.save_changes()
  })
  model.on("change:value", () => {
    btn.innerHTML = `count234 is ${model.get("value")}`
  })
  el.classList.add("seq")
  el.appendChild(btn)
}

export default { render }
