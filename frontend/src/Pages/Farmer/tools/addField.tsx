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
  WMSTileLayer,
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
import L, { Layer } from "leaflet";
import { FileCard, FileUploader } from "evergreen-ui";
import { message } from "antd";
import Dragger_ from "./Dragger";
import { useLocation, useParams } from "react-router-dom";
import { DrawFieldTools } from "../Dashboard_V1";
import AnimatedCursor from "react-animated-cursor";
import { Farmer } from "../../../Redux/Farmer/Interfaces";

export let MapRef_: L.Map = null;
export const drawnItems = new L.FeatureGroup();

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
        <ReactSVG className="fill-Red" src={drIcon} />
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

function requestGeoServerPixelValue(map: L.Map, geoServerUrl, Data: Farmer) {
  // Remove any existing click event listener to prevent duplicate events
  map.off("click");

  // Add a click event listener to the map
  map.on("click", function (e) {
    const layerName = `${Data.currentField?.id}:${Data.RasterKey}_${Data.currentDate}`;
    const latlng = e.latlng; // Get clicked coordinates

    // Define the parameters for GetFeatureInfo request
    const url =
      `${geoServerUrl}?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetFeatureInfo&LAYERS=${layerName}` +
      `&QUERY_LAYERS=${layerName}&STYLES=&BBOX=${map
        .getBounds()
        .toBBoxString()}` +
      `&FEATURE_COUNT=1&HEIGHT=${map.getSize().y}&WIDTH=${map.getSize().x}` +
      `&FORMAT=image/png&INFO_FORMAT=application/json&SRS=EPSG:4326&X=${Math.round(
        e.containerPoint.x
      )}` +
      `&Y=${Math.round(e.containerPoint.y)}`;

    // Make an AJAX request to GeoServer
    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        let content = "No data available";

        // Check if data exists in the response
        if (data.features && data.features.length > 0) {
          const properties = data.features[0].properties;
          // Dynamically get the first attribute in the feature properties
          const firstKey = Object.keys(properties)[0];
          const firstValue = properties[firstKey];

          content = `${firstValue.toFixed(2)}`;
        }

        // Create and show a popup at the clicked location with the data
        L.popup()
          .setLatLng(latlng)
          .setContent(`<pre>${content}</pre>`)
          .openOn(map);
      })
      .catch((err) => {
        console.error("Error fetching GeoServer data:", err);
      });
  });
}
const AddField = (prop: { options_: boolean }) => {
  const path = useLocation();
  const [zoomened, isZoomEnded] = useState(false);
  const MapRef = useRef<L.Map>();
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  const location = useLocation();
  const { page } = useParams();
  const [isLoad, setIsLoad] = useState(true);
  const flyToField = () => {
    setIsLoad(true);
    const len = Data.fieldInfo.length;
    if (MapRef.current && Data.currentField) {
      const boundaries = Data.currentField?.boundaries.coordinates[0];
      const bounds = boundaries!.map((coord) => [coord[1], coord[0]]);
      MapRef.current
        .flyToBounds(bounds, {
          duration: 1,
        })
        .on("moveend", () => setIsLoad(false));
      MapRef.current.on("zoomend", function () {
        isZoomEnded(true);
      });
      MapRef.current.on("zoomstart", function () {
        isZoomEnded(false);
      });
      dispatch(updateFarmerInfo({ boundaries: bounds }));
    } else if (MapRef.current && Data.fieldInfo[len - 1]) {
      const boundaries = Data.fieldInfo[len - 1].boundaries.coordinates[0];
      const bounds = boundaries!.map((coord) => [coord[1], coord[0]]);
      MapRef.current
        .flyToBounds(bounds, {
          duration: 1,
        })
        .on("moveend", () => setIsLoad(false));
      dispatch(updateFarmerInfo({ boundaries: bounds }));
    }
  };

  useEffect(() => {
    if (MapRef.current) {
      MapRef_ = MapRef.current;
      MapRef_.addLayer(drawnItems);
    }
    dispatch(updateFarmerInfo({ boundaries: null }));
    if (document.location.pathname.startsWith("/farmer1")) {
      flyToField();
      // setIsLoad(false);
    }
    if (Data.DrawOption && MapRef.current) MapRef.current.off("click");
    if (MapRef.current && Data.isRasterData) {
      MapRef.current.on("click",requestGeoServerPixelValue(
        MapRef_,
        "http://localhost:8080/geoserver/wms",
        Data
      ));
    }
  }, [
    Data.currentField?.name,
    path.pathname,
    MapRef.current,
    Data.RasterKey,
    Data.currentDate,
    Data.isRasterData,
  ]);
  const [tet, settet] = useState(false);
  return (
    <div
      onMouseEnter={() => {
        settet(true);
      }}
      onMouseLeave={() => {
        settet(false);
      }}
      className="w-full h-full relative map-c"
    >
      <div
        className={`absolute z-40 p-4 ${
          location.pathname.startsWith("/farmer1")
            ? "bottom-0 left-0"
            : "top-0 right-0"
        } `}
      >
        {prop.options_ && <DrawFieldTools />}
      </div>
      {Data.DrawOption && (
        <AnimatedCursor
          color="255, 255, 255"
          outerSize={12}
          innerSize={10}
          outerAlpha={0.1}
          innerScale={1.5}
          outerScale={8}
          innerStyle={{ zIndex: 9999 }}
          showSystemCursor={true}
        />
      )}

      <MapContainer
        center={[31, -8]}
        zoom={6}
        ref={MapRef}
        style={{
          width: "100%",
          height: "100%",
          backgroundColor: "transparent",
        }}
        zoomControl={false}
        // dragging={Data.Location === "Home"} // Disable dragging
      >
        {!page ? (
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
        ) : (
          <></>
          // <TileLayer url={whiteTileUrl} attribution="" />
        )}

        {Data.isRasterData && !Data.DrawOption && (
          <WMSTileLayer
            key={Data.RasterKey + Data.currentDate}
            url="http://localhost:8080/geoserver/wms"
            layers={`${Data.currentField?.id}:${Data.RasterKey}_${Data.currentDate}`}
            format="image/png"
            noWrap
            tileSize={512}
            transparent
            styles={
              Data.RasterKey === "Ks"
                ? "RedGreen"
                : Data.RasterKey === "rzsm_pr"
                ? "RedGreen2"
                : "irrStyle"
            }
            bounds={Data.boundaries}
          />
        )}
        {/* <ZoomControl position="bottomright" /> */}
        {/* {Data.boundaries &&
          zoomened &&
          !Data.DrawOption &&
          !Data.isRasterData && (
            <Polygon
              positions={Data.boundaries}
              pathOptions={{ color: "#F5D152" }}
            />
          )} */}

        {!Data.isRasterData &&
          !isLoad &&
          Data.fieldInfo.map((v, k) => {
            const boundaries = v.boundaries.coordinates[0];
            const bounds = boundaries!.map((coord) => [coord[1], coord[0]]);
            let color = "#fff";
            let opct = 0.5;
            if (v.name === Data.currentField?.name) {
              color = "#ffea00";
              opct = 1;
            }
            return (
              <Polygon
                opacity={9}
                key={k}
                positions={bounds}
                pathOptions={{ color: color, opacity: opct }}
              />
            );
          })}

        {<Shapefile removeLayer={false} />}
      </MapContainer>
      {/* {prop.options_ && (
        <div className="w-full absolute top-0 z-5 flex justify-center p-2 pt-6 gap-4 font-Myfont font-md ">
          <CreateFieldOptions map={MapRef.current} />
        </div>
      )} */}
    </div>
  );
};

export default AddField;
