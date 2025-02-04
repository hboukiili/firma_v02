import {
  Button,
  Card,
  CardBody,
  Divider,
  Select,
  SelectItem,
  Switch,
  Tab,
  Tabs,
} from "@nextui-org/react";
import { useAppDispatch, useAppSelector } from "../../../Redux/hooks";
import { updateFarmerInfo } from "../../../Redux/Farmer/actions";
import bg from "../../../assets/WeatherBg.jpg";
import { useEffect, useState } from "react";
import { MultiChart_ } from "../Aquacrop";
import ReactApexCharts from "react-apexcharts";
import { scaleLinear } from "d3-scale"; // Import d3-scale
import { ReactSVG } from "react-svg";
import sunIcn from "../../../assets/weatherICons/Sunny.png";
import CloudyIcn from "../../../assets/weatherICons/PartlyCloudy.png";
import api from "../../../api/axios.js";
import { ToggleButton, ToggleButtonGroup } from "@mui/material";
import calnIcn from "../../../assets/calendar-month.svg";
import cloudIcn from "../../../assets/cloud-rain.svg";
import tmIcn from "../../../assets/temperature.svg";
import windIcn from "../../../assets/wind.svg";
import hmIcn from "../../../assets/droplets.svg";
const Header = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  return (
    <div className="relative overflow-hidden w-full font-Myfont rounded-full flex p-2 px-4 items-center justify-between">
      <img className="absolute w-full top-0 left-0" src={bg} alt="bg" />
      <Select
        // defaultSelectedKeys={Data.currentField?.name}
        size="lg"
        radius={"full"}
        label="Select field"
        className="max-w-[300px] "
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
      <p className="font-lt z-10 text-[48px] text-white pr-8">
        Weather Information
      </p>
    </div>
  );
};

const WindSpeed = () => {
  // Example data: array of angles (in degrees) and corresponding wind speeds
  const windData = [
    { angle: 0, speed: 3, date: "2024-12-01" },
    { angle: 15, speed: 5, date: "2024-12-01" },
    { angle: 45, speed: 2, date: "2024-12-02" },
    { angle: 90, speed: 6, date: "2024-12-02" },
    { angle: 120, speed: 4, date: "2024-12-03" },
    { angle: 180, speed: 8, date: "2024-12-03" },
    { angle: 270, speed: 7, date: "2024-12-04" },
    { angle: 300, speed: 5, date: "2024-12-04" },
    { angle: 0, speed: 3, date: "2024-12-05" },
    { angle: 16, speed: 5, date: "2024-12-05" },
    { angle: 48, speed: 2, date: "2024-12-06" },
    { angle: 94, speed: 6, date: "2024-12-06" },
    { angle: 10, speed: 4, date: "2024-12-07" },
    { angle: 80, speed: 8, date: "2024-12-07" },
    { angle: 70, speed: 7, date: "2024-12-08" },
    { angle: 30, speed: 5, date: "2024-12-08" },
  ];

  const numBins = 30; // 30 bins
  const binSize = 360 / numBins;
  const windBins = new Array(numBins).fill(0);

  // Create the labels with both direction and date info
  const directions = [
    "N",
    "N12",
    "N24",
    "N36",
    "N48",
    "N60",
    "N72",
    "N84",
    "E",
    "E12",
    "E24",
    "E36",
    "E48",
    "E60",
    "E72",
    "E84",
    "S",
    "S12",
    "S24",
    "S36",
    "S48",
    "S60",
    "S72",
    "S84",
    "W",
    "W12",
    "W24",
    "W36",
    "W48",
    "W60",
    "W72",
  ];

  // Bin the data by angle
  windData.forEach((data) => {
    const binIndex = Math.floor((data.angle + 6) / 12) % numBins;
    windBins[binIndex] += data.speed;
  });

  // Generate direction labels with the date and wind speed
  const labels = directions.map((dir, index) => {
    const speed = windBins[index];
    const date =
      windData.find(
        (entry) => Math.floor((entry.angle + 6) / 12) % numBins === index
      )?.date || "No data";
    return `${dir} - ${date} `;
  });

  // Define custom color ranges based on wind speed ranges
  const getColor = (value) => {
    if (value >= 0 && value <= 2) {
      return "#71A8E7"; // Blue for wind speeds 1-10
    } else if (value >= 3 && value <= 5) {
      return "#42a840"; // Green for wind speeds 11-20
    } else if (value >= 6 && value <= 8) {
      return "#faa237"; // Yellow for wind speeds 21-30
    } else if (value >= 9 && value <= 11) {
      return "#f90"; // Orange for wind speeds 31-40
    } else {
      return "#f00"; // Red for wind speeds above 40
    }
  };

  // Apply color based on the wind speed value
  const colors = windBins.map((value) => getColor(value));

  const options = {
    chart: {
      type: "polarArea",
    },
    labels,

    // Direction labels with date and wind speed
    stroke: {
      width: 0,
    },
    fill: {
      opacity: 0.7,
    },
    legend: {
      show: false,
    },
    plotOptions: {
      polarArea: {
        // rings: {
        //   strokeColor : "#fff",
        //   strokeWidth: 1,
        // },
        spokes: {
          connectorColors: "#fff",
          strokeWidth: 1,
        },
      },
    },
    // theme: {
    //   monochrome: {
    //     enabled: true,
    //     shadeTo: "light",
    //     shadeIntensity: 0.6,
    //   },
    // },
    colors, // Dynamically set the colors for each bar
  };

  return (
    <div className="flexCenter">
      <ReactApexCharts
        options={options}
        series={windBins} // Array of summed wind speeds per bin
        type="polarArea"
        // height={300}
      />
    </div>
  );
};

type WeatherDataType = {
  forcast: {
    T2m_max?: number[];
    irg?: number[];
    Rh_max?: number[];
    Rain_pro?: number[];
    Rain?: number[];
    Ws?: number[];
    Dates?: string[];
  };
  historic: {
    T2m_max?: number[];
    irg?: number[];
    Rh_max?: number[];
    Rain_pro?: number[];
    Rain?: number[];
    Ws?: number[];
    Dates?: string[];
  };
};

function mergeWeatherData(
  dataFr: { name: string; data: number[] }[],
  dataHs: { name: string; data: number[] }[]
): { name: string; data: number[] }[] {
  const historicMap = new Map<string, number[]>(
    dataHs.map((item) => [item.name, item.data || []])
  );

  return dataFr.map((forecastItem) => {
    const historicData = historicMap.get(forecastItem.name) || [];
    return {
      name: forecastItem.name,
      data: [...historicData, ...forecastItem.data],
    };
  });
}

const OtherVariables = () => {
  const [weatherData_, setWeatherData] = useState<WeatherDataType | null>(null);
  const [data_, setData_] = useState<{ name: string; data: number[] }[]>([]);
  const Data = useAppSelector((state) => state.farmer);

  useEffect(() => {
    api.get(`/api/weather?field_id=${Data.currentField?.id}`).then((res) => {
      console.log(res.data);
      setWeatherData(res.data);
    });
  }, [Data.currentField]);

  useEffect(() => {
    if (weatherData_) {
      const data_fr = [
        { name: "Rain (mm)", data: weatherData_.forcast?.Rain ?? [] },
        { name: "Temperature (C°)", data: weatherData_.forcast?.T2m_max ?? [] },
        {
          name: "Global radiation (W/m²)",
          data: weatherData_.forcast?.irg ?? [],
        },
        { name: "Humidity (%)", data: weatherData_.forcast?.Rh_max ?? [] },
        { name: "Wind Speed (m/s)", data: weatherData_.forcast?.Ws ?? [] },
      ];

      const data_hs = [
        { name: "Rain (mm)", data: weatherData_.historic?.Rain ?? [] },
        {
          name: "Temperature (C°)",
          data: weatherData_.historic?.T2m_max ?? [],
        },
        {
          name: "Global radiation (W/m²)",
          data: weatherData_.historic?.irg ?? [],
        },
        { name: "Humidity (%)", data: weatherData_.historic?.Rh_max ?? [] },
        { name: "Wind Speed (m/s)", data: weatherData_.historic?.Ws ?? [] },
      ];

      setData_(mergeWeatherData(data_fr, data_hs));
    }
  }, [weatherData_]);
  const colors = ["#239fd9", "#d92323", "#e3e152", "#239fd9", "#56d63c"];
  return (
    <div className="w-full flex flex-col items-center p-4 relative">
      <Tabs
        classNames={{ wrapper: "w-full" }}
        aria-label="items"
        variant="underlined"
      >
        {data_ &&
          data_.map((item, key) => (
            <Tab className="w-full" key={key} title={item.name}>
              <div className="h-[230px] pr-4">
                <MultiChart_
                  Data={{
                    DateRange: [
                      ...(weatherData_?.historic?.Dates || []),
                      ...(weatherData_?.forcast?.Dates || [])
                    ],
                    datasets: [
                      {
                        data: item.data,
                        name: item.name,
                        type: item.name === "Rain (mm)" ? "bar" : "line",
                        yAxisId: key,
                        color: colors[key],
                        forecastCount: 7
                      }
                    ],
                    yAxes: [{ id: key, title: item.name }]
                  }}
                />
              </div>
            </Tab>
          ))}
      </Tabs>
    </div>
  );
};

const WindAndOthers = () => {
  return (
    <div className="w-full flex blurBg p-2 rounded-[30px] h-[46%]">
      <div className="w-full  rounded-[30px] flex gap-2 ">
        <div className="w-full bg-white rounded-[27px]">
          <OtherVariables />
        </div>
        {/* <Divider className="w-[80%] self-center mb-2" /> */}
        <Forcast />
      </div>
    </div>
  );
};

type cardData = {
  id: number;
  day: string;
  temperature: string;
  "Global radiation": string;
  humidity: string;
  "Precipitation Probability": string;
  Rain: string;
  lowTemp: string;
  "Wind Speed": string;
  icon: string;
};

type WeatherDataFr = {
  name: string;
  data: number[];
};

function transformWeatherData(
  dataFr: WeatherDataFr[],
  dates: string[]
): cardData[] {
  // Helper function to get the day name from a date string
  const getDayName = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", { weekday: "short" }); // Returns "Mon", "Tue", etc.
  };

  return dates.map((date, index) => {
    const dayName = index === 0 ? "Current Weather" : getDayName(date);

    // Construct the data object for each day
    const dayData: cardData = {
      id: index + 1,
      day: dayName,
      temperature:
        (dataFr
          .find((item) => item.name === "Temperature")
          ?.data[index]?.toFixed(2) || "N/A") + " C°",
      lowTemp:
        (dataFr
          .find((item) => item.name === "Temperature")
          ?.data[index]?.toFixed(2) || "N/A") + " C°",
      "Global radiation":
        (dataFr
          .find((item) => item.name === "Global radiation")
          ?.data[index]?.toFixed(2) || "N/A") + " W/m²",
      humidity:
        (dataFr.find((item) => item.name === "Rh")?.data[index]?.toFixed(0) ||
          "N/A") + " %",
      "Precipitation Probability":
        (dataFr
          .find((item) => item.name === "Rain pro")
          ?.data[index]?.toFixed(2) || "N/A") + " %",
      Rain:
        (dataFr.find((item) => item.name === "Rain")?.data[index]?.toFixed(1) ||
          "N/A") + " mm",
      "Wind Speed":
        (dataFr
          .find((item) => item.name === "Wind Speed")
          ?.data[index]?.toFixed(1) || "N/A") + " Km/h",
      icon: CloudyIcn,
    };

    return dayData;
  });
}

const Forcast = () => {
  const [weatherData_, setWeatherData] = useState<WeatherDataType | null>(null);
  const [data_, setData_] = useState<{ name: string; data: number[] }[]>([]);
  const Data = useAppSelector((state) => state.farmer);
  const [wData_, setWdata] = useState<cardData[] | null>([]);
  useEffect(() => {
    api.get(`/api/weather?field_id=${Data.currentField?.id}`).then((res) => {
      setWeatherData(res.data);
    });
  }, [Data.currentField]);

  useEffect(() => {
    if (weatherData_) {
      const data_fr: WeatherDataFr[] = [
        { name: "Temperature", data: weatherData_.forcast?.T2m_max ?? [] },
        { name: "Global radiation", data: weatherData_.forcast?.irg ?? [] },
        { name: "Rh", data: weatherData_.forcast?.Rh_max ?? [] },
        { name: "Rain pro", data: weatherData_.forcast?.Rain_pro ?? [] },
        { name: "Rain", data: weatherData_.forcast?.Rain ?? [] },
        { name: "Wind Speed", data: weatherData_.forcast?.Ws ?? [] },
      ];

      setWdata(transformWeatherData(data_fr, weatherData_.forcast?.Dates));
    }
  }, [weatherData_]);

  const weatherData = [
    {
      id: 1,
      day: "Current Weather",
      temperature: "24.3 C°",
      lowTemp: "11 C°",
      humidity: 33,
      windSpeed: 9.56,
      pressure: 1002,
      icon: sunIcn,
    },
    {
      id: 2,
      day: "Mon",
      temperature: "24.3 C°",
      lowTemp: "11 C°",
      humidity: 33,
      windSpeed: 9.56,
      pressure: 1002,
      icon: CloudyIcn,
    },
    {
      id: 3,
      day: "Mon",
      temperature: "24.3 C°",
      lowTemp: "11 C°",
      humidity: 33,
      windSpeed: 9.56,
      pressure: 1002,
      icon: CloudyIcn,
    },
    {
      id: 4,
      day: "Mon",
      temperature: "24.3 C°",
      lowTemp: "11 C°",
      humidity: 33,
      windSpeed: 9.56,
      pressure: 1002,
      icon: CloudyIcn,
    },
    {
      id: 5,
      day: "Mon",
      temperature: "24.3 C°",
      lowTemp: "11 C°",
      humidity: 33,
      windSpeed: 9.56,
      pressure: 1002,
      icon: CloudyIcn,
    },
    {
      id: 6,
      day: "Mon",
      temperature: "24.3 C°",
      lowTemp: "11 C°",
      humidity: 33,
      windSpeed: 9.56,
      pressure: 1002,
      icon: CloudyIcn,
    },
  ];
  const [activeCard, setActiveCard] = useState<number | null>(1);

  return (
    <div className="flex justify-center gap-2 p-4 blurBg w-full rounded-[27px]">
      {wData_.map((item, key) => {
        if (key + 1 === wData_?.length) return;
        return (
          <div
            className={`
                flex flex-col h-full overflow-hidden bg-white transition-all hover:scale-105 hover:cursor-pointer duration-300  ease-in-out rounded-[35px]
                ${item.id === activeCard ? "grow " : "w-[90px] rounde"}`}
            onClick={() => setActiveCard(item.id)}
          >
            <div className="w-full grow bg-[#36506A] gap-[15%] rounded-[35px] text-white flexCenter flex-col ">
              <p className="font-bld text-center">{item.day}</p>
              <div className="flexCenter w-full gap-2 flex-wrap">
                <img className="w-[60px]" src={item.icon} />
                <div
                  className={`flex flex-col items-start ${
                    item.id != activeCard && "items-center"
                  }`}
                >
                  <p
                    className={`font-bld ${
                      item.id != activeCard ? "text-[15px]" : "text-[20px]"
                    }`}
                  >
                    {item.temperature}
                  </p>
                  <p
                    className={`${
                      item.id != activeCard ? "text-[15px]" : "text-[20px]"
                    }`}
                  >
                    {item.lowTemp}
                  </p>
                </div>
              </div>
            </div>
            {activeCard === item.id && (
              <div className="h-[80px]">
                <div className="flex gap-5 flex-wrap justify-center items-center text-[12px] mt-3">
                  <div className="flex flex-col gap-2">
                    <div className="flex  gap-1 items-center ">
                      <ReactSVG src={cloudIcn} />
                      <p>{item["Precipitation Probability"]}</p>
                    </div>
                    <div className="flex  gap-1 items-center">
                      <ReactSVG src={cloudIcn} />
                      <p>{item.Rain}</p>
                    </div>
                  </div>
                  <div className="flex flex-col gap-2">
                    <div className="flex gap-1">
                      <ReactSVG src={hmIcn} />
                      <p>{item.humidity}</p>
                    </div>
                    <div className="flex gap-1">
                      <ReactSVG src={windIcn} />
                      <p>{item["Wind Speed"]}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

const RainEt0 = () => {
  const Data = useAppSelector((state) => state.farmer);

  return (
    <div className="grow max-h-[405px] flex flex-col items-center gap-4 rounded-[30px]  p-2 pt-4 ">
      <p className="font-bld text-[#757575]">
        Reference Evapotranspiration And Rain (mm)
      </p>
      <div className="grow w-full px-4">
        <MultiChart_
          Data={{
            datasets: [
              {
                data: Data.RasterData?.ETref.mean,
                name: "ET0",
                type: "line",
                yAxisId: 2, // ET on Y-axis 1
                color: "#38f54f",
                forecastCount: 6
              },
              {
                data: Data.RasterData?.Rain.mean,
                name: "Rain",
                type: "bar",
                yAxisId: 1, // ET0 on Y-axis 1
                color: "#71A8E7",
                forecastCount: 6,              }
            ],
            yAxes: [
              { id: 2, title: "ET0" },
              { id: 1, title: "Rain", opposite: true }
            ]
          }}
        />
      </div>
    </div>
  );
};

const ForcastAndEt0 = () => {
  return (
    <div className="w-full h-[49.9%] flex gap-4 bg-white rounded-[30px]">
      {/* <Forcast /> */}
      <div className="max-h-[415px] grow w-[28%] gap-4 flex rounded-[30px]  items-center justify-center flex-col p-2 bg">
        <p className="font-bld text-[#757575]">Wind Speed (m/s)</p>
        <WindSpeed />
      </div>
      <RainEt0 />
    </div>
  );
};
const WeatherInfo = () => {
  const Data = useAppSelector((state) => state.farmer);

  return (
    <div className="z-30 flex flex-col w-full h-full gap-5">
      <Header />
      <div className="w-full flex flex-col gap-4 grow">
        <WindAndOthers />
        <ForcastAndEt0 />
      </div>
    </div>
  );
};

export default WeatherInfo;
