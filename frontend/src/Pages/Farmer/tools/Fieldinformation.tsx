import React, { useEffect } from "react";
import { Input, Select, SelectItem } from "@nextui-org/react";
import "./style.css";
import { updateFarmerInfo } from "../../../Redux/Farmer/actions";
import { useAppDispatch, useAppSelector } from "../../../Redux/hooks";
import { Form } from "antd";

const FieldInformation = () => {
  const irrigation_ = [
    "Surface irrigation",
    "Sprinkler irrigation",
    "Drip irrigation",
    "Subsurface irrigation",
  ];
  const crops_ = ["Wheat", "Maize", "Potatoes"];
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);

  //   const list = ["Irrigation system", "Soil type"];
  const [form] = Form.useForm<{ name: string; age: number }>();
  useEffect(() => {
    if(Data.Field || Data.fieldName)
      dispatch(updateFarmerInfo({fieldName : ""}))
  },[])

  return (
    <div className="w-full h-[370px] flex gap-16 justify-center items-center flex-col">
      <div className="">
        <p className="font-Myfont font-bld text-[40px]">Field information</p>
        <p className="font-Myfont font-md text-[12px]">
          Before providing field details, either draw your polygon <br /> on the
          map or select one of three methods.
        </p>
      </div>
      <div className="flex flex-col w-[350px] gap-4">
        <Form form={form} layout="vertical" autoComplete="off">
          <Form.Item name="Radius" label="Enter the name of your field.">
            <Input
              onChange={(e) => {
                dispatch(updateFarmerInfo({ fieldName: e.target.value }));
              }}
              placeholder="Field name"
              radius="full"
              // variant="bordered"
              classNames={{
                inputWrapper: "bg-white border-white hover:border-white",
              }}
            />
          </Form.Item>
        </Form>
        {/* <Input
          labelPlacement="outside"
          label="Enter the name of your field."
          onChange={(e) => {
            dispatch(updateFarmerInfo({ fieldName: e.target.value }));
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
          placeholder="Field name"
          type="text"
          variant="bordered"
        ></Input> */}
      </div>
    </div>
  );
};

export default FieldInformation;
