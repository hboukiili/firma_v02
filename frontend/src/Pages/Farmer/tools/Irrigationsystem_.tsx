import {
  CalendarDate,
  getLocalTimeZone,
  parseDate,
  today,
} from "@internationalized/date";
import { DateInput } from "@nextui-org/date-input";
import {
  Button,
  Divider,
  Input,
  Modal,
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
  Select,
  SelectItem,
  useDisclosure,
} from "@nextui-org/react";
import React, { useEffect, useState } from "react";
import Dirr from "../../../assets/Dirr.png";
import Sirr from "../../../assets/Sirr.png";
import Rirr from "../../../assets/Rirr.png";
import Srirr from "../../../assets/Srirr.png";
import fsp from "../../../assets/fsp.jpg";
import dsp from "../../../assets/dsp.jpg";
import canld from "../../../assets/canld.png";
import { Form, InputNumber } from "antd";
import { useAppDispatch, useAppSelector } from "../../../Redux/hooks";
import { updateFarmerInfo } from "../../../Redux/Farmer/actions";

const IrrForms = (name: { name: string }) => {
  const Data = useAppSelector((state) => state.farmer);
  const [form] = Form.useForm<{
    //crop prop
    SprinklerRadius_c: number;
    sprinklerCoverage_c: number;
    WaterOutflowRate_c: number;
    numberOfSprinklers_c: number;
    DistanceBetweenTubes_c: number;
    DistanceBetweenDrippers_c: number;
    CoverageAreaOfEachDrippers_c: number;
    //tree prop
    DistanceBetweenRows_t: number;
    DistanceBetweenTrees_t: number;
    NumberOfTubesPerTree_t: number;
    NumberOfDrippersPerTree_t: number;
    FlowRate_t: number;
  }>();
  const Sirr_t = (
    <div className="flex flex-col gap-4 min-w-[400px] w-[50%] ">
      <div className="flex flex-col font-Myfont">
        <p className="text-[32px] font-bld">Sprinkler irrigation</p>
        {Data.PlantingDetails?.type != "Crop and tree" && (
          <p className="text-[12px] font-nrml">
            Enter the details of your Sprinkler Irrigation System below to help
            manage water usage effectively.
          </p>
        )}
      </div>
      <Form form={form} layout="vertical" autoComplete="off">
        <Form.Item
          name={"sprinklerCoverage_c"}
          label="Specify the total coverage area of the sprinkler (in m2)"
        >
          <Input
            radius="full"
            variant="bordered"
            placeholder="sprinkler coverage"
          />
        </Form.Item>

        <Form.Item
          name="WaterOutflowRate_c"
          label="Input the outflow rate of the sprinkler (in L/h)"
        >
          <Input
            radius="full"
            variant="bordered"
            placeholder="Water outflow rate"
          />
        </Form.Item>

        <Form.Item
          name="numberOfSprinklers_c"
          label="Enter the number of sprinklers in use"
        >
          <Input
            radius="full"
            variant="bordered"
            placeholder="number of sprinklers"
          />
        </Form.Item>
      </Form>
    </div>
  );
  const Dirr_t = (
    <div className="flex flex-col gap-4 min-w-[400px] w-[50%]">
      <div className="flex flex-col font-Myfont">
        <p className="text-[32px] font-bld">
          {Data.PlantingDetails?.type != "Crop and tree"
            ? "Drip irrigation"
            : "Tree Irrigation System"}
        </p>
        {Data.PlantingDetails?.type != "Crop and tree" && (
          <p className="text-[12px] font-nrml">
            Enter the details of your Drip Irrigation System to optimize water
            distribution and crop growth.
          </p>
        )}
      </div>
      <Form form={form} layout="vertical" autoComplete="off">
        <Form.Item
          name={"DistanceBetweenRows_t"}
          label="Enter the distance between rows (in meters)"
        >
          <Input
            radius="full"
            variant="bordered"
            placeholder="Distance Between rows"
          />
        </Form.Item>

        <Form.Item
          name="DistanceBetweenTrees_t"
          label="Enter the distance between trees (in meters)"
        >
          <Input
            radius="full"
            variant="bordered"
            placeholder="Distance between trees"
          />
        </Form.Item>
        <Form.Item
          name={"NumberOfTubesPerTree_t"}
          label="Enter the number of tubes per tree"
        >
          <Input
            radius="full"
            variant="bordered"
            placeholder="Number of Tubes per Tree"
          />
        </Form.Item>

        <Form.Item
          name="NumberOfDrippersPerTree_t"
          label="Enter the number of drippers per tree"
        >
          <Input
            radius="full"
            variant="bordered"
            placeholder="Number of Drippers per Tree"
          />
        </Form.Item>
        <Form.Item
          name="WaterOutflowRate_t"
          label="Input the outflow rate (in L/h)"
        >
          <Input
            radius="full"
            variant="bordered"
            placeholder="Water outflow rate"
          />
        </Form.Item>
      </Form>
    </div>
  );
  const Sirr = (
    <div className="flex flex-col gap-4 min-w-[400px] w-[50%] ">
      <div className="flex flex-col font-Myfont">
        <p className="text-[32px] font-bld">Sprinkler irrigation</p>
        <p className="text-[12px] font-nrml">
          Enter the details of your Sprinkler Irrigation System below to help
          manage water usage effectively.
        </p>
      </div>
      <Form form={form} layout="vertical" autoComplete="off">
        <Form.Item
          name={"sprinklerCoverage_c"}
          label="Specify the total coverage area of the sprinkler (in m2)"
        >
          <Input
            radius="full"
            variant="bordered"
            placeholder="sprinkler coverage"
          />
        </Form.Item>

        <Form.Item
          name="WaterOutflowRate_c"
          label="Input the outflow rate of the sprinkler (in L/h)"
        >
          <Input
            radius="full"
            variant="bordered"
            placeholder="Water outflow rate"
          />
        </Form.Item>

        <Form.Item
          name="numberOfSprinklers_c"
          label="Enter the number of sprinklers in use"
        >
          <Input
            radius="full"
            variant="bordered"
            placeholder="number of sprinklers"
          />
        </Form.Item>
      </Form>
    </div>
  );
  const Dirr = (
    <div className="flex flex-col gap-4 min-w-[400px] w-[50%]">
      <div className="flex flex-col font-Myfont">
        <p className="text-[32px] font-bld">
          {Data.PlantingDetails?.type != "Crop and tree"
            ? "Drip irrigation"
            : "Crop Irrigation System"}
        </p>
        {Data.PlantingDetails?.type != "Crop and tree" && (
          <p className="text-[12px] font-nrml">
            Enter the details of your Drip Irrigation System to optimize water
            distribution and crop growth.
          </p>
        )}
      </div>
      <Form form={form} layout="vertical" autoComplete="off">
        <Form.Item
          name={"DistanceBetweenTubes_c"}
          label="Enter the distance between tubes (in meters)"
        >
          <Input
            radius="full"
            variant="bordered"
            placeholder="Distance Between Tubes"
          />
        </Form.Item>

        <Form.Item
          name="DistanceBetweenDrippers_c"
          label="Enter the distance between drippers (in meters)"
        >
          <Input
            radius="full"
            variant="bordered"
            placeholder="Distance between drippers"
          />
        </Form.Item>
      </Form>
    </div>
  );
  const dispatch = useAppDispatch();
  useEffect(() => {
    dispatch(
      updateFarmerInfo({
        IrrigationType: {
          system: name.name,
          prop: form.getFieldsValue(),
        },
      })
    );
  }, [form.isFieldsTouched()]);
  return (
    <div className="w-full flex justify-center mt-6 ">
      {Data.PlantingDetails?.type === "Crop" && (
        <>{name.name === "Drip irrigation" ? Dirr : Sirr}</>
      )}
      {Data.PlantingDetails?.type === "Tree" && (
        <>{name.name === "Drip irrigation" ? Dirr_t : Sirr_t}</>
      )}
      {Data.PlantingDetails?.type === "Crop and tree" && (
        <div className="flex w-full justify-center">
          {name.name === "Drip irrigation" ? (
            <div className="flex justify-center w-full gap-10 p-2">
              {Dirr}
              <Divider orientation="vertical" />

              {Dirr_t}
            </div>
          ) : (
            Sirr_t
          )}
        </div>
      )}
    </div>
  );
};

const IrrgSys = () => {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const [sysName, setSysName] = useState("");
  const dispatch = useAppDispatch();

  function handleEvent(name: string) {
    const Obj = {
      onClick: () => {
        if (name == "Sprinkler irrigation" || name == "Drip irrigation")
          onOpen();
        else {
          dispatch(
            updateFarmerInfo({
              IrrigationType: {
                system: name,
                prop: null,
              },
            })
          );
        }
        setSysName(name);
      },
    };
    return Obj;
  }

  const cards = [
    {
      img: Srirr,
      name: "Surface irrigation",
    },
    {
      img: Sirr,
      name: "Sprinkler irrigation",
    },
    {
      img: Dirr,
      name: "Drip irrigation",
    },
    {
      img: Rirr,
      name: "Rainfed irrigation",
    },
  ];

  const Data = useAppSelector((state) => state.farmer);
  const cardStyle =
    "w-[20%] pb-4  flex group  focus:*:text-white focus:bg-black flex-col  items-center justify-between hover:bg-[#1E6F5C] overflow-hidden rounded-[10px] h-[170px] cursor-pointer";
  return (
    <div className="w-full mb-16 mt-14  flex flex-wrap gap-4 justify-center items-center font-Myfont font-bld">
      {cards.map((val, key) => {
        return (
          <div
            {...handleEvent(val.name)}
            className={`${cardStyle} 
            ${
              val.name === sysName
                ? " text-white bg-[#1E6F5C]"
                : "bg-[#D3E1D1] text-black"
            }
            `}
          >
            <img className="w-full mb-2" src={val.img} alt="" />
            <p className="group-hover:text-white text-[14px]">{val.name}</p>
          </div>
        );
      })}

      <Modal
        isOpen={isOpen}
        onOpenChange={onOpenChange}
        placement="top-center"
        className={`${
          Data.PlantingDetails?.type === "Crop and tree"
            ? "w-[1000px]"
            : "w-[750px]"
        } `}
      >
        <ModalContent
          className={`${
            Data.PlantingDetails?.type === "Crop and tree"
              ? "max-w-[1000px]"
              : "max-w-[600px]"
          } `}
        >
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col  p-0 overflow-hidden ">
                <img
                  src={sysName === "Sprinkler irrigation" ? fsp : dsp}
                  className="w-full"
                  alt=""
                />
              </ModalHeader>
              <ModalBody className="">
                <IrrForms name={sysName} />
              </ModalBody>
              <ModalFooter className="">
                <Button className="bg-" variant="flat" onPress={onClose}>
                  cancel
                </Button>
                <Button
                  radius="full"
                  className="bg-Green text-white"
                  onPress={onClose}
                >
                  save
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </div>
  );
};

const Irrigationsystem_ = () => {
  const list = [
    "Installation date",
    "Last maintenance date",
    // "the flow",
  ];
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
    <div className="w-full pt-14  flex gap-6 justify-center items-center flex-col">
      <div className="">
        <p className="font-Myfont font-bld text-[40px]">Irrigation System</p>
        <p className="font-Myfont font-md text-[12px]">
          Select your preferred method for watering crops from the <br />{" "}
          options provided
        </p>
      </div>
      <div className="w-full flex justify-center items-center">
        <IrrgSys />
      </div>
      {/* <div className="flex flex-col gap-4 label-">
        <Select
          classNames={{
            trigger: "border-[#1E6F5C] text-[#1E6F5C]",
            label: "text-[#1E6F5C]",
          }}
          color="success"
          variant="bordered"
          labelPlacement="outside"
          size="lg"
          radius={"full"}
          label="Select your irrigation method."
          className="w-[375px]"
          placeholder="Irrigation method"
          //   onChange={(e) => {
          //     if (!e.target.value) e.target.value = list[0];
          //   }}
        >
          {soil_.map((val, _) => {
            return (
              <SelectItem key={val} value={val}>
                {val}
              </SelectItem>
            );
          })}
        </Select>
        <DateInput
          label="Enter the Installation date."
          variant="bordered"
          radius="full"
          size="lg"
          classNames={{ inputWrapper: "border-[#1E6F5C]", input: "" }}
          //   defaultValue={parseDate("2024-04-04")}
          placeholderValue={new CalendarDate(1995, 11, 6)}
          labelPlacement="outside"
          startContent={<img className="w-[20px]" src={canld} />}
        ></DateInput>
        <DateInput
          label="Enter the maintenance date"
          variant="bordered"
          radius="full"
          size="lg"
          classNames={{ inputWrapper: "border-[#1E6F5C]", input: "" }}
          //   defaultValue={parseDate("2024-04-04")}
          placeholderValue={new CalendarDate(1995, 11, 6)}
          labelPlacement="outside"
          startContent={<img className="w-[20px]" src={canld} />}
        ></DateInput>
        <Input
          labelPlacement="outside"
          label="Please Enter the flow."
          onChange={(e) => {
            // dispatch(setFieldName(e.target.value))
            console.log(e.target.value);
          }}
          // isRequired
          radius="full"
          size="lg"
          classNames={{
            inputWrapper: "border-[#1E6F5C] hover:border-[#1E6F5C]",
            input: ["placeholder:text-[#1E6F5C]"],
          }}
          className=" w-[375px]"
          placeholder="The flow"
          type="text"
          variant="bordered"
        ></Input>
      </div> */}
    </div>
  );
};

export default Irrigationsystem_;
