import {
  Button,
  Modal,
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
  Popover,
  PopoverContent,
  PopoverTrigger,
  Select,
  SelectItem,
  Tooltip,
  useDisclosure,
} from "@nextui-org/react";
import Dragger_ from "./Dragger";
import { Textarea } from "evergreen-ui";
import { useState } from "react";
import { useAppDispatch, useAppSelector } from "../../../Redux/hooks";
import * as L from "leaflet";
import { message } from "antd";
import { updateFarmerInfo } from "../../../Redux/Farmer/actions";
import { green } from "@mui/material/colors";
import FieldInformation from "./Fieldinformation";
import SoilInfo_ from "./Soilinforamtion";
import Irrigationsystem_ from "./Irrigationsystem_";
import { CropInfo } from "../fieldmanagment";

export const SetupModal = (isShapefile: boolean, isOpen_: boolean) => {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const [Coordinates, SetCoordinates] = useState();
  const [shapeFile, setShapefile] = useState();
  const [target, setTarget] = useState();
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  return (
    // <Modal className="" isOpen={isOpen_} onOpenChange={onOpenChange}>
    <ModalContent className="max-w-[30%] min-w-[400px] font-Myfont font-bld">
      {(onClose) => (
        <>
          <ModalHeader className="flex flex-col gap-1">{}</ModalHeader>
          <ModalBody className="flex justify-center items-end p-3">
            {isShapefile ? (
              <Dragger_ />
            ) : (
              <Textarea
                key={"bordered"}
                variant={"bordered"}
                label="Coordinates"
                labelPlacement="inside"
                placeholder="Enter your Coordinates"
                className="col-span-12 md:col-span-6 mb-6 md:mb-0"
                onChange={(e) => {
                  // const v = JSON.parse(e.target.value);
                  setTarget(e.target.value);
                }}
              />
            )}
          </ModalBody>
          <ModalFooter>
            <Button
              onClick={() => {
                console.log();
                try {
                  if (!isShapefile && Data.Map instanceof L.Map) {
                    let cr = JSON.parse(target);
                    cr = cr.map((coord) => [coord[1], coord[0]]);
                    SetCoordinates(cr);
                    if (Data.polygon_) Data.Map!.removeLayer(Data.polygon_);
                    const polygon = L.polygon(cr, {
                      color: green[900],
                    }).addTo(Data.Map as L.Map);
                    Data.Map!.fitBounds(L.polygon(cr).getBounds());
                    dispatch(updateFarmerInfo({ polygon_: polygon }));
                  } else {
                  }
                  onOpenChange();
                } catch (e) {
                  message.error("Invalid coordinates format");
                }
              }}
              className="bg-[#48A788] text-white"
              radius="full"
            >
              Submit
            </Button>
          </ModalFooter>
        </>
      )}
    </ModalContent>
  );
};

export const DrawTools = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  const [option, setOption] = useState("Field information");
  const [step, setStep] = useState(0);
  function isDisabled_() {
    if (steps[step] === "Field information") {
      if (!Data.fieldName || !Data.Field.length) return true;
    } else if (steps[step] === "Soil information") {
      if (!Data.SoilType && !Data.soilPr?.clay && !Data.soilCheck) return true;
    } else if (steps[step] === "Irrigation system") {
      if (!Data.IrrigationType?.system) return true;
    } else return false;
  }
  const steps = [
    "Field information",
    "Soil information",
    "Crop information",
    "Irrigation system",
    "Validation",
  ];
  const contentCp: { [key: string]: any } = {
    "Field information": <FieldInformation />,
    "Soil information": <SoilInfo_ />,
    "Irrigation system": <Irrigationsystem_ />,
    // "Remove Field": <DeleteField />,
    "Crop information": <CropInfo />,
  };
  return (
    <ModalContent className="max-w-[50%] bg-[#EAF3E9] min-w-[400px] font-Myfont font-bld">
      {(onClose) => (
        <>
          <ModalHeader className="flex flex-col gap-1">{}</ModalHeader>
          <ModalBody className="flex gap-4">{contentCp[option]}</ModalBody>
          <ModalFooter>
            <div className="flex gap-2 justify-center w-full m-8">
              <Button
                isDisabled={!step}
                onClick={() => {
                  setStep(step - 1);
                  setOption(steps[step - 1]);
                }}
                radius="full"
                variant="bordered"
                className="text-lightGreen border-lightGreen "
              >
                Back
              </Button>
              <Button
                isDisabled={isDisabled_()}
                onClick={() => {
                  if (steps[step - 1] === "Irrigation system")
                    api
                      .post("/farmer/register_data", {
                        field: {
                          name: Data.fieldName,
                          boundaries: Data.Field,
                        },
                        irr: Data.IrrigationType,
                        soil: Data.SoilType,
                        planting: Data.PlantingDetails,
                      })
                      .then((e) => {
                        console.log(e.data);
                        document.location.href = "/farmer";
                      })
                      .catch((e) => {
                        console.log(e.data);
                      });
                  else {
                    setStep(step + 1);
                    setOption(steps[step + 1]);
                  }
                }}
                radius="full"
                className="bg-lightGreen text-white"
              >
                Next
              </Button>
            </div>
          </ModalFooter>
        </>
      )}
    </ModalContent>
  );
};
