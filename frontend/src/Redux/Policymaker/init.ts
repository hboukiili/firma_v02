import { initialSubW, policyMaker } from "./Interfaces"

export const initialState: policyMaker = {
    isLoading: false,
    isSubmit: false,
    IsBaseMap: false,
    IsGeoRaster: false,
    IsAllDataReceived: false,
    WatershedId: "",
    SubWatershedId: "",
    SubWatersheds: initialSubW,
    StartDate: "",
    EndDate: "",
    Band: "",
    loadingMsg: "",
    Imgs: [],
    ChartData: null,
    Dates: [],
    Weather: [],
    SurfaceVariable: [],
    Flux: [],
}

