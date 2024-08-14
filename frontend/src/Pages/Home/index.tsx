import React from "react";
import NavBar from "../Components/Navbar";
import Slider_ from "./Slider";
import { Button } from "@nextui-org/react";
import about_img from "../../../assets/about.jpg";
import typesBg from "../../../assets/typesBg.png";
import about_img2 from "../../../assets/about2.png";
import Farmer_icn from "../../../assets/Farmer.svg";
import Policymake_icn from "../../../assets/Policymaker.svg";
import Academic_icn from "../../../assets/Academic.svg";
import { ReactSVG } from "react-svg";

interface card {
  name: string;
  icn: any;
}

const Card = (data: card) => {
  return (
    <div className="w-[260px] p-2 h-[440px] bg-white flex justify-center items-center flex-col gap-[25px] rounded-lg">
      <h1 className="font-Myfont font-bld text-DarkGreen">{data.name}</h1>
      <ReactSVG src={data.icn} />
      <p className="font-Myfont font-lt text-[10px] max-w-[180px] text-center">
        Lorem Ipsum is simply dummy text of the printing and typesetting
        industry. Lorem Ipsum has been the industry's{" "}
      </p>
      <div>
        {/* {data.name === 'Farmer' || data.name === 'Academic' && */}
        <p className="font-Myfont font-bld text-[24px] text-[#F97373]">
          {" "}
          49$/ <span className="font-Myfont text-[16px]">m</span>
        </p>
      </div>
      <ul className="space-y-[10px]">
        <li className="font-Myfont text-[10px] font-smbld">
          Lorem Ipsum is simply dummy
        </li>
        <li className="font-Myfont text-[10px] font-smbld">
          Lorem Ipsum is simply dummy
        </li>
        <li className="font-Myfont text-[10px] font-smbld">
          Lorem Ipsum is simply dummy
        </li>
        <li className="font-Myfont text-[10px] font-smbld">
          Lorem Ipsum is simply dummy
        </li>
      </ul>
      <Button
        radius="full"
        className=" max-w-[140px] bg-Green font-Myfont text-white"
      >
        Unlock
      </Button>
    </div>
  );
};

const Home = () => {
  const cards = [
    { name: "Policymaker", icn: Academic_icn },
    { name: "Farmer", icn: Farmer_icn },
    { name: "Academic", icn: Policymake_icn },
  ];

  return (
    <div className="w-screen flex flex-col h-screen justify-start ">
      <div className="w-full p-4 bg-Lgreen">
        <NavBar />
      </div>
      <div className="w-full flex flex-col items-start  z-10 bg-Lgreen ">
        <div className="w-full flex justify-between h-screen items-center ">
          <div className="w-[40%]">
            <div className="pl-14 pr-14 flex flex-col gap-2 justify-start">
              <p className="text-left text-[100px] font-Myfont font-smbld text-DarkGreen">
                FIRMA
              </p>
              <p className="text-DarkGreen font-Myfont font-smbld text-[16px]">
                Innovative Solutions, Data, and Research
              </p>
              <p className="font-Myfont font-lt">
                Lorem Ipsum is simply dummy text of the printing and typesetting
                industry. Lorem Ipsum has been the industry's Ipsum is simply
                dumm
              </p>
              <Button
                onClick={() => {
                  window.location.href = "/usertypes";
                }}
                radius="full"
                className=" max-w-[140px] bg-Green font-Myfont text-white"
              >
                Get Started
              </Button>
            </div>
          </div>
          <div className="w-[60%] h-[340px]">
            <Slider_ />
          </div>
        </div>
        <div className="relative w-full flex items-center justify-center h-screen ">
          <div className="max-w-[900px] flex gap-[90px] items-center">
            <div className="h-[450px] w-[450px] overflow-hidden rounded-lg">
              <img className="w-[100%]" src={about_img} alt="" />
            </div>
            <div className="max-w-[360px] flex flex-col gap-4">
              <h1 className="font-Myfont font-smbld text-[32px] text-DarkGreen">
                About Firma
              </h1>
              <p className="font-Myfont font-lt">
                Lorem Ipsum is simply dummy text of the printing and typesetting
                industry. Lorem Ipsum has been the industry's Ipsum is simply
                dumm Lorem Ipsum is simply dummy text of the printing and
                typesetting industry. Lorem Ipsum has been the industry's{" "}
              </p>
              <Button
                radius="full"
                className=" max-w-[140px] bg-Green font-Myfont text-white"
              >
                More
              </Button>
            </div>
            <img
              className="absolute right-0 w-[30%] z-[1]"
              src={about_img2}
              alt=""
            />
          </div>
        </div>
        <div className="relative flex flex-col justify-center items-center w-full h-screen">
          <h1 className="font-Myfont font-smbld text-[32px] text-DarkGreen">
            Unlock Your Unique Experience
          </h1>
          <div className="z-10 flex gap-[25px]">
            {cards.map((v, _) => (
              <Card key={_} icn={v.icn} name={v.name} />
            ))}
          </div>
          <img className="absolute left-0 z-0 h-full" src={typesBg} alt="" />
        </div>
      </div>
    </div>
  );
};

export default Home;
