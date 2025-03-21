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
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
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
import circleCheck from "../../assets/circle-check.svg";
import bulb from "../../assets/bulb.svg";
import arrowR from "../../assets/arrow-right.svg";
import dots from "../../assets/dots.svg";
import pSf from "../../assets/player-skip-forward.svg";
import pSb from "../../assets/player-skip-back.svg";
import LiquidFillGauge from "react-liquid-gauge";
import * as echarts from "echarts";
import "echarts-liquidfill";
// import { IconAlarmAverage } from "@tabler/icons-react";
import rosette from "../../assets/rosette-discount-check.svg";
import Sirr from "../../assets/irrRecord.png";
import { Form, message } from "antd";
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

interface Event {
  key: number;
  Field: string;
  Date: string;
  Duration: string;
}

const IrrRecord = () => {
  const [form] = Form.useForm<{ value: string; date: string; unit: string }>();
  const [ok, SetOk] = useState(false);
  const Data = useAppSelector((state) => state.farmer);
  const { isOpen, onOpen, onClose } = useDisclosure();
  const { value, date, unit } = form.getFieldsValue();
  const [isConfirm, setIsConfirm] = useState(false);
  const [rows_, setRows] = useState<
    { date: string; name: string; amount: string }[]
  >([]);
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
      label: "Duration",
    },
  ];
  function createIrrRows(data) {
    return data.map((value, index) => ({
      key: index,
      Field: value.name,
      Date: value.date,
      Duration: value.amount,
    }));
  }
  useEffect(() => {
    api.get("farmer/irr").then((res) => {
      setRows(createIrrRows(res.data));
    });
  }, []);
  console.log(rows_);

  return (
    <AnimatePresence>
      <motion.div
        key={99}
        initial={{ opacity: 0, left: 50 }} // Starting state
        animate={{ opacity: 1, left: 0 }} // Animation to apply
        exit={{ opacity: 0, left: 50 }} // Animation for exit
        // transition={{ duration: 0.3 }}
        className="w-full absolute right-[10000px] z-30  my-2 inset-shadow-sm bg-[#ced6d4] shadow-2xl rounded-[20px] h-[98%] flex flex-col gap-3 justify-between p-2  overflow-hidden"
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
                  <p>Specify Irrigation Time or Volume</p>
                  <div className="flex w-full items-end gap-2">
                    <Form.Item name="value" className="w-[60%]">
                      <Input
                        labelPlacement="outside"
                        className=""
                        type="number"
                        placeholder="Enter value"
                        radius="full"
                        classNames={{
                          inputWrapper: "bg-white  hover:border-black",
                        }}
                      />
                    </Form.Item>
                    <Form.Item name="unit" className="w-[60%]">
                      <Select
                        className=""
                        classNames={{ trigger: "rounded-full" }}
                        label="Units"
                        placeholder="Choose a unit"
                        variant={"bordered"}
                        size="sm"
                      >
                        <SelectItem key={"L / h"}>{"Hour"}</SelectItem>
                        <SelectItem key={"m³"}>{"m³"}</SelectItem>
                      </Select>
                    </Form.Item>
                  </div>

                  <div className="flex gap-2 w-full ">
                    <Form.Item name="date" className="w-[70%]">
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
                        onClick={() => {
                          onOpen();
                          // const { value, date, unit } = form.getFieldsValue();

                          // api
                          //   .post("farmer/irr", {
                          //     value: value,
                          //     field_id: Data.currentField?.id,
                          //     date: date.toString(),
                          //     unity: unit,
                          //   })
                          //   .then((res) => {
                          //     console.log("ssssss");
                          //     message.open({
                          //       type: "success",
                          //       content:
                          //         "Your irrigation details have been recorded.",
                          //       style: {
                          //         height: "200px",
                          //         marginTop: "18vh",
                          //       },
                          //     });
                          //   });
                        }}
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
            <TableBody items={rows_}>
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
      <Modal backdrop={"blur"} isOpen={isOpen} onClose={onClose}>
        <ModalContent>
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1 font-bld">
                Confirm Irrigation Details
              </ModalHeader>
              {value && unit && date.toString() && !isConfirm && (
                <ModalBody className="text">
                  <p>Please review your input before confirming :</p>
                  <p>
                    <span className="font-bld">Value : </span>
                    {value}
                  </p>
                  <p>
                    <span className="font-bld">Unit</span> : {unit}
                  </p>
                  <p>
                    <span className="font-bld">Date :</span> {date.toString()}
                  </p>
                </ModalBody>
              )}
              {isConfirm && (
                <ModalBody className="text flexCenter">
                  <ReactSVG
                    className="w-[150px] h-[150px] fill-Green"
                    src={rosette}
                  />
                  <p>Irrigation details saved.</p>
                </ModalBody>
              )}
              <ModalFooter>
                <Button
                  className="rounded-full"
                  color="danger"
                  variant="light"
                  onPress={onClose}
                >
                  Close
                </Button>
                {!isConfirm && (
                  <Button
                    className="rounded-full text-white"
                    color="success"
                    onClick={() => {
                      setIsConfirm(true);
                      api
                        .post("farmer/irr", {
                          value: value,
                          field_id: Data.currentField?.id,
                          date: date.toString(),
                          unity: unit,
                        })
                        .then((res) => {
                          console.log("ssssss");
                          message.open({
                            type: "success",
                            content:
                              "Your irrigation details have been recorded.",
                            style: {
                              height: "200px",
                              marginTop: "18vh",
                            },
                          });
                        });
                    }}
                  >
                    Confirm
                  </Button>
                )}
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </AnimatePresence>
  );
};

const SideBar_ = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  const [opt, setOpt] = useState("");
  const nav = useNavigate();
  const [sideW, setSideW] = useState("310px");
  return (
    <div className="flex gap-2 bg-red-10 relative">
      <div className=" ml-5 mb-7 z-40 w-[40px] h-[40px] flex absolute bottom-0">
        <Button
          isIconOnly
          radius="full"
          size="md"
          className=" text-white bg-[#58726C]"
          onClick={() => {
            setSideW(sideW === "80px" ? "310px" : "80px");
          }}
        >
          <ReactSVG
            className={`${sideW === "80px" && "rotate-180"}`}
            src={arrowNarrowRight}
          />
        </Button>
      </div>
      {opt === "Irrigation Record" && (
        <div className="h-full w-[400px] absolute -left-[410px]   z-30">
          <Button
            isIconOnly
            radius="full"
            className="absolute z-40 bg-white top-[53px] border-2 borer-Green left-8"
            onPress={() => setOpt("")}
          >
            <ReactSVG src={arrowR} />
          </Button>
          <IrrRecord />
        </div>
      )}
      <motion.div
        key={99}
        initial={{ width: "310px" }}
        animate={{ width: sideW }}
        // exit={{ o }}
        className="overflow-hidden relative flex gap-2 p-2 h-[98%] mt-2  z-10 blurBg rounded-[20px]"
      >
        <div className="w-full h-full overflow-hidden bg-white p-2 rounded-[18px] font-Myfont font-smbld">
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
                setSideW("310px");
                nav("/farmer1");
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
                setSideW("310px");
                nav("/farmer1/weather");
              }}
            ></AccordionItem>
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
                setSideW("310px");
                dispatch(
                  updateFarmerInfo({
                    scrollTo: true,
                  })
                );
              }}
            ></AccordionItem>
            <AccordionItem
              startContent={
                <ReactSVG className="fill-[#58726C]" src={irrIcn} />
              }
              onPress={() => {
                setSideW("310px");
              }}
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
                  setSideW("310px");
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
                  setSideW("310px");
                  if (!opt || opt != "Irrigation Record")
                    nav("/farmer1/irrigationManagement");
                  else setOpt("");
                }}
              >
                Irrigation Tracker
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
      </motion.div>
    </div>
  );
};

interface LegendProps {
  colors: string[];
  min: number;
  max: number;
}

const Legend: React.FC<LegendProps> = ({ colors, min, max }) => {
  if (colors.length === 0) return null;

  const gradientStyle = {
    background: `linear-gradient(to right, ${colors.join(", ")})`,
  };

  return (
    <div className="flex w-[200px] flex-col justify-center items-center p-2 border rounded-lg bg-white shadow-md">
      <div className="w-full h-6 mb-2" style={gradientStyle}></div>
      <div className="flex justify-between w-full text-sm">
        <span>{min}</span>
        <span>{max}</span>
      </div>
    </div>
  );
};

const RasterInfo = () => {
  const Data = useAppSelector((state) => state.farmer);
  const dispatch = useAppDispatch();
  const data_: { min: number[]; mean: number[]; max: number[] } =
    Data.RasterKey === "Ks" ? Data?.RasterData?.Ks : Data?.RasterData?.rzsm_pr;
  console.log(data_);
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
              <div className="w-full flex flex-col gap-2 items-end">
                <Legend
                  colors={
                    Data.RasterKey === "Irrig"
                      ? ["#7DC7E6", "#0077A6", "#00008B"]
                      : ["#d7191c", "#f2db0c", "#0a640c"]
                  }
                  min={Data.RasterKey === "Irrig" ? 1 : 0}
                  max={Data.RasterKey === "Irrig" ? 30 :Data.RasterKey === "Ks" ? 1 : 100}
                />
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
                    <Button
                      isIconOnly
                      className="rounded-full h-7 w-7  bg-Green"
                    >
                      <ReactSVG className="text-white" src={pSb} />
                    </Button>
                    <Button
                      isIconOnly
                      className="rounded-full h-7 w-7  bg-Green"
                    >
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
                        <>
                          {Data.RasterKey === "Irrig" ? (
                            <MultiChart_
                              Data={{
                                datasets: [
                                  {
                                    data: Data.RasterData?.Irrig.mean,
                                    name: "irrigation",
                                    type: "bar",
                                    yAxisId: 0, // ET on Y-axis 1
                                    color: "#6fbcf2",
                                    forecastCount: 5,
                                  },
                                ],
                                yAxes: [{ id: 0, title: "Irrigation (mm)" }],
                              }}
                            />
                          ) : (
                            <MultiChart_
                              Data={{
                                datasets: [
                                  {
                                    data: data_.mean,
                                    name: "mean",
                                    type: "line",
                                    yAxisId: 0, // ET on Y-axis 1
                                    color: "#e7da30",
                                    forecastCount: 5,
                                  },
                                  {
                                    data: data_.min,
                                    name: "min",
                                    type: "line",
                                    yAxisId: 0, // ET on Y-axis 1
                                    color: "#e73930",
                                    forecastCount: 5,
                                  },
                                  {
                                    data: data_.max,
                                    name: "max",
                                    type: "line",
                                    yAxisId: 0, // ET on Y-axis 1
                                    color: "#64e730",
                                    forecastCount: 5,
                                  },
                                ],
                                yAxes: [
                                  {
                                    id: 0,
                                    title:
                                      Data.RasterKey === "Ks"
                                        ? "Ks"
                                        : "Soil Moisture",
                                  },
                                ],
                                DateRange: Data.DateRange,
                              }}
                            />
                          )}
                        </>
                      )}
                    </div>
                  </div>
                </motion.div>
              </div>
            )}
          </AnimatePresence>
        </>
      )}
    </div>
  );
};
function formatDate_(inputDate): string {
  // Create a Date object from the input string
  const date = new Date(inputDate);

  // Get the day of the week (e.g., "Mon", "Tue")
  const dayOfWeek = date.toLocaleString("en-US", { weekday: "short" });

  // Get the day of the month (e.g., "11")
  const dayOfMonth = date.getDate();

  // Combine into the desired format
  return `${dayOfWeek} ${dayOfMonth}`;
}
export const LastIrr = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  const [data_, setData] = useState<{
    latest: { date: string; duration: string };
    recommandation: { date: string; duration: string } | null;
  }>();
  useEffect(() => {
    api.get(`farmer/reco?field_id=${Data.currentField?.id}`).then((res) => {
      console.log(res.data);
      setData(res.data);
    });
  }, [Data.currentField?.id]);
  return (
    <div className="flexCenter h-[90px] grow blurBg z-20 rounded-full p-2 gap-2">
      {data_?.latest && (
        <>
          <div className="font-Myfont justify-center px-6 flex flex-col gap-2 w-[42%] h-full bg-[#ffffff] rounded-full">
            <p className="text-[14px] font-bld text-[#a3a3a3]">
              Previous Irrigation
            </p>
            <div className="flex gap-2 ">
              <div className="flexCenter gap-1">
                <ReactSVG className="stroke-[#7b7a7b]" src={calnIcn} />
                <p className="text-[14px] pt-1 font-bld">
                  {formatDate_(data_?.latest.date)}
                </p>
              </div>
              <div className="flexCenter gap-1">
                <ReactSVG className="stroke-[#7b7a7b]" src={alarmIcn} />
                <p className="text-[14px] pt-1 font-bld">
                  {data_.latest.duration}
                </p>
              </div>
            </div>
          </div>
          <div className="font-Myfont overflow-hidden flex items-center justify-between pl-6  gap-4 w-[42%] h-full bg-white rounded-full">
            <div className="flex flex-col  gap-2">
              <p className="text-[14px] font-bld">Next Irrigation</p>
              <div className="flex gap-2 ">
                {!data_.recommandation ? (
                  <p className="text-[14px] font-bld text-[#a3a3a3]">
                    No irrigation needed.
                  </p>
                ) : (
                  <>
                    <div className="flexCenter gap-1">
                      <ReactSVG className="stroke-[#7b7a7b]" src={calnIcn} />
                      <p className="text-[14px] pt-1 font-bld">Mon 23</p>
                    </div>
                    <div className="flexCenter gap-1">
                      <ReactSVG className="stroke-[#7b7a7b]" src={alarmIcn} />
                      <p className="text-[14px] pt-1 font-bld">4 H</p>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
          <div className="h-[70px] w-[70px] bg-white  rounded-full flexCenter">
            <div className="w-[50px] rounded-full h-[50px] flexCenter bg-gray-200 ">
              <Tooltip showArrow content={"View Raster"} placement="top">
                <button
                  onClick={() => {
                    dispatch(
                      updateFarmerInfo({
                        isRasterData: true,
                        RasterKey: "Irrig",
                        currentDate: Data.DateRange[0],
                      })
                    );
                  }}
                  className="bg-transparet "
                >
                  <ReactSVG src={eyeIcn} />
                </button>
              </Tooltip>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

const CurrentWeather = () => {
  const Data = useAppSelector((state) => state.farmer);
  const nav = useNavigate()
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
          onClick={() => {
            nav("/farmer1/weather")
          }}
        >
          <ReactSVG src={arrowNarrowRight} />
          {/* View more */}
        </Button>
      </Tooltip>
    </div>
  );
};
type WaterDropChartProps = {
  /** Water level as a percentage (0 to 100) */
  percentage: number;
};

function getColors(value) {
  if (value < 25) return "#34eb43";
  else if (value > 25 && value < 50) return "#eb8a36";
  else if (value > 60 && value < 80) return "#edd200";
  else if (value > 80 && value <= 100) return "#3ab552";
}

const WaterDrop: React.FC<WaterDropChartProps> = ({ percentage }) => {
  const chartRef = useRef<HTMLDivElement>(null);
  const chartInstanceRef = useRef<echarts.ECharts | null>(null);
  let color = getColors(percentage);

  // Initialize chart and set up resize listener on mount
  useEffect(() => {
    if (chartRef.current) {
      chartInstanceRef.current = echarts.init(chartRef.current);
    }

    const handleResize = () => {
      chartInstanceRef.current?.resize();
    };

    window.addEventListener("resize", handleResize);
    return () => {
      window.removeEventListener("resize", handleResize);
      chartInstanceRef.current?.dispose();
    };
  }, []);

  // Update chart when the percentage changes
  useEffect(() => {
    if (!chartInstanceRef.current) return;

    const option: echarts.EChartsOption = {
      series: [
        {
          type: "liquidFill",
          data: [
            {
              value: percentage / 100,
              itemStyle: {
                color: "#3783FF",
              },
            },
            {
              value: percentage / 100 - 0.15,
              itemStyle: {
                color: "#3783FF",
              },
            },
          ],
          center: ["50%", "50%"],
          radius: "80%",
          // Use your custom SVG shape (droplet icon) as the liquid fill shape.
          shape:
            "path://M7.502 19.423c2.602 2.105 6.395 2.105 8.996 0c2.602 -2.105 3.262 -5.708 1.566 -8.546l-4.89 -7.26c-.42 -.625 -1.287 -.803 -1.936 -.397a1.376 1.376 0 0 0 -.41 .397l-4.893 7.26c-1.695 2.838 -1.035 6.441 1.567 8.546z",
          backgroundStyle: {
            color: "#fff",
            borderColor: color,
            borderWidth: 1,
            shadowBlur: 10,
            shadowColor: color,
          },
          outline: {
            show: false,
          },
          label: {
            show: false,
            fontSize: 10,
            formatter: (param: any) => `${(param.value * 100).toFixed(0)}%`,
          },
          itemStyle: {
            color: ["#59b3f0", "#59b3f0"],
            shadowBlur: 50,
            shadowColor: "#cdd1d4",
          },
        },
      ],
    };

    chartInstanceRef.current.setOption(option);
  }, [percentage]);

  return <div ref={chartRef} style={{ width: "70px", height: "70px" }} />;
};
function getSoilMoistureMessage(value: number): string {
  if (value < 25) {
    return "Soil is critical. Act now!";
  } else if (value >= 25 && value <= 50) {
    return "Soil is dry.";
  } else if (value > 60 && value <= 80) {
    return "Soil is wet.";
  } else if (value > 80) {
    return "Soil is good.";
  }
}
const Dashboard_ = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  const ref = useRef(null);
  const nav = useNavigate();
  let ksValue;
  let rootValue;
  // console.log(Data.RasterData.rzsm_pr.mean)
  if (Data.RasterData) {
    rootValue =
      Data.RasterData.rzsm_pr.mean[Data.RasterData.rzsm_pr.mean.length - 7];
    ksValue = Data.RasterData!.Ks.mean[Data.DateRange.length - 2] * 100;
  }

  return (
    <div ref={ref} className="overflow-hidden  flex  gap-2 ">
      <div className="flex flex-col gap-2">
        {/* field navigation */}
        <div className="w-[600px] z-20 p-2 h-[70px] flexCenter gap-2 rounded-full blurBg ">
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
            content={!Data.DrawOption ? "Create New Season" : "Cancel"}
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
            <div className="flexCenter  flex-wrap z-20 gap-2 p-2 w-[600px] h-[140px] rounded-[30px] blurBg">
              <div className="w-full h-full flex bg-[#ffffff] justify-between rounded-[24px]">
                <div className="h-full flex justify-between items-center w-[49%] overflow-hidden  ">
                  {/* <div className="h-full w-[40px] bg-Red flexCenter">
                  <ReactSVG src={alertCircle} />
                </div> */}

                  <div className="flex h-full w-full flex-col justify-between items-start p-2 pl-4">
                    <div className="w-full flex justify-between">
                      <p className="font-bld text-[16px] text-[#353636]">
                        Root Zone Soil Moisture
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
                                    RasterKey: "rzsm_pr",
                                    currentDate: Data.DateRange[0],
                                  })
                                );
                              }}
                              className="bg-transparet  bg-ed-50"
                            >
                              <ReactSVG src={eyeIcn} />
                            </button>
                          </Tooltip>
                          {/* <Tooltip
                            showArrow
                            content={"View More"}
                            placement="top"
                          >
                            <button className="bg-transparet ">
                              <ReactSVG className="" src={dotsVertical} />
                            </button>
                          </Tooltip> */}
                        </ButtonGroup>
                      </div>
                    </div>
                    <Divider className="mb-3" />
                    <div className=" w-full h-[80%] flex items-start justify-between">
                      <div className="flex flex-col h-full justify-between ">
                        <p className="text-[12px] font-bld text-[#8f8f8f]">
                          {getSoilMoistureMessage(rootValue)}
                        </p>
                        <p
                          style={{ color: getColors(rootValue) }}
                          className={`font-bld text-[38px] items-center flex  
                          `}
                        >
                          {Data.RasterData ? (
                            <>
                              <CountUp end={rootValue} />
                              <span className="text-[16px] font-bld mt-3">
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
                      </div>
                      <WaterDrop percentage={rootValue} />
                    </div>
                  </div>
                </div>
                <Divider orientation="vertical" className="" />

                <div className="h-full flex justify-between items-center overflow-hidden  w-[49%]">
                  <div className="flex flex-col h-full p-2 pb-2  justify-between items-start w-full">
                    <div className="flex w-full justify-between">
                      <p className="font-bld text-[16px] text-[#353636]">
                        Water Stress
                      </p>
                      <div className="flex pr-1 ">
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
                          {/* <Tooltip
                            showArrow
                            content={"View More"}
                            placement="top"
                          >
                            <button className="bg-transparet ">
                              <ReactSVG className="" src={dotsVertical} />
                            </button>
                          </Tooltip> */}
                        </ButtonGroup>
                      </div>
                    </div>
                    <Divider className="mb-3" />
                    <div className=" w-full h-[80%] flex items-start justify-between">
                      <div className="flex flex-col h-full justify-between ">
                        <p className="text-[12px] font-bld text-[#8f8f8f]">
                          No stress, optimal growth.
                        </p>
                        <p
                          className={`font-bld text-[38px] items-center flex text-Green 
                          `}
                        >
                          {Data.RasterData ? (
                            <>
                              <CountUp end={ksValue - 100} />
                              <span className="text-[16px] font-bld mt-3">
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
                      </div>
                      <WaterDrop percentage={ksValue} />
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
  );
};

const Dashboard_v1 = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  const scRef = useRef(null);
  const [ET_0, setET_0] = useState();
  const { page } = useParams();
  const nav = useNavigate();
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

    api.get(`/api/weather?field_id=${Data.currentField?.id}`).then((res) => {
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
        <div className="w-full h-full relative  flex ">
          <div className="w-full h-full ml-2 absolute top-0 rounded-[10px] overflow-hidden">
            {!page && <AddField options_={Data.DrawOption} />}
          </div>
          <div className="font-Myfont grow m-2 ml-4 flex flex-col justify-between ">
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
                <Dashboard_ />
                {Data.isRasterData && <RasterInfo />}
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
