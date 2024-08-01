import type { IRect } from "@/model";
import { getOutline, getOutlinePoints } from "./getOutline";

const dummyRects: IRect[] = [
  {
    value: 1,
    x: 0,
    y: 100,
    width: 1,
    height: 100,
  },
  {
    value: 2,
    x: 1,
    y: 0,
    width: 1,
    height: 300,
  },
  {
    value: 3,
    x: 2,
    y: 0,
    width: 1,
    height: 200,
  },
];

test("getOutlinePoint with empty rects", () => {
  expect(getOutlinePoints([])).toEqual([]);
});

test("getOutlinePoint with one rect", () => {
  expect(getOutlinePoints([{ x: 0, y: 0, width: 1, height: 100, value: 1 }])).toEqual([
    { x: 0, y: 0, type: "top-left" },
    { x: 0, y: 100, type: "bottom-left" },
    { x: 1, y: 0, type: "top-right" },
    { x: 1, y: 100, type: "bottom-right" },
  ]);
});

test("getOutlinePoint with two rect", () => {
  expect(getOutlinePoints(dummyRects)).toEqual([
    { x: 0, y: 100, type: "top-left" },
    { x: 0, y: 200, type: "bottom-left" },
    { x: 1, y: 0, type: "top-left" },
    { x: 1, y: 100, type: "top-right" },
    { x: 1, y: 200, type: "bottom-right" },
    { x: 1, y: 300, type: "bottom-left" },
    { x: 2, y: 200, type: "bottom-left" },
    { x: 2, y: 300, type: "bottom-right" },
    { x: 3, y: 0, type: "top-right" },
    { x: 3, y: 200, type: "bottom-right" },
  ]);
});

test("getOutline produces correct path", () => {
  expect(getOutline(dummyRects)).toEqual(
    "M 0 100 L 1 100 L 1 0 L 3 0 L 3 200 L 2 200 L 2 300 L 1 300 L 1 200 L 0 200 Z",
  );
});
