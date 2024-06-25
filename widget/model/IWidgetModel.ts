import type ILabelModel from "./ILabelModel";
import type IRectModel from "./IRectModel";

export interface IWidgetModel {
	rects: IRectModel[];
	labels: ILabelModel[];
	n_sequences: number;
	n_length: number;
	width: number;
	height: number;
	grid: boolean;
}
