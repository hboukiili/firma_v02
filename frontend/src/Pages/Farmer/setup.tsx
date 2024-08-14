import React, { useCallback, useEffect, useRef, useState } from "react";
import Stepper from "@mui/material/Stepper";
import Step from "@mui/material/Step";
import StepLabel from "@mui/material/StepLabel";
import { Button } from "@nextui-org/react";
import "../Components/Dashboard/style.css";
import Steps from "./tools/Steps";
import AddField from "./tools/addField";
// import { Step, Stepper, Typography } from "@material-tailwind/react";

const Stepper_ = (step_: { step_: number }) => {
  const steps = [
    // "Add your first field",
    "Field information",
    "Soil information",
    "Irrigation system",
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

const Setup = () => {
  const [step, setStep] = useState(0);
  const steps = [
    // "Add your first field",
    "Field information",
    "Soil information",
    "Irrigation system",
    // "Validation",
  ];

  return (
    <div className="w-full h-[100dvh] flex pt-0 gap-6 items-center justify-center">
      <div className="font-Myfont font-bld w-[50%] min-w-[600px] flex justify-center h-full">
        <AddField
          options_={steps[step] === "Field information" ? true : false}
        />
      </div>
      <div className="w-[60%] flex flex-col h-full rounded-md overflow-hidden  justify-center items-center">
        <div className="w-[580px] gap-6  bg-scBgGreen flex flex-col justify-between p-4 rounded-[10px] items-center">
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
                  step < 2
                    ? setStep(step + 1)
                    : (window.location.href = "/farmer");
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
      </div>
    </div>
  );
};

export default Setup;
