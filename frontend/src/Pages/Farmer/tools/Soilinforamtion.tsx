import {
  Checkbox,
  Input,
  Select,
  SelectItem,
  Tab,
  Tabs,
} from "@nextui-org/react";
import React, { useEffect, useRef, useState } from "react";
import { ReactSVG } from "react-svg";
import icn1 from "../../../assets/soil1.svg";
import icn2 from "../../../assets/soil2.svg";
import icn3 from "../../../assets/soil3.svg";
import SoilTr from "../../../assets/SoilTriangle.svg";

import "./style.css";
import { useAppDispatch, useAppSelector } from "../../../Redux/hooks";
import { updateFarmerInfo } from "../../../Redux/Farmer/actions";
{
  /* <image href={SoilTr} x="0" y="0" width="429" height="374" /> */
}

import Plot from "react-plotly.js";
import { Form } from "antd";

const SoilTextureTrianglePlot = () => {
  const [form] = Form.useForm<{
    clay: number;
    sand: number;
    silt: number;
  }>();
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  const [soilData, setSoilData] = useState<{ a: number; b: number; c: number }>(
    { a: 0, b: 0, c: 0 }
  );

  const soilTypes = [
    {
      name: "sand",
      conditions: (clay, sand, silt) => sand > 85 && clay < 10 && silt < 15,
      color: "#fdd49e",
    },
    {
      name: "loamy sand",
      conditions: (clay, sand, silt) =>
        sand >= 70 && sand <= 90 && (clay < 15 || (clay < 20 && silt < 30)),
      color: "#fdbb84",
    },
    {
      name: "sandy loam",
      conditions: (clay, sand, silt) =>
        (sand >= 43 && sand <= 85 && silt < 50 && clay < 20) ||
        (sand >= 52 && sand <= 70 && silt >= 30 && clay < 20),
      color: "#fc8d59",
    },
    {
      name: "loam",
      conditions: (clay, sand, silt) =>
        clay >= 7 && clay < 27 && silt >= 28 && silt < 50 && sand < 52,
      color: "#e34a33",
    },
    {
      name: "silt loam",
      conditions: (clay, sand, silt) =>
        silt >= 50 && clay <= 28 && sand <= 50 && silt <= 88,
      color: "#b30000",
    },
    {
      name: "sandy clay loam",
      conditions: (clay, sand, silt) =>
        clay >= 20 && clay < 35 && sand >= 45 && sand < 80 && silt < 28,
      color: "#feb24c",
    },

    {
      name: "sandy clay",
      conditions: (clay, sand, silt) => sand >= 45 && sand < 65 && clay >= 35,
      color: "#e31a1c",
    },
    {
      name: "clay",
      conditions: (clay, sand, silt) => clay >= 40 && sand < 45 && silt < 40,
      color: "#800026",
    },
    {
      name: "clay loam",
      conditions: (clay, sand, silt) =>
        clay >= 27 &&
        clay < 40 &&
        sand >= 20 &&
        sand < 45 &&
        silt >= 15 &&
        silt < 53,
      color: "#fd8d3c",
    },
    {
      name: "silty clay",
      conditions: (clay, sand, silt) =>
        clay >= 40 && sand < 20 && silt >= 40 && silt < 60,
      color: "#bd0026",
    },
    {
      name: "silty clay loam",
      conditions: (clay, sand, silt) =>
        clay >= 27 && clay < 40 && sand < 20 && silt >= 40,
      color: "#fc4e2a",
    },

    {
      name: "silt",
      conditions: (clay, sand, silt) => clay <= 12 && sand <= 20 && silt >= 80,
      color: "#000",
    },
  ];
  const colors = {
    sand: "#fdd49e",
    "loamy sand": "#fdbb84",
    "sandy loam": "#fc8d59",
    loam: "#e34a33",
    "silty loam": "#b30000",
    silt: "#7f0000",
    "sandy clay loam": "#feb24c",
    "clay loam": "#fd8d3c",
    "silty clay loam": "#fc4e2a",
    "sandy clay": "#e31a1c",
    "silty clay": "#bd0026",
    clay: "#800026",
  };

  function determineSoilType(clay, sand, silt) {
    for (const soilType of soilTypes) {
      if (soilType.conditions(clay, sand, silt)) {
        return soilType.color;
      }
    }
    return "#ffffff"; // Default color if no type matches
  }

  const generateDataPoints = () => {
    let dataPoints = [];
    for (let clay = 1; clay <= 100; clay++) {
      for (let sand = 1; sand <= 100 - clay; sand++) {
        let silt = 100 - clay - sand;
        if (silt >= 1) {
          dataPoints.push({ a: clay, b: sand, c: silt });
        }
      }
    }
    return dataPoints;
  };
  const data = [
    {
      type: "scatterternary",
      mode: "markers",
      a: generateDataPoints().map((point) => point.a),
      b: generateDataPoints().map((point) => point.b),
      c: generateDataPoints().map((point) => point.c),
      text: generateDataPoints().map(
        (point) => `Clay: ${point.a}%, Sand: ${point.b}%, Silt: ${point.c}%`
      ),
      hoverinfo: "text",
      marker: {
        color: generateDataPoints().map(
          (point) => `rgba(${point.a}, ${point.b}, ${point.c}, 0.2)`
        ),

        // Color points based on their composition
        size: 3,
      },
    },
  ];

  const layout = {
    ternary: {
      sum: 100,
      aaxis: { title: "Clay%", linewidth: 2, ticksuffix: "%" },
      baxis: { title: "Sand%", linewidth: 2, ticksuffix: "%" },
      caxis: { title: "Silt%", linewidth: 2, ticksuffix: "%" },
    },
    width: 580,
    // height: 470,
    showlegend: false,
    paper_bgcolor: "transparent", // Set background color for the entire plot
    plot_bgcolor: "transparent",
    bgcolor: "transparent",
    opacity: 0,
  };
  function onchange_() {
    dispatch(
      updateFarmerInfo({
        soilPr: form.getFieldsValue(),
        soilMethod: "Composition",
      })
    );
    console.log(Data.soilPr);
  }
  // useEffect(() => {
  //   console.log(form.getFieldsValue());
  //   dispatch(
  //     updateFarmerInfo({
  //       soilPr: form.getFieldsValue(),
  //       soilMethod: "Composition",
  //     })
  //   );
  // }, [form.isFieldsTouched()]);
  return (
    <div className="flex flex-col  justify-center items-center relative ">
      <ReactSVG className="absolute top-[100px] w-[313px]" src={SoilTr} />
      <Plot
        className=""
        data={data}
        layout={layout}
        config={{
          displayModeBar: false,
        }}
        onClick={(e) => {
          form.setFieldsValue({
            clay: e.points[0].a,
            sand: e.points[0].b,
            silt: e.points[0].c,
          });
          console.log(e.points);
          setSoilData(e.points[0]);
        }}
      />
      <Form
        className="flex gap-2 w-[350px]"
        form={form}
        layout="vertical"
        autoComplete="off"
      >
        <Form.Item name="clay" label="Clay %">
          <Input
            onChange={onchange_}
            radius="full"
            variant="bordered"
            classNames={{
              inputWrapper: "border-[#1E6F5C] text-[#1E6F5C]",
              label: "text-[#1E6F5C]",
            }}
            // classNames={{ inputWrapper: "bg-white" }}
            type="number"
            placeholder="Clay %"
            labelPlacement="outside"
          />
        </Form.Item>

        <Form.Item name="sand" label="Sand %">
          <Input
            onChange={onchange_}
            radius="full"
            variant="bordered"
            classNames={{
              inputWrapper: "border-[#1E6F5C] text-[#1E6F5C]",
              label: "text-[#1E6F5C]",
            }}
            // classNames={{ inputWrapper: "bg-white" }}
            type="text"
            placeholder="Sand %"
            labelPlacement="outside"
          />
        </Form.Item>

        <Form.Item name="silt" label="Silt %">
          <Input
            onChange={onchange_}
            radius="full"
            variant="bordered"
            classNames={{
              inputWrapper: "border-[#1E6F5C] text-[#1E6F5C]",
              label: "text-[#1E6F5C]",
            }}
            // classNames={{ inputWrapper: "bg-white" }}
            className=""
            type="text"
            placeholder="Silt %"
            labelPlacement="outside"
          />
        </Form.Item>
      </Form>
    </div>
  );
};

const Options = () => {
  const soil_ = [
    "SILT",
    "LOAMY SAND",
    "SAND",
    "SANDY LOAM",
    "LOAM",
    "SANDY CLAY LOAM",
    "CLAY LOAM",
    "SILTY CLAY",
    "SANDY CLAY",
    "CLAY",
  ];
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  useEffect(() => {
    if (Data.SoilType) dispatch(updateFarmerInfo({ SoilType: "" }));
  }, []);
  console.log(Data);
  return (
    <div className="flex w-full h-full flex-col ">
      <Tabs
        classNames={{ cursor: "bg-[#D3E1D1]" }}
        fullWidth={true}
        aria-label="Options"
        variant="bordered"
      >
        <Tab
          className="flex justify-center items-center h-full"
          key="photos"
          title={
            <div className="flex items-center space-x-2">
              <ReactSVG src={icn1} />
              <span>Predefined Soil Types</span>
            </div>
          }
        >
          <div className="flex w-full flex-col items-center pt-20 gap-8 ">
            <div className="">
              <p className="font-Myfont font-bld text-[40px]">Soil Details</p>
              <p className="font-Myfont font-md text-[12px]">
                Successful farming relies on understanding soil composition.{" "}
                <br /> Please share details about the soil in your field.
              </p>
            </div>
            <Select
              classNames={{
                trigger: "bg-white  text-[#1E6F5C] ",
                label: "text-[#1E6F5C]",
              }}
              variant="faded"
              labelPlacement="outside"
              size="md"
              radius={"full"}
              label="Indicate the primary type of soil found in your field"
              className="w-[380px]"
              placeholder="Soil type"
              onChange={(e) => {
                dispatch(
                  updateFarmerInfo({
                    SoilType: e.target.value,
                    soilMethod: "Selection",
                  })
                );
              }}
            >
              {soil_.map((val, _) => {
                return (
                  <SelectItem key={val} value={val}>
                    {val}
                  </SelectItem>
                );
              })}
            </Select>
          </div>
        </Tab>
        <Tab
          key="videos"
          title={
            <div className="flex items-center space-x-2">
              <ReactSVG src={icn3} />
              <span>Interactive Soil Triangle</span>
            </div>
          }
        >
          <SoilTextureTrianglePlot />
        </Tab>
        <Tab
          className="flex justify-center items-center h-full"
          key="music"
          title={
            <div className="flex items-center space-x-2">
              <ReactSVG src={icn2} />

              <span>Auto-Detect Soil Types</span>
            </div>
          }
        >
          <div className="flex flex-col h-full  justify-center items-center pt-16 gap-8 ">
            <div className="w-[440px]  flex flex-col items-start">
              <p className="font-Myfont font-bld text-[40px]">Soil Details</p>
              <p className="font-Myfont font-md text-[12px] ">
                Let us automatically identify your soil type using geospatial
                data for accurate results based on your location.
              </p>
            </div>
            <div className="flex w-[440px] gap-2 justify- ">
              <Checkbox
                onChange={(e) => {
                  dispatch(
                    updateFarmerInfo({
                      soilCheck: e.target.value,
                      soilMethod: "satellite",
                    })
                  );
                }}
                color="success"
                className="text-black"
              >
                Use geospatial `data to identify soil type.
              </Checkbox>
            </div>
          </div>
        </Tab>
      </Tabs>
    </div>
  );
};

const SoilInfo_ = () => {
  return (
    <div className="  h-full flex gap-16 justify-center items-center flex-col ">
      <Options />
    </div>
  );
};

export default SoilInfo_;
