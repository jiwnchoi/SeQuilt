function a({ model: e, el: n }) {
	const t = document.createElement("button");
	(t.innerHTML = `count231 is ${e.get("value")}`),
		t.addEventListener("click", () => {
			e.set("value", e.get("value") + 1), e.save_changes();
		}),
		e.on("change:value", () => {
			t.innerHTML = `count234 is ${e.get("value")}`;
		}),
		n.classList.add("seq"),
		n.appendChild(t);
}
const s = { render: a };
export { s as default };
