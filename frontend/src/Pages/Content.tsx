import React, { lazy, Suspense, useEffect } from "react";

import SideBar from "./Components/Sidebar";
import Header from "./Components/Header";
import { useLocation, useNavigate } from "react-router-dom";
import Setup from "./Farmer/setup";
import { notification } from "antd";
import { useAppDispatch, useAppSelector } from "../Redux/hooks";
import { setErr } from "../Redux/Farmer/actions";
import FieldManagment from "./Farmer/fieldmanagment";
import Cropgrowth_ from "./Farmer/cropgrowth";
import Aquacrop from "./Farmer/Aquacrop";
// import Climate from "./Farmer/climate";

const Dashboard = lazy(() => import(`./Farmer/Dashboard`));
const Policymaker = lazy(() => import(`./Policymaker/Policymaker`));
const Academic = lazy(() => import(`./academin/Academic`));
const Cropgrowth = lazy(() => import(`./Cropgrowth`));
const Climate = lazy(() => import(`./Farmer/climate`))
const FieldCrops = lazy(() => import(`./AddField`));

const Content = () => {
  const location = useLocation();
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  const [api, contextHolder] = notification.useNotification();
  //err handler
  const openNotificationWithIcon = (err: string) => {
    api["error"]({
      placement: "bottomRight",
      message: "Error",
      description: err,
    });
  };

  useEffect(() => {
    if (Data.err) openNotificationWithIcon(Data.err);
    // dispatch(setErr(''))
  }, [Data.err]);
  return (
    <div className=" flex b justify-between w-screen flex-col relative">
      {location.pathname != "/policymaker" &&
        location.pathname != "/farmersetup" && (
          <div className="w-full flex justify-between z-50">
            <div className="relative w-[7%] min-w-[120px] ">
              <SideBar />
            </div>
            {location.pathname != "/farmersetup" && <Header />}
          </div>
        )}
      <div className={`"md:ml-[5rem] flex  items-center  flex-col grow " `}>
        {location.pathname == "/farmer" && <Dashboard />}
        {location.pathname == "/addfield" && <FieldCrops />}
        {location.pathname == "/cropgrowth" && <Cropgrowth_ />}
        {location.pathname.startsWith("/policymaker") && <Policymaker />}
        {location.pathname == "/academic" && <Academic />}
        {location.pathname == "/farmersetup" && <Setup />}
        {location.pathname == "/fieldmanagment" && <FieldManagment />}
        {location.pathname == "/climate" && <Climate />}
        {location.pathname == "/aquacrop" && <Aquacrop />}
      </div>
      {/* {contextHolder} */}
    </div>
  );
};

export default Content;