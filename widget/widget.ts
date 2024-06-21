import type { RenderProps } from "@anywidget/types"
import { WidgetModel } from "@/model"

function render({ model, el }: RenderProps<WidgetModel>) {
  console.log(model.get("ids"))
  console.log(model.get("feature_ids"))

  let btn = document.createElement("button")
  btn.innerHTML = `coun22t231 is ${model.get("value")}`
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
