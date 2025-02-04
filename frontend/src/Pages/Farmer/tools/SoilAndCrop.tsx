import { useEffect, useRef } from "react";
import { MultiChart_ } from "../Aquacrop";
import { updateFarmerInfo } from "../../../Redux/Farmer/actions";
import { useAppDispatch, useAppSelector } from "../../../Redux/hooks";
import { Button } from "@nextui-org/react";
import { ReactSVG } from "react-svg";
import arrowNarrowRight from "../../../assets/arrow-narrow-right.svg";
import w1 from "../../../assets/w1.jpg";
import w2 from "../../../assets/w2.jpg";
import w3 from "../../../assets/w3.jpg";
import w4 from "../../../assets/w4.jpg";
import arrUp from "../../../assets/arrows-up 1.svg";

const PlantDev = () => {
  return (
    <div className="bg-white w-full h-[100%] rounded-[25px]">
      <div className="relative h-full flex items-end w-full p-4">
        <img
          className="absolute flex z-10 top-0 left-0 object-cover w-full h-full rounded-[25px] rounded-t-none "
          src={w1}
          alt=""
        />
        <div className="relative p-[6px] rounded-[30px] w-full h-[100px] blurBg z-30">
          <div className="w-full h-full flex justify-between items-center  bg-white rounded-[23px]">
            <div className="flex flex-col ml-4">
              <p className="font-bld text-[18px]">Plant Growth Stages</p>
              <p className="font-nrml text-[18px]">Stage name</p>
            </div>
            <div className="flex items-center justify-center pr-2 p-4 gap-4 bg-[#e4e9e4] w-[30%] h-full rounded-[23px]">
              <div>
                <p className="font-bld text-[18px] text-gray-700">Gdd</p>
                <p className="font-bld text-[18px] text-gray-800">344 C°</p>
              </div>
              <ReactSVG src={arrUp} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const SoilAndCrop = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  const scRef = useRef(null);

  useEffect(() => {
    const { current } = scRef;
    if (current !== null && Data.scrollTo) {
      current.scrollIntoView({ behavior: "smooth" });
      dispatch(
        updateFarmerInfo({
          scrollTo: false
        })
      );
    }
  }, [Data.scrollTo]);
  return (
    <div
      ref={scRef}
      className="font-Myfont h-screen w-screen flex gap-4  p-2 bg-[#e4ece3] pb-4"
    >
      {Data.RasterData?.Kcb.max && (
        <div className="w-[68%]  flex flex-col justify-between ml-4 mt-2 rounded-[30px]    ">
          <div className="w-full   rounded-[25px] h-[300px] bg-[#fff] flex flex-col gap-3 pr-8 px-6 p-3 ">
            <p className="font-bld  text-[#3a3a3a]">Water availability (Rain & Irrigation)</p>
            <MultiChart_
              Data={{
                datasets: [
                  {
                    data: Data.RasterData?.Rain.mean,
                    name: "Rain",
                    type: "bar",
                    yAxisId: 1, // Rain on Y-axis 0
                    color: "#4fb6f5",
                    forecastCount: 5
                  },
                  {
                    data: Data.RasterData?.Irrig.max,
                    name: "Irrigation",
                    type: "line",
                    yAxisId: 1, // Irrigation also on Y-axis 0
                    color: "#2866eb",
                    forecastCount: 5
                  }
                ],
                yAxes: [
                  { id: 1, title: "Rain and Irrigation" },
                  { id: 1, title: "Irrigation" }
                ]
              }}
            />
          </div>

          <div className="w-full  h-[300px] bg-[#fff] px-6 flex flex-col gap-3 rounded-[25px]  pr-8 p-3">
            <p className="font-bld  text-[#3a3a3a]">Crop water stress levels (Ks & Kcb)</p>
            <MultiChart_
              Data={{
                datasets: [
                  {
                    data: Data.RasterData?.Kcb.mean,
                    name: "Kcb",
                    type: "line",
                    yAxisId: 1,
                    color: "#38f54f",
                    forecastCount: 5
                  },

                  {
                    data: Data.RasterData?.Ks.mean,
                    name: "Ks",
                    type: "line",
                    yAxisId: 1,
                    color: "#f57b42",
                    forecastCount: 5
                  }
                ],
                yAxes: [{ id: 1, title: "Kcb and Ks" }]
              }}
            />
            {/* <div className="w-[180px]  rounded-[18px] flexCenter bg-[#fff8e5]">
              <img className="w-[90px] opacity-85" src={ble} alt="" />
            </div> */}
          </div>

          <div className="w-full  h-[300px] bg-[#fff] px-6 rounded-[25px] flex flex-col gap-3  pr-8 p-3">
            <p className="font-bld  text-[#3a3a3a]">
              Measure water loss from soil and plants (Et & ET0)
            </p>
            <MultiChart_
              Data={{
                datasets: [
                  {
                    data: Data.RasterData?.ETcadj.mean,
                    name: "ET",
                    type: "line",
                    yAxisId: 0, // ET on Y-axis 1
                    color: "#38f54f",
                    forecastCount: 5
                  },
                  {
                    data: Data.RasterData?.ETref.mean,
                    name: "ET0",
                    type: "line",
                    yAxisId: 0, // ET0 on Y-axis 1
                    color: "#f57b42",
                    forecastCount: 5
                  }
                ],
                yAxes: [{ id: 0, title: "ET & ET0" }]
              }}
            />
          </div>
          {/* <div className="w-[50%] h-[850px] rounded-[25px]    p-3">
                <MultiChart_
                  Data={{
                    datasets: [
                      {
                        data: Data.Gdd,
                        name: "Gdd",
                        type: "line",
                        yAxisId: 3, // ET on Y-axis 1
                        color: "#db0f0f",
                      },
                      {
                        data: Data.RasterData?.Kcb.mean,
                        name: "Kcb",
                        type: "line",
                        yAxisId: 2,
                        color: "#6eb6f5",
                      },

                      {
                        data: Data.RasterData?.Ks.mean,
                        name: "Ks",
                        type: "line",
                        yAxisId: 2,
                        color: "#1fe6f3",
                      },
                    ],
                    yAxes: [
                      // { id: 0, title: "Irrigation",  },
                      { id: 3, title: "Gdd" },
                      { id: 2, title: "Ks & Kcb", opposite: true },
                    ],
                  }}
                  annotations={annotationsData}
                />
              </div> */}
        </div>
      )}
      <div className="grow  flex gap-6 flex-col  pt-5  bg-white rounded-[30px] mt-2">
        <div className="w-full flex justify-between items-center px-8 ">
          <p className="font-bld text-[24px]">Soil & Crop Indicators</p>
          <Button
            isIconOnly
            radius="full"
            size="md"
            className=" text-white bg-Green"
          >
            <ReactSVG className="-rotate-90" src={arrowNarrowRight} />
          </Button>
        </div>
        <PlantDev />
      </div>
    </div>
  );
};

export default SoilAndCrop;
