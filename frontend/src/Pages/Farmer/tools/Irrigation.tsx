import { Button, Select, SelectItem, Image } from "@nextui-org/react";
import { useAppDispatch, useAppSelector } from "../../../Redux/hooks";
import { updateFarmerInfo } from "../../../Redux/Farmer/actions";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import "./style.css";
import drop from "../../../assets/irrIcon.svg";
import { ReactSVG } from "react-svg";
import bg from "../../../assets/bg.jpg";
import cloudIcn from "../../../assets/cloud-rain.svg";
import alarmIcn from "../../../assets/alarm-average.svg";
import calnIcn from "../../../assets/calendar-month.svg";
import hstIcn from "../../../assets/history.svg";
import { format } from "date-fns";
import api from "../../../api/axios.js";
import { ArrowLeftIcon } from "evergreen-ui";
// import { BarChart } from "@mui/x-charts/BarChart";
import ReactApexCharts from "react-apexcharts";
import { ApexOptions } from "apexcharts";
import AddField from "./addField";
import { useEffect, useState } from "react";
import { MultiChart_ } from "../Aquacrop";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const LastIrr = () => {
  return (
    <div className="flex f blurBg p-2  w-full gap-2 rounded-full">
      <div className="font-Myfont justify-center px-8 py-2 flex flex-col gap-2 w-full bg-[#628f73a2] rounded-full">
        <p className="text-[12px]  font-bld text-[#ffffff]">
          Previous Irrigation
        </p>
        <div className="flex gap-2 ">
          <div className="flexCenter gap-1">
            <ReactSVG className="stroke-[#ffffff]" src={calnIcn} />
            <p className="text-[12px] text-white pt-1 font-bld">Mon 23</p>
          </div>
          <div className="flexCenter gap-1">
            <ReactSVG className="stroke-[#ffffff]" src={alarmIcn} />
            <p className="text-[12px] text-white pt-1 font-bld">4 H</p>
          </div>
        </div>
      </div>
      <div className="font-Myfont justify-center px-8 py-2 flex flex-col gap-2 w-full  bg-white rounded-full">
        <p className="text-[12px] font-bld">Next Irrigation</p>
        <div className="flex gap-2 ">
          <div className="flexCenter gap-1">
            <ReactSVG className="stroke-[#7b7a7b]" src={calnIcn} />
            <p className="text-[12px] pt-1 font-bld">Mon 23</p>
          </div>
          <div className="flexCenter gap-1">
            <ReactSVG className="stroke-[#7b7a7b]" src={alarmIcn} />
            <p className="text-[12px] pt-1 font-bld">4 H</p>
          </div>
        </div>
      </div>
    </div>
  );
};

const IrrHero = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  return (
    <div className="w-[40%] flex flex-col gap-2 justify-between h-full ">
      <div className="w-full flex flex-col gap-2 overflow-hidden p-2 relative rounded-[20px] grow min-h-[140px]">
        <div>
          <div className="flex items-center p-2 gap-4">
            <div className="border-2 rounded-full p-2 z-20">
              <Button
                onPress={() => {
                  dispatch(updateFarmerInfo({ Location: "Home" }));
                }}
                isIconOnly
                radius="full"
                className="bg-Green"
              >
                <ArrowLeftIcon color="#fff" />
              </Button>
            </div>
            <p className="text-[35px] font-bld text-white z-20">
              Irrigation Management
            </p>
            <Image
              isZoomed
              width={"100%"}
              alt="bg"
              src={bg}
              classNames={{
                wrapper: "absolute left-0 -top-[120px]",
              }}
              // className="w-full absolute top-0 left-0 z-10"
            />
            {/* <img
              src={bg}
              className="absolute w-full transform -scale-x-100 left-0 -top-[120px] z-10 "
              alt=""
            /> */}
          </div>
        </div>
      </div>
      <div className="flex flex-col gap-2 items-center relative">
        <div className="w-full h-full flexCenter rounded-full blurB p-">
          <Select
            // defaultSelectedKeys={Data.currentField?.name}
            size="sm"
            radius={"full"}
            label="Select field"
            className="min-w-[60px] "
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
        </div>
        {/* <LastIrr /> */}
      </div>
    </div>
  );
};

const SimpleBarChart = ({ dates, data }) => {
  const chartData = dates.map((date, index) => ({
    day: date,
    value: data[index],
  }));

  return (
    <ResponsiveContainer width="100%">
      <BarChart data={chartData}>
        <CartesianGrid stroke="#4d7186" strokeDasharray="1 1" />
        <XAxis
          axisLine={false}
          dataKey="day"
          tick={{ fill: "#fff", fontSize: 10 }}
          tickFormatter={(dates) => format(new Date(dates), "dd MMM")} // Formats as "01 Jan"
        />
        <YAxis
          tick={{ fill: "white" }}
          axisLine={false}
          label={{
            value: "Irrigation (mm)",
            angle: -90,
            style: {
              marginLeft: "10px", // Margin on the left
              marginRight: "10px",
              fontWeight: "bold",
              fontSize: 14,
              fill: "#d8d8d8",
            },
            dx: -20,
          }}
        />
        <Tooltip formatter={(value) => value.toFixed(2)} />

        <Bar dataKey="value" fill="#6fbcf2" />
      </BarChart>
    </ResponsiveContainer>
  );
};

const Irrhistory = () => {
  const Data = useAppSelector((state) => state.farmer);
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(
      updateFarmerInfo({
        isRasterData: true,
        RasterKey: "Irrig",
        currentDate: "2024-04-25",
      })
    );
  }, []);
  return (
    <div className="font-Myfont w-[60%] rounded-[20px] h-full flex gap-4 bg-[#eef8ff blurBg p-2">
      <div className="bg-[#0e4666] w-full p-1  h-full rounded-[16px]">
        <div className="pl-3 pt-4 ">
          <p className="font-bld text-[#ffffff]">Irrigation History Tracker</p>
          <p className="text-[12px] font-md text-[#ffffff]">
            Track and analyze your irrigation records with this interactive
            chart.
          </p>
        </div>
        <div className="h-[230px] p-2">
          <SimpleBarChart
            data={Data.RasterData?.Irrig.mean}
            dates={Data.DateRange}
          />
        </div>
      </div>
      {/* <div className="rounded-[16px]  flexCenter flex-col gap-1 overflow-hidden pt-4  grow">
        <p className="font-bld text-[#0e4666]">Irrigation Heatmap Viewer</p>
        <AddField options_={Data.DrawOption} />
      </div> */}
    </div>
  );
};

interface Event {
  id: number;
  className: string;
  title: string;
  start: string;
  extendedProps: {
    dis: string;
    icon: JSX.Element;
    info: string;
  };
}

function createIrrigationEvents(
  irrigationValues: string[],
  dates: string[]
): Event[] {
  return irrigationValues.map((value, index) => {
   // Check if it's one of the last 7 values
      return {
        id: index + "aa",
        className: "event-cln",
        title: "",
        start: dates[index],
        extendedProps: {
          dis: "Irrigation Record", // Set dis based on the condition
          icon: <ReactSVG className="fill-white" src={drop} />,
          info: `Duration : ${value}`,
        },
      };
   
  });
}

function createRainEvents(RainValues: number[], dates: string[]): Event[] {
  return RainValues.map((value, index) => {
    if (value)
      return {
        id: index + 1,
        className: "event-cln",
        title: "test",
        start: dates[index],
        extendedProps: {
          dis: "", // Set dis based on the condition
          icon: <ReactSVG className="fill-white" src={cloudIcn} />,
          info: `${value.toFixed(2)} mm`,
        },
      };
    else return {};
  });
}

export const IrrigationManagement = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  const [irrEv, setIrrEV] = useState<{ duration: string[]; dates: string[] }>(
    null
  );
  let IrrEvents: Event[];
  if (irrEv) IrrEvents = createIrrigationEvents(irrEv.duration, irrEv.dates);
  const RainEvent = createRainEvents(
    Data.RasterData?.Rain.mean,
    Data.DateRange
  );
  useEffect(() => {
    api.get(`farmer/irr?field_id=${Data.currentField?.id}`).then((res) => {
      console.log(res.data)
      setIrrEV(res.data);
    });
  }, []);
  return (
    <div className="z-30 flex flex-col w-full h-full gap-5">
      <div className="w-full flexCenter gap-5">
        <IrrHero />
        <Irrhistory />
      </div>

      <div className="w-full flex gap-5  grow rounded-[20px] lurBg p-2 font-Myfont">
        {/* <div className="rounded-[20px] w-[20%] bg-white"></div> */}
        <div className="rounded-[20px] w-full bg-white p-4">
          {IrrEvents && (
            <FullCalendar
              events={[
                ...IrrEvents,
                ...RainEvent,
                // {
                //   id: 1,
                //   className: "event-cln",
                //   title: "test",
                //   start: "2024-11-22",
                //   extendedProps: {
                //     dis: "Irrigation Reminder",
                //     icon: <ReactSVG className="fill-white" src={drop} />,
                //     info: "Duration : 3H",
                //   },
                // },
                // {
                //   id: 2,
                //   title: "Irrigation Reminder",
                //   start: "2024-11-11",
                //   className: "event-cln",
                //   extendedProps: {
                //     dis: "Irrigation Reminder",
                //     icon: <ReactSVG className="fill-white" src={drop} />,
                //     info: "Duration : 3H",
                //   },
                // },
                // {
                //   id: 3,
                //   title: "Irrigation Reminder",
                //   start: "2024-11-19",
                //   className: "event-cln",
                //   extendedProps: {
                //     dis: "Irrigation Reminder",
                //     icon: <ReactSVG className="fill-white" src={drop} />,
                //     info: "Duration : 3H",
                //   },
                // },
                // {
                //   id: 4,
                //   title: "Irrigation Reminder",
                //   start: "2025-02-07",
                //   className: "event-cln",
                //   extendedProps: {
                //     dis: "",
                //     icon: <ReactSVG className="fill-white" src={cloudIcn} />,
                //     info: "7 mm",
                //   },
                // },
                // {
                //   id: 5,
                //   title: "Irrigation Reminder",
                //   start: "2024-11-06",
                //   className: "event-cln",
                //   extendedProps: {
                //     dis: "",
                //     icon: <ReactSVG className="fill-white" src={cloudIcn} />,
                //     info: "5 mm",
                //   },
                // },
              ]}
              plugins={[dayGridPlugin]}
              height={"100%"}
              initialView="dayGridMonth"
              themeSystem="bootstrap4"
              eventContent={(event) => {
                const style = !event.event.extendedProps.dis
                  ? " bg-[#115780] p-2 px-2 max-w-[110px] m-1 flex justify-center item-center"
                  : "bg-[#62c6ff] m-1 p-1";
                return (
                  <div
                    className={`flex items-center min-h-[30px] rounded-full gap-2 ${style} border-none`}
                  >
                    <span>{event.event.extendedProps.icon}</span>
                    <div className="flex flex-col">
                      <span className="font-Myfont font-bld ">
                        {event.event.extendedProps.dis}
                      </span>
                      <span className="text-[12px] font-bld text-[#c9ebff]">
                        {event.event.extendedProps.info}
                      </span>
                    </div>
                  </div>
                );
              }}
            />
          )}
        </div>
      </div>
    </div>
  );
};
