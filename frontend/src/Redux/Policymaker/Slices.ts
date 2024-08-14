import { createSlice } from "@reduxjs/toolkit"
import { initialState } from "./init"

export const policyMakerSlice = createSlice({
    name: "Policymaker",

    initialState,

    reducers: {
        SetIsGeoRaster: (state, action) => {
            state.IsGeoRaster = action.payload
        },
        SetIsBaseMap: (state, action) => {
            state.IsBaseMap = action.payload
        },
        SetChartData: (state, action) => {
            state.ChartData = action.payload
        },
        SetisLoading: (state, action) => {
            state.isLoading = action.payload
        },
        SetWaterShedId: (state, action) => {
            state.WatershedId = action.payload
        },
        SetStartDate: (state, action) => {
            state.StartDate = action.payload
        },
        SetEndDate: (state, action) => {
            state.EndDate = action.payload
        },
        SetBand: (state, action) => {
            state.Band = action.payload
        },
        SetLoadingMsg: (state, action) => {
            state.loadingMsg = action.payload
        },
        SetIsSubmit: (state, action) => {
            state.isSubmit = action.payload
        },
        SetSubWaterShedId: (state, action) => {
            state.SubWatershedId = action.payload
        },
        SetWeather: (state, action) => {
            state.Weather = action.payload
            if (state.Flux.length && state.SurfaceVariable.length && state.Weather.length)
                state.IsAllDataReceived = true
            if (state.Weather)
                state.Dates = state.Weather[0].dates.map((item, _) => new Date(item))
        },
        SetSurfaceVariable: (state, action) => {
            state.SurfaceVariable = action.payload
            if (state.Flux.length && state.SurfaceVariable.length && state.Weather.length)
                state.IsAllDataReceived = true
            if (state.SurfaceVariable)
                state.Dates = state.SurfaceVariable[0].dates.map((item, _) => new Date(item))
        },
        SetFlux: (state, action) => {
            state.Flux = action.payload
            if (state.Flux.length && state.SurfaceVariable.length && state.Weather.length)
                state.IsAllDataReceived = true
            if (state.Flux)
                state.Dates = state.Flux[0].dates.map((item, _) => new Date(item))
        },
        SetDates: (state, action) => {
            state.Dates = action.payload
        },
    }
})