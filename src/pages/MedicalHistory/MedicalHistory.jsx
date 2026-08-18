import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
    FaArrowLeft,
    FaEdit,
    FaTrash,
    FaPlus,
    FaSave,
} from "react-icons/fa";

import "./MedicalHistory.css";
import { apiGet, apiPost, apiPut } from "../../api/client";

const HISTORY_TYPES = [
    "conditions",
    "medications",
    "allergies",
    "surgeries",
];

function emptyHistory(lastCheckup = "") {
    return {
        conditions: [],
        medications: [],
        allergies: [],
        surgeries: [],
        lastCheckup,
    };
}

function mapApiRecordsToHistory(records, lastCheckup = "") {
    const next = emptyHistory(lastCheckup);

    records.forEach((record) => {
        const type = HISTORY_TYPES.includes(record.condition_name)
            ? record.condition_name
            : "conditions";

        next[type].push({
            id: record.id,
            name: record.notes,
            dateAdded: record.created_at.slice(0, 10),
        });
    });

    return next;
}

function MedicalHistory() {
    const navigate = useNavigate();

    const [medicalHistory, setMedicalHistory] = useState(emptyHistory());
    const [editing, setEditing] = useState(false);
    const [newItem, setNewItem] = useState({
        type: "conditions",
        name: "",
    });

    useEffect(() => {
        loadMedicalHistory();
    }, []);

    const loadMedicalHistory = async () => {
        const accessToken = localStorage.getItem("access_token");

        if (!accessToken) {
            navigate("/");
            return;
        }

        const savedLastCheckup = localStorage.getItem("last_checkup") || "";

        try {
            const records = await apiGet("/api/v1/medical-history", accessToken);
            const mapped = mapApiRecordsToHistory(records, savedLastCheckup);
            setMedicalHistory(mapped);
            localStorage.setItem("medicalHistory", JSON.stringify(mapped));
        } catch (error) {
            alert(error.message || "Unable to load medical history");
        }
    };

    const addItem = async () => {
        if (!newItem.name.trim()) {
            return;
        }

        const accessToken = localStorage.getItem("access_token");

        if (!accessToken) {
            navigate("/");
            return;
        }

        try {
            await apiPost(
                "/api/v1/medical-history",
                {
                    condition_name: newItem.type,
                    notes: newItem.name,
                },
                accessToken
            );

            setNewItem({
                type: "conditions",
                name: "",
            });

            await loadMedicalHistory();
        } catch (error) {
            alert(error.message || "Unable to add medical history item");
        }
    };

    const deleteItem = () => {
        alert("Delete is not supported by the current backend API yet.");
    };

    const editItem = async (type, id) => {
        const item = medicalHistory[type].find((entry) => entry.id === id);

        const newName = prompt("Edit entry:", item.name);

        if (!newName || !newName.trim()) {
            return;
        }

        const accessToken = localStorage.getItem("access_token");

        if (!accessToken) {
            navigate("/");
            return;
        }

        try {
            await apiPut(
                `/api/v1/medical-history/${id}`,
                {
                    condition_name: type,
                    notes: newName.trim(),
                },
                accessToken
            );

            await loadMedicalHistory();
        } catch (error) {
            alert(error.message || "Unable to update medical history item");
        }
    };

    const updateCheckup = (value) => {
        const updatedHistory = {
            ...medicalHistory,
            lastCheckup: value,
        };

        setMedicalHistory(updatedHistory);
        localStorage.setItem("last_checkup", value);
        localStorage.setItem("medicalHistory", JSON.stringify(updatedHistory));
    };

    const formatDate = (dateString) => {
        if (!dateString) {
            return "Not recorded";
        }

        const date = new Date(`${dateString}T00:00:00`);

        return date.toLocaleDateString("en-US", {
            month: "long",
            day: "numeric",
            year: "numeric",
        });
    };

    const renderSection = (title, type) => {
        return (
            <div className="history-section">
                <div className="history-section-header">
                    <h3>{title}</h3>
                </div>

                {medicalHistory[type].length === 0 ? (
                    <p className="empty-message">No {title.toLowerCase()} recorded.</p>
                ) : (
                    medicalHistory[type].map((item) => {
                        return (
                            <div className="history-item" key={item.id}>
                                <div className="history-item-info">
                                    <strong>{item.name}</strong>
                                    <span>Added: {formatDate(item.dateAdded)}</span>
                                </div>

                                {editing && (
                                    <div className="history-actions">
                                        <button
                                            type="button"
                                            onClick={() => editItem(type, item.id)}
                                        >
                                            <FaEdit />
                                        </button>

                                        <button type="button" onClick={deleteItem}>
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
            <div className="medical-history-header">
                <Link to="/dashboard">
                    <FaArrowLeft className="back-icon" />
                </Link>

                <h2>Medical History</h2>

                <button className="edit-button" onClick={() => setEditing(!editing)}>
                    {editing ? <FaSave /> : <FaEdit />}
                    {editing ? "Done" : "Edit"}
                </button>
            </div>

            {editing && (
                <div className="add-history">
                    <h3>Add Medical History</h3>

                    <select
                        value={newItem.type}
                        onChange={(e) =>
                            setNewItem({
                                ...newItem,
                                type: e.target.value,
                            })
                        }
                    >
                        <option value="conditions">Condition</option>
                        <option value="medications">Medication</option>
                        <option value="allergies">Allergy</option>
                        <option value="surgeries">Surgery</option>
                    </select>

                    <input
                        type="text"
                        placeholder="Enter medical information"
                        value={newItem.name}
                        onChange={(e) =>
                            setNewItem({
                                ...newItem,
                                name: e.target.value,
                            })
                        }
                    />

                    <button type="button" onClick={addItem}>
                        <FaPlus />
                        Add
                    </button>
                </div>
            )}

            <div className="checkup-section">
                <h3>Last Checkup Date</h3>

                <input
                    type="date"
                    value={medicalHistory.lastCheckup}
                    onChange={(e) => updateCheckup(e.target.value)}
                />
            </div>

            {renderSection("Conditions", "conditions")}
            {renderSection("Medications", "medications")}
            {renderSection("Allergies", "allergies")}
            {renderSection("Surgeries", "surgeries")}
        </div>
    );
}

export default MedicalHistory;
