import React from "react"
import FieldInformation from "./Fieldinformation"
import AddField from "./addField"
import Irrigationsystem_ from "./Irrigationsystem_"
import { Button } from "@material-tailwind/react";
import SoilInfo_ from "./Soilinforamtion";

interface Steps {
    name: string
}

const Steps = (prop: Steps) => {

    const Components: { [step: string]: JSX.Element } = {
        // "Add your first field": <AddField />,
        "Field information": <FieldInformation />,
        "Irrigation system": <Irrigationsystem_ />,
        "Soil information" : <SoilInfo_/>
    }

    return (
        <div className="w-full" >
            {Components[prop.name]}
        </div >
    )
}

export default Steps