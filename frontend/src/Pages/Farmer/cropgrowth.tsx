import React from "react";
import AddField from "./tools/addField";
import { Lengend } from "../Policymaker/Policymaker";
import {
  Button,
  DateInput,
  Input,
  Pagination,
  Select,
  SelectItem,
  image,
} from "@nextui-org/react";
import { CalendarDate } from "@internationalized/date";
import { CalendarIcon } from "./tools/Irrigationsystem_";
import canld from "../../assets/canld.png";
import cropBg from "../../assets/cropBg.png";
// import { config } from "./Dashboard";
import ReactApexCharts from "react-apexcharts";

const config: { series: [{}]; options: ApexCharts.ApexOptions } = {
  series: [
    {
      name: "NDVI",
      data: [
        -0.81, 0, -0.44, -0.9, -0.29, 0.22, 0.52, 0.9, 0.12, 0.7, 0.19, 0.5,
        0.13, 0.9, 0.17, -0.33, 0.7, 0.5,
      ],
    },
  ],
  options: {
    colors: ["#1E6F5C"],
    chart: {
      height: 350,
    },
    forecastDataPoints: {
      count: 8,
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      width: 3,
      curve: "smooth",
    },
    xaxis: {
      type: "datetime",
      categories: [
        "1/11/2000",
        "2/11/2000",
        "3/11/2000",
        "4/11/2000",
        "5/11/2000",
        "6/11/2000",
        "7/11/2000",
        "8/11/2000",
        "9/11/2000",
        "10/11/2000",
        "11/11/2000",
        "12/11/2000",
        "1/11/2001",
        "2/11/2001",
        "3/11/2001",
        "4/11/2001",
        "5/11/2001",
        "6/11/2001",
      ],
      tickAmount: 10,
      labels: {
        formatter: function (value, timestamp, opts) {
          return opts.dateFormatter(new Date(timestamp), "dd MMM");
        },
      },
    },
    title: {
      text: "NDVI (Normalized Difference Vegetation Index)",
      align: "left",
      style: {
        fontSize: "14px",
        color: "#666",
      },
    },

    fill: {
      type: "gradient",
      gradient: {
        shade: "dark",

        // gradientToColors: ["red", "#F1EA3B", "#F02929"],
        shadeIntensity: 1,

        type: "vertical",
        opacityFrom: 1,
        opacityTo: 0.1,
        stops: [0],
        colorStops: [
          {
            offset: 33.3,
            color: "green",
            opacity: 1,
          },
          {
            offset: 66.3,
            color: "yellow",
            opacity: 1,
          },
          {
            offset: 100,
            color: "red",
            opacity: 1,
          },
        ],
      },
    },
  },
};

const Cropgrowth_ = () => {
  const Fields = ["field1", "field2", "field3", "field4", "field5"];
  return (
    <div className="w-full flex gap-3 p-2">
      <div className="flex flex-col gap-3 w-[40%] ">
        <div className="w-full relative  h-[685px] rounded-[10px] overflow-hidden">
          <div className="w-full absolute z-40 p-2">
            <Select
              size="sm"
              radius={"lg"}
              label="Select field"
              className="grow  "
              classNames={{
                trigger: "bg-scBgGreen",
              }}
            >
              {Fields.map((val, _) => {
                return (
                  <SelectItem key={val} value={val}>
                    {val}
                  </SelectItem>
                );
              })}
            </Select>
          </div>
          <AddField options_={false} />
        </div>
        <div className="rounded-[10px] bg-scBgGreen w-full  flex flex-col items-center p-2 justify-evenly">
          <Lengend max={1} min={0} />
        </div>
        {/* <Pagination
            page={3}
            // onChange={SetImgIndex}
            classNames={{
              item: "border-[#D3E1D1] text-DarkGreen ",
              cursor: "bg-[#48A788]",
            }}
            variant="bordered"
            showControls
            total={10}
            initialPage={1}
          /> */}
      </div>
      <div className="grow flex flex-col gap-3">
        <div className="flex w-full p-2 bg-scBgGreen rounded-[10px] pl-10">
          <div className="flex flex-col gap-8 m-4">
            <div className="">
              <p className="font-Myfont font-bld text-[32px]">
                Crop health and growth
              </p>
              <p className="font-Myfont font-md text-[12px]">
                This visualization combines NDVI (Normalized Difference
                Vegetation <br /> Index) to give you a comprehensive view of
                your crop's performance.
              </p>
            </div>
            <div className="flex flex-col gap-4 label-">
              <DateInput
                label="Enter the start date."
                variant="bordered"
                radius="full"
                size="lg"
                // className="max-w-[260px]"
                classNames={{ inputWrapper: "border-[#1E6F5C]", input: "" }}
                //   defaultValue={parseDate("2024-04-04")}
                placeholderValue={new CalendarDate(1995, 11, 6)}
                labelPlacement="outside"
                startContent={<img className="w-[20px]" src={canld} />}
              ></DateInput>
              <DateInput
                label="Enter the end date"
                variant="bordered"
                // className="max-w-[260px]"
                radius="full"
                size="lg"
                classNames={{
                  inputWrapper: "border-[#1E6F5C]",

                  //   segment: "text-white",
                }}
                //   defaultValue={parseDate("2024-04-04")}
                placeholderValue={new CalendarDate(1995, 11, 6)}
                labelPlacement="outside"
                startContent={<img className="w-[20px]" src={canld} />}
              ></DateInput>
              <div className="flex gap-2 mt-2">
                <Button radius="full" className="bg-[#1E6F5C] text-white">
                  Submit
                </Button>
                <Button
                  radius="full"
                  variant="bordered"
                  className="border-red-300 text-red-300"
                >
                  Clear all
                </Button>
              </div>
            </div>
          </div>
          <div className="grow flex justify-center items-center">
            <img className="w-[300px]" src={cropBg} alt="" />
          </div>
        </div>
        <div className="grow bg-scBgGreen rounded-[10px] p-2">
          <ReactApexCharts
            height={335}
            type="line"
            options={{
              ...config.options,
              //   title: {
              //     text: "",
              //     align: "left",
              //   },
            }}
            series={config.series}
          />
        </div>
      </div>
    </div>
  );
};

export default Cropgrowth_;
