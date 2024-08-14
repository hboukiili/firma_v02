import { Progress, Radio, RadioGroup, Select, SelectItem, Skeleton, Spinner } from "@nextui-org/react";
import { Button } from "@nextui-org/react";
import React, { useEffect, useRef, useState } from "react";
import Map_ from "./Dashboard/Map";
import Chartx from "./Dashboard/Chartx";
import { saveAs } from 'file-saver';
import Papa from 'papaparse';
import api from "../../api/axios.js";
import { Slider } from "@nextui-org/react";



interface Analytics_ {
    SetVrbName: React.Dispatch<React.SetStateAction<string>>;
    isForDownload: React.Dispatch<React.SetStateAction<boolean>>;
    SetFileData: React.Dispatch<React.SetStateAction<any>>;
    SetIsForChart: React.Dispatch<React.SetStateAction<boolean>>;
    data: any;
    fileData: any;
    FieldName: string;
    variableName: string;
}

const Analytics = (Data: Analytics_) => {

    const [variable, SetVariable] = useState("");
    const [Format, SetFormat] = useState("");
    const [Variable_, SetVariable_] = useState(Data.variableName);
    const [isTheUserSelectInfo, SetIsUserSelectInfo] = useState(true);
    const ref_ = useRef(null)


    const variables = ["NDVI", "LST", "Ta", "Rs", "Rh", "Ws", "Lai", "Fc"];

    let loading = true;
    const [downloading, Setdownloading] = useState(true);
    console.log(Data, "----")
    if (Data.data) loading = false
    useEffect(() => {
        console.log("hona")
        if (Data.fileData) {
            if (Format === "Csv") {
                const csvContent = [
                    Object.keys(Data.fileData[0]).join(','), // Headers
                    ...Data.fileData.map(obj => Object.values(obj).join(',')) // Rows
                ].join('\n');
                let type = Format === "Csv" ? 'text/csv' : 'application/pdf';
                const blob = new Blob([csvContent], { type: type });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'data.csv';
                a.click();
                URL.revokeObjectURL(url);

                Data.SetFileData(null);
                SetIsUserSelectInfo(false);
                Data.isForDownload(false);
                Setdownloading(true);
            }
        }
    }, [Data.fileData])

    return (
        <>
            <div className="flex flex-col items-end gap-[1rem] grow">
                {/* <div className="flex w-full items-center justify-between">

                </div> */}
                <div className="h-[34rem] w-full">
                    <Map_ field={Data.FieldName} />
                </div>
            </div>
            <div className="w-[45rem] flex flex-col justify-start gap-4 ">
                <Select
                    radius="lg"
                    label="Select variable"

                    className="max-w-[15rem]  select-field"
                    onChange={(e) => {
                        Data.SetVrbName(e.target.value)
                        SetVariable_(e.target.value);
                        Data.SetIsForChart(true)
                        // Data.data = null
                        loading = true;
                    }}
                >
                    {variables.map((val, _) => {
                        return (
                            <SelectItem key={val} value={val}>
                                {val}
                            </SelectItem>)
                    }
                    )}
                </Select>
                <div className="w-full h-[15rem] flex justify-center items-center">
                    {!loading ?
                        < Chartx ref_={ref_} band={Variable_} Data={Data.data} />
                        :
                        <Spinner className="" color="success" />
                    }
                </div>
                <div className="w-full h-[13rem] flex justify-center items-center">
                    <div className="w-full h-full flex  justify-between items-center gap-1">
                        <div className="w-[50%] h-full  p-[15px] bg-DarkGreen rounded-lg">
                            <h1 className="font-Myfont text-Green font-bld text">Data Exporter</h1>
                            <div className="flex items-end w-[100%] gap-5 justify-between">
                                <RadioGroup
                                    color="warning"
                                    label="Choose Data and Download Format"
                                    className="gap-2 text-[14px] radio- w-full font-Myfont "
                                    onChange={(e) => {
                                        SetVariable(e.target.value)
                                        if (Format.length)
                                            SetIsUserSelectInfo(false)
                                    }}

                                >
                                    <div className="flex gap-6 ">

                                        <div className="flex flex-col gap-1 radio-">
                                            <Radio className="text-white" size="sm" value="NDVI">Ndvi</Radio>
                                            <Radio className="text-white" size="sm" value="LST">Lst</Radio>

                                        </div>
                                        <div className="flex flex-col gap-1 radio-">
                                            <Radio size="sm" value="Rh">Rh</Radio>
                                            <Radio size="sm" value="Ws">Ws</Radio>

                                        </div>
                                        <div className="flex flex-col gap-1 radio-">

                                            <Radio className="text-white" size="sm" value="Ta">Ta</Radio>
                                            <Radio className="text-white" size="sm" value="Rs">Rs</Radio>
                                        </div>
                                        <div className="flex flex-col gap-1 radio-">

                                            <Radio size="sm" value="Lai">Lai</Radio>
                                            <Radio size="sm" value="Fc">Fc</Radio>
                                        </div>
                                    </div>

                                </RadioGroup>
                                <RadioGroup
                                    color="danger"
                                    className="gap-6 text-[14px] w-full font-Myfont "
                                    onChange={(e) => {
                                        SetFormat(e.target.value)
                                        if (variable.length)
                                            SetIsUserSelectInfo(false)
                                    }}
                                >
                                    {/* <Radio value="NDVI">Pdf</Radio> */}
                                    <Radio className="radio-"
                                        isDisabled={!variable ? true : false} size="sm" value="Csv">Csv</Radio>

                                </RadioGroup>
                            </div>
                            <div className="w-full flex flex-col pt-3 gap-3 ">
                                <Button onClick={() => {
                                    Data.SetVrbName(variable)
                                    Data.isForDownload(true)
                                    SetIsUserSelectInfo(true);
                                    Setdownloading(false);
                                }} isDisabled={isTheUserSelectInfo} radius="full" className="w-[100px] h-[35px] text-white bg-Green">
                                    Download
                                </Button>
                                {!downloading && <Progress
                                    size="sm"
                                    color="warning"
                                    isIndeterminate
                                    aria-label="Loading..."
                                    className="max-w-md"
                                />}
                            </div>
                        </div>
                        <div className="rounded-lg w-[45%] h-full flex flex-col items-center justify-center gap-6">

                        </div>
                    </div>
                </div>
            </div>
        </>
    )

}

export default Analytics;
