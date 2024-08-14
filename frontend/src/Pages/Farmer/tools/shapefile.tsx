// import './index.css';
import { Autocomplete, AutocompleteItem } from "@nextui-org/react";
import { countries } from "./data"
import {
  Button,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Divider,
  Select,
} from "@nextui-org/react";
import polygon from "../../../../assets/draw/polygon.svg";
import close from "../../../../assets/close.svg";
import { useDispatch } from "react-redux";
import { updateShapeFile, updateRemoveLayer, updateDrawEnabled, clearShape } from "../../../../slices/shapeFileSlice";
import { extractShapes } from "../../map/shapeFile/utils";
import { useRef, useState } from "react";
import { updateError, updateErrorModal } from "../../../../slices/errorSlice";
import JSZip from 'jszip';
import proj4 from 'proj4';
import * as shp from 'shpjs';
import Axios from "../../../api/axios";
import { updateResponse, updateShpPath } from "../../../../slices/formSlice";
import { updateShape } from "../../../../slices/mapSlice";
import { count } from "console";

let zip = new JSZip();
export default function ShapefileDraw(props) {

  const dispatch = useDispatch();
  const [label, setLabel] = useState("Morocco");

  let fileInput = useRef(null);

  const checkZip = (prjFile, dbfFile, shpFile, shxFile) => {
    if (!prjFile) {
      dispatch(updateError("No .prj file found in the zip")) &&
        dispatch(updateErrorModal(true));
    } else if (!dbfFile) {
      dispatch(updateError("No .dbf file found in the zip")) &&
        dispatch(updateErrorModal(true));
    }
    else if (!shpFile) {
      dispatch(updateError("No .shp file found in the zip")) &&
        dispatch(updateErrorModal(true));
    }
    else if (!shxFile) {
      dispatch(updateError("No .shx file found in the zip")) &&
        dispatch(updateErrorModal(true));
    }
  }
  const handleFile = async (e: any) => {
    e.preventDefault();
    if (!e.target.files[0].name.endsWith('.zip')) {
      dispatch(updateError("Please upload a zip file")) &&
        dispatch(updateErrorModal(true));
    }
    else {
      const zipFile = e.target.files?.[0];
      console.log('Zip File:', e.target.files)
      if (zipFile) {
        try {
          const zip = await JSZip.loadAsync(zipFile);
          console.log('Shapefile:');
          const shpFile = zip.file(/\.shp$/i)[0];
          const shxFile = zip.file(/\.shx$/i)[0];
          const prjFile = zip.file(/\.prj$/i)[0];
          const dbfFile = zip.file(/\.dbf$/i)[0];
          if (shpFile && shxFile && prjFile && dbfFile) {
            dispatch(updateShape("shapefile"));
            dispatch(updateShapeFile(await extractShapes(e.target.files)));
            const shpData = await shpFile.async('uint8array');
            const shxData = await shxFile.async('uint8array');

            const formData = new FormData();
            formData.append('shpFile', new Blob([shpData]), 'file.shp');
            formData.append('shxFile', new Blob([shxData]), 'file.shx');
            Axios.post("rasteres/store/", formData, {
              headers: {
                "Content-Type": "multipart/form-data",
              },
            }).then((response) => {
              dispatch(updateResponse(response.data));
              dispatch(updateShpPath(response.data.shpPath));
            });
          } else {
            checkZip(prjFile, dbfFile, shpFile, shxFile);
          }
        } catch (error) {
          console.log(error);
          dispatch(updateError("Error reading zip file")) &&
            dispatch(updateErrorModal(true));
        }
      }
    }
  };

  const clearShapeFile = () => {
    dispatch(updateRemoveLayer(true));
    dispatch(clearShape());

  };


  const handleUpload = () => {
    dispatch(updateRemoveLayer(false));
    fileInput.current.click();

  };

  const serveShapefile = async (e: any) => {
    const response = await Axios.post(`rasteres/serveShp/`, { "label": e.target.value }, { responseType: 'arraybuffer' })
    console.log('Response data type:', typeof response.data);


    try {
      const blob = new Blob([response.data], { type: 'application/zip' });

      const file = new File([blob], `${e.target.value}.zip`, { type: 'application/zip' });
      console.log('Blob size:', file);
      // Programmatically set the file input value
      const fileInputElement = fileInput.current;
      if (fileInputElement) {
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInputElement.files = dataTransfer.files;
        fileInputElement.dispatchEvent(new Event('change', { bubbles: true }));
      }
    }
    catch (err) {
      console.log(err)
    }
    // const blob = new Blob([response.data], { type: 'application/zip' });
    // const files = new File([blob], `${e.target.value}.zip`, { type: 'application/zip' });
    // console.log('Files:', files);
    // dispatch(updateRemoveLayer(false));
    // dispatch(updateShape("shapefile"));
    // // dispatch(updateShapeFile( await extractShapes([files])));
    // const shapesData = await extractShapes(files);
    // console.log('Shapes Data:', shapesData);

  }

  return (
    <div
      className={`absolute z-[11] flex flex-col justify-center items-center h-[32%] ml-4  top-4 w-72 bg-white rounded-lg border-[1vw] border-white text-black  duration-300`}
    >
      <Card radius="sm" className="w-[100%] h-[100%] bg-input">
        <CardHeader className="flex ">
          <div className="flex absolute top-2 right-4">
            <div
              className="flex justify-center items-center"
              style={{
                width: 12,
                height: 12,
                left: 0,
                top: 0,
                position: "absolute",
                background: "#D9D9D9",
                borderRadius: 9999,
              }}
            >
              <img
                onClick={props.CloseShapefile}
                className="w-[100%] h-[100%]"
                src={close}
                alt="close"
              />
            </div>
          </div>
          <div className="flex w-[100%]">
            <div
              className="w-[12%] h-7 flex justify-center items-center"
              style={{ background: "#21437F", borderRadius: 5.28 }}
            >
              <img
                src={polygon}
                className="w-[80%] h-[80%]"
                alt="polygon Icon"
              />
            </div>
            <div className="flex flex-col justify-start items-start w-[95%]">
              <div
                className=" flex w-[90%] pl-2 font-semibold"
                style={{ fontSize: 12, letterSpacing: 0.06 }}
              >
                Shapefile
              </div>
            </div>
          </div>
        </CardHeader>
        <Divider />
        <CardBody className="overflow-hidden w-[100%]  ">
          <div className="flex flex-col justify-start items-start w-[100%] h-[100%]">
            <div
              className=" flex w-[100%]  font-normal"
              style={{ color: "#5a5a5a", fontSize: 12 }}
            >
              <Autocomplete
                defaultItems={countries}
                label="Choose a Shapefile"
                placeholder="Search "
                defaultSelectedKey="Morocco"
                size="sm"
                className="max-w-xs"
                onSelect={serveShapefile}
              >
                {(item) => <AutocompleteItem key={item.value} value={item.value} >{item.label}</AutocompleteItem>}
              </Autocomplete>

            </div>
          </div>
        </CardBody>
        <Divider />
        <CardFooter>
          <div className="flex  justify-center items-center w-[100%] gap-10">
            <input
              ref={fileInput}
              style={{ display: "none" }}
              type="file"
              name="file"
              accept=".zip"
              id="file"
              onChange={handleFile}
              className="inputfile"
            />
            <div className="flex w-[90%] justify-between items-center space-x-4">
              <button
                onClick={handleUpload}
                type="submit"
                className="Save"

                style={{
                  width: 68,
                  height: 32,
                  textAlign: "center",
                  borderRadius: 8,
                  background: "#21437F",
                  color: "white",
                  fontSize: 13,
                  wordWrap: "break-word",
                }}
              >
                Upload
              </button>
              <Button size="sm" onClick={clearShapeFile} className="Discard">
                Remove
              </Button>
            </div>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}
