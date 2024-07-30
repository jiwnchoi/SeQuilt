import { IPoint, IRect } from "@/model";

declare global {
	interface Array<T> {
		findRight(
			predicate: (value: T, index: number, obj: T[]) => unknown,
		): T | undefined;
	}
}

Array.prototype.findRight = function <T>(
	this: T[],
	predicate: (value: T, index: number, obj: T[]) => unknown,
): T | undefined {
	return this.reduceRight(
		(acc: T | undefined, current: T, index: number, array: T[]) => {
			if (acc !== undefined) {
				return acc;
			}
			return predicate(current, index, array) ? current : undefined;
		},
		undefined,
	);
};

function getOutlinePoints(rects: IRect[]): IPoint[] {
	const processedSet = new Set<string>();
	const duplicateSet = new Set<string>();

	const points: IPoint[] = rects.flatMap((rect) => [
		{ x: rect.x, y: rect.y, type: "top-left" },
		{ x: rect.x + rect.width, y: rect.y, type: "top-right" },
		{ x: rect.x, y: rect.y + rect.height, type: "bottom-left" },
		{ x: rect.x + rect.width, y: rect.y + rect.height, type: "bottom-right" },
	]);

	points.forEach((point) => {
		const key = `${point.x},${point.y}`;
		if (!processedSet.has(key) && !duplicateSet.has(key)) {
			processedSet.add(key);
		} else if (processedSet.has(key) && !duplicateSet.has(key)) {
			processedSet.delete(key);
			duplicateSet.add(key);
		}
	});

	return points
		.filter((point) => processedSet.has(`${point.x},${point.y}`))
		.sort((a, b) => (a.x === b.x ? a.y - b.y : a.x - b.x));
}

function _getNextPoint(currentPoint: IPoint, points: IPoint[]) {
	if (currentPoint.type == "top-left") {
		return points.find(
			(point) => point.y === currentPoint.y && point.type === "top-right",
		);
	} else if (currentPoint.type == "top-right") {
		return points.find((point) => point.x === currentPoint.x);
	} else if (currentPoint.type == "bottom-right") {
		return points.findRight(
			(point) => point.y === currentPoint.y && point.type === "bottom-left",
		);
	} else if (currentPoint.type == "bottom-left") {
		return points.findRight((point) => point.x === currentPoint.x);
	}
	return undefined;
}

function getOutline(rects: IRect[]): string {
	let points = getOutlinePoints(rects);
	const initialPoint = points.shift();
	if (!initialPoint) return "";

	let path = `M ${initialPoint.x} ${initialPoint.y}`;
	let currentPoint = initialPoint;

	while (points.length > 0) {
		const nextPoint = _getNextPoint(currentPoint, points);
		if (!(nextPoint && "x" in nextPoint)) break;
		points = points.filter(
			(point) => !(point.x === nextPoint.x && point.y === nextPoint.y),
		);

		path += ` L ${nextPoint.x} ${nextPoint.y}`;
		currentPoint = nextPoint;
	}

	path += " Z";
	return path;
}

export { getOutline, getOutlinePoints };

