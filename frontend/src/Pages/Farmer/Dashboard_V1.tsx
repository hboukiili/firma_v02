import React, { useEffect, useRef, useState } from "react";
import AddField, { drawnItems } from "./tools/addField";
import {
  Button,
  Modal,
  Select,
  SelectItem,
  Tooltip,
  useDisclosure,
} from "@nextui-org/react";
import { updateFarmerInfo } from "../../Redux/Farmer/actions";
import { useAppDispatch, useAppSelector } from "../../Redux/hooks";
import api from "../../api/axios.js";
import { ReactSVG } from "react-svg";
import createIcn from "../../assets/create.svg";
import anime from "animejs/lib/anime.es.js";
import locationIcn from "../../assets/locationIcn.svg";
import deleteIcn from "../../assets/deleteIcn.svg";
import polygonIcn from "../../assets/PolygonIcon.svg";
import uploadIcn from "../../assets/uploadIcn.svg";
import * as L from "leaflet";
import "leaflet-draw";
import { MapRef_ } from "./tools/addField";
import { DrawTools, SetupModal } from "./tools/modals.js";
import { useMap } from "react-leaflet";

export const DrawFieldTools = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const [isShapefile, setIsShapefile] = useState(false);
  const toolRef = useRef(null);
  const [DrawPoly, setDrawPoly] = useState(false);
  const [setupButton, SetSetupBtn] = useState(false);
  let deleteMode = false;
  let polygonDrawer: L.Draw.Polygon;
  const polygonDrawerRef = useRef<L.Draw.Polygon>(); // Use ref to keep track of the polygon drawer

  function enablePoly() {
    polygonDrawerRef.current = new L.Draw.Polygon(MapRef_, {
      allowIntersection: false,
      repeatMode: false,
      shapeOptions: {
        color: !deleteMode ? "#F5D152" : "#fff",
        weight: 4,
        opacity: 0.7,
      },
      showArea: true,
      metric: false,
    });
    polygonDrawerRef.current.enable();
    MapRef_.on(L.Draw.Event.CREATED, function (event) {
      const layer = event.layer;

      // Add the polygon to drawnItems so it stays on the map
      drawnItems.addLayer(layer);

      // Handle the polygon data (e.g., convert to GeoJSON)
      const geoJson = JSON.stringify(layer.toGeoJSON());
      dispatch(
        updateFarmerInfo({
          Field: geoJson,
        })
      );

      // Optionally enable editing
      layer.editing.enable();

      // Disable the drawing tool after creation
      polygonDrawerRef.current.disable();
    });
  }
  
  useEffect(() => {
    anime({
      targets: toolRef.current,
      translateX: 100,
      delay: 50,
      easing: "spring(0, 100, 10, 0)",
    });
    anime({
      width: "200px",
      targets: ".CnStp",
      delay: 50,
    });
  }, []);

  function deleteLayers() {
    drawnItems.clearLayers();
  }

  const drawTools = [
    {
      icon: polygonIcn,
      info: "Draw Polygon",
    },

    {
      icon: uploadIcn,
      info: "Upload ShapeFile",
    },
    {
      icon: locationIcn,
      info: "Add Coordinates",
    },
    {
      icon: deleteIcn,
      info: "Delete layer",
    },
  ];

  return (
    <>
      {setupButton && (
        <div className="CnStp p-[4px] overflow-hidden transition-all font-Myfont self-end relative z-10 order-2  ">
          <Button
            onPress={onOpen}
            className="rounded-full font-bld  bg-[#4FC38F] text-white"
          >
            Continue Field Setup
          </Button>
        </div>
      )}
      <div
        ref={toolRef}
        className="relative left-[-100px] w-[60px] h-[200px] p-[4px] rounded-full justify-self-end  bg-white/50 backdrop-blur-sm border-[2px] border-white z-10"
      >
        <div className="bg-white w-full h-full rounded-full flex gap-4 flex-col items-center justify-center p-2">
          {drawTools.map((v) => {
            return (
              <>
                <Tooltip showArrow content={v.info} placement="right-start">
                  <Button
                    onPress={() => {
                      if (v.info === "Upload ShapeFile") {
                        setIsShapefile(true);
                        onOpen();
                      } else if (v.info === "Add Coordinates") {
                        setIsShapefile(false);
                        onOpen();
                      } else if (v.info === "Draw Polygon") {
                        enablePoly();
                      } else {
                        deleteLayers();
                      }
                    }}
                    isIconOnly
                    className="bg-transparent"
                  >
                    <ReactSVG src={v.icon} />
                  </Button>
                </Tooltip>
              </>
            );
          })}
        </div>

        <Modal
          className=""
          isOpen={isOpen}
          onOpenChange={onOpenChange}
          onClose={() => {
            // MapRef_.removeLayer(layer);
            dispatch(updateFarmerInfo({ DrawOption: false }));
            polygonDrawer.disable();
          }}
        >
          {isShapefile ? (
            <SetupModal isShapefile={true} isOpen_={isOpen} />
          ) : (
            <DrawTools />
          )}
        </Modal>
      </div>
    </>
  );
};

const Dashboard_v1 = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  const ref = useRef(null);

  useEffect(() => {
    api.get("/farmer/field").then((res) => {
      dispatch(updateFarmerInfo({ fieldInfo: res.data }));
    });
    anime({
      targets: ref.current,
      delay: 3000,
      width: "560px",
      easing: "easeOutBack",
    });

    if (!Data.fieldInfo)
      api.get("/farmer/field").then((res) => {
        dispatch(updateFarmerInfo({ fieldInfo: res.data }));
      });
    api
      .post("/api/ogimet", {
        field_id: Data.currentField?.id,
        start_date: "2024-06-17",
        end_date: "2024-06-25",
      })
      .then((res) => {
        console.log(res.data);
        // setWeatherData(res.data);
      });
  }, [Data.currentField, Data.DrawOption]);
  return (
    <div className="w-dvw pb-3 pr-4 h-svh absolute top-0 pt-[85px] font-Myfont">
      <div className="w-full h-full  relative flex justify-between">
        <div className="w-full h-full ml-2 absolute top-0 rounded-[10px] overflow-hidden">
          <AddField options_={false} />
        </div>
        <div className="font-Myfont m-2 ml-4 flex flex-col justify-between ">
          <div
            ref={ref}
            className="overflow-hidden w-0  flex flex-col z-10 gap-2"
          >
            <div className="w-[480px] p-2 h-[70px] flex gap-2 justify-center items-center rounded-full border-white border-[2px]   backdrop-blur-sm bg-white/30">
              <Select
                // defaultSelectedKeys={Data.currentField?.name}
                size="sm"
                radius={"full"}
                label="Select field"
                className="w-[260px]"
                classNames={{
                  trigger: "bg-white",
                }}
                onChange={(e) => {
                  dispatch(
                    updateFarmerInfo({
                      currentField: Data.fieldInfo[e.target.value],
                    })
                  );
                }}
              >
                {Data.fieldInfo.map((val, _) => {
                  return (
                    <SelectItem key={_} value={val.name}>
                      {val.name}
                    </SelectItem>
                  );
                })}
              </Select>
              <Button
                className={
                  !Data.DrawOption
                    ? "bg-white text-[14px] grow flex justify-start gap-2 p-2"
                    : "bg-red-500 grow flex justify-center font-bld p-2 text-white"
                }
                radius="full"
                size="lg"
                startContent={!Data.DrawOption && <ReactSVG src={createIcn} />}
                onClick={() => {
                  if (Data.DrawOption) drawnItems.clearLayers();

                  dispatch(updateFarmerInfo({ DrawOption: !Data.DrawOption }));
                }}
              >
                {!Data.DrawOption ? "Create New Season" : "Cancel Creation"}
              </Button>
            </div>

            {/* <div className="flex flex-wrap justify-center items-center gap-2 p-2 w-[480px] h-[210px] rounded-[30px] border-white border-[2px]  backdrop-blur-sm bg-white/30">
              <div className="rounded-[17px] bg-white h-[85px] flex flex-col  w-[225px] items-center justify-center">
                <p className="font-bld text-[16px] ml-2 text-[#353636]">
                  Soil Surface Moisture
                </p>
                <div className="h-[40px] gap-2 w-[80%] flex items-center justify-center">
                  <p className="font-bld text-[28px] text-[#E79345]">
                    35<span className="text-[16px] font-bld">%</span>
                  </p>
                </div>
              </div>
              <div className="rounded-[17px] bg-white h-[85px] flex flex-col  w-[225px] items-center justify-center">
                <p className="font-bld text-[16px] ml-2 text-[#353636]">
                  Root Zone Moisture
                </p>
                <div className="h-[40px] gap-2 w-[80%] flex items-center justify-center">
                  <p className="font-bld text-[28px] text-[#3CC630]">
                    65<span className="text-[16px] font-bld">%</span>
                  </p>
                </div>
              </div>
              <div className="rounded-[17px] bg-white h-[85px] flex flex-col  w-[225px] items-center justify-center">
                <p className="font-bld text-[16px] ml-2 text-[#353636]">
                  Water Stress
                </p>
                <div className="h-[40px] gap-2 w-[80%] flex items-center justify-center">
                  <p className="font-bld text-[28px] text-Red">
                    20<span className="text-[16px] font-bld">%</span>
                  </p>
                </div>
              </div>
              <div className="rounded-[17px] bg-white h-[85px] flex flex-col  w-[225px] items-center justify-center">
                <p className="font-bld text-[16px] ml-2 text-[#353636]">
                  Water Stress
                </p>
                <div className="h-[40px] gap-2 w-[80%] flex items-center justify-center">
                  <p className="font-bld text-[28px] text-Red">
                    20<span className="text-[16px] font-bld">%</span>
                  </p>
                </div>
              </div>
            </div> */}
          </div>
          <div className="flex gap-2">
            {/* {Data.DrawOption && <DrawFieldTools />} */}
          </div>
        </div>
        <div className="w-[310px] flex flex-col gap-2 p-2 h-[98%] mt-2  z-10 bg-white/50 backdrop-blur-sm border-[2px] border-white rounded-[20px]">
          <div className="w-full h-[270px] bg-white rounded-[15px]"></div>
          <div className="w-full grow bg-white rounded-[15px]"></div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard_v1;
