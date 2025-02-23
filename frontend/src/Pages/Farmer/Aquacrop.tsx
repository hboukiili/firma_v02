import { useEffect, useState } from "react";
import api from "../../api/axios.js";
import ReactApexCharts from "react-apexcharts";
import { getDateRange } from "./Dashboard.tsx";
import { useAppDispatch, useAppSelector } from "../../Redux/hooks.ts";
import { Button, DateInput, Select, SelectItem } from "@nextui-org/react";
import { updateFarmerInfo } from "../../Redux/Farmer/actions.ts";
import AddField from "./tools/addField.tsx";
import { CalendarDate } from "@internationalized/date";
import canld from "../../assets/canld.png";
import PuffLoader from "react-spinners/PuffLoader";
import { format } from "date-fns";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ComposedChart,
} from "recharts";
interface DataSet {
  name: string;
  data: number[];
  color: string;
  type: "line" | "bar";
  yAxisId: number;
  forecastCount?: number; // Number of forecasted points
}

interface YAxisConfig {
  id: number;
  title: string;
  opposite?: boolean;
}

interface ChartProps {
  Data: {
    datasets: DataSet[];
    DateRange: string[];
    yAxes: YAxisConfig[];
  };
}

export const MultiChart_ = ({ Data }: ChartProps) => {
  const { DateRange, datasets, yAxes } = Data;
  const Data_ = useAppSelector((state) => state.farmer);

  let DateRange_ = DateRange ? DateRange : Data_.DateRange;

  // Ensure chartData is structured properly
  const chartData = DateRange_.map((date, index) => {
    let entry: Record<string, any> = { date };

    datasets.forEach((dataset) => {
      const totalPoints = dataset.data.length;
      const forecastIndex = totalPoints - dataset.forecastCount!; // Start of forecast points

      entry[dataset.name] = dataset.data[index];

      // If index is within forecasted range, separate actual and forecasted values
      if (dataset.forecastCount && index >= forecastIndex) {
        entry[`${dataset.name}_forecast`] = dataset.data[index]; // Forecasted values
        entry[`${dataset.name}_actual`] = null; // Hide from actual line
      } else {
        entry[`${dataset.name}_actual`] = dataset.data[index]; // Actual values
        entry[`${dataset.name}_forecast`] = null; // Hide from forecasted line
      }
    });

    return entry;
  });

  return (
    <ResponsiveContainer width="100%" className="">
      <ComposedChart data={chartData}>
        <CartesianGrid strokeDasharray="2 2" />
        <XAxis
          dataKey="date"
          tickFormatter={(date) => format(new Date(date), "dd MMM")} // Formats as "01 Jan"
          tick={{ fontSize: 10 }} // Reduces font size
          axisLine={false}
        />

        {/* Generate multiple Y-Axes dynamically */}
        {yAxes.map((axis) => (
          <YAxis
            padding={{ top: 20 }}
            key={axis.id}
            yAxisId={axis.id}
            axisLine={false}
            label={{
              value: axis.title,
              angle: -90,
              style: {
                marginLeft: "10px", // Margin on the left
                marginRight: "10px",
                fontWeight: "bold",
                fontSize: 14,
              },

              dx: axis.opposite ? 20 : -20,

              // dy: -20,
            }}
            orientation={axis.opposite ? "right" : "left"} // Right or left placement
          />
        ))}

        <Tooltip formatter={(value) => value.toFixed(2)} />

        <Legend
          wrapperStyle={{ paddingTop: "0px" }}
          iconSize={0}
          layout="horizontal"
          height={0}
          iconType="circle"
          align="right"
          verticalAlign="bottom"
        />

        {/* Render datasets dynamically based on type */}
        {datasets.map((dataset) =>
          dataset.type === "bar" ? (
            <Bar
              key={dataset.name}
              dataKey={dataset.name}
              fill={dataset.color}
              yAxisId={dataset.yAxisId}
            />
          ) : (
            <>
              {/* Solid line for actual data (shows in legend) */}
              <Line
                key={`${dataset.name}_actual`}
                type="monotone"
                dataKey={`${dataset.name}_actual`}
                stroke={dataset.color}
                yAxisId={dataset.yAxisId}
                strokeWidth={2}
                dot={false}
                name={dataset.name} // Keep in legend
              />

              {/* Dashed line for forecasted data (HIDDEN in legend) */}
              <Line
                key={`${dataset.name}_forecast`}
                type="monotone"
                dataKey={`${dataset.name}_forecast`}
                stroke={dataset.color}
                yAxisId={dataset.yAxisId}
                strokeWidth={2}
                dot={false}
                strokeDasharray="5 5"
                name=" " // Hide from legend
              />
            </>
          )
        )}
      </ComposedChart>
    </ResponsiveContainer>
  );
};

// export const MultiChart_ = ({ Data, annotations }: ChartProps) => {
//   const Data_ = useAppSelector((state) => state.farmer);
//   const series = Data.datasets.map((dataset) => ({
//     name: dataset.name,
//     data:
//       // dataset.name === "Rain"
//       //   ? dataset.data.map((v) => {
//       //       if (v) return v;
//       //       return "-";
//       //     })
//       //   :
//       dataset.data,
//     color: dataset.color,
//     type: dataset.type,
//     id: dataset.yAxisId,
//   }));

//   // Handle range area by combining min and max arrays into pairs
//   if (Data.rangeArea && Data.rangeArea.max && Data.rangeArea.min) {
//     const rangeData = Data.DateRange.map((date, index) => ({
//       x: new Date(date).getTime(), // Convert date to timestamp
//       y: [Data.rangeArea.min[index], Data.rangeArea.max[index]],
//     }));

//     series.push({
//       name: "Range Area",
//       data: rangeData,
//       type: "rangeArea", // Make sure ApexCharts supports this type if using a range area
//       color: "#b0e57c",
//       fill: {
//         type: "gradient",
//         gradient: {
//           shade: "light",
//           type: "vertical",
//           opacityFrom: 0.5,
//           opacityTo: 0,
//         },
//       },
//     });
//   }

//   const options = {
//     forecastDataPoints: {
//       count: Data.DateRange ? 7 : 5,
//     },
//     chart: {

//       toolbar: {
//         show: true,
//         offsetX: -30,
//         // offsetY: 10,
//       },
//       animations: {
//         enabled: false,
//       },
//     },
//     tooltip: {
//       enabled: true,
//       shared: true,
//       intersect: false,
//       followCursor: true,
//       x: { show: true },
//       y: { show: true },
//     },
//     dataLabels: { enabled: false },
//     stroke: { curve: "smooth", width: 4 },
//     grid: {
//       row: { colors: ["#f3f3f3", "transparent"], opacity: 0.5 },

//     },
//     xaxis: {
//       categories: Data.DateRange ? Data.DateRange : Data_.DateRange,
//       type: "datetime",
//       tickAmount: 6,
//       // min: new Date("15 Jan 2024").getTime(),
//       // max: new Date("30 May 2024").getTime(),
//     },
//     yaxis: Data.yAxes.map((axis) => ({
//       opposite: axis.opposite || false,
//       title: { text: axis.title },
//       labels: {
//         formatter: (value: number) => value.toFixed(2),
//       },
//     })),
//     legend: {
//       position: "top",
//       horizontalAlign: "start",
//       // floating: true,

//       offsetX: 5,
//       // offsetX: 100,
//     },
//     // annotations: {
//     //   yaxis: annotations, // Pass the annotations prop here
//     // },
//   };

//   let updatedOptions;
//   if (annotations)
//     updatedOptions = {
//       ...options,
//       annotations: { yaxis: annotations },
//     };
//   else updatedOptions = options;

//   return (
//     <ReactApexCharts
//       className="grow"
//       height="100%"
//       options={updatedOptions}
//       series={series}
//     />
//   );
// };

const Aquacrop = () => {
  return <div></div>;
};

export default Aquacrop;
