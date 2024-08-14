import React, { useEffect, useState } from "react";
import { useAppDispatch, useAppSelector } from "../../Redux/hooks";
import { SetWaterShedId,SetLoadingMsg } from "../../Redux/Policymaker/Actions";
import { loukkous_r } from "../../assets/Watershed/SvgCoordinates/Loukkous";
import { OumErRbia_r } from "../../assets/Watershed/SvgCoordinates/Oum Er Rbia";
import { souss_r } from "../../assets/Watershed/SvgCoordinates/Souss Massa";
import { sahara_r } from "../../assets/Watershed/SvgCoordinates/Sahara";
import { bouregreg_r } from "../../assets/Watershed/SvgCoordinates/Bouregreg";
import { sebou_r } from "../../assets/Watershed/SvgCoordinates/Sebou";
import { guirZizRhris_r } from "../../assets/Watershed/SvgCoordinates/Guir - Ziz - Rhris";
import { tensift_r } from "../../assets/Watershed/SvgCoordinates/Tensift";
import { daraa_r } from "../../assets/Watershed/SvgCoordinates/Daraa";
import { moulouya_r } from "../../assets/Watershed/SvgCoordinates/Moulouya";

const MrMap = () => {
    const dispatch = useAppDispatch()
    const Data = useAppSelector((state) => state.policyMaker)

    const [position, SetPosition] = useState({ x: 0, y: 0 })
    const [isHover, SetisHover] = useState(false);
    const [WatershedName, SetWatershedName] = useState("");
    useEffect(() => {
        const handleMouseMove = (event) => {
            SetPosition({ x: event.clientX, y: event.clientY });
        };
        document.addEventListener('mousemove', handleMouseMove);
    }, []);
    const pathObj = (name: string) => {
        const Obj = {
            onMouseLeave: () => SetisHover(false),
            onMouseEnter: () => { SetisHover(true); SetWatershedName(name) },
            onClick: () => { dispatch(SetWaterShedId(name)); dispatch(SetLoadingMsg("Processing Your Request"))},
        }
        return (Obj)
    }

    return (
        <div className="w-full flex justify-center items-center">
            {isHover &&
                <div style={{
                    position: "absolute",
                    left: position.x + 10,
                    top: position.y + 10,
                    transition: 'left 0.3s ease, top 0.3s ease',
                }}
                    className={`bg-white w-[150px] h-10 z-20 rounded-r-lg rounded-tl-0 rounded-bl-lg font-Myfont flex justify-center items-center font-lt`}>
                    <p>{WatershedName}</p>
                </div>
            }

            <svg className="w-[40%] min-w-[300px] relative" viewBox="0 0 393 369" xmlns="http://www.w3.org/2000/svg">

                <path
                    {...pathObj("Loukkous")}
                    className={Data.WatershedId != "Loukkous" ? "fill-[#18614A] hover:opacity-50 hover:cursor-pointer"
                        : "fill-[#D29569]"} d={loukkous_r} />

                <path
                    {...pathObj("Oum Er Rbia")}
                    className={Data.WatershedId != "Oum Er Rbia" ? "fill-[#13825F] hover:opacity-50 hover:cursor-pointer"
                        : "fill-[#D29569]"} d={OumErRbia_r} />

                <path
                    {...pathObj("Souss Massa")}
                    className={Data.WatershedId != "Souss Massa" ? "fill-[#13825F] hover:opacity-50 hover:cursor-pointer"
                        : "fill-[#D29569]"} d={souss_r} />

                <path
                    {...pathObj("Sahara")}
                    className={Data.WatershedId != "Sahara" ? "fill-[#6CB09A] hover:opacity-50 hover:cursor-pointer"
                        : "fill-[#D29569]"} d={sahara_r} />

                <path
                    {...pathObj("Bouregreg")}
                    className={Data.WatershedId != "Bouregreg" ? "fill-[#3C8E74] hover:opacity-50 hover:cursor-pointer"
                        : "fill-[#D29569]"}
                    stroke="#EAF3E9" strokeWidth="0.98" d={bouregreg_r} />

                <path
                    {...pathObj("Sebou")}
                    className={Data.WatershedId != "Sebou" ? "fill-[#227359] hover:opacity-50 hover:cursor-pointer"
                        : "fill-[#D29569]"}
                    stroke="#EAF3E9" strokeWidth="0.98" d={sebou_r} />

                <path
                    {...pathObj("Guir - Ziz - Rhris")}
                    className={Data.WatershedId != "Guir - Ziz - Rhris" ? "fill-[#227359] hover:opacity-50 hover:cursor-pointer"
                        : "fill-[#D29569]"}
                    stroke="#EAF3E9" strokeWidth="0.98" d={guirZizRhris_r} />

                <path
                    {...pathObj("Tensift")}
                    className={Data.WatershedId != "Tensift" ? "fill-[#227359] hover:opacity-50 hover:cursor-pointer"
                        : "fill-[#D29569]"}
                    stroke="#EAF3E9" strokeWidth="0.98" d={tensift_r} />

                <path
                    {...pathObj("Daraa")}
                    className={Data.WatershedId != "Daraa" ? "fill-[#3C8E74] hover:opacity-50 hover:cursor-pointer"
                        : "fill-[#D29569]"}
                    stroke="#EAF3E9" strokeWidth="0.98" d={daraa_r} />

                <path
                    {...pathObj("Moulouya")}
                    className={Data.WatershedId != "Moulouya" ? "fill-[#18614A] hover:opacity-50 hover:cursor-pointer"
                        : "fill-[#D29569]"}
                    stroke="#EAF3E9" strokeWidth="0.98" d={moulouya_r} />

            </svg>
        </div>

    )
};

export default MrMap