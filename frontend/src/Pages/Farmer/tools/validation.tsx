import {
  getKeyValue,
  Table,
  TableBody,
  TableCell,
  TableColumn,
  TableHeader,
  TableRow,
} from "@nextui-org/react";
import { useAppDispatch, useAppSelector } from "../../../Redux/hooks";

const columns = [
  {
    key: "Attribute",
    label: "ATTRIBUTE",
  },
  {
    key: "EnteredValue",
    label: "ENTERED VALUE",
  },
];

const Validation = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  function SoilData() {
    if (Data.SoilType) return Data.SoilType;
    else if (Data.soilPr?.clay) {
      const { clay, sand, silt } = Data.soilPr;
      return `Clay : ${clay}, Sand : ${sand}, Silt : ${silt}`;
    }
  }

  function IrrigationData() {
    let result = [];
    const props = Data.IrrigationType?.prop;
    const type = Data.IrrigationType?.system;
    const plant = Data.PlantingDetails?.type;
    if (plant === "Crop") {
      if (type === "Sprinkler irrigation") {
        result.push(
          {
            key: "5",
            Attribute: "Sprinkler Coverage",
            EnteredValue: props?.sprinklerCoverage_c,
          },
          {
            key: "6",
            Attribute: "Water Outflow Rate",
            EnteredValue: props?.WaterOutflowRate_c,
          },
          {
            key: "7",
            Attribute: "Number of Sprinklers",
            EnteredValue: props?.numberOfSprinklers_c,
          }
        );
      } else if (type === "Drip irrigation") {
        result.push(
          {
            key: "5",
            Attribute: "Distance Between Tubes",
            EnteredValue: props?.DistanceBetweenTubes_c,
          },
          {
            key: "6",
            Attribute: "Distance Between Drippers",
            EnteredValue: props?.DistanceBetweenDrippers_c,
          }
        );
      }
    } else if (plant === "Tree") {
      if (type === "Sprinkler irrigation") {
        result.push(
          {
            key: "5",
            Attribute: "Sprinkler Coverage",
            EnteredValue: props?.sprinklerCoverage_c,
          },
          {
            key: "6",
            Attribute: "Water Outflow Rate",
            EnteredValue: props?.WaterOutflowRate_c,
          },
          {
            key: "7",
            Attribute: "Number of Sprinklers",
            EnteredValue: props?.numberOfSprinklers_c,
          }
        );
      } else if (type === "Drip irrigation") {
        result.push(
          {
            key: "5",
            Attribute: "Distance Between Rows",
            EnteredValue: props?.DistanceBetweenRows_t,
          },
          {
            key: "6",
            Attribute: "Distance Between Trees",
            EnteredValue: props?.DistanceBetweenTrees_t,
          },
          {
            key: "7",
            Attribute: "Number of Tubes Per Tree",
            EnteredValue: props?.NumberOfTubesPerTree_t,
          },
          {
            key: "8",
            Attribute: "Number of Drippers Per Tree",
            EnteredValue: props?.NumberOfDrippersPerTree_t,
          },
          {
            key: "9",
            Attribute: "Water Outflow Rate",
            EnteredValue: props?.WaterOutflowRate_t,
          }
        );
      }
    } else {
      if (type === "Sprinkler irrigation") {
        result.push(
          {
            key: "5",
            Attribute: "Sprinkler Coverage",
            EnteredValue: props?.sprinklerCoverage_c,
          },
          {
            key: "6",
            Attribute: "Water Outflow Rate",
            EnteredValue: props?.WaterOutflowRate_c,
          },
          {
            key: "7",
            Attribute: "Number of Sprinklers",
            EnteredValue: props?.numberOfSprinklers_c,
          }
        );
      } else if (type === "Drip irrigation") {
        result.push(
          {
            key: "5",
            Attribute: "Distance Between Tubes",
            EnteredValue: props?.DistanceBetweenTubes_c,
          },
          {
            key: "6",
            Attribute: "Distance Between Drippers",
            EnteredValue: props?.DistanceBetweenDrippers_c,
          },
          {
            key: "7",
            Attribute: "Distance Between Rows",
            EnteredValue: props?.DistanceBetweenRows_t,
          },
          {
            key: "8",
            Attribute: "Distance Between Trees",
            EnteredValue: props?.DistanceBetweenTrees_t,
          },
          {
            key: "9",
            Attribute: "Number of Tubes Per Tree",
            EnteredValue: props?.NumberOfTubesPerTree_t,
          },
          {
            key: "10",
            Attribute: "Number of Drippers Per Tree",
            EnteredValue: props?.NumberOfDrippersPerTree_t,
          },
          {
            key: "11",
            Attribute: "Water Outflow Rate",
            EnteredValue: props?.WaterOutflowRate_t,
          }
        );
      }
    }
    return result;
  }

  function plantType() {
    const type = Data.PlantingDetails?.type;
    let res: { text: string; date: string };
    if (type === "Tree")
      res = {
        text: Data.PlantingDetails!.Tree.value,
        date: Data.PlantingDetails!.Tree.date,
      };
    else if (type === "Crop")
      res = {
        text: Data.PlantingDetails!.Crop.value,
        date: Data.PlantingDetails!.Crop.date,
      };
    else {
      const tree = Data.PlantingDetails?.Tree.value;
      const crop = Data.PlantingDetails?.Crop.value;
      res = {
        text: `tree : ${tree}, crop : ${crop}`,
        date: Data.PlantingDetails!.Crop.date,
      };
    }
    return res;
  }

  const irrRows = IrrigationData();
  const rows = [
    {
      key: "1",
      Attribute: "Field name",
      EnteredValue: Data.fieldName,
    },
    {
      key: "2",
      Attribute: "Soil type",
      EnteredValue: SoilData(),
    },
    {
      key: "3",
      Attribute: "Plant type",
      EnteredValue: plantType().text,
    },
    {
      key: "4",
      Attribute: "Planting date",
      EnteredValue: plantType().date,
    },
    {
      key: "5",
      Attribute: "Irrigation system",
      EnteredValue: Data.IrrigationType?.system,
    },
  ];

  if (
    Data.IrrigationType?.system != "Rainfed irrigation" &&
    Data.IrrigationType?.system != "Surface irrigation"
  )
    rows.push(...irrRows);

  return (
    <div className="font-Myfont  w-[600px] flex flex-col gap-4">
      <div className="p-1">
        <p className="font-bld text-[40px]">Field Setup Validation</p>
        <p className=" font-md text-[12px]">
          Review your field setup details below, including irrigation and
          planting information. Ensure all entries are correct before submission
          to optimize your farming practices.
        </p>
      </div>
      <Table aria-label="Example table with dynamic content">
        <TableHeader columns={columns}>
          {(column) => (
            <TableColumn key={column.key}>{column.label}</TableColumn>
          )}
        </TableHeader>
        <TableBody items={rows}>
          {(item) => (
            <TableRow key={item.key}>
              {(columnKey) => (
                <TableCell>{getKeyValue(item, columnKey)}</TableCell>
              )}
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );
};

export default Validation;
