import TiznitIfni from "./Tiznit - Ifni"
import Massa from "./Massa"
import Tamri from "./Tamri"
import Souss from "./Souss"
import { useEffect, useState } from "react"
import { useAppDispatch, useAppSelector } from "../../../../Redux/hooks"
import { SetSubWaterShedId } from "../../../../Redux/Policymaker/Actions"
const SoussMassa = () => {
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
            <svg className="w-[45%] min-w-[360px] relative" viewBox="0 0 331 254" xmlns="http://www.w3.org/2000/svg">
                <path
                    {...pathObj("Tiznit - Ifni")}
                    d={TiznitIfni}
                />
                <path
                    {...pathObj("Massa")}
                    d={Massa} stroke="#EAF3E9" stroke-width="0.98"
                />
                <path
                    {...pathObj("Tamri")}
                    d={Tamri}
                />
                <path
                    {...pathObj("Souss")}
                    d={Souss} stroke="#EAF3E9" stroke-width="0.98"
                />
            </svg>

        </div>
    )
}

export default SoussMassa