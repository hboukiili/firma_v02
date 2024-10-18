import { useEffect, useState } from "react";
import api from "../../api/axios.js";
import ReactApexCharts from "react-apexcharts";
import { getDateRange } from "./Dashboard.tsx";
import { useAppDispatch, useAppSelector } from "../../Redux/hooks.ts";
import { Button, DateInput, Select, SelectItem } from "@nextui-org/react";
import { updateFarmerInfo } from "../../Redux/Farmer/actions.ts";
import AddField from "./tools/addField.tsx";
import { CalendarDate } from "@internationalized/date";
import canld from "../../assets/canld.png";
import PuffLoader from "react-spinners/PuffLoader";

export const config: { series: [{}]; options: ApexCharts.ApexOptions } = {
  options: {
    colors: ["#01A5CF", "#1E6F5C", "#E6DD3B"],
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

    // xaxis: {
    //     type: "datetime",
    //     tickAmount: 6,
    //     min: new Date("01 Jan 2019").getTime(),
    //     max: new Date("01 May 2019").getTime(),
    //     categories: getDateRange("2019-01-01", "2019-01-05"),
    // },
    // tooltip: {
    //   x: {
    //     format: "dd MMM yyyy HH:mm",
    //   },
    // },
    fill: {},
    // fill: {
    //   type: "gradient",
    //   gradient: {
    //     // opacityTo:[]
    //     // shadeIntensity: 1,
    //     // opacityFrom: 0.7,
    //     opacityTo: 0,
    //     // stops: [0, 100],
    //   },
    // },
    grid: {
      show: true,
    },
  },
};

function setSeries(data) {
  const series = [
    [
      {
        name: "Irrigation mm/day",
        type: "column",
        data: data.IrrDay,
      },
      {
        name: "Deep Perc",
        type: "line",
        data: data.DeepPerc,
      },
      {
        name: "ET",
        type: "line",
        data: data.ET,
      },
    ],
    [
      {
        name: "Irrigation mm/day",
        type: "column",
        data: data.IrrDay,
      },
      {
        name: "SM1",
        type: "line",
        data: data.Th1,
      },
      {
        name: "SM2",
        type: "line",
        data: data.Th2,
      },
      {
        name: "SM3",
        type: "line",
        data: data.th3,
      },
    ],
    [
      {
        name: "Irrigation mm/day",
        type: "column",
        data: data.IrrDay,
      },
      {
        name: "Canopy cover",
        type: "line",
        data: data.canopy_cover,
      },
      {
        name: "Biomass",
        type: "line",
        data: data.biomass,
      },
    ],
    [
      {
        name: "Z root",
        type: "column",
        data: data.z_root,
      },
      {
        name: "Gdd cum",
        type: "line",
        data: data.gdd_cum,
      },
    ],
    [
      {
        name: "Harvest index",
        type: "column",
        data: data.harvest_index,
      },
      {
        name: "Dry Yield",
        type: "line",
        data: data.DryYield,
      },
      {
        name: "Fresh Yield",
        type: "line",
        data: data.FreshYield,
      },
    ],
  ];
  return series;
}

const Aquacrop = () => {
  const [Data, SetData] =
    useState<{ name: string; type: string; data: any }[][]>();
  const [dates, Setdates] = useState();
  const Data_ = useAppSelector((state) => state.farmer);
  const dispatch = useAppDispatch();
  console.log(Data_);
  const [isLoad, setIsLoad] = useState(false);
  const [start_date, SetSrtDate] = useState("");
  const [end_date, SetEndDate] = useState("");
  const [fID, SetFid] = useState();
  const [sub, Setsub] = useState(true);
  const [loader , SetLoader] = useState(false)
  useEffect(() => {
    // api
    //   .get("/api/aquacrop")
    //   .then((res) => {
    //     SetData(setSeries(res.data));
    //     Setdates(res.data.dates);
    //     console.log(res.data);
    //   })
    //   .catch((err) => {
    //     console.log(err);
    //   });
    if (end_date && start_date && fID) Setsub(false);
  }, [end_date, start_date, fID]);

  return (
    <div className="w-screen p-2">
      <div className="w-[100%] flex flex-col gap-4">
        {isLoad ? (
          Data?.map((val, _) => {
            return (
              <ReactApexCharts
                className="bg-white rounded-md p-4"
                //   key={_}
                height={400}
                // type="area"
                options={{
                  ...config.options,
                  xaxis: {
                    type: "datetime",
                    categories: dates,
                  },
                  yaxis: [
                    {
                      min: 0,
                      seriesName: val[0].name,
                      //   opposite: true,
                      axisTicks: {
                        show: true,
                      },
                      axisBorder: {
                        show: true,
                        //   color: "black",
                      },
                      labels: {
                        formatter: function (value: number) {
                          return value.toFixed(2); // Format the labels to have 2 decimal places if needed
                        },
                      },
                      title: {
                        text: val[0].name,
                        style: {
                          //   color: "#00E396",
                        },
                      },
                    },
                    {
                      min: Math.min(...val[1].data),
                      seriesName: val[1].name,
                      opposite: true,
                      axisTicks: {
                        show: true,
                      },
                      axisBorder: {
                        show: true,
                        //   color: "black",
                      },
                      labels: {
                        formatter: function (value: number) {
                          return value.toFixed(2); // Format the labels to have 2 decimal places if needed
                        },
                      },
                      title: {
                        text: val[1].name,
                        style: {
                          //   color: "#00E396",
                        },
                      },
                    },
                  ],
                  //   title: {
                  //     text: vr[0].name,
                  //     align: "left",
                  //   },
                }}
                series={val}
              />
            );
          })
        ) : (
          <div className="w-full flex flex-col">
            <div className="relative w-full h-[760px] overflow-hidden rounded-[10px]">
              <div className="w-[35%] absolute z-40 p-4 rounded-lg flex flex-col gap-2 bg-white m-2">
                <Select
                  // defaultSelectedKeys={Data.currentField?.name}
                  size="sm"
                  radius={"lg"}
                  label="Select field"
                  className="w-full  "
                  classNames={{
                    trigger: "bg-scBgGreen",
                  }}
                  onChange={(e) => {
                    SetFid(Data_.fieldInfo[e.target.value].id);
                    dispatch(
                      updateFarmerInfo({
                        currentField: Data_.fieldInfo[e.target.value],
                      })
                    );
                  }}
                >
                  {Data_.fieldInfo.map((val, _) => {
                    return (
                      <SelectItem key={_} value={val.name}>
                        {val.name}
                      </SelectItem>
                    );
                  })}
                </Select>
                <div className="w-full flex gap-2 font-Myfont">
                  <DateInput
                    onChange={(e) => {
                      // console.log(e.toString(),"3333")
                      if (e.day && e.month && e.year) SetSrtDate(e.toString());
                    }}
                    label="Enter the start date."
                    variant="faded"
                    radius="full"
                    size="lg"
                    classNames={{ inputWrapper: "border[#1E6F5C]", input: "" }}
                    //   defaultValue={parseDate("2024-04-04")}
                    placeholderValue={new CalendarDate(1995, 11, 6)}
                    labelPlacement="outside"
                    startContent={<img className="w-[20px]" src={canld} />}
                  ></DateInput>
                  <DateInput
                    onChange={(e) => {
                      // console.log(e.toString(),"3333")
                      SetEndDate(e.toString());
                    }}
                    label="Enter the end date."
                    variant="faded"
                    radius="full"
                    size="lg"
                    classNames={{ inputWrapper: "border[#1E6F5C]", input: "" }}
                    //   defaultValue={parseDate("2024-04-04")}
                    placeholderValue={new CalendarDate(1995, 11, 6)}
                    labelPlacement="outside"
                    startContent={<img className="w-[20px]" src={canld} />}
                  ></DateInput>
                </div>
                <Button
                  onClick={() => {
                    SetLoader(true)
                    Setsub(true)
                    api
                      .post("/api/aquacrop", {
                        field_id: Data_.fieldInfo[0].id,
                        start_date: "2019-01-01",
                        end_date: "2019-05-05",
                      })
                      .then((res) => {
                        SetData(setSeries(res.data));
                        Setdates(res.data.dates);
                        setIsLoad(true);
                        console.log(res.data);
                      })
                      .catch((err) => {
                        console.log(err);
                      });
                  }}
                  // isDisabled={sub}
                  className="mt-2 bg-Green text-white"
                  radius="full"
                >
            {loader ? <PuffLoader className="w-[15px]" color="#fff" />
             : "Submit"}
                </Button>
              </div>
              <AddField options_={false} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Aquacrop;
