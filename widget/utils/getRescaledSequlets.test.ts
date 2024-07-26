import { ILabel, ISequlet } from "@/model/event";
import getRescaledSequlets from "./getRescaledSequlets";

describe("getRescaledSequlets", () => {
	it("should correctly rescale sequlets with default margin", () => {
		const sequlets: ISequlet[] = [
			{
				id: 0,
				rects: [
					{ x: 0, y: 0, width: 10, height: 10, value: 1 },
					{ x: 10, y: 10, width: 10, height: 10, value: 2 },
				],
			},
		];
		const legend: ILabel[] = [
			{ value: 1, name: "One" },
			{ value: 2, name: "Two" },
		];
		const width = 120;
		const height = 120;

		const result = getRescaledSequlets(sequlets, legend, width, height);

		expect(result).toHaveLength(1);
		expect(result[0].rects).toHaveLength(2);

		expect(result[0].rects[0].x).toBe(10);
		expect(result[0].rects[0].y).toBe(10);
		expect(result[0].rects[0].width).toBe(50);
		expect(result[0].rects[0].height).toBe(50);
		expect(result[0].rects[0].color).toMatch(/^#[0-9A-Fa-f]{6}$/);

		expect(result[0].rects[1].x).toBe(60);
		expect(result[0].rects[1].y).toBe(60);
		expect(result[0].rects[1].width).toBe(50);
		expect(result[0].rects[1].height).toBe(50);
		expect(result[0].rects[1].color).toMatch(/^#[0-9A-Fa-f]{6}$/);

		expect(result[0].rects[0].color).not.toBe(result[0].rects[1].color);
	});

	it("should correctly rescale sequlets with custom margin", () => {
		const sequlets: ISequlet[] = [
			{
				id: 0,
				rects: [
					{ x: 0, y: 0, width: 10, height: 10, value: 1 },
					{ x: 10, y: 10, width: 10, height: 10, value: 2 },
				],
			},
		];
		const legend: ILabel[] = [
			{ value: 1, name: "One" },
			{ value: 2, name: "Two" },
		];
		const width = 140;
		const height = 140;
		const margin = { top: 20, right: 20, bottom: 20, left: 20 };

		const result = getRescaledSequlets(sequlets, legend, width, height, margin);

		expect(result[0].rects[0].x).toBe(20);
		expect(result[0].rects[0].y).toBe(20);
		expect(result[0].rects[0].width).toBe(50);
		expect(result[0].rects[0].height).toBe(50);

		expect(result[0].rects[1].x).toBe(70);
		expect(result[0].rects[1].y).toBe(70);
		expect(result[0].rects[1].width).toBe(50);
		expect(result[0].rects[1].height).toBe(50);
	});

	it("should handle empty input", () => {
		const result = getRescaledSequlets([], [], 100, 100);
		expect(result).toEqual([]);
	});
});
