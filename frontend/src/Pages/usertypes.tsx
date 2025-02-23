import React from "react";
import { Button, card } from "@nextui-org/react";
import { ReactSVG } from "react-svg";
import Farmer_icn from "../assets/Farmer.svg";
import Policymake_icn from "../assets/Policymaker.svg";
import Academic_icn from "../assets/Academic.svg";
import typesBg from "../assets/typesBg.png";
import { useAppDispatch, useAppSelector } from "../Redux/hooks";
import { updateUserInfo } from "../Redux/userInfo/Actions";
import { useNavigate } from "react-router-dom";

interface card {
  name: string;
  icn: any;
}

const Card = (data: card) => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.userInfo);
  const navTo = useNavigate();

  return (
    <div className="w-[300px] p-2 h-[400px] bg-white flex justify-between py-6 items-center flex-col gap-[25px] rounded-[20px]">
      <h1 className="font-Myfont font-bld text-DarkGreen text-[18px]">{data.name}</h1>
      <ReactSVG src={data.icn} />
      <p className="font-Myfont font-lt text-[14px] max-w-[80%] text-center">
        Lorem Ipsum is simply dummy text of the printing and typesetting
        industry. Lorem Ipsum has been the industry's
      </p>
      <Button
        onClick={() => {
          navTo("/register");
          dispatch(updateUserInfo({ type: data.name.toLowerCase() }));
        }}
        radius="full"
        className=" w-[240px] bg-[#4FC38F] font-Myfont text-white"
      >
        Unlock
      </Button>
    </div>
  );
};

const Usertypes = () => {
  const cards = [
    { name: "Policymaker", icn: Academic_icn },
    { name: "Farmer", icn: Farmer_icn },
    { name: "Academic", icn: Policymake_icn },
  ];
  return (
    <div className="relative font-Myfont flex flex-col justify-center items-center gap-20 w-full  h-screen">
      <div className="flex flex-col justify-center gap-2 items-center w-[50%]">
        <h1 className=" font-bld text-[32px] text-DarkGreen">
          Unlock Your Unique Experience
        </h1>
        <p className="w-[65%] text-center">
          Select your role to personalize your experience and unlock features
          designed specifically for your needs, whether you're a farmer,
          policymaker, or academic.
        </p>
      </div>
      <div className="z-10 flex gap-[25px]">
        {cards.map((v, _) => (
          <Card icn={v.icn} name={v.name} />
        ))}
      </div>
      <img className="absolute h-full left-0 z-0" src={typesBg} alt="" />
    </div>
  );
};

export default Usertypes;
