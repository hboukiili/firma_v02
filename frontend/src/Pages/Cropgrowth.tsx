import React, { useEffect, useState } from "react";
import Map_ from "./Components/Dashboard/Map"
import api from "../api/axios.js"
import { Button, Input, Select, SelectItem, Skeleton, Spinner, divider } from "@nextui-org/react";
import { Data_ } from "./Farmer/Dashboard.js";
import Chartx from "./Components/Dashboard/Chartx.js";
import Analytics from "./Components/Analytics.js";


const Cropgrowth = () => {

    const [FieldId, SetFieldId] = useState();
    const [SelectPixel, setSelectPixel] = useState(false);
    const [IsPixelLoaded, setIsPixelLoaded] = useState(false);
    const [Bounds, setBounds] = useState()
    const [ImageUrl, setImageUrl] = useState()
    const [Center, setCenter] = useState()
    const [selectedPoint, setSelectedPoint] = useState([]);
    const [ndviPixel, setNdviPixel] = useState([]);

    const [ChartData, SetChartData] = useState()
    const [Data, SetData] = useState<Data_>([]);
    const [FieldName, SetFieldName] = useState("");
    const [loading, setLoading] = useState(true);
    const [variablesName, SetVrbName] = useState("NDVI");
    const Satellites = ["Sentinel2", "Landsate8"];
    const [SatelliteName, SetSatelliteName] = useState("");
    const [StartDate, SetStartDate] = useState("");
    const [EndDate, SetEndDate] = useState("");
    const [Issub, SetIssub] = useState(false);
    const variables = ["NDVI", "LST", "Ta", "Rs", "Rh", "Ws", "Lai", "Fc"];
    const [ArrOfDays, SetArrOfDays] = useState([]);
    const [isForDownload, SetisForDownload] = useState(false);
    const [isForChart, SetisForChart] = useState(false);
    const [FileData, SetFileData] = useState();
    useEffect(() => {
        async function fetch() {
            api.get("/api/field/")
                .then((res) => {
                    SetData(res.data);
                    if (!FieldName)
                        SetFieldName(Object.keys(res.data)[0])
                })
                .catch((err) => {
                    console.log(err);
                })
        }
        fetch()
    }, [])

    useEffect(() => {
        if (StartDate && EndDate && FieldName && SatelliteName && variablesName) {
            async function fetch() {
                if (isForChart) { SetChartData(null), SetisForChart(false) }
                await api.post('/irrigation/chart/', {
                    field: Data[FieldName].field_id,
                    start_date: StartDate,
                    end_date: EndDate,
                    satellite: SatelliteName,
                    band: variablesName,
                    arr_of_days: ArrOfDays,

                })
                    .then(response => {
                        if (isForDownload) SetFileData(response.data)
                        else if (isForChart) SetChartData(response.data)
                        if (!ArrOfDays.length)
                            SetArrOfDays(response.data.map((item) => item.date))
                    })
                    .catch(error => {
                        console.log("err", error);
                    });
            }
            fetch()
        }
    }, [variablesName, isForDownload])
    return (
        <div className="flex w-full h-screen flex-col max-w-[1800px] p-[4%] justify-between items-center gap-[1rem] md:p-[2%]">

            {!Issub ? <form className="w-full h-full flex flex-col justify-center items-center gap-6 ">
                Data Analytics
                <Select
                    radius={"full"}
                    label="Select Field"
                    className="max-w-[21rem] max-h-[90] select-field"
                    onChange={(e) => {
                        SetFieldName(e.target.value)
                    }}
                >
                    {Object.keys(Data).map(key => {
                        return (
                            <SelectItem key={Data[key].name} value={Data[key].name}>
                                {Data[key].name}
                            </SelectItem>)
                    }
                    )}
                </Select>
                <Select
                    radius={"full"}
                    label="Select Satellite"
                    className="max-w-[21rem] max-h-[90] select-field"
                    onChange={(e) => {
                        SetSatelliteName(e.target.value)
                    }}
                >
                    {Satellites.map((val, _) => {
                        return (
                            <SelectItem key={val} value={val}>
                                {val}
                            </SelectItem>)
                    }
                    )}
                </Select>
                <Select
                    radius={"full"}
                    label="Select variable"
                    className="max-w-[21rem] h-[90] select-field"
                    onChange={(e) => {
                        SetVrbName(e.target.value)
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
                <Input
                    label="Start Date"
                    variant="bordered"
                    placeholder="Start Date"
                    type={"date"}
                    radius={"full"}
                    classNames={{
                        base: "max-w-[21rem]",
                        inputWrapper: [
                            "bg-white",
                        ],
                    }}
                    required
                    onChange={(e) => SetStartDate(e.target.value)}
                />
                <Input
                    label="End Date"
                    variant="bordered"
                    placeholder="End Date"
                    type={"date"}
                    radius={"full"}
                    classNames={{
                        base: "max-w-[21rem]",
                        inputWrapper: [
                            "bg-white",
                        ],
                    }}
                    required
                    onChange={(e) => SetEndDate(e.target.value)}
                />
                <Button onClick={() => {
                    if (StartDate && EndDate && FieldName && SatelliteName && variablesName) {
                        async function fetch() {
                            await api.post('/irrigation/chart/', {
                                field: Data[FieldName].field_id,
                                start_date: StartDate,
                                end_date: EndDate,
                                satellite: SatelliteName,
                                band: variablesName,
                                arr_of_days: ArrOfDays,

                            })
                                .then(response => {
                                    SetChartData(response.data)
                                    setLoading(false);
                                    if (!ArrOfDays.length)
                                        SetArrOfDays(response.data.map((item) => item.date))

                                })
                                .catch(error => {
                                    console.log("err", error);
                                });
                        }
                        fetch()
                        SetIssub(true);
                    }
                }} radius="full" className="bg-Green  text-white  ">
                    submit
                </Button>
            </form>
                :
                <div className="w-full h-full flex items-end justify-between">
                    {!loading ? <div className="flex w-full h-full justify-center gap-4 pt-4">
                        <Analytics
                            fileData={FileData} variableName={variablesName} data={ChartData}
                            FieldName={FieldName} isForDownload={SetisForDownload}
                            SetVrbName={SetVrbName} SetFileData={SetFileData}
                            SetIsForChart={SetisForChart} />
                    </div>
                        :
                        <Spinner className="absolute top-[55%] left-[53%]" color="success" />
                    }
                </div>
            }
        </div>
    )
}

export default Cropgrowth