import React, { useCallback, useEffect, useRef, useState } from "react";
import Stepper from "@mui/material/Stepper";
import Step from "@mui/material/Step";
import StepLabel from "@mui/material/StepLabel";
import { Button } from "@nextui-org/react";
import "../Components/Dashboard/style.css";
import Steps, { Waiting } from "./tools/Steps";
import AddField from "./tools/addField";
import api from "../../api/axios.js";
import { useAppSelector } from "../../Redux/hooks";
// import { Step, Stepper, Typography } from "@material-tailwind/react";

const Stepper_ = (step_: { step_: number }) => {
  const steps = [
    "Field information",
    "Soil information",
    "Crop information",
    "Irrigation system",
    "Validation",
  ];
  return (
    <Stepper className="w-full pr-20 pl-20 pt-8" activeStep={step_.step_}>
      {steps.map((label) => (
        <Step key={label}>
          <StepLabel></StepLabel>
        </Step>
      ))}
    </Stepper>
  );
};

function setupRequest(Data) {
  let soil;
  let data;

  switch (Data.soilMethod) {
    case "Selection":
      soil = Data.SoilType;
      break;
    case "Composition":
      soil = Data.soilPr;
      break;
    case "satellite":
      soil = true;
      break;
  }

  api
    .post("/farmer/register_data", {
      field : {
        name: Data.fieldName,
        boundaries: Data.Field,
      },
      plant: Data.PlantingDetails,
      soil: {
        method: Data.soilMethod,
        value: soil,
      },
      irr: Data.IrrigationType,
    })
    .then((res) => {
      data = res.data;
      window.location.href = "/farmer1";
      console.log(res.data);
    })
    .catch((err) => {
      console.log(err);
    });
  return data;
}

const Setup = () => {
  const Data = useAppSelector((state) => state.farmer);
  console.log(Data.soilMethod);
  const [step, setStep] = useState(0);
  const steps = [
    "Field information",
    "Soil information",
    "Crop information",
    "Irrigation system",
    "Validation",
  ];

  return (
    <div className="w-full h-[100dvh] flex pt-0 gap-6 items-center justify-center bg-[#F2F9F3]">
      <div className="font-Myfont font-bld grow min-w-[600px] flex justify-center h-full">
        <AddField
          options_={steps[step] === "Field information" ? true : false}
        />
      </div>
      <div className=" flex flex-col h-full rounded-md overflow-hidden  justify-center items-center">
        {step < 5 ? (
          <div className="w-[900px] bg-back h-full  gap-6  bg-scBgGren flex flex-col justify-between p-4 rounded-[10px] items-center">
            <Stepper_ step_={step} />
            <Steps name={steps[step]} />
            <div className="flex justify-between p-5 font-Myfont ">
              <div className="flex gap-2">
                <Button
                  isDisabled={!step}
                  onClick={() => {
                    setStep(step - 1);
                  }}
                  radius="full"
                  variant="bordered"
                  className="text-lightGreen border-lightGreen "
                >
                  Back
                </Button>
                <Button
                  onClick={() => {
                    if (steps[step] === "Validation") setupRequest(Data);
                    setStep(step + 1);
                  }}
                  radius="full"
                  className="bg-lightGreen text-white"
                >
                  Next
                </Button>
              </div>
            </div>
            <p className="text-[10px] font-Myfont font-md">
              Skipping all steps for now? No problem, you can always return to
              provide more details later.{" "}
              <span
                onClick={() => {
                  window.location.href = "/farmer";
                }}
                className="font-bld underline cursor-pointer"
              >
                Skip
              </span>
            </p>
          </div>
        ) : (
          <Waiting />
        )}
      </div>
    </div>
  );
};

export default Setup;
