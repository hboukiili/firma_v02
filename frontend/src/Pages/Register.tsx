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
    console.log(Data)
    api
      .post("/farmer/register", {
        first_name: Data.first_name,
        last_name: Data.last_name,
        email: Data.email,
        password: Data.password,
        type: 'farmer',
      })
      .then((res) => {
        window.location.href = "/farmersetup";
        console.log(res)
    })
      .catch((res) => {
        console.log(res)
        SetData(res.response.data.message);
      });
  };

  return (
    <div className="h-screen w-full flex justify-center items-center">
      <form
        className="w-[25%] gap-[30px] flex flex-col justify-between items-center max-lg:w-[40%] max-md:w-[60%]"
        onSubmit={(e) => {
          e.preventDefault();
          post();
        }}
      >
        <h2 className="text-DarkGreen font-Myfont font-md">Register</h2>
        <div className="w-full gap-[20px] flex flex-col  items-center ">
          <Input
            required
            label="First name"
            placeholder="Enter your first name"
            type={"text"}
            className="max-w-xs"
            classNames={{ inputWrapper: "bg-[#EAF3E9]" }}
            onChange={(e) => {
              dispatch(updateUserInfo({ first_name: e.target.value }));
            }}
          />
          <Input
            required
            label="Last name"
            placeholder="Enter your last name"
            type={"text"}
            className="max-w-xs"
            classNames={{ inputWrapper: "bg-[#EAF3E9]" }}
            onChange={(e) => {
              dispatch(updateUserInfo({ last_name: e.target.value }));
            }}
          />
          <Input
            required
            label="Email"
            placeholder="Enter your Email"
            type={"email"}
            className="max-w-xs"
            classNames={{
              inputWrapper: "bg-[#EAF3E9]",
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
            classNames={{ inputWrapper: "bg-[#EAF3E9]" }}
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
            className="max-w-xs"
            onChange={(e) => {
              if (!e.target.checked)
                dispatch(updateUserInfo({ password: e.target.value }));
            }}
          />
          <Input
            required
            label="Confirm Password"
            placeholder="Confirm Your Password"
            classNames={{ inputWrapper: "bg-[#EAF3E9]" }}
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
            className="max-w-xs"
            onChange={(e) => SetpassVer(e.target.value)}
          />
        </div>
        <div className="w-full gap-[20px] flex flex-col justify-between items-center">
          <Button
            type="submit"
            radius="full"
            className="bg-Green  text-white  "
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
