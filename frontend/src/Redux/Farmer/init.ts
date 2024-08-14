import L from "leaflet";
import { Farmer } from "./Interfaces";

export const initialState: Farmer = {
  name: "",
  id: "",
  IrrigationType:  null,
  SoilType: "",
  PlantingDetails : null,
  fieldNames: [],
  Data: undefined,
  loadingMsg: "",
  isLoading: false,
  isTheFirstTime: false,
  err: "",
  file: [],
  polygon_: null,
  fieldName: "",
  layer: null,
  Field: [],
  DrawOption: false,
  Map: undefined,
  currentField: null,
  fieldInfo: [],
  boundaries : []
};
