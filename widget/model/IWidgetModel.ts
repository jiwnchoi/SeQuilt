import type ILabelModel from "./ILabelModel";
import type TSequenceModel from "./TSequenceModel";

export interface IWidgetModel {
	sequences: TSequenceModel[];
	labels: ILabelModel[];
}
