import { Point, Rect } from "@/model";

function getOutlinePoints(rects: Rect[]): Point[] {
	const processedSet = new Set<string>();
	const duplicateSet = new Set<string>();

	const points: Point[] = rects.flatMap((rect) => [
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

function _getNextPoint(currentPoint: Point, points: Point[]) {
	if (currentPoint.type == "top-left") {
		return points.find((point) => point.y === currentPoint.y);
	} else if (currentPoint.type == "top-right") {
		return points.find((point) => point.x === currentPoint.x);
	} else if (currentPoint.type == "bottom-right") {
		return points.reduceRight(
			(acc, point) => (point.y === currentPoint.y ? point : acc),
			{} as Point,
		);
	} else if (currentPoint.type == "bottom-left") {
		return points.reduceRight(
			(acc, point) => (point.x === currentPoint.x ? point : acc),
			{} as Point,
		);
	}
	return undefined;
}

function getOutline(rects: Rect[]): string {
	let points = getOutlinePoints(rects);
	const initialPoint = points.shift();
	if (!initialPoint) return "";

	let path = `M${initialPoint.x} ${initialPoint.y}`;
	let currentPoint = initialPoint;

	while (points.length > 0) {
		const nextPoint = _getNextPoint(currentPoint, points);
		if (!(nextPoint && "x" in nextPoint)) break;
		points = points.filter(
			(point) => !(point.x === nextPoint.x && point.y === nextPoint.y),
		);
		path += ` L${nextPoint.x} ${nextPoint.y}`;
		currentPoint = nextPoint;
	}

	path += " Z";
	return path;
}

export { getOutlinePoints, getOutline };
