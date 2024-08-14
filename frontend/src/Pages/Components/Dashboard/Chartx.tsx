import { LineChart } from '@mui/x-charts';
// import { ResponsiveLine } from '@nivo/line'
import { Spinner } from '@nextui-org/react';
import React, { useRef, useState } from 'react';

interface Chart_ {
    Data: any;
    band: string;
    ref_: any;
}

const Chartx = (data: Chart_) => {
    console.log(data)
    let Title;
    if (!data)
        return (<></>)

    let dates;
    let Values;

    const Data = data.Data

    Values = Data.map((item) => item.value);
    dates = Data.map((item) => new Date(item.date));
    console.log(dates)
    Title = data.band + " Chart"



    return (
        <div className='bg-gray-50 w-full overflow-hidden   h-full flex justify-center pt-[0.5rem] flex-col items-center rounded-lg'>
            <h6 className='font-Myfont font-smbld text-[0.7rem] self-start pl-[1rem]' >{Title}</h6>
            <LineChart
                ref={data.ref_}
                xAxis={[
                    {
                        
                        data: dates,
                        scaleType: 'time',
                        valueFormatter: (dates) => {
                            const year = dates.getFullYear().toString().slice(-2);
                            const month = String(dates.getMonth() + 1).padStart(2, '0'); // Months are 0-based, so add 1 and pad with '0' if needed
                            const day = String(dates.getDate()).padStart(2, '0');
                            return (`${year}-${month}-${day}`)
                        },
                    }
                ]}
                series={[
                    {
                        color: "#5BAD6B",
                        data: Values,
                        // curve: "linear",
                        area: true,
                    },
                ]}
                margin={{ left: 40, right: 40, top: 30, bottom: 30 }}
            />
        </div>
    )
}

export default Chartx