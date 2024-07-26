import { ILabel, ISequlet } from "./event";

interface IWidget {
	labels: ILabel[];
	sequlets: ISequlet[];

	width: number; // rendered width
	height: number; // rendered height

	grid: boolean;
}

export default IWidget;
