import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
    FaArrowLeft,
    FaEdit,
    FaTrash,
    FaPlus,
    FaSave
} from "react-icons/fa";

import "./MedicalHistory.css";


function MedicalHistory() {

    const [medicalHistory, setMedicalHistory] = useState({
        conditions: [],
        medications: [],
        allergies: [],
        surgeries: [],
        lastCheckup: ""
    });


    const [editing, setEditing] = useState(false);

    const [newItem, setNewItem] = useState({
        type: "conditions",
        name: ""
    });


    // Load medical history when page opens
    useEffect(() => {

        const savedMedicalHistory =
            JSON.parse(localStorage.getItem("medicalHistory"));

        if (savedMedicalHistory) {

            setMedicalHistory(savedMedicalHistory);

        }

    }, []);


    // Save medical history
    const saveMedicalHistory = (updatedHistory) => {

        setMedicalHistory(updatedHistory);

        localStorage.setItem(
            "medicalHistory",
            JSON.stringify(updatedHistory)
        );

    };


    // Add a new medical history item
    const addItem = () => {

        if (!newItem.name.trim()) {
            return;
        }


        const item = {

            id: Date.now(),

            name: newItem.name,

            dateAdded:
                new Date().toISOString().split("T")[0]

        };


        const updatedHistory = {

            ...medicalHistory,

            [newItem.type]: [
                ...medicalHistory[newItem.type],
                item
            ]

        };


        saveMedicalHistory(updatedHistory);


        setNewItem({
            type: "conditions",
            name: ""
        });

    };


    // Delete item
    const deleteItem = (type, id) => {

        const updatedHistory = {

            ...medicalHistory,

            [type]: medicalHistory[type].filter(
                (item) => item.id !== id
            )

        };


        saveMedicalHistory(updatedHistory);

    };


    // Edit item
    const editItem = (type, id) => {

        const item =
            medicalHistory[type].find(
                (item) => item.id === id
            );


        const newName =
            prompt("Edit entry:", item.name);


        if (!newName || !newName.trim()) {
            return;
        }


        const updatedHistory = {

            ...medicalHistory,

            [type]: medicalHistory[type].map(
                (item) => {

                    if (item.id === id) {

                        return {
                            ...item,
                            name: newName
                        };

                    }

                    return item;

                }
            )

        };


        saveMedicalHistory(updatedHistory);

    };


    // Update last checkup
    const updateCheckup = (value) => {

        const updatedHistory = {

            ...medicalHistory,

            lastCheckup: value

        };


        saveMedicalHistory(updatedHistory);

    };


    // Display date nicely
    const formatDate = (dateString) => {

        if (!dateString) {
            return "Not recorded";
        }


        const date =
            new Date(dateString + "T00:00:00");


        return date.toLocaleDateString(
            "en-US",
            {
                month: "long",
                day: "numeric",
                year: "numeric"
            }
        );

    };


    // Render each medical history section
    const renderSection = (title, type) => {
    
        return (
            <div className="history-section">
    
                <div className="history-section-header">
    
                    <h3>
                        {title}
                    </h3>
    
                </div>
    
    
                {medicalHistory[type].length === 0 ? (
    
                    <p className="empty-message">
                        No {title.toLowerCase()} recorded.
                    </p>
    
                ) : (
    
                    medicalHistory[type].map((item) => {
    
                        return (
                            <div
                                className="history-item"
                                key={item.id}
                            >
    
                                <div className="history-item-info">
    
                                    <strong>
                                        {item.name}
                                    </strong>
    
                                    <span>
                                        Added: {formatDate(item.dateAdded)}
                                    </span>
    
                                </div>
    
    
                                {editing && (
    
                                    <div className="history-actions">
    
                                        <button
                                            type="button"
                                            onClick={() =>
                                                editItem(
                                                    type,
                                                    item.id
                                                )
                                            }
                                        >
                                            <FaEdit />
                                        </button>
    
    
                                        <button
                                            type="button"
                                            onClick={() =>
                                                deleteItem(
                                                    type,
                                                    item.id
                                                )
                                            }
                                        >
                                            <FaTrash />
                                        </button>
    
                                    </div>
    
                                )}
    
                            </div>
                        );
    
                    })
    
                )}
    
            </div>
        );
    };

    

    return (

        <div className="medical-history-page">


            {/* Header */}

            <div className="medical-history-header">

                <Link to="/dashboard">

                    <FaArrowLeft className="back-icon" />

                </Link>


                <h2>
                    Medical History
                </h2>


                <button
                    className="edit-button"
                    onClick={() =>
                        setEditing(!editing)
                    }
                >

                    {editing
                        ? <FaSave />
                        : <FaEdit />
                    }

                    {editing
                        ? "Done"
                        : "Edit"
                    }

                </button>

            </div>



            {/* Add New Entry */}

            {editing && (

                <div className="add-history">

                    <h3>
                        Add Medical History
                    </h3>


                    <select
                        value={newItem.type}
                        onChange={(e) =>
                            setNewItem({
                                ...newItem,
                                type: e.target.value
                            })
                        }
                    >

                        <option value="conditions">
                            Condition
                        </option>

                        <option value="medications">
                            Medication
                        </option>

                        <option value="allergies">
                            Allergy
                        </option>

                        <option value="surgeries">
                            Surgery
                        </option>

                    </select>


                    <input
                        type="text"
                        placeholder="Enter information..."
                        value={newItem.name}
                        onChange={(e) =>
                            setNewItem({
                                ...newItem,
                                name: e.target.value
                            })
                        }
                    />


                    <button
                        className="add-button"
                        onClick={addItem}
                    >

                        <FaPlus />

                        Add

                    </button>

                </div>

            )}



            {/* Conditions */}

            {renderSection(
                "Conditions",
                "conditions"
            )}



            {/* Medications */}

            {renderSection(
                "Medications",
                "medications"
            )}



            {/* Allergies */}

            {renderSection(
                "Allergies",
                "allergies"
            )}



            {/* Surgeries */}

            {renderSection(
                "Surgeries",
                "surgeries"
            )}



            {/* Last Checkup */}

            <div className="history-section">

                <h3>
                    Last Checkup
                </h3>


                {editing ? (

                    <input
                        type="date"
                        value={
                            medicalHistory.lastCheckup
                        }
                        onChange={(e) =>
                            updateCheckup(
                                e.target.value
                            )
                        }
                    />

                ) : (

                    <p>
                        {formatDate(
                            medicalHistory.lastCheckup
                        )}
                    </p>

                )}

            </div>


        </div>

    );

}


export default MedicalHistory;
