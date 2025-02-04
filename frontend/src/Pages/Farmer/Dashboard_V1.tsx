import React, { useEffect, useRef, useState } from "react";
import AddField, { drawnItems } from "./tools/addField";
import {
  Accordion,
  AccordionItem,
  Button,
  ButtonGroup,
  Checkbox,
  Chip,
  CircularProgress,
  DatePicker,
  DateRangePicker,
  Divider,
  getKeyValue,
  Input,
  Modal,
  Select,
  SelectItem,
  Slider,
  Table,
  TableBody,
  TableCell,
  TableColumn,
  TableHeader,
  TableRow,
  Tooltip,
  useDisclosure,
} from "@nextui-org/react";
import { updateFarmerInfo } from "../../Redux/Farmer/actions";
import { useAppDispatch, useAppSelector } from "../../Redux/hooks";
import api from "../../api/axios.js";
import { ReactSVG } from "react-svg";
import Flicking from "@egjs/react-flicking";

import createIcn from "../../assets/create.svg";
import anime from "animejs/lib/anime.es.js";
import locationIcn from "../../assets/locationIcn.svg";
import deleteIcn from "../../assets/deleteIcn.svg";
import polygonIcn from "../../assets/PolygonIcon.svg";
import uploadIcn from "../../assets/uploadIcn.svg";
import rasterIcn from "../../assets/rasterIcn.svg";
import indxIcn from "../../assets/indexIcon.svg";
import WeatherIcn from "../../assets/WeatherIcn.svg";
import dashboardIcn from "../../assets/dashboardIcn.svg";
import irrIcn from "../../assets/irrIcon.svg";
import tasksIcn from "../../assets/tasksIcn.svg";
import alarmIcn from "../../assets/alarm-average.svg";
import calnIcn from "../../assets/calendar-month.svg";
import cloudIcn from "../../assets/cloud-rain.svg";
import tmIcn from "../../assets/temperature.svg";
import windIcn from "../../assets/wind.svg";
import hmIcn from "../../assets/droplets.svg";
import alertCircle from "../../assets/alert-circle.svg";
import eyeIcn from "../../assets/eye.svg";
import ble from "../../assets/ble.png";
import dotsVertical from "../../assets/dots-vertical.svg";
import * as L from "leaflet";
import "leaflet-draw";
import { MapRef_ } from "./tools/addField";
import { DrawTools, SetupModal } from "./tools/modals.js";
import CountUp from "react-countup";
import { AnimatePresence, motion } from "framer-motion";
import { Chart_, MultiChart_ } from "./Aquacrop.js";
import PuffLoader from "react-spinners/PuffLoader.js";
import arrowNarrowRight from "../../assets/arrow-narrow-right.svg";
import circleCheck from "../../assets/circle-check.svg"
import bulb from "../../assets/bulb.svg";
import arrowR from "../../assets/arrow-right.svg";
import dots from "../../assets/dots.svg";
import pSf from "../../assets/player-skip-forward.svg";
import pSb from "../../assets/player-skip-back.svg";

// import { IconAlarmAverage } from "@tabler/icons-react";

import Sirr from "../../assets/irrRecord.png";
import { Form } from "antd";
import { IrrigationManagement } from "./tools/Irrigation.js";
import WeatherInfo from "./tools/WeatherInfo.js";
import { useNavigate, useParams } from "react-router-dom";
import SoilAndCrop from "./tools/SoilAndCrop.tsx";

export const DrawFieldTools = () => {
  const dispatch = useAppDispatch();
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const [isShapefile, setIsShapefile] = useState(false);
  const toolRef = useRef(null);
  const [setupButton, SetSetupBtn] = useState(false);
  let deleteMode = false;
  let polygonDrawer: L.Draw.Polygon;
  const polygonDrawerRef = useRef<L.Draw.Polygon>(); // Use ref to keep track of the polygon drawer

  function enablePoly() {
    polygonDrawerRef.current = new L.Draw.Polygon(MapRef_, {
      allowIntersection: false,
      repeatMode: false,
      shapeOptions: {
        color: !deleteMode ? "#F5D152" : "#fff",
        weight: 4,
        opacity: 0.7,
      },
      showArea: true,
      metric: false,
    });
    polygonDrawerRef.current.enable();
    MapRef_.on(L.Draw.Event.CREATED, function (event) {
      const layer = event.layer;

      // Add the polygon to drawnItems so it stays on the map
      drawnItems.addLayer(layer);

      // Handle the polygon data (e.g., convert to GeoJSON)
      const geoJson = JSON.stringify(layer.toGeoJSON());
      dispatch(
        updateFarmerInfo({
          Field: geoJson,
        })
      );

      // Optionally enable editing
      layer.editing.enable();

      // Disable the drawing tool after creation
      polygonDrawerRef.current.disable();
    });
  }

  useEffect(() => {
    anime({
      targets: toolRef.current,
      translateX: 100,
      delay: 50,
      easing: "spring(0, 100, 10, 0)",
    });
    anime({
      width: "200px",
      targets: ".CnStp",
      delay: 50,
    });
  }, []);

  function deleteLayers() {
    drawnItems.clearLayers();
  }

  const drawTools = [
    {
      icon: polygonIcn,
      info: "Draw Polygon",
    },

    {
      icon: uploadIcn,
      info: "Upload ShapeFile",
    },
    {
      icon: locationIcn,
      info: "Add Coordinates",
    },
    {
      icon: deleteIcn,
      info: "Delete layer",
    },
  ];

  return (
    <>
      {setupButton && (
        <div className="CnStp p-[4px] overflow-hidden transition-all font-Myfont self-end relative z-10 order-2  ">
          <Button
            onPress={onOpen}
            className="rounded-full font-bld  bg-[#4FC38F] text-white"
          >
            Continue Field Setup
          </Button>
        </div>
      )}
      <div
        ref={toolRef}
        className="relative left-[-100px] w-[60px] h-[200px] p-[4px] rounded-full justify-self-end  bg-white/50 backdrop-blur-sm border-[2px] border-white z-10"
      >
        <div className="bg-white w-full h-full rounded-full flex gap-4 flex-col items-center justify-center p-2">
          {drawTools.map((v) => {
            return (
              <>
                <Tooltip showArrow content={v.info} placement="right-start">
                  <Button
                    onPress={() => {
                      if (v.info === "Upload ShapeFile") {
                        setIsShapefile(true);
                        onOpen();
                      } else if (v.info === "Add Coordinates") {
                        setIsShapefile(false);
                        onOpen();
                      } else if (v.info === "Draw Polygon") {
                        enablePoly();
                      } else {
                        deleteLayers();
                      }
                    }}
                    isIconOnly
                    className="bg-transparent"
                  >
                    <ReactSVG className="fill-Red" src={v.icon} />
                  </Button>
                </Tooltip>
              </>
            );
          })}
        </div>

        <Modal
          className=""
          isOpen={isOpen}
          onOpenChange={onOpenChange}
          onClose={() => {
            // MapRef_.removeLayer(layer);
            dispatch(updateFarmerInfo({ DrawOption: false }));
            polygonDrawer.disable();
          }}
        >
          {isShapefile ? (
            <SetupModal isShapefile={true} isOpen_={isOpen} />
          ) : (
            <DrawTools />
          )}
        </Modal>
      </div>
    </>
  );
};

const IrrRecord = () => {
  const [form] = Form.useForm<{ name: string; age: number }>();
  const [ok, SetOk] = useState(false);
  const columns = [
    {
      key: "Field",
      label: "Filed Name",
    },
    {
      key: "Date",
      label: "Date",
    },
    {
      key: "Duration",
      label: "DURATION",
    },
  ];

  const rows = [
    {
      key: "1",
      Field: "Field name",
      Date: "2024-02-02",
      Duration: "2H",
    },
    {
      key: "2",
      Field: "Name",
      Date: "2024-02-06",
      Duration: "2H",
    },
    {
      key: "3",
      Field: "FiledName",
      Date: "2024-03-01",
      Duration: "2H",
    },
    {
      key: "4",
      Field: "FiledNAme",
      Date: "2024-03-24",
      Duration: "2H",
    },
    {
      key: "1",
      Field: "Field name",
      Date: "2024-02-02",
      Duration: "2H",
    },
    {
      key: "2",
      Field: "Name",
      Date: "2024-02-06",
      Duration: "2H",
    },
    {
      key: "3",
      Field: "FiledName",
      Date: "2024-03-01",
      Duration: "2H",
    },
    {
      key: "4",
      Field: "FiledNAme",
      Date: "2024-03-24",
      Duration: "2H",
    },
  ];
  return (
    <AnimatePresence>
      <motion.div
        key={99}
        initial={{ opacity: 0, width: "0px" }} // Starting state
        animate={{ opacity: 1, width: "400px" }} // Animation to apply
        exit={{ opacity: 0, width: "0px" }} // Animation for exit
        // transition={{ duration: 0.3 }}
        className="w-[200px] my-2 blurBg rounded-[20px] h-[98%] flex flex-col gap-3 justify-between p-2 z-40 overflow-hidden"
      >
        <div className="w-full relative bg-white  p-2 rounded-[16px]">
          <div className="flexCenter flex-col ">
            <img className="" src={Sirr} alt="" />
            {/* title and his dis */}
            <div className="p-2 flex flex-col gap-1">
              <p className="self-start font-bld text-[18px] ">
                Irrigation Record
              </p>
              <p className="text-[14px] ">
                Log irrigation amounts and dates to track your watering
                schedule.
              </p>
            </div>

            <div className="w-full p-3 mt-2 rounded-[16px] border-2 border-[#e5e5e5]">
              <div className="flex flex-col gap-2">
                <Chip
                  startContent={<ReactSVG className="ml-1" src={bulb} />}
                  variant="solid"
                  color="danger"
                  className="font-bld h-8 text-white"
                >
                  Irrigation Recommended
                </Chip>
                <p className="text-[16px]">
                  Irrigate on{" "}
                  <span className="font-bld">01-01-2024 for 4H</span>
                </p>
                <Checkbox
                  onChange={(e) => SetOk(e.target.checked)}
                  classNames={{
                    label: "text-[14px]",
                  }}
                  color="success"
                >
                  Confirm to procced
                </Checkbox>
              </div>
            </div>
            {/* Form */}

            {!ok && (
              <div className="w-full flex p-3 mt-2 border-2 border-[#e5e5e5] rounded-[16px]">
                <Form
                  form={form}
                  className="w-full"
                  layout="vertical"
                  autoComplete="off"
                >
                  <Form.Item>
                    <Input
                      labelPlacement="outside"
                      label="Specify the duration of irrigation"
                      className="w-full"
                      onChange={(e) => {
                        // dispatch(updateFarmerInfo({ fieldName: e.target.value }));
                      }}
                      type="number"
                      placeholder="Irrigation Duration"
                      radius="full"
                      // variant="bordered"
                      classNames={{
                        inputWrapper:
                          "bg-white border-white hover:border-black",
                      }}
                    />
                  </Form.Item>

                  <div className="flex gap-2 w-full ">
                    <Form.Item className="w-[70%]">
                      <DatePicker
                        labelPlacement="outside"
                        label="Enter the Irrigation date "
                        size="md"
                        className="w-"
                        radius="full"
                      />
                    </Form.Item>
                    <Form.Item className="w-[25%] flex items-end">
                      <Button
                        radius="full"
                        className="bg-Green text-white  font-smbld w-full"
                      >
                        Submit
                      </Button>
                    </Form.Item>
                  </div>
                </Form>
              </div>
            )}
          </div>
        </div>
        <div className="w-full grow rounded-[18px] bg-white overflow-hidden hover:overflow-y-scroll">
          <Table aria-label="Example table with dynamic content">
            <TableHeader columns={columns}>
              {(column) => (
                <TableColumn key={column.key}>{column.label}</TableColumn>
              )}
            </TableHeader>
            <TableBody items={rows}>
              {(item) => (
                <TableRow key={item.key}>
                  {(columnKey) => (
                    <TableCell>{getKeyValue(item, columnKey)}</TableCell>
                  )}
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
      </motion.div>
    </AnimatePresence>
  );
};

const SideBar_ = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  const [opt, setOpt] = useState("");
  const nav = useNavigate();
  return (
    <div className="flex gap-2">
      <div className="h-full relative z-30">
        {opt === "Irrigation Record" && (
          <>
            <Button
              isIconOnly
              radius="full"
              className="absolute z-40 bg-white top-[53px] border-2 borer-Green left-8"
              onPress={() => setOpt("")}
            >
              <ReactSVG src={arrowR} />
            </Button>
            <IrrRecord />
          </>
        )}
      </div>
      <div className="relative w-[310px] flex gap-2 p-2 h-[98%] mt-2  z-10 blurBg rounded-[20px]">
        <div className="w-full h-full bg-white p-2 rounded-[18px] font-Myfont font-smbld">
          <Accordion variant="light" className={"p-2"}>
            <AccordionItem
              hideIndicator
              isCompact
              startContent={<ReactSVG src={dashboardIcn} />}
              classNames={{
                titleWrapper: "drop-shadow-none text-[12px]",
                title: "text-[14px]",
              }}
              key="40"
              aria-label="Dashboard"
              title="Dashboard"
              onPress={() => {
                nav("/farmer1");
                // dispatch(
                //   updateFarmerInfo({
                //     Location : "Weather",
                //   })
                // );
              }}
            ></AccordionItem>
            <AccordionItem
              hideIndicator
              isCompact
              startContent={<ReactSVG src={WeatherIcn} />}
              classNames={{
                titleWrapper: "drop-shadow-none text-[12px]",
                title: "text-[14px]",
              }}
              key="4"
              aria-label="Weather Information"
              title="Weather Information"
              onPress={() => {
                nav("/farmer1/weather");
                // dispatch(
                //   updateFarmerInfo({
                //     Location : "Weather",
                //   })
                // );
              }}
            >
              {/* {defaultContent} */}
            </AccordionItem>
            <AccordionItem
              hideIndicator
              isCompact
              startContent={<ReactSVG src={indxIcn} />}
              classNames={{
                trigger: "",
                titleWrapper: " drop-shadow-none text-[12px]",
                title: "text-[14px]",
              }}
              key="1"
              aria-label="Soil & Crop Indicators"
              title="Soil & Crop Indicators"
              onPress={() => {
                dispatch(
                  updateFarmerInfo({
                    scrollTo: true,
                  })
                );
              }}
            >
              {/* {defaultContent} */}
            </AccordionItem>
            <AccordionItem
              startContent={
                <ReactSVG className="fill-[#58726C]" src={irrIcn} />
              }
              classNames={{
                titleWrapper: "drop-shadow-none text-[12px]",
                title: "text-[14px]",
              }}
              key="2"
              aria-label="Irrigation"
              title="Irrigation"
            >
              <Button
                startContent={
                  <ReactSVG className="text-gray-300" src={arrowNarrowRight} />
                }
                className="w-full justify-start bg-transparent text-gray-700"
                onPress={() => {
                  if (!opt || opt != "Irrigation Record")
                    setOpt("Irrigation Record");
                  else setOpt("");
                }}
              >
                Irrigation Record
              </Button>
              <Button
                startContent={
                  <ReactSVG className="text-gray-300" src={arrowNarrowRight} />
                }
                className="w-full justify-start bg-transparent text-gray-700"
                onPress={() => {
                  if (!opt || opt != "Irrigation Record")
                    nav("/farmer1/irrigationManagement");
                  // dispatch(
                  //   updateFarmerInfo({
                  //     Location: "Irrigation Management",
                  //   })
                  // );
                  else setOpt("");
                }}
              >
                Irrigation Management
              </Button>
              {/* {defaultContent} */}
            </AccordionItem>

            {/* <AccordionItem
              startContent={<ReactSVG src={tasksIcn} />}
              classNames={{
                titleWrapper: "drop-shadow-none text-[12px]",
                title: "text-[14px]",
              }}
              key="3"
              aria-label="Current Tasks"
              title="Current Tasks"
              >
              </AccordionItem> */}
          </Accordion>
        </div>
      </div>
    </div>
  );
};

const RasterInfo = () => {
  const Data = useAppSelector((state) => state.farmer);
  const dispatch = useAppDispatch();

  function getDateRange() {
    const start = new Date(Data.DateRange[0]);
    const end = new Date(Data.DateRange[Data.DateRange.length - 1]);
    const dateArray = [];

    while (start <= end) {
      // Format the date as "YYYY-MM-DD"
      const year = start.getFullYear();
      const month = String(start.getMonth() + 1).padStart(2, "0");
      const day = String(start.getDate()).padStart(2, "0");

      dateArray.push(`${year}-${month}-${day}`);

      // Move to the next day
      start.setDate(start.getDate() + 1);
    }

    return Data.DateRange;
  }

  useEffect(() => {
    // if (key) GetData();
    dispatch(
      updateFarmerInfo({
        DateRange: getDateRange(),
        currentDate: getDateRange()[0],
      })
    );
  }, []);
  return (
    <div className="flex flex-col z-20 gap-2 items-end">
      {!Data.DrawOption && (
        <>
          <div className="z-20 flex w-full gap-4 items-end"></div>
          <AnimatePresence>
            {Data.isRasterData && (
              <motion.div
                key={99}
                initial={{ opacity: 0, height: "0px" }} // Starting state
                animate={{ opacity: 1, height: "300px" }} // Animation to apply
                exit={{ opacity: 0, height: "0px" }} // Animation for exit
                transition={{ duration: 0.3 }}
                className="w-full h-0 rounded-[20px] gap-2  blurBg z-20 flexCenter flex-col p-2 overflow-hiden"
              >
                <div className="w-full bg-white rounded-full flexCenter gap-2  h-[60px] p-2">
                  <Button
                    onClick={() => {
                      dispatch(
                        updateFarmerInfo({
                          isRasterData: false,
                        })
                      );
                    }}
                    isIconOnly
                    className="rounded-full bg-Red"
                  >
                    <ReactSVG
                      className="fill-white rotate-90 text-white"
                      src={arrowR}
                    />
                  </Button>
                  <Button isIconOnly className="rounded-full h-7 w-7  bg-Green">
                    <ReactSVG className="text-white" src={pSb} />
                  </Button>
                  <Button isIconOnly className="rounded-full h-7 w-7  bg-Green">
                    <ReactSVG className="text-white" src={pSf} />
                  </Button>
                  <div className="w-full flexCenter px-4 max-h-[40px]">
                    <Slider
                      key={Data.DateRange[1]}
                      size="sm"
                      step={1}
                      color="success"
                      showTooltip
                      tooltipProps={{
                        content: Data.currentDate
                          ? Data.currentDate
                          : Data.DateRange[0],
                        color: "foreground",
                      }}
                      aria-label="vd"
                      // label="Temperature"
                      // showSteps={true}
                      maxValue={Data.DateRange.length - 1}
                      minValue={0}
                      defaultValue={Data.DateRange.indexOf(Data.currentDate)}
                      className="w-full"
                      disableThumbScale={true}
                      onChange={(e) => {
                        dispatch(
                          updateFarmerInfo({
                            currentDate: Data.DateRange[e as number],
                          })
                        );
                      }}
                    />
                  </div>
                </div>

                <div className="h-full w-full bg-white rounded-[20px] flex">
                  <div className="flex grow p-2 pt-6 pr-8">
                    {Data.RasterData && (
                      <MultiChart_
                        Data={{
                          datasets: [
                            {
                              data: Data.RasterData?.Ks.mean,
                              name: "mean",
                              type: "line",
                              yAxisId: 0, // ET on Y-axis 1
                              color: "#e7da30",
                            },
                            {
                              data: Data.RasterData?.Ks.min,
                              name: "min",
                              type: "line",
                              yAxisId: 0, // ET on Y-axis 1
                              color: "#e73930",
                            },
                            {
                              data: Data.RasterData?.Ks.max,
                              name: "max",
                              type: "line",
                              yAxisId: 0, // ET on Y-axis 1
                              color: "#64e730",
                            },
                          ],
                          yAxes: [{ id: 0, title: "Ks" }],
                          DateRange: Data.DateRange,
                        }}
                      />
                    )}
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </>
      )}
    </div>
  );
};

export const LastIrr = () => {
  const content = [
    {
      duration: {
        icon: <ReactSVG className="stroke-[#b0b9af]" src={alarmIcn} />,
        value: "2:30h",
      },
      date: {
        icon: <ReactSVG className="stroke-[#b0b9af]" src={calnIcn} />,
        value: "2024-01-01",
      },
    },
    {
      duration: {
        icon: <ReactSVG className="stroke-[#b0b9af]" src={alarmIcn} />,
        value: "2h",
      },
      date: {
        icon: <ReactSVG className="stroke-[#b0b9af]" src={calnIcn} />,
        value: "2024-01-02",
      },
    },
    {
      duration: {
        icon: <ReactSVG className="stroke-[#b0b9af]" src={alarmIcn} />,
        value: "1:30h",
      },
      date: {
        icon: <ReactSVG className="stroke-[#b0b9af]" src={calnIcn} />,
        value: "2024-01-03",
      },
    },
  ];

  return (
    <div className="flexCenter h-[90px] grow blurBg z-20 rounded-full p-2 gap-2">
      {/* <div className="font-Myfont p-2 flex flex-col gap-2 grow h-full bg-white rounded-full">

        {/* <div className="flex justify-between items-start pr-2">
          <Chip
            startContent={<ReactSVG src={irrIcn} />}
            variant="light"
            className="font-bld h-"
          >
            Recent Irrigations
          </Chip>
          <Button isIconOnly className="bg-transparent" size="sm">
            <ReactSVG src={dots} />
          </Button>
          {/* <p className="cursor-pointer m-0 p-0 font-bld font-">. . .</p> 
        </div> */}

      {/* <div className="w-[120px] h-[30px]"></div> */}
      {/* <div className="w-full flex gap-2">
        {content.map((val, key) => {
          return (
            <>
              <div
                key={key}
                className="bg-[#f8f8f8 rounded-md grow flex flex-col"
              >
                <Chip
                  startContent={val.date.icon}
                  variant="light"
                  className="font-bld h-[]"
                >
                  {val.date.value}
                </Chip>
                <Chip
                  startContent={val.duration.icon}
                  variant="light"
                  className="font- h-[]"
                >
                  Duration : {val.duration.value}
                </Chip>
              </div>
              {key != content.length - 1 && <Divider orientation="vertical" />}
            </>
          );
        })}
      </div> 
      </div> */}

      <div className="font-Myfont justify-center px-6 flex flex-col gap-2 w-[42%] h-full bg-[#ffffff] rounded-full">
        <p className="text-[14px] font-bld text-[#a3a3a3]">
          Previous Irrigation
        </p>
        <div className="flex gap-2 ">
          <div className="flexCenter gap-1">
            <ReactSVG className="stroke-[#7b7a7b]" src={calnIcn} />
            <p className="text-[14px] pt-1 font-bld">Mon 23</p>
          </div>
          <div className="flexCenter gap-1">
            <ReactSVG className="stroke-[#7b7a7b]" src={alarmIcn} />
            <p className="text-[14px] pt-1 font-bld">4 H</p>
          </div>
        </div>
      </div>
      <div className="font-Myfont justify-center px-6 flex flex-col gap-2 w-[42%] h-full bg-white rounded-full">
        <p className="text-[14px] font-bld">Next Irrigation</p>
        <div className="flex gap-2 ">
          <div className="flexCenter gap-1">
            <ReactSVG className="stroke-[#7b7a7b]" src={calnIcn} />
            <p className="text-[14px] pt-1 font-bld">Mon 23</p>
          </div>
          <div className="flexCenter gap-1">
            <ReactSVG className="stroke-[#7b7a7b]" src={alarmIcn} />
            <p className="text-[14px] pt-1 font-bld">4 H</p>
          </div>
        </div>
      </div>
      <div className="h-[70px] w-[70px] bg-white  rounded-full flexCenter">
        <Button
          isIconOnly
          radius="full"
          size="md"
          className=" text-white bg-Green"
        >
          <ReactSVG src={arrowNarrowRight} />
        </Button>
      </div>
    </div>
  );
};

const CurrentWeather = () => {
  const Data = useAppSelector((state) => state.farmer);

  const content = [
    {
      name: "Temperature",
      value: Data.currentWeather?.temperature,
      icon: tmIcn,
    },
    { name: "Rain", value: Data.currentWeather?.rain, icon: cloudIcn },
    {
      name: "Wind Speed",
      value: Data.currentWeather?.wind_speed,
      icon: windIcn,
    },
    { name: "Humidity", value: Data.currentWeather?.humidity, icon: hmIcn },
  ];
  return (
    <div className="w-full h-full p-2 flex gap-2">
      {content.map((val, key) => {
        const [value, unit] = (val.value ?? "")
          .trim()
          .replace(",", ".")
          .split(" ");
        return (
          <div className="bg-white h-full w-[90px] flex gap-2 px-2 justify-center items-center  rounded-full">
            <ReactSVG className="" src={val.icon} />
            <div className="font-bld">
              {/* <p className="text-[#58726C] text-[12px]">{val.name}</p> */}
              <div className="flex items-end gap-[4px]">
                <CountUp end={value} />
                <p className="text-[#878787] text-[12px] mb-[2px]">{unit}</p>
              </div>
            </div>
          </div>
        );
      })}

      <Tooltip showArrow content={"View More"} placement="bottom">
        <Button
          isIconOnly
          className="bg-[#4FC38F] h-full text-white font-bld min-w-[50px] rounded-full"
        >
          <ReactSVG src={arrowNarrowRight} />
          {/* View more */}
        </Button>
      </Tooltip>
    </div>
  );
};

const Dashboard_v1 = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  const ref = useRef(null);
  const scRef = useRef(null);
  const [ET_0, setET_0] = useState();
  const { page } = useParams();
  const nav = useNavigate();
  console.table(Data.RasterData);
  const generateAnnotationsData = (dateRanges: string[]) => {
    const ranges = [
      {
        y: 125,
        y2: 160,
        opacity: 0.5,
        borderColor: "#FF4500",
        fillColor: "#FFEEEE",
        label: { text: "Émergence" },
      },
      {
        y: 169,
        y2: 208,
        opacity: 0.5,
        borderColor: "#FF4500",
        fillColor: "#FFEECC",
        label: { text: "Développement foliaire" },
      },
      {
        y: 369,
        y2: 421,
        opacity: 0.5,
        borderColor: "#FFA500",
        fillColor: "#FFF5CC",
        label: { text: "tallage" },
      },
      {
        y: 592,
        y2: 659,
        opacity: 0.5,
        borderColor: "#FFD700",
        fillColor: "#FFFBCC",
        label: { text: "Allongement de la tige" },
      },
      {
        y: 807,
        y2: 901,
        opacity: 0.5,
        borderColor: "#ADFF2F",
        fillColor: "#F0FFCC",
        label: { text: "Floraison" },
      },
      {
        y: 1068,
        y2: 1174,
        opacity: 0.5,
        borderColor: "#32CD32",
        fillColor: "#E8FFCC",
        label: { text: "Remplissage des graines" },
      },
      {
        y: 1434,
        y2: 1556,
        opacity: 0.5,
        borderColor: "#000",
        fillColor: "#D0FFCC",
        label: { text: "Stade pâte" },
      },
      {
        y: 1538,
        y2: 1665,
        opacity: 0.5,
        borderColor: "#000",
        fillColor: "#C0FFCC",
        label: { text: "Maturité complète" },
      },
    ];

    return ranges.map((range, index) => {
      const startDate = new Date(dateRanges[index]).getTime();
      const endDate = dateRanges[index + 1]
        ? new Date(dateRanges[index + 1]).getTime()
        : new Date().getTime(); // Use current date if no next range
      return {
        x: startDate, // Horizontal range start
        x2: endDate, // Horizontal range end
        y: range.y, // Vertical range start
        y2: range.y2, // Vertical range end
        opacity: 0.5,
        borderColor: "#FF4500",
        fillColor: range.fillColor,
        label: {
          text: range.label,
          style: {
            color: "#000",
          },
        },
      };
    });
  };

  const annotationsData = generateAnnotationsData(Data.DateRange);
  // const annotationsData = [
  //   {
  //     y: 125,
  //     y2: 160,
  //     opacity: 0.5,
  //     borderColor: "#FF4500",
  //     fillColor: "#FFEEEE",
  //     label: { text: "Émergence" },
  //   },
  //   {
  //     y: 169,
  //     y2: 208,
  //     opacity: 0.5,
  //     borderColor: "#FF4500",
  //     fillColor: "#FFEECC",
  //     label: { text: "Développement foliaire" },
  //   },
  //   {
  //     y: 369,
  //     y2: 421,
  //     opacity: 0.5,
  //     borderColor: "#FFA500",
  //     fillColor: "#FFF5CC",
  //     label: { text: "tallage" },
  //   },
  //   {
  //     y: 592,
  //     y2: 659,
  //     opacity: 0.5,
  //     borderColor: "#FFD700",
  //     fillColor: "#FFFBCC",
  //     label: { text: "Allongement de la tige" },
  //   },
  //   {
  //     y: 807,
  //     y2: 901,
  //     opacity: 0.5,
  //     borderColor: "#ADFF2F",
  //     fillColor: "#F0FFCC",
  //     label: { text: "Floraison" },
  //   },
  //   {
  //     y: 1068,
  //     y2: 1174,
  //     opacity: 0.5,
  //     borderColor: "#32CD32",
  //     fillColor: "#E8FFCC",
  //     label: { text: "Remplissage des graines" },
  //   },
  //   {
  //     y: 1434,
  //     y2: 1556,
  //     opacity: 0.5,
  //     borderColor: "#000",
  //     fillColor: "#D0FFCC",
  //     label: { text: "Stade pâte" },
  //   },
  //   {
  //     y: 1538,
  //     y2: 1665,
  //     opacity: 0.5,
  //     borderColor: "#000",
  //     fillColor: "#C0FFCC",
  //     label: { text: "Maturité complète" },
  //   },
  // ];
  useEffect(() => {
    api
      .get(`/api/current_weather?field_id=${Data.currentField?.id}`)
      .then((res) => {
        dispatch(updateFarmerInfo({ currentWeather: res.data }));
      });

    api.get(`/api/fao_test?field_id=${Data.currentField?.id}`).then((res) => {
      console.log(res.data);
      dispatch(
        updateFarmerInfo({
          RasterData: res.data,
          DateRange: res.data.dates,
          currentDate: res.data.dates[0],
        })
      );
    });
    api
      .get(
        `api/gdd?field_id=${Data.currentField?.id}&start_date=2024-01-15&end_date=2024-05-30`
      )
      .then((res) => {
        dispatch(
          updateFarmerInfo({
            Gdd: res.data,
          })
        );
      });

    api
      .get("/api/weather?field_id=1&start_date=2024-01-15&end_date=2024-05-30")
      .then((res) => {
        setET_0(res.data.Et0);
      });

    api.get("/farmer/field").then((res) => {
      dispatch(updateFarmerInfo({ fieldInfo: res.data }));
    });

    if (!Data.fieldInfo)
      api.get("/farmer/field").then((res) => {
        dispatch(updateFarmerInfo({ fieldInfo: res.data }));
      });
  }, [Data.currentField, Data.DrawOption, Data.scrollTo]);

  function CheckLocation() {
    const condation = {
      irrigationManagement: true,
      weather: true,
    };
    if (condation[page]) return true;
    else return false;
  }

  const Pages = {
    irrigationManagement: <IrrigationManagement />,
    weather: <WeatherInfo />,
  };
  return (
    <>
      <div className="w-dvw pb-3 pr-4 h-svh absolute top-0 pt-[85px] font-Myfont">
        <div className="w-full h-full relative flex ">
          <div className="w-full h-full ml-2 absolute top-0 rounded-[10px] overflow-hidden">
            {!page && <AddField options_={Data.DrawOption} />}
          </div>
          <div className="font-Myfont grow  m-2 ml-4 flex flex-col justify-between ">
            <AnimatePresence>
              {CheckLocation() && (
                <motion.div
                  initial={{ opacity: 0 }} // Starting state
                  animate={{ opacity: 1 }} // Animation to apply
                  exit={{ opacity: 0 }} // Animation for exit
                  transition={{ duration: 0.3 }}
                  className="grow relative"
                >
                  {Pages[page]}
                </motion.div>
              )}
            </AnimatePresence>

            {!page && (
              <>
                <div ref={ref} className="overflow-hidden  flex  gap-2 ">
                  <div className="flex flex-col gap-2">
                    {/* field navigation */}
                    <div className="w-[550px] z-20 p-2 h-[70px] flexCenter gap-2 rounded-full blurBg ">
                      <Select
                        // defaultSelectedKeys={Data.currentField?.name}
                        size="sm"
                        radius={"full"}
                        label="Select field"
                        className="min-w-[260px] "
                        classNames={{
                          trigger: "bg-white",
                        }}
                        onChange={(e) => {
                          dispatch(
                            updateFarmerInfo({
                              currentField: Data.fieldInfo[e.target.value],
                            })
                          );
                        }}
                      >
                        {Data.fieldInfo.map((val, _) => {
                          return (
                            <SelectItem key={_} value={val.name}>
                              {val.name}
                            </SelectItem>
                          );
                        })}
                      </Select>
                      <Tooltip
                        showArrow
                        content={
                          !Data.DrawOption ? "Create New Season" : "Cancel"
                        }
                        placement="bottom"
                      >
                        <Button
                          onClick={() => {
                            if (Data.DrawOption) drawnItems.clearLayers();
                            nav("/farmersetup");
                            // dispatch(
                            //   updateFarmerInfo({ DrawOption: !Data.DrawOption })
                            // );
                          }}
                          size="lg"
                          className="rounded-full bg-white"
                          isIconOnly
                        >
                          {!Data.DrawOption ? (
                            <ReactSVG src={createIcn} />
                          ) : (
                            <ReactSVG className="fill-Red" src={deleteIcn} />
                          )}
                        </Button>
                      </Tooltip>
                    </div>

                    {!Data.DrawOption && (
                      <>
                        <div className="flexCenter  flex-wrap z-20 gap-2 p-2 w-[550px] h-[110px] rounded-[30px] blurBg">
                          <div className="rounded-[17px] bg-white h-[85px] flex justify-start items-center overflow-hidden  w-[260px]">
                            <div className="h-full w-[40px] bg-Red flexCenter">
                              <ReactSVG src={alertCircle} />
                            </div>
                            <div className="flex grow flex-col items-start pl-4">
                              <div className="w-full flex justify-between">
                                <p className="font-bld text-[14px] text-[#353636]">
                                  Root Zone Soil Moisture
                                </p>
                              </div>
                              <div className="h-[40px] w-full pr-2 gap-2 flex items-end justify-between">
                                <p className="font-bld text-[22px] items-center flex text-Red">
                                  <CircularProgress
                                    // label="Speed"
                                    size="sm"
                                    value={30}
                                    color="danger"
                                    classNames={{ svg: "w-6 h-6 " }}
                                    className="mr-2"
                                    // formatOptions={{ style: "unit", un }}
                                    // showValueLabel={true}
                                  />
                                  <CountUp end={30} />
                                  <span className="text-[16px] font-bld mt-1">
                                    %
                                  </span>
                                </p>

                                <div className="flex">
                                  <ButtonGroup>
                                    <Tooltip
                                      showArrow
                                      content={"View Raster"}
                                      placement="top"
                                    >
                                      <button className="bg-transparet  bg-ed-50">
                                        <ReactSVG src={eyeIcn} />
                                      </button>
                                    </Tooltip>
                                    <Tooltip
                                      showArrow
                                      content={"View More"}
                                      placement="top"
                                    >
                                      <button className="bg-transparet ">
                                        <ReactSVG
                                          className=""
                                          src={dotsVertical}
                                        />
                                      </button>
                                    </Tooltip>
                                  </ButtonGroup>
                                </div>
                              </div>
                            </div>
                          </div>

                          <div className="rounded-[17px] bg-white h-[85px] flex justify-start items-center overflow-hidden  w-[260px]">
                            <div
                              className={`h-full w-[40px] flexCenter  ${
                                Data.RasterData?.Ks > 50 ? "bg-Green" : "bg-Green"
                              }`}
                            >
                              {/* <ReactSVG src={alertCircle} /> */}

                              <ReactSVG src={circleCheck} />
                            </div>
                            <div className="flex flex-col items-start pl-4 w-full">
                              <p className="font-bld text-[14px] text-[#353636]">
                                Water Stress
                              </p>
                              <div className="h-[40px] w-full pr-2 gap-2 flex items-end justify-between">
                                <p
                                  className={`font-bld text-[22px] items-center flex text-Green
                                    `}
                                >
                                  {Data.RasterData ? (
                                    <>
                                      <CircularProgress
                                        // label="Speed"
                                        size="sm"
                                        value={
                                          Data.RasterData!.Ks.mean[
                                            Data.DateRange.length - 2
                                          ] * 100
                                        }
                                        color="success"
                                        classNames={{ svg: "w-6 h-6 " }}
                                        className="mr-2"
                                        // formatOptions={{ style: "unit", un }}
                                        // showValueLabel={true}
                                      />
                                      <CountUp
                                      
                                        end={
                                          Data.RasterData!.Ks.mean[
                                            Data.DateRange.length - 2
                                          ] * 100
                                        }
                                      />
                                      <span className="text-[16px] font-bld mt-1">
                                        %
                                      </span>
                                    </>
                                  ) : (
                                    <PuffLoader
                                      size={35}
                                      color="#4598ea"
                                      className="fill-[#fff]"
                                    />
                                  )}
                                </p>
                                <div className="flex">
                                  <ButtonGroup>
                                    <Tooltip
                                      showArrow
                                      content={"View Raster"}
                                      placement="top"
                                    >
                                      <button
                                        onClick={() => {
                                          dispatch(
                                            updateFarmerInfo({
                                              isRasterData: true,
                                              RasterKey: "Ks",
                                              currentDate: Data.DateRange[0],
                                            })
                                          );
                                        }}
                                        className="bg-transparet  bg-ed-50"
                                      >
                                        <ReactSVG src={eyeIcn} />
                                      </button>
                                    </Tooltip>
                                    <Tooltip
                                      showArrow
                                      content={"View More"}
                                      placement="top"
                                    >
                                      <button className="bg-transparet ">
                                        <ReactSVG
                                          className=""
                                          src={dotsVertical}
                                        />
                                      </button>
                                    </Tooltip>
                                  </ButtonGroup>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                        {/* Indicators */}
                        <LastIrr />
                      </>
                    )}
                  </div>
                  {!Data.DrawOption && (
                    <div className="w-[450px] flexCenter blurBg h-[70px] rounded-full z-50 self-start">
                      <CurrentWeather />
                    </div>
                  )}
                </div>
                <RasterInfo />
              </>
            )}
          </div>
          {!Data.DrawOption && <SideBar_ />}
        </div>
        <SoilAndCrop />
      </div>
    </>
  );
};

export default Dashboard_v1;
