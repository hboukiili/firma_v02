import React, { useEffect, useRef, useState } from "react";
import {
  FeatureGroup,
  ImageOverlay,
  MapContainer,
  Polygon,
  TileLayer,
  Popup,
  Marker,
  useMap,
  LayersControl,
  LayerGroup
} from 'react-leaflet'
import '../../../index.css'
import { useLocation, useNavigate } from "react-router-dom";
import { EditControl } from "react-leaflet-draw";
import api from "../../../api/axios.js"

interface Map {
  Bounds: any;
  field: any;
  imageUrl: any
  point: any
  setNdviPixel: React.Dispatch<React.SetStateAction<any>>;
  startDate: any;
  endDate: any;
  isPxLoaded: React.Dispatch<React.SetStateAction<boolean>>
}

function LeafletgeoSearch() {
  const map = useMap();
  useEffect(() => {
    const provider = new OpenStreetMapProvider();

    const searchControl = new GeoSearchControl({
      provider,
      marker: {
        icon
      }
    });

    map.addControl(searchControl);

    return () => map.removeControl(searchControl);
  }, []);

  return null;
}
const Map_ = (prop: Map) => {
  console.log(prop)
  const mapRef = useRef()
  const location = useLocation();
  const [Boundaries, SetBoundaries] = useState()
  const [Data, SetData] = useState<{test : string}>();
  const [point, setSelectedPoint] = useState();

  const flyToField = (Field) => {
    if (mapRef.current) {
      const boundaries = JSON.parse(Field[prop.field].boundaries);
      const bounds = boundaries.map((coord) => [coord[1], coord[0]]);
      mapRef.current.flyToBounds(bounds);
    }
  };
 
  const handleMarkerClick = (latlng) => {
    // setSelectedPoint([latlng.lat, latlng.lng]); // Update the clicked point
    // Make API call to fetch NDVI time series for the selected pixel 
    let Point = [latlng.lng, latlng.lat]
    // Make API call to fetch NDVI time series for the selected pixel
    api.post('/api/tsonepixel/', {
      start_date: prop.startDate,
      end_date: prop.endDate,
      point: Point,
    })

      .then(response => {
        console.log(response);
        prop.setNdviPixel(response.data.ndvi);
        prop.isPxLoaded(true);
        console.log("Time series data for the selected pixel:", response.data.ndvi);
      })

      .catch(error => {
        console.log(error);
      });
  };

  useEffect(() => {
    api.get("/api/field/")
      .then((res) => {
        if (prop.field) {
          console.log("here")
          SetBoundaries(res.data[prop.field]?.boundaries)
          SetData(res.data)
        }
        else {
          Object.keys(res.data).map(key => { SetBoundaries(res.data[key]?.boundaries), SetData(res.data[key]) })
        }
        return res
      })
      .then((res) => {
        flyToField(res.data)
      })

  }, [prop.field])
  return (
    <div className="flex justify-center items-center  h-[100%] w-[100%] overflow-hidden rounded-lg">
      <MapContainer center={[34.245242, -5.828727]} zoom={10} ref={mapRef}
        style={{ width: "100%", height: "100%" }}>
        <LayersControl>
          <LayersControl.BaseLayer checked name="Satellite">
            <LayerGroup>
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
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


        {Boundaries && !prop.imageUrl &&
          <Polygon positions={JSON.parse(Boundaries).map(coord => [coord[1], coord[0]])} pathOptions={{ color: 'yellow' }} />
        }
        <FeatureGroup>
          {location.pathname != "/" && !prop.imageUrl &&
            <EditControl
              position="topleft"
              draw={{
                polygon: {
                  shapeOptions: {
                    color: '#5BAD6B',
                    weight: 3
                  },
                },
                polyline: false,
                circle: false,
                marker: false,
                circlemarker: false
              }}
            />
          }
          {prop.point &&
            <EditControl
              onCreated={(e) => {
                const latlng = e.layer.getLatLng();
                setSelectedPoint([latlng.lat, latlng.lng]);
                handleMarkerClick(latlng);
              }}
              position="topright"
              draw={{
                polyline: false,
                circle: false,
                marker: prop.point,
                circlemarker: false,
                polygon: false,
                rectangle: false,
              }}
            />
          }
        </FeatureGroup>
        {prop.imageUrl && prop.Bounds &&
          <ImageOverlay url={prop.imageUrl} bounds={prop.Bounds} />
        }
      </MapContainer>

    </div >
  );
}

export default Map_