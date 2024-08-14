import React, { useEffect, useState } from "react";
import CtAtlantiques from "./Côtiers atlantiques";
import Chaouia from "./Chaouia";
import Bouregreg_ from "./Bouregreg_";
import { useAppDispatch, useAppSelector } from "../../../../Redux/hooks";
import { SetSubWaterShedId } from "../../../../Redux/Policymaker/Actions";




const Bouregreg = () => {
    const [position, SetPosition] = useState({ x: 0, y: 0 })
    const [isHover, SetisHover] = useState(false);
    const [WatershedName, SetWatershedName] = useState("");
    useEffect(() => {
        const handleMouseMove = (event) => {
            SetPosition({ x: event.clientX, y: event.clientY });
        };
        document.addEventListener('mousemove', handleMouseMove);
    }, []);
    const dispatch = useAppDispatch()
    const Data = useAppSelector((state) => state.policyMaker)

    const pathObj = (name: string) => {
        const Obj = {
            onMouseLeave: () => SetisHover(false),
            onMouseEnter: () => { SetisHover(true); SetWatershedName(name) },
            onClick: () => { dispatch(SetSubWaterShedId(name)); },
            className: Data.SubWatershedId != name ?
                "fill-[#18614A] hover:opacity-50 hover:cursor-pointer"
                : "fill-[#D29569]"
        }
        return (Obj)
    }
    // Tamri Souss Massa Tiznit - Ifni
    return (
        <div className="flex">
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
            <svg width="330" height="167" viewBox="0 0 330 167" xmlns="http://www.w3.org/2000/svg">
                <path
                    {...pathObj("Bouregreg")}
                    d={Bouregreg_}
                />
                <path
                    {...pathObj("Côtiers Atlantiques")}
                    d={CtAtlantiques}
                />
                <path
                    {...pathObj("Chaouia")}
                    d={Chaouia} stroke="#EAF3E9" stroke-width="0.98"
                />
            </svg>
        </div>

    )
}

export default Bouregreg