import React, { useEffect, useRef, useState } from "react";
import {
    FeatureGroup,
    ImageOverlay,
    MapContainer,
    Polygon,
    TileLayer,
    Popup,
    Marker,
    useMap,
    LayersControl,
    LayerGroup,
    ZoomControl
} from 'react-leaflet'
import { EditControl } from "react-leaflet-draw";
import '../index.css'
import { Button, Card, CardBody, Checkbox, CheckboxGroup, Input, Modal, ModalBody, ModalContent, ModalFooter, ModalHeader, Select, SelectItem, Tab, Tabs, useDisclosure } from "@nextui-org/react";
import { ReactSVG } from "react-svg";
import Prm_icn from "../assets/sett.svg"
import Ta_icn from "../assets/Ta.svg"
import Ws_icn from "../assets/ws.svg"
import Rh_icn from "../assets/rh.svg"
import Rs_icn from "../assets/rs.svg"
import Rn_icn from "../assets/rain.svg"
import { LineChart } from "@mui/x-charts";


// import 

const Map_ = () => {
    const mapRef = useRef()
    return (
        <div className="flex justify-center items-center  h-[100%] w-[100%] overflow-hidden rounded-lg">
            <MapContainer zoomControl={false} center={[34.245242, -5.828727]} ref={mapRef} zoom={13}
                style={{ width: "100%", height: "100%" }}>
                <LayersControl position="bottomleft">
                    <LayersControl.BaseLayer checked name="Satellite">
                        <LayerGroup>
                            <TileLayer
                                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                                url="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
                            />
                            <TileLayer
                                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
                                url='https://{s}.basemaps.cartocdn.com/rastertiles/voyager_only_labels/{z}/{x}/{y}{r}.png'
                            />
                        </LayerGroup>
                    </LayersControl.BaseLayer>
                    <LayersControl.BaseLayer name="Mapbox Map">
                        <TileLayer
                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                            url='https://tile.openstreetmap.org/{z}/{x}/{y}.png'
                        />
                    </LayersControl.BaseLayer>
                </LayersControl>

                <ZoomControl position="bottomleft"></ZoomControl>

                <FeatureGroup>
                    <EditControl
                        // onCreated={(e) => {
                        //     const latlng = e.layer.getLatLng();
                        //     setSelectedPoint([latlng.lat, latlng.lng]);
                        //     handleMarkerClick(latlng);
                        // }}
                        position="bottomright"
                        draw={{
                            polyline: false,
                            circle: false,
                            marker: true,
                            circlemarker: false,
                            polygon: true,
                            rectangle: false,
                        }}
                    />

                </FeatureGroup>
            </MapContainer>

        </div >
    )
}

interface Policymaker_ {
    SetIsSubmit: React.Dispatch<React.SetStateAction<boolean>>;
    SetWatershedId: React.Dispatch<React.SetStateAction<string>>;
    SetInputs: React.Dispatch<React.SetStateAction<{
        StDate: string;
        EdDate: string;
        Band: string;
    } | undefined>>,
    isAcademic: boolean,
    Watershed: string,

}

export const InputsBar = (attributs: Policymaker_) => {
    const variables = ["Weather", "Surface Variables"];
    const variable = ["30m", "1km"];

    const [VrbName, SetVrbName] = useState("")
    const [EndDate, SetEndDate] = useState("")
    const [StartDate, SetStartDate] = useState("")
    const [Resolution, SetResolution] = useState("")
    const WatershedNames = [
        "Bouregreg",
        "Daraa",
        "Guir - Ziz - Rhris",
        "Loukkous",
        "Moulouya",
        "Oum Er Rbia",
        "Souss Massa",
        "Sahara",
        "Sebou",
        "Tensift",
    ]
    const [isFilled, SetIsFilled] = useState(false)
    useEffect(() => {
        if (VrbName && EndDate && StartDate && Resolution)
            SetIsFilled(true);
        console.log(VrbName, EndDate, StartDate, Resolution)
        attributs.SetInputs({ Band: VrbName, EdDate: EndDate, StDate: StartDate })
    }, [VrbName, EndDate, StartDate, Resolution])

    console.log(attributs.Watershed, "000")
    return (
        <div className="min-w-[670px] rounded-[10px] b-[#134C39] h-full w-[95%] flex justify-center items-center gap-5">
            {!attributs.isAcademic &&
                <>
                    <Select
                        size="sm"
                        radius={"full"}
                        label={"Select Watershed"}
                        className="max-w-[18rem] select-field"
                        defaultValue={"dddd"}
                        onChange={(e) => {
                            attributs.SetWatershedId(e.target.value)
                        }}
                    >
                        {WatershedNames.map((val, _) => {
                            return (
                                <SelectItem key={val} value={val}>
                                    {val}
                                </SelectItem>)
                        }
                        )}
                    </Select>
                </>
            }
            <Select
                size="sm"
                radius={"full"}
                label="Select Band"
                className="max-w-[18rem] select-field"
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
                size="sm"

                label="Start Date"
                variant="bordered"
                placeholder="Start Date"
                type={"date"}
                radius={"full"}
                classNames={{

                    base: "max-w-[18rem]",
                    inputWrapper: [
                        "bg-white",
                        "border-none"
                    ],
                }}
                required
                onChange={(e) => SetStartDate(e.target.value)}
            />
            <Input
                size="sm"
                label="End Date"
                variant="bordered"
                placeholder="End Date"
                type={"date"}
                radius={"full"}
                classNames={{
                    base: "max-w-[18rem]",
                    inputWrapper: [
                        "bg-white",
                        "border-none"

                    ],
                }}
                required
                onChange={(e) => SetEndDate(e.target.value)}
            />
            {
                attributs.isAcademic &&
                <>
                    <Select
                        size="sm"
                        radius={"full"}
                        label="Select Resolution"
                        className="max-w-[18rem] h-[] select-field "
                        onChange={(e) => {
                            SetResolution(e.target.value)
                        }}
                    >
                        {variable.map((val, _) => {
                            return (
                                <SelectItem key={val} value={val}>
                                    {val}
                                </SelectItem>)
                        }
                        )}
                    </Select>
                    <Button isDisabled={!isFilled}
                        onClick={() => attributs.SetIsSubmit(true)}
                        radius="full" className="bg-[#43C69C] text-white font-Myfont">
                        Progress
                    </Button>
                </>
            }
        </div >
    )
}


const InputButton = (attributs: Policymaker_) => {
    return (
        <div className="rounded-[10px]  transition-all w-full flex  justify-center items-start">
            <Button onClick={() => attributs.SetIsSubmit(false)} className="bg-[#134C39] w-full h-[55px] text-white font-Myfont font-bld gap-2 flex justify-center items-center">
                <ReactSVG className="w-[18px]" src={Prm_icn} />
                <p>Change Data Collection</p>
            </Button>
        </div>
    )
}

const TimeSeries = () => {

    const Data = [
        { name: "Temperature", body: "Temperature", icn: Ta_icn },
        { name: "Wind speed", body: "Wind speed", icn: Ws_icn },
        { name: "Humidity", body: "Humidity", icn: Rh_icn },
        { name: "Solar Radiation", body: "Solar Radiation", icn: Rs_icn },
        { name: "Rain", body: "Rain", icn: Rn_icn },
    ]
    const test = ["2022-01-02", "2022-01-03", "2022-01-04", "2022-01-05", "2022-01-06", "2022-01-07"]
    const dates = test.map((item) => new Date(item));
    const Values = [10, 28, 20, 22, 32, 24]
    const { isOpen, onOpen, onOpenChange } = useDisclosure();
    return (
        <div className="relative  w-full h-[280px] flex flex-col">
            <div className="absolute right-0 flex gap-2">
                <Button onPress={onOpen} className=" bg-Green w-[260px] text-white" radius="full">Download Data</Button>
                <Modal backdrop="blur" className="z-[100]" isOpen={isOpen} onOpenChange={onOpenChange}>
                    <ModalContent>
                        {(onClose) => (
                            <>
                                <ModalHeader className="flex flex-col gap-1">Download Data</ModalHeader>
                                <ModalBody className="flex justify- items-start">
                                    <CheckboxGroup
                                        color="success"
                                        label="Select variable"
                                    >
                                        <div className="flex gap-32">
                                            <div className="flex flex-col">
                                                <Checkbox value="Temperature">Temperature</Checkbox>
                                                <Checkbox value="Wind speed">Wind speed</Checkbox>
                                                <Checkbox value="Humidity">Humidity</Checkbox>
                                                <Checkbox value="Solar Radiation">Solar Radiation</Checkbox>
                                            </div>
                                            <div className="flex flex-col">
                                                <Checkbox value="NDVI">NDVI</Checkbox>
                                                <Checkbox value="LST">LST</Checkbox>
                                                <Checkbox value="LAI">LAI</Checkbox>
                                            </div>
                                        </div>
                                    </CheckboxGroup>
                                </ModalBody>
                                <ModalFooter>
                                    <Button color="danger" variant="light" onPress={onClose}>
                                        Close
                                    </Button>
                                    <Button onPress={onClose} className=" bg-Green text-white" radius="full">Download</Button>

                                </ModalFooter>
                            </>
                        )}
                    </ModalContent>
                </Modal>
            </div>
            <Tabs
                className="w-[70%]"
                classNames={{
                    tabList: "border-Green",
                    cursor: "bg-Green text-red-300 ",
                    tabContent: "text-DarkGreen fill-DarkGreen group-data-[selected=true]:text-white ",
                }} radius="full" variant="bordered" aria-label="Disabled Options">
                {
                    Data.map((value, _) => {
                        return (
                            <Tab key={value.name} title={
                                <div className="flex gap-4 justify-center items-center">
                                    <ReactSVG className="group-data-[selected=true]:fill-white fill-DarkGreen" src={value.icn} />
                                    <p>{value.name}</p>
                                </div>
                            }>
                                <Card className=" ">
                                    <CardBody className="h-[225px] ">
                                        <LineChart
                                            // ref={data.ref_}
                                            sx={{
                                                '& .MuiAreaElement-series-value': {
                                                    fill: "#57ea7585",
                                                },
                                            }}
                                            xAxis={[
                                                {

                                                    data: dates,
                                                    scaleType: 'time',
                                                    valueFormatter: (dates) => {
                                                        const year = dates.getFullYear().toString().slice(-2);
                                                        const month = String(dates.getMonth() + 1).padStart(2, '0'); // Months are 0-based, so add 1 and pad with '0' if needed
                                                        const day = String(dates.getDate()).padStart(2, '0');
                                                        return (`${year}-${month}-${day}`)
                                                    },
                                                }
                                            ]}
                                            series={[
                                                {
                                                    id: "value",
                                                    color: "#5BAD6B",
                                                    data: Values,
                                                    // curve: "linear",
                                                    area: true,
                                                },
                                            ]}
                                            margin={{ left: 30, right: 10, top: 10, bottom: 20 }}
                                        />
                                    </CardBody>
                                </Card>
                            </Tab>
                        )
                    })
                }
            </Tabs>
        </div >
    )
}

const DownloadVr = () => {
    return (
        <div className="bg-white grow h-[280px] rounded-lg">

        </div>
    )
}
const Academic = () => {
    const [isSubmit, SetIsSubmit] = useState(false)
    const [Inputs, SetInputs] = useState<{ StDate: string, EdDate: string, Band: string }>();

    return (
        <div className={!isSubmit ? "w-full flex flex-col justify-center items-center gap-4"
            : "w-full flex justify-between items-center gap-4"}>
            <div className={!isSubmit ? "relative w-[98%] h-[600px] " : " ml-4 w-[98%] h-[600px] gap-4 flex"}>
                <div className="transition-all h-full grow ">
                    <Map_ />
                </div>
                <div className={!isSubmit ? "absolute  w-[100%] h-[70px] top-7 z-50 flex justify-center items-center transition-all"
                    : "h-full w-[65%] z-50 flex flex-col gap-4 transition-all"}>
                    {!isSubmit ?
                        <InputsBar SetIsSubmit={SetIsSubmit} SetInputs={SetInputs} isAcademic={true} />
                        :
                        <>
                            <InputButton SetIsSubmit={SetIsSubmit} isAcademic={true} SetInputs={SetInputs} />
                            <div className="grow w-full flex gap-4">
                                <div className="h-full grow rounded-lg bg-white"></div>
                                <div className="h-full grow rounded-lg bg-white"></div>
                                <div className="h-full grow rounded-lg bg-white"></div>
                            </div>
                            <div className=" flex gap-4 w-full   justify-e items-end ">
                                <TimeSeries />
                            </div>
                        </>
                    }
                </div>
            </div>

        </div>
    )
}

export default Academic