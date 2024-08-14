import React, { useEffect, useState } from "react";
import "./Dashboard/style.css"
import api from "../../api/axios.js"
import { Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button, useDisclosure, Input } from "@nextui-org/react";
import SelectField from "./Dashboard/SelectField";
import { useLocation } from "react-router-dom";


// interface PopUp_ {
//     Boundry: any 
// }

const PopUp = (polygon) => {
    const [selectedFieldName, setSelectedFieldName] = useState('');
    const [selectedFieldDate, setSelectedFieldDate] = useState('');
    // const [selectedSoilType, setSelectedSoilType] = useState('');
    // const [selectedDistanceFromWater, setSelectedDistanceFromWater] = useState('');
    // const [selectedIrrigationSystem, setSelectedIrrigationSystem] = useState('');
    // const [soils, setSoils] = useState([]);
    const location = useLocation();
    const [User, setUser] = useState([]);

    const { isOpen, onOpen, onClose } = useDisclosure();
    const [backdrop, setBackdrop] = React.useState('opaque')
    // useEffect(() => {
    //     // get name user connected
    //     api.get('/api_auth/')
    //         .then(response => {
    //             console.log(response.data);
    //             setUser(response.data);
    //         }
    //         )
    //         .catch(error => {
    //             console.log(error);
    //         }
    //         );
    // }, []);

    const handleSubmit = (event) => {
        event.preventDefault();
        // Find the selected soil using the selectedSoilType
        // const selectedSoil = soils.find(soil => soil.soil_type === selectedSoilType);
        console.log(polygon)
        api.post('/api/field/', {
            name: selectedFieldName,
            boundaries: JSON.stringify(polygon.polygon.Boundry),
            
        })
            .then(response => {
                console.log(response.data);
                // Reset the form values
                setSelectedFieldName('');
                // setSelectedSoilType('');
                // setSelectedDistanceFromWater('');
                // setSelectedIrrigationSystem('');
                // Show a success message using SweetAlert
                // Swal.fire({
                //     title: 'Success!',
                //     text: 'Field added successfully!',
                //     icon: 'success',
                //     confirmButtonText: 'OK'
                // });


            })
            .catch(error => {
                console.log(error);
                // Show an error message using SweetAlert
                // Swal.fire({
                //     title: 'Error!',
                //     text: 'Unable to add field!',
                //     icon: 'error',
                //     confirmButtonText: 'OK',
                // });

            });
    };

    const handleOpen = (backdrop) => {
        setBackdrop(backdrop)
        onOpen();
    }

    return (
        <>
            <div className="flex flex-wrap gap-3">
                <Button
                    key="blur"
                    variant="flat"
                    radius="full"
                    onPress={() => handleOpen("blur")}
                    className="capitalize bg-Green text-white"
                >
                    Save
                </Button>
            </div>
            <Modal className="bg-gray-50" backdrop={backdrop} isOpen={isOpen} onClose={onClose}>
                <ModalContent>
                    {(onClose) => (
                        <>
                            <ModalHeader className="flex flex-col gap-1">Add Field</ModalHeader>
                            <ModalBody >
                                <form className="w-full flex flex-col items-center gap-6" onSubmit={handleSubmit}>
                                    <Input
                                        label="Field Name"
                                        placeholder="Enter Field Name"
                                        type={"text"}
                                        radius="full"
                                        className="max-w-[60%] "
                                        required
                                        onChange={(e) => setSelectedFieldName(e.target.value)}
                                    />                                    
                                    <Button radius="full" type="submit" className="bg-Green text-white mb-[2rem]" onPress={onClose}>
                                        Add
                                    </Button>
                                </form>
                            </ModalBody>
                        </>
                    )}
                </ModalContent>
            </Modal>
        </>
    );
}


export default PopUp