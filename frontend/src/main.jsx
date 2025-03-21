import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'
import { NextUIProvider } from '@nextui-org/system'
import { Provider } from 'react-redux';
import { store, persistor } from './Redux/Store.ts'
import { ThemeProvider } from "@material-tailwind/react";
import { PersistGate } from 'redux-persist/integration/react';


ReactDOM.createRoot(document.getElementById('root')).render(
  // <React.StrictMode>
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <NextUIProvider>
          <ThemeProvider>
            <App />
          </ThemeProvider>
        </NextUIProvider>
      </PersistGate>
    </Provider>
  // {/* </React.StrictMode>, */}
)
