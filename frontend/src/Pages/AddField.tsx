import React, { useState } from "react";
// import Map_ from "./Components/Dashboard/Map";
import { Button } from "@nextui-org/button";
import { FeatureGroup, LayerGroup, LayersControl, MapContainer, TileLayer } from "react-leaflet";
import { EditControl } from "react-leaflet-draw";
import PopUp from "./Components/PopUp";
import "./Components/Dashboard/style.css"


const FieldCrops = () => {
    const [selectedFile, setselectedFile] = useState(null);
    const [mapLayers, setMapLayers] = useState([]);
    const _onCreate = (e) => {
        const { layerType, layer } = e;
        if (layerType === "polygon") {
            const latlngs = layer
                .getLatLngs()[0]
                .map((latlng) => [latlng.lng, latlng.lat]);
            setMapLayers(latlngs);
        }
    };

    const _onEdited = (e) => {
        const {
            layers: { _layers },
        } = e;

        const editedLayers = Object.values(_layers);

        if (editedLayers.length > 0) {
            const editedLatlngs = editedLayers[0]._latlngs[0].map((latlng) => [
                latlng.lng,
                latlng.lat,
            ]);

            setMapLayers([...editedLatlngs]);
        }
    };

    const _onDeleted = (e) => {
        setMapLayers([]);
    };
    return (
        <div className="w-full h-screen flex flex-col items-center justify-center gap-[1rem] p-[2rem] md:flex-row">
            <div className=" w-[60%] h-[40%] md:h-[80%] md:p-[1rem] flex justify-center items-center">
                <div className="flex justify-center items-center  h-[100%] w-[100%] overflow-hidden rounded-[25px]">
                    <MapContainer center={[34.245242, -5.828727]} zoom={15}
                        style={{ width: "100%", height: "100%" }}>
                        <LayersControl>
                            <LayersControl.BaseLayer checked name="Satellite">
                                <LayerGroup>
                                    <TileLayer
                                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                                        url="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
                                    // opacity={0}
                                    />
                                    <TileLayer
                                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
                                        url='https://{s}.basemaps.cartocdn.com/rastertiles/voyager_only_labels/{z}/{x}/{y}{r}.png'
                                    />
                                </LayerGroup>
                            </LayersControl.BaseLayer>
                            
                            <LayersControl.BaseLayer name="Mapbox Map">
                                <TileLayer
                                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                                    url='https://tile.openstreetmap.org/{z}/{x}/{y}.png'
                                />
                            </LayersControl.BaseLayer>
                        </LayersControl>

                        <FeatureGroup>
                            {location.pathname != "/" &&
                                <EditControl
                                    position="topleft"
                                    onCreated={_onCreate}
                                    onEdited={_onEdited}
                                    onDeleted={_onDeleted}
                                    draw={{
                                        polygon: {
                                            shapeOptions: {
                                                color: '#FFDC23',
                                                weight: 4
                                            },
                                        },
                                        polyline: false,
                                        circle: false,
                                        marker: true,
                                        circlemarker: false

                                    }}
                                />
                            }
                        </FeatureGroup>
                    </MapContainer>

                </div >
            </div>
            <form className="w-[30%] h-[20rem] flex flex-col gap-[1rem] items-center justify-center " action="">
                <div className="bg-gray-50 rounded-[1.5rem] w-full h-[70%] flex flex-col   justify-evenly items-center">
                    <Button radius="full" className="bg-Green text-white w-[80%]">Draw Polygon</Button>
                    <Button radius="full" className="bg-Green text-white w-[80%]">Upload ShapeFile</Button>
                    <Button radius="full" className="bg-Green text-white w-[80%]">Add Coordinates</Button>
                </div>
                <PopUp polygon={{ Boundry: mapLayers }} />
            </form>
        </div>
    )
}

export default FieldCrops;