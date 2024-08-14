import { createSlice } from "@reduxjs/toolkit";
import { initialState } from "../Farmer/init";
import { setup_ } from "./Interfaces";

export const FarmerSlice = createSlice({
  name: "Farmer",
  initialState,
  reducers: {
    updateFarmerInfo: (state, action) => {
      Object.keys(action.payload).forEach((key) => {
        if (key in state) {
          state[key] = action.payload[key];
        }
      });
      if (!state.currentField && state.fieldInfo)
        state.currentField = state.fieldInfo[0];
    },
  },
});
