import { useEffect, useRef, useState } from "react";
import { useAppDispatch, useAppSelector } from "../../../Redux/hooks";
import {
  Modal,
  ModalBody,
  ModalContent,
  ModalFooter,
  ModalHeader,
  Textarea,
  useDisclosure,
} from "@nextui-org/react";
import {
  FeatureGroup,
  LayerGroup,
  LayersControl,
  MapContainer,
  Pane,
  Polygon,
  TileLayer,
  ZoomControl,
} from "react-leaflet";
import { EditControl } from "react-leaflet-draw";
import Shapefile, { handleShapefile } from "./Addshapefile";
import { Button } from "@nextui-org/react";
import { ReactSVG } from "react-svg";
import locIcon from "../../../assets/locationIcon.svg";
import uplIcon from "../../../assets/uploadIcon.svg";
import drIcon from "../../../assets/polygonIcon.svg";
import { updateFarmerInfo } from "../../../Redux/Farmer/actions";
import { green, yellow } from "@mui/material/colors";
import L from "leaflet";
import { FileCard, FileUploader } from "evergreen-ui";
import { message } from "antd";
import Dragger_ from "./Dragger";
import { useLocation } from "react-router-dom";

export const CreateFieldOptions = (prop: { map: L.Map }) => {
  const { isOpen, onOpen, onOpenChange } = useDisclosure();
  const [Coordinates, SetCoordinates] = useState();
  const [isShapefile, setIsShapefile] = useState(false);
  const [shapeFile, setShapefile] = useState();
  const [target, setTarget] = useState();
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  return (
    <>
      <Button
        onClick={() => {
          setIsShapefile(false);
        }}
        onPress={onOpen}
        radius="full"
        className="bg-scBgGreen w-44 text-[#072B1F] z-10 grow p-8 text-[16px]"
      >
        <ReactSVG src={locIcon} />
        Add Coordinates
      </Button>
      <Button
        onClick={() => {
          dispatch(updateFarmerInfo({ DrawOption: !Data.DrawOption }));
        }}
        radius="full"
        className="bg-scBgGreen w-44 p-8 text-[#072B1F] z-10 grow text-[16px]"
      >
        <ReactSVG src={drIcon} />
        Draw Polygon
      </Button>
      <Button
        onPress={onOpen}
        onClick={() => {
          setIsShapefile(true);
        }}
        radius="full"
        className="bg-scBgGreen w-44 text-[#072B1F] z-10 grow p-8 text-[16px]"
      >
        <ReactSVG src={uplIcon} />
        Upload ShapeFile
      </Button>
      <Modal className="" isOpen={isOpen} onOpenChange={onOpenChange}>
        <ModalContent className="max-w-[30%] min-w-[400px] font-Myfont font-bld">
          {(onClose) => (
            <>
              <ModalHeader className="flex flex-col gap-1">{}</ModalHeader>
              <ModalBody className="flex justify-center items-end p-3">
                {isShapefile ? (
                  <Dragger_ />
                ) : (
                  <Textarea
                    key={"bordered"}
                    variant={"bordered"}
                    label="Coordinates"
                    labelPlacement="inside"
                    placeholder="Enter your Coordinates"
                    className="col-span-12 md:col-span-6 mb-6 md:mb-0"
                    onChange={(e) => {
                      // const v = JSON.parse(e.target.value);
                      setTarget(e.target.value);
                    }}
                  />
                )}
              </ModalBody>
              <ModalFooter>
                <Button
                  onClick={() => {
                    console.log();
                    try {
                      if (!isShapefile) {
                        let cr = JSON.parse(target);
                        cr = cr.map((coord) => [coord[1], coord[0]]);
                        SetCoordinates(cr);
                        if (Data.polygon_) prop.map!.removeLayer(Data.polygon_);
                        const polygon = L.polygon(cr, {
                          color: green[900],
                        }).addTo(prop.map as L.Map);
                        prop.map!.fitBounds(L.polygon(cr).getBounds());
                        dispatch(updateFarmerInfo({ polygon_: polygon }));
                      } else {
                      }
                      onOpenChange();
                    } catch (e) {
                      message.error("Invalid coordinates format");
                    }
                  }}
                  className="bg-[#48A788] text-white"
                  radius="full"
                >
                  Submit
                </Button>
              </ModalFooter>
            </>
          )}
        </ModalContent>
      </Modal>
    </>
  );
};

const AddField = (prop: { options_: boolean }) => {
  const path = useLocation();

  const MapRef = useRef<L.Map>();
  const [isDraw, setIsDraw] = useState(false);
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  const location = useLocation();
  const _onCreate = (e) => {
    const geoJson = JSON.stringify(e.layer.toGeoJSON());
    dispatch(
      updateFarmerInfo({
        Field: geoJson,
      })
    );
    console.log(e.layer.toGeoJSON().geometry.coordinates);
  };
  const flyToField = () => {
    if (MapRef.current && Data.currentField) {
      console.log("tetstst")
      const boundaries = Data.currentField?.boundaries.coordinates[0];
      const bounds = boundaries!.map((coord) => [coord[1], coord[0]]);
      MapRef.current.flyToBounds(bounds);
      dispatch(updateFarmerInfo({ boundaries: bounds }));
    }
  };
  useEffect(() => {
    dispatch(updateFarmerInfo({ Map: MapRef.current }));
    flyToField();
  }, [Data.currentField, path.pathname]);
  return (
    <div className="w-full h-full relative map-c">
      <MapContainer
        center={[30, -8]}
        zoom={6}
        ref={MapRef}
        style={{ width: "100%", height: "100%" }}
        zoomControl={false}
      >
        <LayersControl position="bottomright">
          <LayersControl.BaseLayer checked name="Satellite">
            <LayerGroup>
              <TileLayer
                attribution="Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community"
                url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
              />
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
                url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager_only_labels/{z}/{x}/{y}{r}.png"
              />
            </LayerGroup>
          </LayersControl.BaseLayer>
        </LayersControl>
        <ZoomControl position="bottomright" />
        {Data.boundaries && (
          <Polygon
            positions={Data.boundaries}
            pathOptions={{ color: "yellow" }}
          />
        )}
        <FeatureGroup>
          {Data.DrawOption && (
            <EditControl
              position="bottomright"
              onCreated={_onCreate}
              // onEdited={_onEdited}
              // onDeleted={_onDeleted}
              draw={{
                polygon: {
                  isDraw,
                  shapeOptions: {
                    color: yellow[900],
                    weight: 4,
                  },
                },
                polyline: false,
                circle: false,
                marker: false,
                circlemarker: false,
                rectangle: false,
              }}
            />
          )}
        </FeatureGroup>
        {<Shapefile removeLayer={false} />}
      </MapContainer>

      {/* <div className="w-full absolute top-0 z-5 flex justify-center p-2">
                <Input onChange={(e) => {
                    dispatch(setFieldName(e.target.value))
                    console.log(e.target.value)
                }} radius="full" size="sm" classNames={{ inputWrapper: 'bg-scBgGreen' }} className="absolute z-10 w-[30%] " placeholder="Field name" type="text">

                </Input>
            </div> */}
      {prop.options_ && (
        <div className="w-full absolute top-0 z-5 flex justify-center p-2 pt-6 gap-4 font-Myfont font-md ">
          <CreateFieldOptions map={MapRef.current} />
        </div>
      )}
    </div>
  );
};

export default AddField;
