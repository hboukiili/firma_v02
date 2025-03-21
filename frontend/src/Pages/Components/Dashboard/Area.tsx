import React , {useEffect, useState} from "react";
import api from "../../../api/axios.js"
const Area = (Field_id) => {
    const [Area, SetArea] = useState();
    useEffect(() => {
    console.log(Field_id)

        api.post('/api/area/', {
            field_id: Field_id.Field_id
          }).then((res) => {
            SetArea(res.data.area)
          });
    },[Field_id])
    return(
        <div className="h-[176px] w-[48%] bg-[#EAF3E9]   rounded-md flex flex-col justify-evenly items-center">
            <h5 className="font-Myfont font-smbld text-DarkGreen ">
            Area of Field
            </h5>
            <p className="font-Myfont font-smbld text-DarkGreen text-[50px]">{Area}
            <span className="font-Myfont font-smbld text-DarkGreen  text-[20px]">Ha</span>    
            </p>
        </div>
    )
}
export default Area