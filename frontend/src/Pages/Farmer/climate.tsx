import React, { useEffect, useState } from "react";
import AddField from "./tools/addField";
import { ResponsiveLine_ } from "./Dashboard";
import { Select, SelectItem } from "@nextui-org/react";
import { useAppDispatch, useAppSelector } from "../../Redux/hooks";
import { updateFarmerInfo } from "../../Redux/Farmer/actions";
import api from "../../api/axios.js";
const Climate = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  const [WeatherData, setWeatherData] = useState<{
    station: string;
    "Rainfall mm": [];
    "Temperature C": [];
    "Visibility Km": [];
    "WinDir deg": [];
    "WindSpeed m.s-1": [];
    "Tdew C": [];
    "Pressure mb": [];
  }>();
  useEffect(() => {
    api
      .post("/api/ogimet", {
        field_id: Data.currentField?.id,
        start_date: "2024-05-04",
        end_date: "2024-05-15",
      })
      .then((res) => {
        setWeatherData(res.data);
      });
  }, [Data.currentField]);
  return (
    <div className="w-full p-2 flex gap-2 ">
      <div className="w-[33%] flex flex-col gap-2 ">
        <div className="relative w-full h-[650px] overflow-hidden rounded-[10px]">
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
              onChange={(e) => {
                console.log(e);
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
        <div className="w-full h-[280px] bg-scBgGreen rounded-[10px] "></div>
      </div>
      <div className="w-[67%] flex flex-col gap-2">
        <div className="w-full h-[315px] flex gap-2">
          {Array.from({ length: 4 }, (_, i) => {
            let Bg = !(i % 2) ? "#1E6F5C" : "#289672";
            return (
              <div
                style={{ backgroundColor: Bg }}
                className="h-full grow rounded-[10px]"
              ></div>
            );
          })}
        </div>
        <div className="w-full flex gap-2">
          <div className="w-[50%] flex flex-wrap gap-2">
            {Array.from({ length: 6 }, (_, i) => {
              let Bg = (!(i % 2) && i != 2) || i === 3 ? "#EAF3E9" : "#FFFF";
              return (
                <div
                  style={{ backgroundColor: Bg }}
                  className="h-[200px] w-[49%] rounded-[10px] flex flex-col content-cente"
                >
                  <div></div>
                  <div className="w-[70%] h-6">
                    <ResponsiveLine_ color="#C68E3A" />
                  </div>
                </div>
              );
            })}
          </div>
          <div className="grow bg-scBgGreen rounded-[10px]"></div>
        </div>
      </div>
    </div>
  );
};

export default Climate;
