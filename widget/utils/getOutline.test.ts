import { IRect } from "@/model";
import { getOutline, getOutlinePoints } from "./getOutline";

const dummyRects: IRect[] = [
	{
		x: 0,
		y: 0,
		width: 100,
		height: 100,
	},
	{
		x: 100,
		y: 0,
		width: 100,
		height: 150,
	},
];

test("getOutlinePoint with empty rects", () => {
	expect(getOutlinePoints([])).toEqual([]);
});

test("getOutlinePoint with one rect", () => {
	expect(getOutlinePoints([{ x: 0, y: 0, width: 100, height: 100 }])).toEqual([
		{ x: 0, y: 0, type: "top-left" },
		{ x: 0, y: 100, type: "bottom-left" },
		{ x: 100, y: 0, type: "top-right" },
		{ x: 100, y: 100, type: "bottom-right" },
	]);
});

test("getOutlinePoint with two rect", () => {
	expect(getOutlinePoints(dummyRects)).toEqual([
		{ x: 0, y: 0, type: "top-left" },
		{ x: 0, y: 100, type: "bottom-left" },
		{ x: 100, y: 100, type: "bottom-right" },
		{ x: 100, y: 150, type: "bottom-left" },
		{ x: 200, y: 0, type: "top-right" },
		{ x: 200, y: 150, type: "bottom-right" },
	]);
});

test("getOutline produces correct path", () => {
	expect(getOutline(dummyRects)).toEqual(
		"M0 0 L200 0 L200 150 L100 150 L100 100 L0 100 Z",
	);
});
