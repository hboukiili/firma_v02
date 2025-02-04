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

import { ArrowLeftIcon } from "evergreen-ui";
import { BarChart } from "@mui/x-charts/BarChart";
import ReactApexCharts from "react-apexcharts";
import { ApexOptions } from "apexcharts";
import AddField from "./addField";
import { useEffect } from "react";

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
                wrapper : "absolute left-0 -top-[120px]"
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

const IrrChart = () => {
  const Data = useAppSelector((state) => state.farmer);

  function ChartData() {
    let data = Data.RasterData?.Irrig.mean
      .map((val, key) => {
        if (val) {
          return { dates: Data.DateRange[key], series: val };
        } else return null;
      })
      .filter((item) => item !== null);

    return data;
  }
  const dates = ChartData()?.map((v) => v.dates);
  const series = ChartData()?.map((v) => v.series);

  const opt: ApexOptions = {
    chart: {
      toolbar: { show: false },
      height: 350,
      zoom: false,
      type: "bar",
      animations: {
        enabled: false,
      },
    },
   
    colors: ["#fff"],
    plotOptions: {
      bar: {
        borderRadius: 2,
        dataLabels: {
          position: "top", // top, center, bottom
        },
      },
    },
    xaxis: {
      categories: dates,
      type: "category",
      labels: {
        show: false,
        maxHeight: 16,
      },
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
    },
    grid: {
      show: false,
    },
    
    forecastDataPoints: {
      count: 14
    },
    annotations : {
      xaxis: [{
        // x : new Date("2024-04-22").getTime(),
        x: 440,
        strokeDashArray: 0,
        borderColor: '#775DD0',
        label: {
          borderColor: '#775DD0',
          style: {
            color: '#fff',
            background: '#775DD0',
          },
          text: 'Forcast',
        }
      },
    ]
    },
    yaxis: {
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: true,
      },
      labels: {
        maxWidth: 30,

        show: true,
        formatter: (value: number) => value.toFixed(2),
        style: { colors: "#fff", fontSize: "9px" },
      },
    },
  };
  console.log(dates)
  return (
    <div className="h-full irr">
      <ReactApexCharts
        width="100%"
        height="100%"
        options={opt}
        series={[
          {
            type: "bar",
            name: "irrigation",
            data: series,
          },
        ]}
      />
    </div>
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
        <div className="h-[230px]">
          <IrrChart />
        </div>
      </div>
      {/* <div className="rounded-[16px]  flexCenter flex-col gap-1 overflow-hidden pt-4  grow">
        <p className="font-bld text-[#0e4666]">Irrigation Heatmap Viewer</p>
        <AddField options_={Data.DrawOption} />
      </div> */}
    </div>
  );
};

export const IrrigationManagement = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  return (
    <div className="z-30 flex flex-col w-full h-full gap-5">
      <div className="w-full flexCenter gap-5">
        <IrrHero />
        <Irrhistory />
      </div>

      <div className="w-full flex gap-5  grow rounded-[20px] lurBg p-2 font-Myfont">
        {/* <div className="rounded-[20px] w-[20%] bg-white"></div> */}
        <div className="rounded-[20px] w-full bg-white p-4">
          <FullCalendar
            events={[
              {
                id: 1,
                className: "event-cln",
                title: "test",
                start: "2024-11-22",
                extendedProps: {
                  dis: "Irrigation Reminder",
                  icon: <ReactSVG className="fill-white" src={drop} />,
                  info: "Duration : 3H",
                },
              },
              {
                id: 2,
                title: "Irrigation Reminder",
                start: "2024-11-11",
                className: "event-cln",
                extendedProps: {
                  dis: "Irrigation Reminder",
                  icon: <ReactSVG className="fill-white" src={drop} />,
                  info: "Duration : 3H",
                },
              },
              {
                id: 3,
                title: "Irrigation Reminder",
                start: "2024-11-19",
                className: "event-cln",
                extendedProps: {
                  dis: "Irrigation Reminder",
                  icon: <ReactSVG className="fill-white" src={drop} />,
                  info: "Duration : 3H",
                },
              },
              {
                id: 4,
                title: "Irrigation Reminder",
                start: "2024-11-07",
                className: "event-cln",
                extendedProps: {
                  dis: "",
                  icon: <ReactSVG className="fill-white" src={cloudIcn} />,
                  info: "7 mm",
                },
              },
              {
                id: 5,
                title: "Irrigation Reminder",
                start: "2024-11-06",
                className: "event-cln",
                extendedProps: {
                  dis: "",
                  icon: <ReactSVG className="fill-white" src={cloudIcn} />,
                  info: "5 mm",
                },
              },
            ]}
            plugins={[dayGridPlugin]}
            height={"100%"}
            initialView="dayGridMonth"
            themeSystem="bootstrap4"
            eventContent={(event) => {
              const style = !event.event.extendedProps.dis
                ? " bg-[#115780] p-1 max-w-[100px] m-1"
                : "bg-[#62c6ff] m-1";
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
        </div>
      </div>
    </div>
  );
};
