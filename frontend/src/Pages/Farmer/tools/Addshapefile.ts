import L from "leaflet";
import { useEffect, useRef } from "react";
import { useMap } from "react-leaflet";
import JSZip from "jszip";
import { message, Upload } from "antd";
import shp from "shpjs";
import { useAppDispatch, useAppSelector } from "../../../Redux/hooks";
import { updateFarmerInfo } from "../../../Redux/Farmer/actions";
import { green } from "@mui/material/colors";

interface addCoordinates_ {
  map: any;
  latlngs: any;
  polygon: L.Polygon<any>;
}

export function AddCoordinates(prop: addCoordinates_) {
  if (prop.map) {
    prop.polygon = L.polygon(prop.latlngs, { color: green[900] }).addTo(
      prop.map
    );
    prop.map.fitBounds(L.polygon(prop.latlngs).getBounds());
  }
}

const checkZip = (prjFile, dbfFile, shpFile, shxFile) => {
  if (!prjFile) {
    message.error("No .prj file found in the zip");
  } else if (!dbfFile) {
    message.error("No .dbf file found in the zip");
  } else if (!shpFile) {
    message.error("No .shp file found in the zip");
  } else if (!shxFile) {
    message.error("No .shx file found in the zip");
  }
};

export const handleShapefile = async (e) => {
  let file = e;
  if (!file[0].name.endsWith(".zip")) {
    message.error("Please upload a zip file");
  } else {
    const zipFile = file[0];
    if (zipFile) {
      try {
        const zip = await JSZip.loadAsync(zipFile);
        console.log(zip);
        const shpFile = zip.file(/\.shp$/i)[0];
        const shxFile = zip.file(/\.shx$/i)[0];
        const prjFile = zip.file(/\.prj$/i)[0];
        const dbfFile = zip.file(/\.dbf$/i)[0];
        if (shpFile && shxFile && prjFile && dbfFile) {
          let tt = await extractShapes(file);
          message.success("Uploaded successfully");
          return tt;
          // const shpData = await shpFile.async('uint8array');
          // const shxData = await shxFile.async('uint8array');
          // const formData = new FormData();
          // formData.append('shpFile', new Blob([shpData]), 'file.shp');
          // formData.append('shxFile', new Blob([shxData]), 'file.shx');
        } else checkZip(prjFile, dbfFile, shpFile, shxFile);
      } catch (error) {
        console.log(error);
        message.error("Error reading zip file");
      }
    }
  }
};

const extractShapes = async (files: any) => {
  console.log("extractShapes", files);
  let result = {
    hasError: false,
    errorMessage: "",
    data: null,
  };

  const _formatShape = (_data) => {
    return _data.features;
  };

  const _parseFile = async (_file: any) => {
    let _result = {
      hasError: false,
      errorMessage: "",
      data: null,
    };

    try {
      let _data = await _file.arrayBuffer().then((_buffer) => shp(_buffer));
      _result.data = _formatShape(_data);
      if (_result.hasError) return _result;

      if (!_result.data || _result.data.length < 1) {
        _result.hasError = true;
        _result.errorMessage = "EXTRACT_FILE_EMPTY";
        message.error("EXTRACT_FILE_EMPTY");
      }
      return _result;
    } catch (err) {
      _result.hasError = true;
      _result.errorMessage = "EXTRACT_FILE_EMPTY";
      message.error("EXTRACT_FILE_EMPTY");
      return _result;
    }
  };
  // read the files
  result.data = await Promise.all(Array.prototype.map.call(files, _parseFile));

  if (result.hasError) return result;

  if (!result.data || result.data.length < 1) {
    result.hasError = true;
    result.errorMessage = "IMPORT_SHAPE_EMPTY";
    message.error("IMPORT_SHAPE_EMPTY");
  }

  return result.data[0].data;
};

export default function Shapefile({ removeLayer }: { removeLayer: boolean }) {
  const map = useMap();
  const Layer = useRef<L.GeoJSON | null>(null);
  const Data = useAppSelector((state) => state.farmer);
  const dispatch = useAppDispatch();

  // console.log(Data.file, "88888")
  useEffect(() => {
    
    // if (!data || !map) return;
    if (Data.file && Data.file.length) {
      Layer.current = L.geoJson(
        {
          features: [],
        },
        {
          style: function () {
            return { color: green[900] };
          },
          onEachFeature: function popUp(f, l) {
            var out = [];
            if (f.properties) {
              for (var key in f.properties) {
                out.push(key + ": " + f.properties[key]);
              }
              l.bindPopup(out.join(`<br />`));
            }
          },
        }
      ).addTo(map);
      Layer.current.addData(Data.file);
      map.fitBounds(Layer.current.getBounds());
      dispatch(updateFarmerInfo({layer : Layer.current}));
    }
  }, [map, removeLayer, Data.file]);

  return null;
}

export { extractShapes };
