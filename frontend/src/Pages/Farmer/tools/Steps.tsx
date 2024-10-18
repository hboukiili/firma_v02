import React from "react";
import FieldInformation from "./Fieldinformation";
import AddField from "./addField";
import Irrigationsystem_ from "./Irrigationsystem_";
import { Button } from "@material-tailwind/react";
import SoilInfo_ from "./Soilinforamtion";
import { CropInfo } from "../fieldmanagment";
import { AnimatePresence, motion } from "framer-motion";
import Validation from "./validation";
import PuffLoader from "react-spinners/PuffLoader";

interface Steps {
  name: string;
}

export const Waiting = () => {
  return (
    <motion.div
      initial={{ opacity: 0, x: 60 }} // Starting state
      animate={{ opacity: 1, x: 0 }} // Animation to apply
      transition={{ duration: 0.4 }}
      className="font-Myfont w-[800px] flex items-center flex-col gap-4"
    >
      <PuffLoader className="" color="#48A788" />
      <p className="font-bld text-[22px] text-center">
        Processing your data, please wait
      </p>
      <p className="text-center w-[300px] text-[12px]">
        We are validating your field information and optimizing the irrigation
        and planting details. This might take a few moments. Thank you for your
        patience!
      </p>
    </motion.div>
  );
};

const Steps = (prop: Steps) => {
  const Components: { [step: string]: JSX.Element } = {
    "Field information": <FieldInformation />,
    "Soil information": <SoilInfo_ />,
    "Irrigation system": <Irrigationsystem_ />,
    "Crop information": <CropInfo />,
    Validation: <Validation />,
  };

  return (
    <div className="w-full h-[600px] ">
      {/* <AnimatePresence exitBeforeEnter> */}
      <motion.div
        key={prop.name}
        initial={{ opacity: 0, y: 20 }} // Starting state
        animate={{ opacity: 1, y: 0 }} // Animation to apply
        exit={{ opacity: 0, y: -20 }} // Animation for exit
        transition={{ duration: 0.4 }}
        className="h-full w-full flex justify-center items-center" // Duration of the transition
      >
        {Components[prop.name] || <Waiting />}
      </motion.div>
      {/* </AnimatePresence> */}
    </div>
  );
};

export default Steps;
