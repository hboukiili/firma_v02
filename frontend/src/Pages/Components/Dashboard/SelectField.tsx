import React from "react";
import {Select, SelectItem} from "@nextui-org/react";
import "./style.css"


interface option_ {
  option:string
}
export const fields = [
    {label: "Field1", value: "Field1", description: "description"},
    {label: "Field2", value: "Field2", description: "description"},
    {label: "Field3", value: "Field3", description: "description"},
    {label: "Field4", value: "Field4", description: "description"},
    {label: "Field5", value: "Field5", description: "description"},
    
  ];
const SelectField = (option:option_) => {

  return (
    <>
        <Select
          radius={"full"}
          label={option.option}
        //   placeholder="Select Field"
        //   defaultSelectedKeys={["Field1"]}
          className="max-w-[60%] max-h-[90] select-field"
        >
          {fields.map((field) => (
            <SelectItem key={field.value} value={field.value}>
              {field.label}
            </SelectItem>
          ))}
        </Select>
    </>  
  );
}

export default SelectField
