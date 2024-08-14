// import L from "leaflet";

interface field_ {
  id: number;
  name: string;
  boundaries: { type: string; coordinates: [][] };
}

interface IrrigationSystem {
  system : string,
  prop : {
    SprinklerRadius : number,
    sprinklerCoverage : number,
    WaterOutflowRate : number,
    numberOfSprinklers : number,
    DistanceBetweenTubes : number,
    DistanceBetweenDrippers : number,
    CoverageAreaOfEachDrippers : number,
  } | null
}

interface PlantingDetails {
  type: string,
  value : string,
  date : any,
}

export interface Farmer {
  [key: string]: any;
  IrrigationType: IrrigationSystem | null;
  SoilType: string;
  PlantingDetails : PlantingDetails | null
  fieldNames: string[];
  Data: undefined;
  loadingMsg: string;
  isLoading: boolean;
  isTheFirstTime: boolean;
  err: string;
  file: [];
  polygon_: any;
  fieldName: string;
  layer: any;
  DrawOption: boolean;
  Map: undefined;
  Field: [];
  currentField: field_ | null;
  fieldInfo: field_[],
  boundaries : []
}
