import React, { useEffect, useState } from "react";
import AddField from "./tools/addField";
import { Button, Select, SelectItem } from "@nextui-org/react";
import fllsc from "../../assets/fullScreen.svg";
import { ReactSVG } from "react-svg";
import moment from "moment";
import "./tools/style.css";
import CropPie from "../Components/Dashboard/CropPie";
import { ResponsiveLine } from "@nivo/line";
import sunIcon from "../../assets/sun.svg";
import dropIcon from "../../assets/drop.svg";
import windIcon from "../../assets/wind.svg";
import prchIcon from "../../assets/prch.svg";
import Chart from "react-apexcharts";
import ReactApexCharts from "react-apexcharts";
import { ResponsiveCalendar } from "@nivo/calendar";
import api from "../../api/axios.js";
import { useAppDispatch, useAppSelector } from "../../Redux/hooks";
import { updateFarmerInfo } from "../../Redux/Farmer/actions";

const tooltip = ({ point }) => {
  return (
    <div
      className="justify-center items-center font-Myfont gap-2 rounded-md overflow-hidden"
      style={{
        background: "white",
        // width:"100px",
        borderRadius: "5px",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div className="font-bld w-full bg-Green text-white p-2 flex justify-center">
        {point.data.y.toString()}
      </div>
      {/* <div className="p-2 text-[14px]">{point.data.x.toString()}</div> */}
    </div>
  );
};

export  function getDateRange(startDateStr: string, endDateStr: string) {
  const startDate = moment(startDateStr, "DD-MM-YYYY");
  const endDate = moment(endDateStr, "DD-MM-YYYY");

  // Create an empty array to store the date range
  const dateRange = [];

  // Iterate through the dates using a loop
  let current = startDate.clone(); // Clone to avoid modifying startDate

  while (current.isSameOrBefore(endDate)) {
    // Create a new Date object from the current Moment.js date
    const dateObject = new Date(current.toDate());
    // Add the date object to the array
    dateRange.push(dateObject);
    // Increment current date by 1 day
    current.add(1, "days");
  }
  return dateRange;
}

const data = [
  {
    id: "japan",
    data: [
      { x: "24-01-01", y: 215 },
      { x: "24-01-02", y: 212 },
      { x: "24-01-03", y: 169 },
      { x: "24-01-04", y: 148 },
      { x: "24-01-05", y: 72 },
      { x: "24-01-06", y: 123 },
      { x: "24-01-07", y: 12 },
      { x: "24-01-08", y: 287 },
      { x: "24-01-09", y: 253 },
      { x: "24-01-10", y: 70 },
      { x: "24-01-11", y: 178 },
      { x: "24-01-12", y: 47 },
      { x: "24-01-13", y: 215 },
      { x: "24-01-14", y: 212 },
      { x: "24-01-15", y: 169 },
      { x: "24-01-16", y: 148 },
      { x: "24-01-17", y: 72 },
      { x: "24-01-18", y: 123 },
      { x: "24-01-19", y: 12 },
      { x: "24-01-20", y: 287 },
      { x: "24-01-21", y: 253 },
      { x: "24-01-22", y: 70 },
      { x: "24-01-23", y: 178 },
      { x: "24-01-24", y: 47 },
      { x: "24-01-25", y: 215 },
      { x: "24-01-26", y: 212 },
      { x: "24-01-27", y: 169 },
      { x: "24-01-28", y: 148 },
      { x: "24-01-29", y: 72 },
      { x: "24-01-30", y: 123 },
      { x: "24-01-31", y: 12 },
      { x: "24-02-01", y: 287 },
    ],
  },
];
const ResponsivChart_ = () => {
  return (
    <ResponsiveLine
      tooltip={tooltip}
      data={data}
      margin={{ top: 40, right: 10, bottom: 50, left: 10 }}
      xScale={{ type: "point" }}
      yScale={{
        type: "linear",
        min: "auto",
        max: "auto",
        stacked: true,
        reverse: false,
      }}
      yFormat=" >-.2f"
      curve="linear"
      axisTop={null}
      axisRight={null}
      axisBottom={null}
      axisLeft={null}
      // axisBottom={{
      //   tickSize: 5,
      //   tickPadding: 5,
      //   tickRotation: 0,
      //   legend: "transportation",
      //   legendOffset: 36,
      //   legendPosition: "middle",
      //   truncateTickAt: 0,
      // }}
      // axisLeft={{
      //   tickSize: 8,
      //   tickPadding: 6,
      //   tickRotation: 0,
      //   legend: "count",
      //   legendOffset: -45,
      //   legendPosition: "middle",
      //   truncateTickAt: 0,
      // }}

      colors={"#1E6F5C"}
      enableGridX={false}
      enableGridY={false}
      enablePoints={false}
      pointSize={10}
      pointColor={{ theme: "background" }}
      pointBorderWidth={2}
      pointBorderColor={{ from: "serieColor" }}
      pointLabel="data.yFormatted"
      pointLabelYOffset={-12}
      enableArea={true}
      areaOpacity={0.3}
      enableTouchCrosshair={true}
      useMesh={true}
      legends={[]}
    />
  );
};

export const ResponsiveLine_ = (prop: { color: string }) => {
  return (
    <ResponsiveLine
      data={data}
      tooltip={tooltip}
      margin={{ top: 5, right: 0, bottom: 5, left: 0 }}
      yFormat=" >-.2f"
      curve="cardinal"
      axisTop={null}
      axisRight={null}
      axisBottom={null}
      axisLeft={null}
      enableGridX={false}
      enableGridY={false}
      lineWidth={2}
      enablePoints={false}
      pointSize={10}
      pointBorderWidth={2}
      colors={prop.color}
      pointBorderColor={{ from: "serieColor" }}
      pointLabel="data.yFormatted"
      pointLabelYOffset={-12}
      enableTouchCrosshair={true}
      enableCrosshair={true}
      useMesh={true}
    />
  );
};

const Tasks = () => {
  const [weekdays, setWeekdays] =
    useState<{ day: string; month: string; color: string }[]>();

  useEffect(() => {
    const currentMoment = moment();
    const startOfWeek = currentMoment.clone().startOf("isoWeek");
    const colors: string[] = [
      "#1E6F5C",
      "#F6E868",
      "#D3E1D1",
      "#73D1EA",
      "#F6E868",
      "#1E6F5C",
      "#D3E1D1",
    ];
    const week: { day: string; month: string; color: string }[] = [];
    for (let i = 0; i < 7; i++) {
      const day = startOfWeek.clone().add(i, "days");

      week.push({
        day: day.format("ddd"),
        month: day.format("D"),
        color: colors[i],
      }); // "ddd" for day name abbreviation, "Do" for day of month
    }
    setWeekdays(week);
  }, []);

  return (
    <div className="font-Myfont flex flex-col w-full  p-4 gap-4">
      <div className="flex w-full gap-10 justify-center items-center">
        <p className="font-bld text-[12px]">TASKS FOR THIS WEEK</p>
        <div className="grow h-[35px] border-scBgGreen border-[2px] rounded-full"></div>
      </div>
      <div className="flex gap-2 w-full">
        {weekdays?.map((time, _) => {
          return (
            <div className="w-full flex flex-col gap-4 justify-center items-center font-bld">
              <p className="text-[12px] text-[#1E6F5C]">{time.day}</p>
              <div
                style={{ backgroundColor: time.color }}
                className={`h-[165px] flex flex-col w-full text-white rounded-full justify-center items-center`}
              >
                {time.month}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

const LastIrrigations = () => {
  return (
    <div className="w-full flex flex-col p-4 gap-2">
      <p className="font-bld text-[12px]">{"last irrigations".toUpperCase()}</p>

      <div className="flex flex-col grow gap-3">
        <div className="w-full h-[45px] bg-scBgGreen rounded-full flex text-[12px] font-bld justify-evenly items-center">
          {[
            "Field name",
            "Date",
            "Duration",
            "Amount of Water",
            "Irrigation Method",
          ].map((name, _) => {
            return <p>{name}</p>;
          })}
        </div>
        <div className=" overflow-hidden hover:overflow-y-scroll h-[160px] ">
          <div className="flex flex-col gap-2">
            <div className="w-full border-2 border-scBgGreen h-[45px] rounded-full"></div>
            <div className="w-full border-2 border-scBgGreen h-[45px] rounded-full"></div>
            <div className="w-full border-2 border-scBgGreen h-[45px] rounded-full"></div>
            <div className="w-full border-2 border-scBgGreen h-[45px] rounded-full"></div>
            <div className="w-full border-2 border-scBgGreen h-[45px] rounded-full"></div>
            <div className="w-full border-2 border-scBgGreen h-[45px] rounded-full"></div>
            <div className="w-full border-2 border-scBgGreen h-[45px] rounded-full"></div>
          </div>
        </div>
      </div>
    </div>
  );
};
const data__ = [];

data__.push(data[0].data.map((v) => v.y));

console.log();
export const config: { series: [{}]; options: ApexCharts.ApexOptions } = {
  options: {
    colors: ["#1E6F5C"],
    chart: {
      toolbar: {
        show: true,
      },
    },

    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: "straight",
      width: 3,
    },

    xaxis: {
      type: "datetime",
      tickAmount: 6,
      // min: new Date("01 Jan 2024").getTime(),
      // max: new Date("01 Feb 2024").getTime(),
      // categories: getDateRange("2023-11-01", "2023-12-05"),
    },
    tooltip: {
      x: {
        format: "dd MMM yyyy HH:mm",
      },
    },
    fill: {
      type: "gradient",
      gradient: {
        // opacityTo:[]
        // shadeIntensity: 1,
        // opacityFrom: 0.7,
        opacityTo: 0,
        // stops: [0, 100],
      },
    },
    grid: {
      show: false,
    },
  },
};

const Dashboard = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  const [WeatherData, setWeatherData] = useState<{
    [key: string]: any;
    station: string;
    "Rainfall mm": [];
    "Temperature C": [];
    "Visibility Km": [];
    "WinDir deg": [];
    "WindSpeed m.s-1": [];
    "Tdew C": [];
    "Pressure mb": [];
  }>();
  const series = [
    {
      name: "Temperature C",
      data: WeatherData?.["Temperature C"]?.map((point) => [
        point[0] * 1000,
        point[1],
      ]),
    },
  ];
  const series_ = [
    "Rainfall mm",
    "Temperature C",
    "Visibility Km",
    "WinDir deg",
    "WindSpeed m.s-1",
    "Tdew C",
    "Pressure mb",
  ].map((name) => {
    const serie = [
      {
        name: name,
        data: WeatherData?.[name]?.map((point) => [point[0] * 1000, point[1].toFixed(2)]),
      },
    ];
    return serie;
  });

  useEffect(() => {
    api.get("/farmer/field").then((res) => {
      dispatch(updateFarmerInfo({ fieldInfo: res.data }));
    });
    api
      .post("/api/ogimet", {
        field_id: Data.currentField?.id,
        start_date: "2024-06-17",
        end_date: "2024-06-25",
      })
      .then((res) => {
        console.log(res.data);
        setWeatherData(res.data);
      });
  }, [Data.currentField]);
  const weather__ = [
    { value: "33", icon: dropIcon, uni: "%" },
    { value: "9.56", icon: windIcon, uni: "m/s" },
    { value: "1002", icon: prchIcon, uni: "hpa" },
  ];
  return (
    <div className="w-full max-w-[2000px] flex p-2 gap-2 font-Myfont">
      <div className="flex flex-col w-[33%] gap-[11px]">
        <div className="relative w-full h-[580px] overflow-hidden rounded-[10px]">
          <div className="w-full absolute z-40 p-2">
            <Select
              // defaultSelectedKeys={Data.currentField?.name}
              size="sm"
              radius={"lg"}
              label="Select field"
              className="grow  "
              classNames={{
                trigger: "bg-scBgGreen",
              }}
              onChange={(e)=> {
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
          <AddField options_={false} />
        </div>
        <div className="flex w-full gap-[11px]">
          <div className="w-[50%]  h-[287px] flex flex-col gap-8 bg-gradient-to-b from-[#EAF3E9] to-[#F8F2D8] rounded-[10px] p-3">
            <div className="flex flex-col ">
              <p className="text-[18px] font-bld text-[#1E6F5C]">
                Current Weather
              </p>
              <p className="text-[14px] font-md text-[#1E6F5C]">Sunny</p>
            </div>
            <div className="flex justify-center items-center gap-6">
              <ReactSVG src={sunIcon} />
              <p className="text-[35px] font-bld text-[#1E6F5C]">
                24.3 <span className="text-[20px]">C°</span>
              </p>
            </div>
            <div className="flex justify-center gap-4">
              {weather__.map((v, _) => {
                return (
                  <div className="flex gap-2 justify-center items-center">
                    <ReactSVG src={v.icon} />
                    <p className="font-bld text-[14px] text-[#6B9E8A]">
                      {v.value}
                      <span className="text-[10px]">{v.uni}</span>
                    </p>
                  </div>
                );
              })}
            </div>
          </div>
          <div className="w-[50%] h-[287px] bg-[#1E6F5C] rounded-[10px] flex flex-col p-3 gap-8">
            <div className="flex flex-col ">
              <p className="text-[18px] font-bld text-white">
                Forecast Weather
              </p>
              <p className="text-[14px] font-md text-white">Sunny</p>
            </div>
            <div className="flex justify-center items-center gap-6">
              <ReactSVG src={sunIcon} />
              <p className="text-[35px] font-bld text-white">
                24.3 <span className="text-[20px]">C°</span>
              </p>
            </div>
            <div className="w-full flex gap-3">
              <Button
                variant="bordered"
                radius="full"
                className="w-[50%] border-white text-white"
              >
                See more
              </Button>
              <Button radius="full" className="w-[50%] bg-white text-[#1E6F5C]">
                Next days
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="flex flex-col w-[33%]  gap-[11px]">
        <div className="flex gap-2 w-full ">
          <div className="flex flex-col w-[50%] gap-2 ">
            <div className=" h-[82px] rounded-[10px]  bg-scBgGreen p-4 flex items-center justify-center gap-2">
              <Button
                onClick={() => {
                  window.location.href = "/fieldmanagment";
                }}
                variant="bordered"
                radius="full"
                className="grow border-[#1E6F5C] text-[#1E6F5C]"
              >
                New field
              </Button>
              <Button radius="full" className="grow bg-[#1E6F5C] text-white">
                New Season
              </Button>
            </div>
            <div className="w-full   h-[220px] rounded-[10px] bg-scBgGreen flex flex-col justify-center items-center">
              <p className="font-bld text-[18px]">Area of Field</p>
              <p className="font-bld text-[78px] text-[#1E6F5C]">
                35<span className="text-[20px]">Ha</span>
              </p>
            </div>
          </div>

          <div className="rounded-[10px] bg-scBgGreen h-[311px]  p-2  flex flex-col grow max-w-[50%] items-center gap-8">
            <div className="flex justify-between items-center  w-full">
              <p className="font-bld text-[18px] ml-2">Water Stress</p>
              <Button isIconOnly className="bg-transparent">
                <ReactSVG
                  className="fill-[#8cda9c] hover:fill-[#5BAD6B]"
                  src={fllsc}
                />
              </Button>
            </div>
            <p className="font-bld text-[78px] text-Red">
              20<span className="text-[20px]">%</span>
            </p>
            <div className="h-[40px] w-[80%]">
              <ResponsiveLine_ color="#DC4545" />
            </div>
          </div>
        </div>

        <div className="rounded-[10px] bg-white w-full h-[557px]">
          <Tasks />
          <LastIrrigations />
        </div>
      </div>

      <div className="flex w-[33%] flex-col gap-[11px]">
        <div className="w-full flex gap-2">
          <div className="rounded-[10px] bg-scBgGreen flex w-[50%] h-[311px] p-2 flex-col items-center max-w-[338px] gap-8">
            <div className="flex justify-between items-center  w-full">
              <p className="font-bld text-[18px] ml-2">
                Soil Surface water content{" "}
              </p>
              <Button isIconOnly className="bg-transparent">
                <ReactSVG
                  className="fill-[#8cda9c] hover:fill-[#5BAD6B]"
                  src={fllsc}
                />
              </Button>
            </div>
            <p className="font-bld text-[78px] text-[#C68E3A]">
              40<span className="text-[20px]">%</span>
            </p>
            <div className="h-[40px] w-[80%]">
              <ResponsiveLine_ color="#C68E3A" />
            </div>
          </div>
          <div className="rounded-[10px] bg-scBgGreen flex grow h-[311px] max-w-[338px] p-2 flex-col items-center">
            <p className="font-bld  text-[18px] m-2">Crops</p>
            <CropPie />
          </div>
        </div>
        <div className=" rounded-[10px] bg-scBgGreen h-[557px] overflow-hidden hover:overflow-y-scroll">
          <div className="h-[1000px] min-w-full pt-4 pl-1">
            <div className="w-full h-[300px]">
              {series_.map((vr, _) => {
                if (vr[0].name === "Rainfall mm")
                  return
                return (
                  <div className="w-[99%] h-full flex flex-col ">
                    {/* <p className="font-bld text-[18px] ">{"s"}</p> */}
                    
                    <ReactApexCharts
                      height={280}
                      type="area"
                      options={{
                        ...config.options,
                        title: {
                          text: vr[0].name,
                          align: "left",
                        },
                      }}
                      series={vr}
                    />
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
