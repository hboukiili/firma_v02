import { useEffect, useRef } from "react";
import { MultiChart_ } from "../Aquacrop";
import { updateFarmerInfo } from "../../../Redux/Farmer/actions";
import { useAppDispatch, useAppSelector } from "../../../Redux/hooks";
import { Button, Divider, Select, SelectItem } from "@nextui-org/react";
import { ReactSVG } from "react-svg";
import arrowNarrowRight from "../../../assets/arrow-narrow-right.svg";
import infoIcn from "../../../assets/info-square-rounded.svg";
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
        <div className="relative p-[6px] rounded-[30px] w-full blurBg z-30">
          <div className="w-full h-full flex flex-col gap-2 items-start p-4 pl-5 bg-white rounded-[23px]">
            <div className="flex flex-col">
              <p className="font-bld text-[18px]">Plant Growth Stages :</p>
              <p className="font-nrml text-[18px]">Emergence</p>
            </div>
            <Divider className="" />
            <div className="flex items-start gap-2">
              <ReactSVG className="-ml-1 fill-blue-gray-500" src={infoIcn} />
              <p className="text-blue-gray-500">
                The tip of the leaf barely emerges from the aerial coleoptile.
              </p>
            </div>
            {/* <div className="flex items-center justify-center pr-2 p-4 gap-4 bg-[#e4e9e4] w-[30%] h-full rounded-[23px]">
              <div>
                <p className="font-bld text-[18px] text-gray-700">Gdd</p>
                <p className="font-bld text-[18px] text-gray-800">344 C°</p>
              </div>
              <ReactSVG src={arrUp} />
            </div> */}
          </div>
        </div>
      </div>
    </div>
  );
};

const Charts_ = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  return (
    <div className="w-[68%] flex flex-col ml-4 mt-2 rounded-[30px] bg-[#fff] ">
      <div className="p-2">
        <Select
          // defaultSelectedKeys={Data.currentField?.name}
          size="sm"
          radius={"full"}
          label="Select field"
          className="max-w-[260px] "
          key={11}
          classNames={{
            trigger: "bg-gray-200",
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
      <Divider className="" />
      <div className="w-full   rounded-[25px] h-[29%]  flex flex-col gap-3 pr-4 px-6 p-3 ">
        <p className="font-bld  text-[#3a3a3a]">
          Water availability (Rain & Irrigation)
        </p>
        <MultiChart_
          Data={{
            datasets: [
              {
                data: Data.RasterData?.Rain.mean,
                name: "Rain",
                type: "bar",
                yAxisId: 1, // Rain on Y-axis 0
                color: "#4fb6f5",
                forecastCount: 5,
              },
              {
                data: Data.RasterData?.Irrig.max,
                name: "Irrigation",
                type: "bar",
                yAxisId: 2, // Irrigation also on Y-axis 0
                color: "#2866eb",
                forecastCount: 5,
              },
            ],
            yAxes: [
              { id: 1, title: "Rain (mm)" },
              { opposite: true, id: 2, title: "Irrigation (mm)" },
            ],
          }}
        />
      </div>
      <Divider className="" />
      <div className="w-full  h-[29%] px-6 flex flex-col gap-3 rounded-[25px]  pr-4 pt-3">
        <p className="font-bld  text-[#3a3a3a]">
          Crop water stress levels (Ks & Kcb)
        </p>
        <div className="h-[90%] w-full">
          <MultiChart_
            Data={{
              datasets: [
                {
                  data: Data.RasterData?.Kcb.mean,
                  name: "Kcb",
                  type: "line",
                  yAxisId: 2,
                  color: "#38f54f",
                  forecastCount: 5,
                },

                {
                  data: Data.RasterData?.Ks.mean,
                  name: "Ks",
                  type: "line",
                  yAxisId: 1,
                  color: "#f57b42",
                  forecastCount: 5,
                },
              ],
              yAxes: [
                { id: 1, title: "Ks" },
                { id: 2, title: "Kcb", opposite: true },
              ],
            }}
          />
        </div>
      </div>
      <Divider className="my-4" />
      <div className="w-full  h-[29%] px-6 rounded-[25px] flex flex-col gap-3  pr-4">
        <p className="font-bld  text-[#3a3a3a]">
          Measure water loss from soil and plants (Et & ET0)
        </p>
        <div className="h-[90%] w-full">
          <MultiChart_
            Data={{
              datasets: [
                {
                  data: Data.RasterData?.ETcadj.mean,
                  name: "ET",
                  type: "line",
                  yAxisId: 0, // ET on Y-axis 1
                  color: "#38f54f",
                  forecastCount: 5,
                },
                {
                  data: Data.RasterData?.ETref.mean,
                  name: "ET0",
                  type: "line",
                  yAxisId: 1, // ET0 on Y-axis 1
                  color: "#f57b42",
                  forecastCount: 5,
                },
              ],
              yAxes: [
                { id: 0, title: "ET (mm)" },
                { id: 1, title: "ET0 (mm)", opposite: true },
              ],
            }}
          />
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
          scrollTo: false,
        })
      );
    }
  }, [Data.scrollTo]);
  return (
    <div
      ref={scRef}
      className="font-Myfont h-screen w-screen flex gap-4  p-2 bg-[#e4ece3] pb-4"
    >
      {Data.RasterData?.Kcb.max && <Charts_ />}

      <div className="grow  flex gap-6 flex-col  pt-5  bg-white rounded-[30px] mt-2">
        <div className="w-full flex justify-between items-center px-8 ">
          <p className="font-bld text-[24px]">Soil & Crop Indicators</p>
          <Button
            isIconOnly
            radius="full"
            size="md"
            className=" text-white bg-Green"
            onClick={() => {
              window.scrollTo({
                top: 0, // Scroll to the top of the page
                behavior: "smooth", // Optional: Adds smooth scrolling
              });
            }}
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
