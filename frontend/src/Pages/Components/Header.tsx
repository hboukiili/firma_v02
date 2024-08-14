import React from "react";
import { ReactSVG } from "react-svg";
import not from "./../../assets/notif.svg";
import out from "./../../assets/logout.svg";
import set from "./../../assets/sett.svg";
import api from "../../api/axios.js";
import Logo from "./../../assets/logo.svg";
import { useLocation } from "react-router-dom";

const Header = () => {
  const location = useLocation();

  return (
    <div
      className={`${
        location.pathname == "/farmer" ? "max-w-[93%] " : "w-[99%]"
      } grow rounded-lg m-2 h-[68px] p-6 z-10  bg-gray-50 flex items-center justify-between self-end`}
    >
      <ReactSVG className="w-[50px]" src={Logo} />
      <div className="w-[10%] flex justify-between items-center mr-[3%]">
        <button>
          <ReactSVG className="w-[15px]" src={not} />
        </button>
        <button>
          <ReactSVG className="w-[15px]" src={set} />
        </button>
        <button
          onClick={() => {
            api.get("/api_auth/").then((res) => {
              console.log(res);
            });
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            localStorage.clear();
            window.location.href = "/login"; // Redirect to the login page
          }}
        >
          <ReactSVG className="w-[15px]" src={out} />
        </button>
      </div>
    </div>
  );
};

export default Header;
