import React, { useEffect, useState } from "react";
import cotierEssaouira from "./Cotier Essaouira";
import tensift_ from "./tensift_r";
import { useAppDispatch, useAppSelector } from "../../../../Redux/hooks";
import { SetSubWaterShedId } from "../../../../Redux/Policymaker/Actions";
import anime from "animejs/lib/anime.es.js";


const Tensift = () => {
  const [position, SetPosition] = useState({ x: 0, y: 0 });
  const [isHover, SetisHover] = useState(false);
  const [WatershedName, SetWatershedName] = useState("");
  useEffect(() => {
    const handleMouseMove = (event) => {
      SetPosition({ x: event.clientX, y: event.clientY });
    };
    document.addEventListener("mousemove", handleMouseMove);
    anime({
      targets: ".bsn",
      duration: 5000,
      opacity: 1,
    });
  }, []);
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.policyMaker);

  const pathObj = (name: string) => {
    const Obj = {
      onMouseLeave: () => SetisHover(false),
      onMouseEnter: () => {
        SetisHover(true);
        SetWatershedName(name);
      },
      onClick: () => {
        dispatch(SetSubWaterShedId(name));
      },
      className:
        Data.SubWatershedId != name
          ? "fill-[#18614A] hover:opacity-50 hover:cursor-pointer"
          : "fill-[#D29569]",
    };
    return Obj;
  };

  return (
    <div className="flex w-full justify-center items-center bsn opacity-0 drop-shadow-2xl">
      {isHover && (
        <div
          style={{
            position: "absolute",
            left: position.x,
            top: position.y - 210,
            transition: "left 0.3s ease, top 0.3s ease",
          }}
          className={`bg-white w-[150px] h-10 z-20 rounded-r-lg rounded-tl-0 rounded-bl-lg font-Myfont flex justify-center items-center font-lt`}
        >
          <p>{WatershedName}</p>
        </div>
      )}
      <svg
        className="w-[75%] max-h-[400px] h-full  relative"
        viewBox="0 0 337 260"
        xmlns="http://www.w3.org/2000/svg"
      >
        {Data.SubWatersheds[Data.WatershedId]?.item.map((item, _) => {
          return (
            <>
              <path
                {...pathObj(item.name)}
                stroke="#EAF3E9"
                stroke-width="0.98"
                d={item.d}
              />
            </>
          );
        })}
        {/* <path
                    {...pathObj("Cotier Essaouira")}
                    d={cotierEssaouira} />
                <path
                    {...pathObj("Tensift")}
                    d={tensift_} stroke="#EAF3E9" stroke-width="0.98" /> */}
      </svg>
    </div>
  );
};

export default Tensift;
