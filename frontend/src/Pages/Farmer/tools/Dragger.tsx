import { useEffect, useState } from "react";
import { useAppDispatch, useAppSelector } from "../../../Redux/hooks";
import { updateFarmerInfo } from "../../../Redux/Farmer/actions";
import { FileCard, FileUploader, Pane } from "evergreen-ui";
import { handleShapefile } from "./Addshapefile";
import { green } from "@mui/material/colors";
import { useMap } from "react-leaflet";

const Dragger_ = () => {
  const dispatch = useAppDispatch();
  const Data = useAppSelector((state) => state.farmer);
  const [fileRejections, setFileRejections] = useState([]);
  const [file, Setfile] = useState([]);
  const handleRejected = (fileRejections) =>
    setFileRejections([fileRejections[0]]);
  const handleRemove = () => {
    Setfile([]);
    dispatch(updateFarmerInfo({ file: [] }));
    setFileRejections([]);
  };

  async function handlechange(e) {
    // console.log(e)
    Setfile(e);
    const file = await handleShapefile(e);
    dispatch(updateFarmerInfo({ file: file }));
  }
  //   useEffect(() => {
  //   console.log(Data.file, "ssasasaww");
  //   }, [Data.file]);
  return (
    <Pane className="w-full p-3 ">
      <FileUploader
        backgroundColor={green[50]}
        label="Upload Shapefile"
        description="You can upload Zip files only"
        maxSizeInBytes={50 * 1024 ** 2}
        maxFiles={1}
        onChange={handlechange}
        onRejected={handleRejected}
        renderFile={(file) => {
          const { name, size, type } = file;
          const fileRejection = fileRejections.find(
            (fileRejection) => fileRejection.file === file
          );
          const { message } = fileRejection || {};
          return (
            <FileCard
              key={name}
              isInvalid={fileRejection != null}
              name={name}
              onRemove={handleRemove}
              sizeInBytes={size}
              type={type}
              validationMessage={message}
            />
          );
        }}
        values={file}
      />
    </Pane>
  );
};

export default Dragger_;
