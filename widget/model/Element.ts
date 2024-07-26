export interface Rect {
	x: number;
	y: number;
	width: number;
	height: number;
}

export interface Point {
	x: number;
	y: number;
	type: "top-left" | "top-right" | "bottom-left" | "bottom-right";
}
