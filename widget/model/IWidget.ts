import { ILabel, ISequlet } from "./event";

interface IWidget {
	labels: ILabel[];
	sequlets: ISequlet[];

	width: number; // rendered width
	height: number; // rendered height

	grid: boolean;

	canvasWidth: number; // canvas width (sequence length)
	canvasHeight: number; // canvas height (compressed height)
}

export default IWidget;
