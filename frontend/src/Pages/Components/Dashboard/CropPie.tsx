import { PieChart } from "@mui/x-charts";
import React from "react";

const CropPie = () => {
  return (
    <PieChart
      slotProps={{
        legend: {
          hidden: true,
          direction: "row",
          position: { vertical: "bottom", horizontal: "middle" },
          padding: -10,
        },
      }}
      series={[
        {
          data: [
            { value: 10, color: "#289672", label: "Wheat" },
            { value: 15, color: "#1E6F5C", label: "Maize" },
            { value: 20, color: "#F6D743", label: "Potatoes" },
          ],
        },
      ]}
      // width={200}
      height={200}
      margin={{ right: 0, left: 0, top: 0, bottom: 40 }}
    />
  );
};

export default CropPie;
