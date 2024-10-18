import React, {
  JSXElementConstructor,
  useEffect,
  useState,
  lazy,
  Suspense,
  useRef,
} from "react";
import titleSvg from "../assets/titlePlcy.svg";
import { ReactSVG } from "react-svg";
import {
  Button,
  DateRangePicker,
  Input,
  Modal,
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
  Pagination,
  Select,
  SelectItem,
  Spinner,
  divider,
  useDisclosure,
} from "@nextui-org/react";
import MrMap from "../Components/MrMap.tsx";
import { LineChart } from "@mui/x-charts";
import chroma, { scale } from "chroma-js";
import { useAppDispatch, useAppSelector } from "../../Redux/hooks.ts";
import fllsc from "../../assets/fullScreen.svg";
import MapIcon from "../../assets/mapicon.svg";
import Bg from "../assets/plcyBg.svg";
import Tensift from "../../assets/Watershed/SvgSubCoordinates/Tensift/Tensift.tsx";
import {
  SetBand,
  SetEndDate,
  SetIsSubmit,
  SetStartDate,
  SetSurfaceVariable,
  SetWaterShedId,
  SetWeather,
  SetisLoading,
  SetChartData,
  SetDates,
  SetIsBaseMap,
  SetFlux,
  SetIsGeoRaster,
  SetLoadingMsg,
} from "../../Redux/Policymaker/Actions.ts";
import plain from "../../assets/plain.svg";
import sun from "../../assets/rs.svg";
import api from "../../api/axios.js";
import {
  SurfaceVariable,
  Weather_,
  policyMaker,
} from "../../Redux/Policymaker/Slices.js";
import PuffLoader from "react-spinners/PuffLoader";
import * as d3 from "d3";
import gridBg from "../../assets/gridBg.png";

const SubWaterShed = lazy(
  () => import(`../../assets/Watershed/SvgSubCoordinates/Tensift/Tensift.tsx`)
);

export async function policyMakerData(Data: policyMaker) {
  let response;
  const EndPoint = Data.Band == "Flux" ? "pytseb/bassin/" : "irrigation/test/";
  await api
    .post(EndPoint, {
      Bassin: Data.WatershedId,
      start_date: Data.StartDate,
      end_date: Data.EndDate,
      band: Data.Band,
    })
    .then((res) => {
      console.log(res, "req->");
      response = res.data;
    })
    .catch((err) => {
      console.log(err);
    });
  return response;
}

// Data base

const TimeSeries = (Data: Weather_) => {
  let minValue: number = Math.min(...Data.values);
  let percentage: number = 0.2 * minValue;
  const dates = Data.dates.map((item) => new Date(item));

  return (
    <>
      <LineChart
        sx={{
          "& .MuiAreaElement-series-value": {
            fill: "#D2E7D4",
          },
          "& .MuiMarkElement-root": {
            width: "5px",
            fill: "#206f41",
            strokeWidth: 0,
          },
        }}
        xAxis={[
          {
            data: dates,
            scaleType: "time",
            valueFormatter: (dates) => {
              const year = dates.getFullYear().toString().slice(-2);
              const month = String(dates.getMonth() + 1).padStart(2, "0"); // Months are 0-based, so add 1 and pad with '0' if needed
              const day = String(dates.getDate()).padStart(2, "0");
              return `${day}-${month}-${year}`;
            },
          },
        ]}
        yAxis={[
          {
            min: minValue - percentage,
          },
        ]}
        series={[
          {
            id: "value",
            color: "#5BAD6B",
            data: Data.values,
            curve: "linear",
            area: true,
            showMark: false,
          },
        ]}
        margin={{ left: 40, right: 40, top: 10, bottom: 20 }}
      />
    </>
  );
};

export const InputsBar_ = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.policyMaker);
  const [allDataFormed, SetallDataFormed] = useState(true);
  const variables = [
    "Weather",
    "Surface Variable",
    "Flux",
    "Digital Elevation Model",
  ];
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
  ];
  useEffect(() => {
    // Data.Band &&
    Data.EndDate &&
      Data.StartDate &&
      Data.WatershedId &&
      SetallDataFormed(false);
  }, [Data]);
  return (
    <div className="flex w-full flex-col justify-center items-center gap-5 ">
      <Select
        selectedKeys={Data.WatershedId && new Set([Data.WatershedId])}
        size="md"
        radius={"full"}
        label={"Select Watershed"}
        className="w-full select-field"
        onChange={(e) => {
          if (!e.target.value) e.target.value = WatershedNames[0];
          dispatch(SetWaterShedId(e.target.value));
        }}
      >
        {WatershedNames.map((val, _) => {
          return (
            <SelectItem key={val} value={val}>
              {val}
            </SelectItem>
          );
        })}
      </Select>
      {/* <Select
        size="sm"
        radius={"full"}
        label="Select Band"
        className="max-w-[18rem] select-field"
        onChange={(e) => {
          dispatch(SetBand(e.target.value));
        }}
      >
        {variables.map((val, _) => {
          return (
            <SelectItem key={val} value={val}>
              {val}
            </SelectItem>
          );
        })}
      </Select> */}
      <DateRangePicker
        label="Time range"
        className="w-full"
        classNames={{ inputWrapper: "bg-white rounded-full p-4" }}
        onChange={(e) => {
          dispatch(SetStartDate(e.start.toString()));
          dispatch(SetEndDate(e.end.toString()));
        }}
      />
      {/* <Input
        id="date"
        size="sm"
        label="Start Date"
        variant="bordered"
        placeholder="Start Date"
        type={"date"}
        radius={"full"}
        classNames={{
          base: "w-full",
          inputWrapper: ["bg-white", "border-none"],
        }}
        required
        onChange={(e) => dispatch(SetStartDate(e.target.value))}
      />
      <Input
        size="sm"
        label="End Date"
        placeholder="End Date"
        type={"date"}
        radius={"full"}
        classNames={{
          base: "w-full",
          inputWrapper: ["bg-white"],
        }}
        required
        onChange={(e) => dispatch(SetEndDate(e.target.value))}
      /> */}
      <Button
        isDisabled={allDataFormed}
        onClick={() => {
          dispatch(SetLoadingMsg("Processing Your Request"));
          dispatch(SetIsSubmit(true));

          // policyMakerData(Data).then((res) => {
          //   Data.Band === "Weather"
          //     ? dispatch(SetWeather(res))
          //     : Data.Band === "Surface Variable"
          //     ? dispatch(SetSurfaceVariable(res))
          //     : dispatch(SetFlux(res));
          //   dispatch(SetIsSubmit(true));
          //   dispatch(SetisLoading(false));
          // });
        }}
        radius="full"
        className="bg-[#48A788] text-white font-Myfont w-full"
      >
        Submit
      </Button>
    </div>
  );
};

const MrMapOption = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.policyMaker);

  return (
    <div className="w-full h-full flex justify-center items-center">
      <MrMap />
    </div>
  );
};

function GetData(): SurfaceVariable[] | Weather_[] {
  const Data = useAppSelector((state) => state.policyMaker);
  if (Data.Band === "Surface Variable") return Data.SurfaceVariable;
  else if (Data.Band === "Weather") return Data.Weather;
  else return Data.Flux;
}

const RaseterAndLegend = (prpo: { vr: number; ImgIndex: number }) => {
  const Data = GetData();
  const max = Math.max(...Data[prpo.vr].values);
  const min = Math.min(...Data[prpo.vr].values);
  return (
    <div className="w-full flex justify-center items-center flex-col gap-8">
      <img
        className="w-[60%] drop-shadow-lg "
        src={Data[prpo.vr].url[prpo.ImgIndex - 1]}
        alt=""
      />
      <Lengend max={max} min={min} />
    </div>
  );
};

export const Lengend = (prop: { min: number; max: number }) => {
  const scale = chroma.scale("RdYlGn");
  const [Value, SetValue] = useState({ color: scale(12).hex(), value: "" });
  return (
    <div className="w-full max--[300px] p-4 rounded-lg flex justify-center items-center gap-3 bg-[#D3E1D1]">
      <div className="w-[20%]  flex gap-2 items-center">
        <p>{Value.value}</p>
        <span
          style={{ backgroundColor: Value.color }}
          className={`min-w-5 h-5 rounded-md`}
        ></span>
      </div>
      <div className="grow  overflow-hidden rounded-md hover:cursor-crosshair justify-center flex">
        {Array.from({ length: 100 }, (_, i) => {
          // if(i >= )
          return (
            <span
              onMouseEnter={() => {
                SetValue({
                  color: scale(i / 100).hex(),
                  value: (prop.min + i / 100).toFixed(2),
                });
              }}
              onMouseLeave={() => {
                SetValue({ color: scale(0).hex(), value: prop.min.toFixed(2) });
              }}
              style={{ backgroundColor: scale(i / 100).hex() }}
              className={`grow h-5 hover:opacity-5`}
            ></span>
          );
        })}
      </div>
    </div>
  );
};

const ImgOptions = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.policyMaker);
  const SelectItems: { [category: string]: string[] } = {
    Weather: [
      "Temperature",
      "Wind speed",
      "Humidity",
      "Solar Radiation",
      // "Rain",g
    ],
    "Surface Variable": ["NDVI", "LST", "LAI", "FC"],
    Flux: ["LE", "ET_day"],
  };
  const [ImgIndex, SetImgIndex] = useState(1);
  const [variable, SetVariable] = useState(0);
  // const defaultKey = SelectItems[Data.Band][0].toString();
  return (
    <div className="w-full h-full  flex flex-col items-center gap-10">
      <div className="flex w-full justify-between items-center gap-2">
        <Select
          size="sm"
          radius={"lg"}
          label="Select Variable"
          className="grow select-field"
          // defaultSelectedKeys={[defaultKey]}
          onChange={(e) => {
            //i should fix this !!!!!!!
            let v = e.target.value;
            if (v === "LAI" || v === "Solar Radiation") SetVariable(3);
            if (v === "LST" || v === "Wind speed") SetVariable(2);
            if (v === "FC" || v === "ET_day" || v === "Temperature")
              SetVariable(1);
            if (v === "NDVI" || v === "LE" || v === "Humidity") SetVariable(0);
          }}
        >
          {SelectItems["Surface Variable"].map((val, _) => {
            return (
              <SelectItem key={val} value={val}>
                {val}
              </SelectItem>
            );
          })}
        </Select>

        <Button
          isDisabled={Data.isLoading}
          isIconOnly
          onClick={() => {
            dispatch(SetWaterShedId(""));
            dispatch(SetIsBaseMap(true));
            dispatch(SetLoadingMsg("Please Select a Watershed"));
          }}
          className="bg-[#48A788] w-[5%] text-white"
          size="lg"
          radius="lg"
        >
          <ReactSVG className="w-[60%] stroke-[7px] fill-white" src={MapIcon} />
        </Button>

        <Button
          isDisabled
          isIconOnly
          className="bg-[#48A788] w-[5%] text-white"
          size="lg"
          radius="lg"
        ></Button>

        <Button
          isDisabled={Data.isLoading}
          className="bg-[#48A788] w-[30%] text-white"
          onClick={() => dispatch(SetIsGeoRaster(!Data.IsGeoRaster))}
          size="lg"
          radius="full"
        >
          {Data.IsGeoRaster ? "Hide Raster" : "Show Raster"}
        </Button>
      </div>
      <Suspense fallback={<div>waiting...</div>}>
        {Data.IsGeoRaster ? (
          <div
            id="test"
            className={`w-full flex flex-col justify-center items-center gap-10`}
          >
            <RaseterAndLegend vr={variable} ImgIndex={ImgIndex} />
          </div>
        ) : (
          <div className="w-full relative flex overflow-hidden pt-10 mt-10 justify-center items-center">
            <img
              className="absolute opacity-[20%] w-full"
              src={gridBg}
              alt=""
            />
            {!Data.WatershedId ? <MrMap /> : <SubWaterShed />}
          </div>
        )}
      </Suspense>
      <div className="w-full  flex flex-col gap-4 text-DarkGreen justify-center items-center">
        {Data.IsGeoRaster && (
          <>
            <p className="font-Myfont font-smbld ">
              {Data.Dates[ImgIndex - 1].toDateString()}
            </p>
            <Pagination
              page={ImgIndex}
              onChange={SetImgIndex}
              classNames={{
                item: "border-[#D3E1D1] text-DarkGreen",
                cursor: "bg-[#48A788]",
              }}
              variant="bordered"
              showControls
              total={Data.Dates.length}
              initialPage={1}
            />
          </>
        )}
      </div>
    </div>
  );
};

const MainChart = (prop: {
  item: Weather_ | SurfaceVariable;
  onOpen: () => void;
  band: string;
}) => {
  const dispatch = useAppDispatch();
  return (
    <div
      className={`font-Myfont font-bld w-[98%] h-[190px] flex flex-col gap-4`}
    >
      <div className="flex justify-between ">
        <p className="text-DarkGreen">{prop.item.type}</p>
        <Button
          className="bg-transparent"
          isIconOnly
          onPress={prop.onOpen}
          onClick={() => {
            dispatch(SetChartData(prop.item));
          }}
        >
          <ReactSVG
            className="fill-[#8cda9c] hover:fill-[#5BAD6B]"
            src={fllsc}
          />
        </Button>
      </div>
      <TimeSeries
        type={prop.item.type}
        dates={prop.item.dates}
        values={prop.item.values}
      />
    </div>
  );
};

const Loading = () => {
  const Data = useAppSelector((state) => state.policyMaker);
  return (
    <div className="flex flex-col justify-center items-center gap-2 font-Myfont font-md text-[12px] text-[#286952] h-[600px] bgblack">
      <PuffLoader className="" color="#48A788" />
      <p>{Data.loadingMsg}</p>
    </div>
  );
};

// const Policymaker = () => {
//   const dispatch = useAppDispatch();
//   const Data = useAppSelector((state) => state.policyMaker);
//   const { isOpen, onOpen, onOpenChange } = useDisclosure();
//   let CurrentData: SurfaceVariable[] | Weather_[] = GetData();
//   const bands = [
//     { name: "Weather", icon: sun },
//     { name: "Surface Variable", icon: plain },
//     { name: "Flux", icon: "" },
//     // { name: "Digital Elevation Model", icon: "" }
//   ];
//   if (!isOpen) dispatch(SetChartData(null));
//   useEffect(() => {
//     if (
//       !Data.IsAllDataReceived &&
//       Data.isSubmit &&
//       Data.WatershedId &&
//       Data.IsBaseMap
//     ) {
//       policyMakerData(Data).then((res) => {
//         if (Data.Band === "Weather" && !Data.Weather.length)
//           dispatch(SetWeather(res));
//         else if (
//           Data.Band === "Surface Variable" &&
//           !Data.SurfaceVariable.length
//         ) {
//           dispatch(SetSurfaceVariable(res));
//         } else if (Data.Band === "Flux" && !Data.Flux.length)
//           dispatch(SetFlux(res));
//         if (Data.Band === "Weather" && Data.IsBaseMap)
//           dispatch(SetWeather(res));
//         else if (Data.Band === "Surface Variable" && Data.IsBaseMap) {
//           dispatch(SetSurfaceVariable(res));
//         } else if (Data.Band === "Flux" && Data.IsBaseMap)
//           dispatch(SetFlux(res));
//         dispatch(SetisLoading(false));
//         dispatch(SetIsBaseMap(false));
//       });
//     } else dispatch(SetisLoading(false));
//   }, [Data.WatershedId, Data.Band]);

//   return Data.isLoading ? (
//     <Loading />
//   ) : !Data.ChartData ? (
//     <div
//       className={`w-[99%] flex justify-center overflow-hidden h-screen pt-4  ${
//         !Data.isSubmit
//           ? "flex-col gap-14 items-center justify-center pt-7"
//           : " items-center flex-row justify-center grow pb-3 "
//       }`}
//     >
//       <div
//         className={` z-10 flex flex-col justify-center gap-4 pt-6 ${
//           Data.isSubmit
//             ? "relative w-[50%] order-2 bg-[#EAF3E9] rounded-[10px] h-full overflow-y-scroll justify-start"
//             : "w-[75%] "
//         }`}
//       >
//         {!Data.isSubmit ? (
//           <div className="w-full flex flex-col justify-center items-center gap-4 ">
//             <p className="font-Myfont font-md text-[#194233] text-[14px]">
//               Select a watershed, band, and date range to effectively analyze
//               and visualize your data.
//             </p>
//             <div className="flex  items-center gap-4 w-full max-w-[900px] justify-center">
//               <InputsBar_ />
//             </div>
//           </div>
//         ) : Data.WatershedId && !Data.IsBaseMap ? (
//           <div className="flex flex-col justify-start items-center gap-12 w-full p-4 h-[1000px] absolute top-0">
//             {CurrentData.map((item, _) => {
//               return <MainChart band={Data.Band} item={item} onOpen={onOpen} />;
//             })}
//           </div>
//         ) : (
//           <Loading />
//         )}
//       </div>
//       <div
//         className={`z-10 flex justify-start  order-1  ${
//           !Data.isSubmit
//             ? "w-[100%] items-center justify-center"
//             : "w-[50%] h-full justify-start gap-4 pr-4 "
//         }`}
//       >
//         <div
//           className={
//             !Data.isSubmit
//               ? "w-[60%] flex justify-center items-center transition-all pr-8 "
//               : "transition-all grow  h-full bg-[#EAF3E9] rounded-[10px] flex flex-col justify-center gap-16 items-center p-3"
//           }
//         >
//           {(!Data.isSubmit || !Data.WatershedId) && !Data.isLoading ? (
//             !Data.isSubmit ? (
//               <MrMap />
//             ) : (
//               <MrMapOption />
//             )
//           ) : (
//             <ImgOptions />
//           )}
//         </div>
//         {Data.isSubmit && (
//           <div
//             className={`${
//               Data.IsGeoRaster
//                 ? "w-[0%] h-full transition-all overflow-hidden"
//                 : " transition-all h-full w-[15%] bg-white flex flex-col gap-2 justify-start items-center p-2 rounded-[10px]"
//             }`}
//           >
//             {!Data.IsGeoRaster &&
//               bands.map((value, _) => {
//                 return (
//                   <Button
//                     isDisabled={Data.isLoading}
//                     onClick={() => {
//                       // the req sent twice
//                       dispatch(SetLoadingMsg("Processing Your Request"));
//                       if (Data.Band != value.name) {
//                         dispatch(SetBand(value.name));
//                         if (!Data.IsAllDataReceived)
//                           dispatch(SetIsBaseMap(true));
//                       }
//                     }}
//                     className={`hover:bg-[#EAF3E9] w-full h-20
//                                     flex justify-center p-1 gap-2 items-center text-[#0c4e27] flex-col border-[3px] border-[#EAF3E9] rounded-lg
//                                     ${
//                                       Data.Band === value.name
//                                         ? "bg-[#EAF3E9] text-[#0c4e27]"
//                                         : "bg-transparent"
//                                     }`}
//                   >
//                     <ReactSVG
//                       className={`${
//                         value.name === "Weather" ? "w-[30%]" : "w-[25%]"
//                       } fill-[#0c4e27]`}
//                       src={value.icon}
//                     />
//                     <p className="font-bld text-[10px] ">{value.name}</p>
//                   </Button>
//                 );
//               })}
//           </div>
//         )}
//       </div>
//     </div>
//   ) : (
//     <Modal className="left-10" isOpen={isOpen} onOpenChange={onOpenChange}>
//       <ModalContent className="max-w-[88%] font-Myfont font-bld">
//         {(onClose) => (
//           <>
//             <ModalHeader className="flex flex-col gap-1">
//               {Data.ChartData!.type}
//             </ModalHeader>
//             <ModalBody className="flex justify-center items-end p-3">
//               <div
//                 className={`font-Myfont font-bld w-[98%] h-[190px] flex justify-center items-center`}
//               >
//                 <TimeSeries
//                   dates={Data.ChartData!.dates}
//                   values={Data.ChartData!.values}
//                 />
//               </div>
//             </ModalBody>
//             <ModalFooter>
//               <Button className="bg-[#48A788] text-white" radius="full">
//                 Download as csv
//               </Button>
//             </ModalFooter>
//           </>
//         )}
//       </ModalContent>
//     </Modal>
//   );
// };

const Pform = () => {
  return (
    <div className="flex bg-[#EAF3E9] rounded-2xl h-[635px] w-[1500px] justify-between mt-12">
      <div className="w-[580px] font-Myfont flex flex-col ml-16 p-20 items-start justify-center gap-9">
        <div className="flex flex-col items-start">
          <p className="text-[32px] font-bld text-[#58726C]">Welcome Back,</p>
          <p className="text-[#58726C] text-[14px]">
            Use the map of Morocco to choose a watershed or select its name
            manually. Set the start and end dates to refine your data selection.
          </p>
        </div>
        <InputsBar_ />
      </div>
      <div className="relative h-full w-[670px] flex justify-center items-center">
        <img
          className="absolute top-0 right-0 w-full opacity-[50%]"
          src={gridBg}
          alt=""
        />
        <MrMap />
      </div>
    </div>
  );
};

const Bands_ = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.policyMaker);
  const bands = [
    { name: "Weather", icon: sun },
    { name: "Indices", icon: plain },
    { name: "Evapotranspiration", icon: plain },
    { name: "Surface Variable", icon: plain },
    { name: "Land cover", icon: plain },
    { name: "Soil", icon: plain },
    // { name: "Digital Elevation Model", icon: "" }
  ];
  return (
    <>
      {!Data.IsGeoRaster &&
        bands.map((value, _) => {
          return (
            <Button
              isDisabled={Data.isLoading}
              onClick={() => {
                // the req sent twice
                dispatch(SetLoadingMsg("Processing Your Request"));
                if (Data.Band != value.name) {
                  dispatch(SetBand(value.name));
                  if (!Data.IsAllDataReceived) dispatch(SetIsBaseMap(true));
                }
              }}
              className={`hover:bg-[#EAF3E9] w-full h-20
                                    flex justify-center p-1 gap-2 items-center text-[#0c4e27] flex-col border-[3px] border-[#EAF3E9] rounded-2xl
                                    ${
                                      Data.Band === value.name
                                        ? "bg-[#EAF3E9] text-[#0c4e27]"
                                        : "bg-transparent"
                                    }`}
            >
              <ReactSVG
                className={`${
                  value.name === "Weather" ? "w-[20%]" : "w-[15%]"
                } fill-[#0c4e27]`}
                src={value.icon}
              />
              <p className="font-bld text-[10px] ">{value.name}</p>
            </Button>
          );
        })}
    </>
  );
};

const DataView_ = () => {
  return (
    <div className="w-full pb-28 flex  gap-2 flex-wrap">
      <div className="grow rounded-3xl p-2  max-w-[850px] min-w-[650px] flex flex-col">
        <ImgOptions />
      </div>
      <div className="grow rounded-3xl max-w-[130px] h-[820px] bg-white flex flex-col gap-2 p-2">
        <Bands_ />
      </div>
      <div className="grow rounded-3xl bg-[#EAF3E9] min-w-[650px] h-[820px]"></div>
    </div>
  );
};



const Policymaker = () => {
  const Data = useAppSelector((state) => state.policyMaker);

  return (
    <div className="w-full p-2 flex flex-col justify-center items-center ">
      {Data.isSubmit ? <DataView_ /> : <Pform />}
    </div>
  );
};

export default Policymaker;
