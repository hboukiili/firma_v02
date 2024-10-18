import { useState } from "react";
import "./App.css";
import { BrowserRouter, Route, Router, Routes } from "react-router-dom";
import React, { lazy, Suspense } from "react";
import PuffLoader from "react-spinners/PuffLoader";
import "./Pages/Farmer/tools/style.css"
const Home = lazy(() => import(`./Pages/Home/index`));
const Login = lazy(() => import(`./Pages/Login`));
const Register = lazy(() => import(`./Pages/Register`));
const Content = lazy(() => import(`./Pages/Content`));
const Usertypes = lazy(() => import(`./Pages/usertypes`));
const Documentation = lazy(() => import("./Pages/Home/Documentation"));


function App() {
  return (
    <div className=" flex justify-center items-center relative bgF">
      <Suspense
        fallback={
          <div className="flex justify-center items-center h-screen">
            <PuffLoader className="" color="#48A788" />{" "}
          </div>
        }
      >
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<Home />} />
            <Route path="/register" element={<Register />} />
            <Route path="/usertypes" element={<Usertypes />} />
            <Route path="/farmer" element={<Content />} />
            <Route path="/farmer1" element={<Content />} />
            <Route path="/addfield" element={<Content />} />
            <Route path="/cropgrowth" element={<Content />} />
            <Route path="/policyMaker" element={<Content />} />
            <Route path="/academic" element={<Content />} />
            <Route path="/farmerSetup" element={<Content />} />
            <Route path="/fieldmanagment" element={<Content/>}/>
            <Route path="/newseason" element={<Content/>}/>
            <Route path="/climate" element={<Content/>}/>
            <Route path="/aquacrop" element={<Content/>}/>
            <Route path="/documentation" element={<Documentation/>}/>
          </Routes>
        </BrowserRouter>
      </Suspense>
    </div>
  );
}

export default App;