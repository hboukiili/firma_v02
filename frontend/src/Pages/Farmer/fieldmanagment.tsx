import React, { useEffect, useState } from "react";
import AddField, { CreateFieldOptions } from "./tools/addField";
import rmIc from "../../assets/removeIc.svg";
import adIc from "../../assets/addIC.svg";
import edIc from "../../assets/editIc.svg";
import { ReactSVG } from "react-svg";
import FieldInformation from "./tools/Fieldinformation";
import plantIcon from "../../assets/plant.svg";
import treeIcon from "../../assets/tree.svg";

import {
  CalendarDate,
  getLocalTimeZone,
  parseDate,
  today,
} from "@internationalized/date";
import {
  Button,
  DateInput,
  Input,
  Listbox,
  ListboxItem,
  Modal,
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
  Radio,
  RadioGroup,
  Select,
  SelectItem,
  SelectSection,
  useDisclosure,
} from "@nextui-org/react";
import locIcon from "../../assets/locationIcon.svg";
import uplIcon from "../../assets/uploadIcon.svg";
import drIcon from "../../assets/polygonIcon.svg";
import { useAppDispatch, useAppSelector } from "../../Redux/hooks";
import Steps from "./tools/Steps";
import api from "../../api/axios.js";
import SoilInfo_ from "./tools/Soilinforamtion.js";
import Irrigationsystem_ from "./tools/Irrigationsystem_.js";
import { Divider, Progress } from "antd";
import canld from "../../assets/canld.png";
import { updateFarmerInfo } from "../../Redux/Farmer/actions.js";
import { redirect } from "react-router-dom";

// const  = () => {
//   return (
//     <div className="">
//       <p className="font-Myfont font-bld text-[40px]">Field information</p>
//       <p className="font-Myfont font-md text-[12px]">
//         Before providing field and crop details, either draw your <br />
//         polygon on the map or select one of three methods.
//       </p>
//     </div>
//   );
// };

const DeleteField = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  const { isOpen, onOpen, onOpenChange } = useDisclosure();

  const [selectedKeys, setSelectedKeys] = useState(new Set([""]));
  const findField = (id: number) => {
    return Data.fieldInfo.map((field) => {
      if (field.id === id) return field;
    });
  };

  return (
    <div className="mt-6 flex flex-col gap-8 w-[40%] items-center font-Myfont ">
      {/* <p className="font-bld text-[24px]">Please select one of your fields</p> */}
      <div className="w-full flex justify-start items-start bg- p-2 rounded-lg overflow-x-hidden overflow-y-scroll max-h-[300px]">
        <Listbox
          aria-label="Single selection example"
          variant="faded"
          disallowEmptySelection
          selectionMode="single"
          // selectedKeys={selectedKeys}
          onSelectionChange={setSelectedKeys}
        >
          {Data.fieldInfo.map((v) => {
            return (
              <ListboxItem className="font-md" key={v.id}>
                {v.name}
              </ListboxItem>
            );
          })}
        </Listbox>
      </div>
      <p className="text-small text-default-500">
        {/* Selected value: {selectedValue} */}
      </p>
      <div>
        <Button onPaste={onOpen} radius="full" className="bg-Red text-white">
          Delete
        </Button>
      </div>
      <Modal className="left-10" isOpen={isOpen} onOpenChange={onOpenChange}>
        <ModalContent className="max-w-[88%] font-Myfont font-bld">
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1">
                {Data.ChartData!.type}
              </ModalHeader>
              <ModalBody className="flex justify-center items-end p-3"></ModalBody>
              <ModalFooter>
                <Button className="bg-[#48A788] text-white" radius="full">
                  Download as csv
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </div>
  );
};

export const CropInfo = () => {
  const trees = [
    "Olive Tree",
    "Argan Tree",
    "Orange Tree",
    "Lemon Tree",
    "Mandarin Tree",
    "Almond Tree",
    "Date Palm",
    "Carob Tree",
    "Fig Tree",
  ];

  const crops_ = [
    "Broccoli",
    "Cabbage",
    "Carrots",
    "Cauliflower",
    "Lettuce",
    "Dry Onions",
    "Green Onions",
    "Seed Onions",
    "Spinach",
    "Radishes",
    "Eggplant",
    "Sweet Peppers",
    "Tomato",
    "Cantaloupe",
    "Cucumber",
    "Pumpkin",
    "Sweet Melons",
    "Watermelon",
    "Beets",
    "Potato",
    "Sugar Beet",
    "Green Beans",
    "Faba Bean",
    "Green Gram",
    "Cowpeas",
    "Groundnut",
    "Lentil",
    "Peas",
    "Soybeans",
    "Artichokes",
    "Asparagus",
    "Cotton",
    "Flax",
    "Sunflower",
    "Barley",
    "Oats",
    "Spring Wheat",
    "Winter Wheat",
    "Field Corn",
    "Sweet Corn",
    "Millet",
    "Rice",
    "Alfalfa Hay",
    "Bermuda Hay",
    "Banana First Year",
    "Banana Second Year",
    "Pineapple",
    "Olives",
    "Pistachios",
  ];

  const [plantType, SetPlantType] = useState("Crop");
  const [date, setDate] = useState("");
  const [value, Setvalue] = useState("");
  const [tree, Settree] = useState("");
  const dispatch = useAppDispatch();

  const list = plantType === "Tree" ? trees : crops_;
  useEffect(() => {
    dispatch(
      updateFarmerInfo({
        PlantingDetails: {
          type : plantType,
          Tree: {
            value: tree,
            date: date,
          },
          Crop : {
            value : value,
            date : date,
          }
        },
      })
    );
  }, [plantType, date, value]);

  return (
    <div className="flex flex-col justify-center items-center pt-20 gap-8 w-full">
      <div className="w-[50%]">
        <p className="font-Myfont font-bld text-[40px]">Pick Your Planting</p>
        <p className="font-Myfont font-md text-[12px]">
          Identify your plant type and planting date to receive tailored advice
          and resources for your planting activities.
        </p>
      </div>
      <div className="w-[60%] flex justify-center items-center">
        <RadioGroup
          onValueChange={SetPlantType}
          defaultValue="Crop"
          orientation="horizontal"
        >
          <div className="flex gap-4">
            <Radio color="success" value="Tree">
              <div className="flex gap-1">
                <ReactSVG src={treeIcon} />
                {"Tree"}
              </div>
            </Radio>
            <Divider type="vertical" />

            <Radio color="success" value="Crop">
              <div className="flex gap-1">
                <ReactSVG src={plantIcon} />
                {"Crop"}
              </div>
            </Radio>
            <Divider type="vertical" />

            <Radio color="success" value="Crop and tree">
              <div className="flex gap-1">
                <ReactSVG src={plantIcon} />
                <ReactSVG src={treeIcon} />
                {"Crop and tree"}
              </div>
            </Radio>
          </div>
        </RadioGroup>
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
        label={`Please select your ${
          plantType === "Tree" ? "tree" : "crop"
        } type`}
        className="w-[50%]"
        placeholder={`${plantType === "Tree" ? "Tree" : "Crop"} type`}
        onChange={(e) => {
          if (plantType === "Tree") Settree(e.target.value);
          else Setvalue(e.target.value);
        }}
      >
        {list.map((val, _) => {
          return (
            <SelectItem key={val} value={val}>
              {val}
            </SelectItem>
          );
        })}
      </Select>
      {plantType == "Crop and tree" && (
        <Select
          classNames={{
            trigger: "bg-white  text-[#1E6F5C] ",
            label: "text-[#1E6F5C]",
          }}
          variant="faded"
          labelPlacement="outside"
          size="md"
          radius={"full"}
          label={`Please select your tree type`}
          className="w-[50%]"
          placeholder={`Tree type`}
          onChange={(e) => {
            Settree(e.target.value);
          }}
        >
          {trees.map((val, _) => {
            return (
              <SelectItem key={val} value={val}>
                {val}
              </SelectItem>
            );
          })}
        </Select>
      )}
      <DateInput
        label="Please enter planting date."
        variant="faded"
        radius="full"
        size="md"
        classNames={{ inputWrapper: "bg-white", input: "" }}
        //   defaultValue={parseDate("2024-04-04")}
        placeholderValue={new CalendarDate(1995, 11, 6)}
        labelPlacement="outside"
        startContent={<img className="w-[20px]" src={canld} />}
        className="w-[50%] "
        onChange={(e) => {
          setDate(e.toString());
        }}
      ></DateInput>
    </div>
  );
};

const FieldManagment = () => {
  const [option, setOption] = useState("Field information");
  const Data = useAppSelector((state) => state.farmer);
  const contentCp: { [key: string]: any } = {
    "Field information": <FieldInformation />,
    "Soil information": <SoilInfo_ />,
    "Irrigation system": <Irrigationsystem_ />,
    "Remove Field": <DeleteField />,
    "Crop information": <CropInfo />,
  };
  const content = [
    {
      option: "Add Field",
      dsc: "Create a custom field to track new farm data.",
      icn: adIc,
    },
    {
      option: "Edit Field",
      dsc: "Update details of a field (name, Coordinates, etc.).",
      icn: edIc,
    },
    {
      option: "Remove Field",
      dsc: "This allows you to permanently delete a field you no longer need.",
      icn: rmIc,
    },
  ];

  const [step, setStep] = useState(0);
  const steps = [
    "Field information",
    "Soil information",
    "Crop information",
    "Irrigation system",
    "Validation",
  ];
  console.log(Data);
  function isDisabled_() {
    if (steps[step] === "Field information") {
      if (!Data.fieldName || !Data.Field.length) return true;
    } else if (steps[step] === "Soil information") {
      if (!Data.SoilType) return true;
    } else if (steps[step] === "Irrigation system") {
      if (!Data.IrrigationType?.system) return true;
    } else return false;
  }
  return (
    <div className="w-screen h-screen  p-2 pt-[85px] top-0 left-0  absolute font-Myfont  ">
      <div className="w-full h-full  relative">
        <div className="w-full h-full rounded-[10px] overflow-hidden">
          <AddField options_={false} />
        </div>
        <div className="rounded-[10px] min-w-[500px] w-[47%] h-[98%]  absolute top-2 left-2 z-40 flex flex-col gap-2">
          {/* <div className="flex w-full gap-2 p-2 bg-scBgGreen rounded-[10px]">
            {content.map((v, _) => {
              return (
                <button
                  onClick={() => {
                    if (v.option === "Add Field") {
                      setOption("Field information");
                      setStep(0);
                    } else setOption(v.option);
                  }}
                  className="flex forced-colors:to-black cursor-pointer hover:bg-[#D3E1D1]  w-[33%] p-2 justify-between items-center h-[50px] border-2 border-[#D3E1D1] rounded-[10px]"
                >
                  <p className="font-bld ">{v.option}</p>
                  {/* <p className="text-[11px] ">{v.dsc}</p> */}
          {/* <ReactSVG className=" " src={v.icn} />
                </button>
              );
            })}
          </div> */}

          <div className="w-full grow bg-scBgGreen rounded-[10px] flex flex-col items-center ">
            <Progress
              size={"small"}
              strokeColor={"#43c67e"}
              className="pl-2 pr-2"
              percent={step * 20}
              showInfo={false}
            />
            {steps[step] === "Field information" && (
              <div className="w-[90%] flex justify-center pt-4">
                <CreateFieldOptions map={Data.Map} />
              </div>
            )}
            <div className="w-full mt-5 flex gap-8 justify-center items-center flex-col ">
              <div className="w-full flex justify-center items-center">
                {contentCp[option]}
              </div>
              {option != "Remove Field" && (
                <div className="flex gap-2">
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
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FieldManagment;
