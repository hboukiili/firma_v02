import React, { useState } from "react";
import { Button, Input } from "@nextui-org/react";
import { EyeSlashFilledIcon } from "./Components/Login/EyeSlashFilledIcon";
import { EyeFilledIcon } from "./Components/Login/EyeFilledIcon";
import { ReactSVG } from "react-svg";
import logo from "../assets/logo.svg";
import { Link } from "react-router-dom";
import api from "../api/axios.js";
import { useAppDispatch, useAppSelector } from "../Redux/hooks.js";

const Login = () => {
  const [isVisible, setIsVisible] = React.useState(false);
  const toggleVisibility = () => setIsVisible(!isVisible);
  const [username, SetUsername] = useState("");
  const [password, SetPassword] = useState("");
  const [Error, setError] = useState("");
  const [Loading, setLoading] = useState(true);
  const [data, SetData] = useState<{
    access_token: string;
    refresh_token: string;
  }>();
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.userInfo);
  const post = async () => {
    if (!username || !password) {
      setError("Please enter both username and password.");
    } else {
      const user = {
        email: username,
        password: password,
      };
      await api
        .post("/farmer/login", user)
        .then((res) => {
          if (res.data?.access_token && res.data?.refresh_token) {
            localStorage.setItem("access_token", res.data?.access_token);
            localStorage.setItem("refresh_token", res.data?.refresh_token);
            window.location.href = res.data.is_new
              ? "/farmersetup"
              : "/farmer1";
          } else setError("Invalid username or password.");
        })
        .catch((error) => {
          console.log(error);
          console.log("error");

          if (error.response) {
            if (error.response.status === 401)
              setError("Invalid username or password.");
            else if (error.response.status === 400)
              setError("Please enter valid credentials.");
            else setError(error.response.data.message);
          } else
            setError(
              "Network error. Please check your internet connection.111"
            );
        });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    post();
  };

  return (
    <div className="w-screen h-screen flex justify-center items-center">
      <form
        onSubmit={handleSubmit}
        className="w-[25%] gap-[25px] flex flex-col justify-between items-center max-lg:w-[40%] max-md:w-[60%]"
      >
        <div className=" h-[100px] w-full flex justify-center items-center">
          <ReactSVG className="w-[130px]" src={logo} />
        </div>
        <div className="w-full gap-[30px] flex flex-col  items-center ">
          <Input
            label="Email"
            placeholder="Enter Email"
            type={"text"}
            className="max-w-xs"
            classNames={{ inputWrapper: "bg-[#EAF3E9]" }}
            required
            onChange={(e) => SetUsername(e.target.value)}
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
            onChange={(e) => SetPassword(e.target.value)}
          />
        </div>

        <div className="w-[67%] gap-[20px] flex flex-col justify-between items-center">
          <Button
            type="submit"
            radius="full"
            className="bg-Green text-white  w-full"
          >
            Login
          </Button>
          <h6 className="font-Myfont font-normal">
            Don't have an account?
            <Link className="text-Green" to="/register">
              Register
            </Link>
          </h6>
          <h6 className="font-Myfont font-md text-[12px] text-[#DC4545]">
            {Error}
          </h6>
        </div>
      </form>
    </div>
  );
};
export default Login;
