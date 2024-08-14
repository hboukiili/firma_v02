import { combineReducers, configureStore, getDefaultMiddleware } from "@reduxjs/toolkit";
import { policyMakerSlice } from "./Policymaker/Slices";
import { FarmerSlice } from "./Farmer/Slices";
import {
  persistStore,
  persistReducer,
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER,
} from "redux-persist";

import storage from "redux-persist/lib/storage";
import {thunk} from 'redux-thunk';
import { userSlice } from "./userInfo/Slices";

// import createSagaMiddleware from 'redux-saga';
// const sagaMiddleware = createSagaMiddleware();

const persistConfig = {
  key: "root",
  storage,
};

const rootReducer = combineReducers({ 
  userInfo: userSlice.reducer,
    policyMaker: policyMakerSlice.reducer,
    farmer: FarmerSlice.reducer,
})

const persistedReducer = persistReducer(persistConfig, rootReducer);

export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
        ignoredPaths: ['farmer.someNonSerializablePath'], // Adjust this path as necessary

      },
    }).concat(thunk),
  // {
  //   userInfo: userSlice.reducer,
  //   policyMaker: policyMakerSlice.reducer,
  //   farmer: FarmerSlice.reducer,
    // middleware: (getDefaultMiddleware) =>
    //   getDefaultMiddleware({
    //     serializableCheck: false, // Disable serializable checks
    //   }),
    // middleware: (getDefaultMiddleware) =>
    //   getDefaultMiddleware().concat(sagaMiddleware),
  // },
});

export const persistor = persistStore(store);
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
