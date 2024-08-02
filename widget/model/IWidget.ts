import type ILabel from "./ILabel";
import type ISequlet from "./ISequlet";

interface IWidget {
  labels: ILabel[];
  sequlets: ISequlet[];

  width: number; // rendered width
  height: number; // rendered height

  grid: boolean;
}

export default IWidget;
