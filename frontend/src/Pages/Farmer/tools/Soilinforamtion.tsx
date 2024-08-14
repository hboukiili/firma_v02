import { Input, Select, SelectItem, Tab, Tabs } from "@nextui-org/react";
import React from "react";
import { ReactSVG } from "react-svg";
import icn1 from "../../../assets/soil1.svg";
import icn2 from "../../../assets/soil2.svg";
import icn3 from "../../../assets/soil3.svg";

import "./style.css";
import { useAppDispatch } from "../../../Redux/hooks";
import { updateFarmerInfo } from "../../../Redux/Farmer/actions";

const Options = () => {
  const soil_ = [
    "SILT",
    "LOAMY SAND",
    "SAND",
    "SANDY LOAM",
    "LOAM",
    "SANDY CLAY LOAM",
    "CLAY LOAM",
    "SILTY CLAY",
    "SANDY CLAY",
    "CLAY",
  ];
  const dispatch = useAppDispatch();

  return (
    <div className="flex w-full  p-2 flex-col">
      <Tabs
        classNames={{ cursor: "bg-[#D3E1D1]" }}
        fullWidth={true}
        aria-label="Options"
        variant="bordered"
      >
        <Tab
          className="flex justify-center"
          key="photos"
          title={
            <div className="flex items-center space-x-2">
              <ReactSVG src={icn1} />
              <span>Predefined Soil Types</span>
            </div>
          }
        >
          <div className="flex w-[60%] flex-col justify-center items-center pt-20 gap-8 ">
            <div className="w-">
              <p className="font-Myfont font-bld text-[40px]">Soil Details</p>
              <p className="font-Myfont font-md text-[12px]">
                Successful farming relies on understanding soil composition.{" "}
                <br /> Please share details about the soil in your field.
              </p>
            </div>
            <Select
              classNames={{
                trigger: "bg-white  text-[#1E6F5C] ",
                label: "text-[#1E6F5C]",
              }}
              variant="faded"
              labelPlacement="outside"
              size="md"
              radius={"full"}
              label="Indicate the primary type of soil found in your field"
              className="w-[70%]"
              placeholder="Soil type"
              onChange={(e) => {
                dispatch(updateFarmerInfo({ SoilType: e.target.value }));
              }}
            >
              {soil_.map((val, _) => {
                return (
                  <SelectItem key={val} value={val}>
                    {val}
                  </SelectItem>
                );
              })}
            </Select>
          </div>
        </Tab>
        <Tab
          key="music"
          title={
            <div className="flex items-center space-x-2">
              <ReactSVG src={icn2} />

              <span>Custom Percentages</span>
            </div>
          }
        >
          <div className="flex flex-col justify-center items-center pt-20 gap-8 label-">
            <div className="">
              <p className="font-Myfont font-bld text-[40px]">Soil Details</p>
              <p className="font-Myfont font-md text-[12px]">
                Successful farming relies on understanding soil composition.{" "}
                <br /> Please share details about the soil in your field.
              </p>
            </div>
            <div className="flex w-full max-w-[375px] gap-2 justify-center label-">
              <Input
                radius="full"
                variant="bordered"
                classNames={{
                  inputWrapper: "border-[#1E6F5C] text-[#1E6F5C]",
                  label: "text-[#1E6F5C]",
                }}
                // classNames={{ inputWrapper: "bg-white" }}
                className=""
                type="text"
                placeholder="Sand %"
              />
              <Input
                radius="full"
                variant="bordered"
                classNames={{
                  inputWrapper: "border-[#1E6F5C] text-[#1E6F5C]",
                  label: "text-[#1E6F5C]",
                }}
                // classNames={{ inputWrapper: "bg-white" }}
                className=""
                type="text"
                placeholder="Clay %"
              />
              <Input
                radius="full"
                variant="bordered"
                classNames={{
                  inputWrapper: "border-[#1E6F5C] text-[#1E6F5C]",
                  label: "text-[#1E6F5C]",
                }}
                // classNames={{ inputWrapper: "bg-white" }}
                className=""
                type="text"
                placeholder="Silt %"
              />
            </div>
          </div>
        </Tab>
        <Tab
          key="videos"
          title={
            <div className="flex items-center space-x-2">
              <ReactSVG src={icn3} />

              <span>Interactive Soil Triangle</span>
            </div>
          }
        />
      </Tabs>
    </div>
  );
};

const SoilInfo_ = () => {
  const soil_ = [
    "SILT",
    "LOAMY SAND",
    "SAND",
    "SANDY LOAM",
    "LOAM",
    "SANDY CLAY LOAM",
    "CLAY LOAM",
    "SILTY CLAY",
    "SANDY CLAY",
    "CLAY",
  ];
  return (
    <div className="w-full flex gap-16 justify-center items-center flex-col ">
      <Options />
    </div>
  );
};

export default SoilInfo_;
