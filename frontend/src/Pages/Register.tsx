import React, { useState } from "react";
import { Button, Input } from "@nextui-org/react";
import { EyeSlashFilledIcon } from "./Components/Login/EyeSlashFilledIcon";
import { EyeFilledIcon } from "./Components/Login/EyeFilledIcon";
import { ReactSVG } from "react-svg";
import { Link } from "react-router-dom";
// import axios from "axios";
import api from "../api/axios.js";
import { useAppDispatch, useAppSelector } from "../Redux/hooks.js";
import { updateUserInfo } from "../Redux/userInfo/Actions.js";
import bg_ from "../assets/rg_bg.jpg";
import whLogo from "../assets/whLogo.svg";
interface register_ {
  username: string;
  password: string;
  password_verify: string;
  email: string;
}

const Register = () => {
  const toggleVisibility = () => setIsVisible(!isVisible);
  const [isVisible, setIsVisible] = React.useState(false);
  const [password_verify, SetpassVer] = useState("");
  const [data, SetData] = useState("");
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.userInfo);

  const post = () => {
    console.log(Data);
    api
      .post("/farmer/register", {
        first_name: Data.first_name,
        last_name: Data.last_name,
        email: Data.email,
        password: Data.password,
        type: "farmer",
      })
      .then((res) => {
        window.location.href = "/login";
        console.log(res);
      })
      .catch((res) => {
        console.log(res);
        SetData(res.response.data.message);
      });
  };

  return (
    <div className=" font-Myfont h-screen w-full flex items-center bg-[#f0f5ef]">
      <div className="relative flex flex-col justify-between w-[50%] h-full overflow-hidden drop-shadow-2xl">
        <div className="z-20 p-4 w-full flex justify-center pt-10">
          <img className="w-[120px]" src={whLogo} alt="logo" />
        </div>
        <div className="z-20 flex flex-col gap-2 justify-center items-center w-full text-white h-[20%]">
          <p className="font-bld text-[32px] ">Join FIRMA Today</p>
          <p className="text-center w-[50%]">
            Optimize your irrigation management with smart decision support
            tools that use real-time data and remote sensing to improve water
            efficiency and crop performance.
          </p>
        </div>
        <img className="inse-0 absolute bottom-0 w-full" src={bg_} alt="" />
      </div>
      <form
        className="w-[50%] bg-[#f0f5ef gap-[25px] flex flex-col items-center max-lg:w-[40%] max-md:w-[60%]"
        onSubmit={(e) => {
          e.preventDefault();
          post();
        }}
      >
        <div className="w-[49%] text-[#2b2b2b] flex flex-col gap-2">
          <h2 className="font-Myfont font-bld text-[24px]">
            Create Your Account
          </h2>
          <p className="text-wrap w-full">
            Gain access to real-time insights, remote sensing data, and
            field-scale recommendations.
          </p>
        </div>
        <div className="w-full gap-[20px] flex flex-col  items-center ">
          <Input
            required
            label="First name"
            placeholder="Enter your first name"
            type={"text"}
            className="max-w-[50%]"
            classNames={{ inputWrapper: "bg-[#fbfffb] " }}
            onChange={(e) => {
              dispatch(updateUserInfo({ first_name: e.target.value }));
            }}
          />
          <Input
            required
            label="Last name"
            placeholder="Enter your last name"
            type={"text"}
            className="max-w-[50%]"
            classNames={{ inputWrapper: "bg-[#fbfffb] " }}
            onChange={(e) => {
              dispatch(updateUserInfo({ last_name: e.target.value }));
            }}
          />
          <Input
            required
            label="Email"
            placeholder="Enter your Email"
            type={"email"}
            className="max-w-[50%]"
            classNames={{
              inputWrapper: "bg-[#fbfffb] ",
              mainWrapper: "hover:bg-black",
            }}
            onChange={(e) => {
              dispatch(updateUserInfo({ email: e.target.value }));
            }}
          />
          <Input
            required
            label="Password"
            placeholder="Enter your password"
            classNames={{ inputWrapper: "bg-[#fbfffb] " }}
            endContent={
              <button
                className="focus:outline-none"
                type="button"
                onClick={toggleVisibility}
              >
                {isVisible ? (
                  <EyeSlashFilledIcon className="text-2xl text-default-400 pointer-events-none" />
                ) : (
                  <EyeFilledIcon className="text-2xl text-default-400 pointer-events-none" />
                )}
              </button>
            }
            type={isVisible ? "text" : "password"}
            className="max-w-[50%]"
            onChange={(e) => {
              if (!e.target.checked)
                dispatch(updateUserInfo({ password: e.target.value }));
            }}
          />
          <Input
            required
            label="Confirm Password"
            placeholder="Confirm Your Password"
            classNames={{ inputWrapper: "bg-[#fbfffb] " }}
            endContent={
              <button
                className="focus:outline-none"
                type="button"
                onClick={toggleVisibility}
              >
                {isVisible ? (
                  <EyeSlashFilledIcon className="text-2xl text-default-400 pointer-events-none" />
                ) : (
                  <EyeFilledIcon className="text-2xl text-default-400 pointer-events-none" />
                )}
              </button>
            }
            type={isVisible ? "text" : "password"}
            className="max-w-[50%]"
            onChange={(e) => SetpassVer(e.target.value)}
          />
        </div>
        <div className="w-full gap-[20px] flex flex-col justify-between items-center">
          <Button
            type="submit"
            radius="full"
            className="bg-Green font-bld  text-white w-[50%] "
          >
            Register
          </Button>

          <h1 className="text-[#DC4545] font-Myfont font-bld text-[12px]">
            {data}
          </h1>
        </div>
      </form>
    </div>
  );
};

export default Register;
