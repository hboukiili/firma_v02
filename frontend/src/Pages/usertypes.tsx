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
    <div className="w-[260px] p-2 h-[300px] bg-white flex justify-center items-center flex-col gap-[25px] rounded-lg">
      <h1 className="font-Myfont font-bld text-DarkGreen">{data.name}</h1>
      <ReactSVG src={data.icn} />
      <p className="font-Myfont font-lt text-[10px] max-w-[180px] text-center">
        Lorem Ipsum is simply dummy text of the printing and typesetting
        industry. Lorem Ipsum has been the industry's
      </p>
      <Button
        onClick={() => {
          dispatch(updateUserInfo({ type: data.name.toLowerCase() }));
          navTo("/register");
        }}
        radius="full"
        className=" max-w-[140px] bg-Green font-Myfont text-white"
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
    <div className="relative flex flex-col justify-center items-center gap-10 w-full h-screen">
      <h1 className="font-Myfont font-smbld text-[32px] text-DarkGreen">
        Unlock Your Unique Experience
      </h1>
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
