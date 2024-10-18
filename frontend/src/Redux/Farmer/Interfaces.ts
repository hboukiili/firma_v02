import L from "leaflet";

interface field_ {
  id: number;
  name: string;
  boundaries: { type: string; coordinates: [][] };
}

interface IrrigationSystem {
  system: string;
  prop: {
    //crop prop

    sprinklerCoverage_c: number;
    WaterOutflowRate_c: number;
    numberOfSprinklers_c: number;
    DistanceBetweenTubes_c: number;
    DistanceBetweenDrippers_c: number;

    //tree prop
    DistanceBetweenRows_t: number;
    DistanceBetweenTrees_t: number;
    NumberOfTubesPerTree_t: number;
    NumberOfDrippersPerTree_t: number;
    WaterOutflowRate_t: number;
  } | null;
}

interface PlantingDetails {
  type : string,
  Tree: { value: string; date: string };
  Crop: { value: string; date: string };
}

export interface SoilPr {
  clay: number;
  sand: number;
  silt: number;
}

export interface Farmer {
  [key: string]: any;
  IrrigationType: IrrigationSystem | null;
  SoilType: string;
  PlantingDetails: PlantingDetails | null;
  fieldNames: string[];
  Data: undefined;
  loadingMsg: string;
  isLoading: boolean;
  isTheFirstTime: boolean;
  err: string;
  file: [];
  polygon_: any;
  fieldName: string;
  layer: Map<any, any>;
  DrawOption: boolean;
  Map: L.Map;
  Field: [];
  currentField: field_ | null;
  fieldInfo: field_[];
  boundaries: [];
  soilPr: SoilPr | null;
  soilCheck: boolean;
  soilMethod : string
}
