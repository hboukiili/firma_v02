import React, { useEffect, useState } from "react";
import Map_ from "../Components/Dashboard/Map.js";
import CropPie from "../Components/Dashboard/CropPie.js";
import WaterStress from "../Components/Dashboard/WaterStress.js";
import { Button } from "@nextui-org/button";
import Chartx from "../Components/Dashboard/Chartx.js";
import Weather from "../Components/Dashboard/Weather.js";
import Area from "../Components/Dashboard/Area.js";
import api from "../../api/axios.js"
import { Select, SelectItem } from "@nextui-org/react";


export interface Data_ {
    [key: string]: any;
}

const Dashboard = () => {
    const [Data, SetData] = useState<Data_>([]);
    const [Field, SetField] = useState("");
    const [FieldName, SetName] = useState("");

    useEffect(() => {
        api.get("api/field/")
            .then((res) => {
                console.log(Object.keys(res.data)[0], "hona")
                SetData(res.data);
                SetName(Object.keys(res.data)[0])
            })
            .catch((err) => {
                console.log(err);
            })
    }, [])
    return (
        <>
            <div className="flex w-full  flex-col max-w-[1800px]  justify-between items-center gap-2 md:p-[2%]">
                <div className="w-full flex flex-col  items-end lg:flex-row gap-2">
                    <div className="flex w-full flex-col gap-2 items-center sm:flex-row lg:w-[65%]">
                        <div className="w-[100%] h-[20rem] sm:h-[26rem] md:w-[48%] flex justify-center items-center rounded-md overflow-hidden z-[6900]">
                            <Map_ field={FieldName} />
                        </div>
                        <div className="flex flex-col gap-2 w-full md:w-[50%]">
                            <div className="flex justify-between items-center">
                                <Select
                                    radius={"full"}
                                    label="Select Field"
                                    onChange={(e) => {
                                        SetField(e.target.value)
                                        SetName(e.target.value)
                                    }}
                                    //   placeholder="Select Field"
                                    //   defaultSelectedKeys={Data[FieldName].name}
                                    className="max-w-[60%] max-h-[90] select-field"
                                >
                                    {Object.keys(Data).map(key => {
                                        if (!FieldName)
                                            SetName(Data[key].name)
                                        return (
                                            <SelectItem key={Data[key].name} value={Data[key].name}>
                                                {Data[key].name}
                                            </SelectItem>)
                                    }
                                    )}

                                </Select>
                                <Button className="w-[35%] bg-Green text-white  " radius="full" >
                                    Add New Season
                                </Button>
                            </div>

                            <div className="flex gap-2 w-full">
                                <WaterStress />
                                <Area Field_id={Data[FieldName]?.field_id} />
                            </div>
                            <div className="h-[11rem] bg-[#EAF3E9] rounded-md  ">
                            </div>
                        </div>
                    </div>
                    <div className="flex flex-col w-full gap-2 sm:flex-row lg:flex-col lg:w-[50%] md:items-end">
                        <div className="w-[100%]  flex justify-center items-center ">
                            <CropPie />
                        </div>
                        <div className="w-[100%] h-[11rem] bg-[#EAF3E9]  rounded-md flex justify-center items-center ">
                            {/* <Chartx /> */}
                        </div>
                    </div>
                </div>
                <div className="w-full flex">
                    <Weather Name={FieldName} />
                </div>
            </div>
        </>
    )
}

export default Dashboard;