import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./UpcomingAppointments.css";

import {
    FaArrowLeft,
    FaCalendarAlt,
    FaClock,
    FaUserMd,
    FaPlus,
    FaEdit,
} from "react-icons/fa";
import { apiGet, apiPost, apiPut } from "../../api/client";

const timeSlots = [];

for (let hour = 8; hour <= 17; hour++) {
    for (let minute = 0; minute < 60; minute += 30) {
        if (hour === 17 && minute > 0) {
            continue;
        }

        const hour12 = hour > 12 ? hour - 12 : hour;
        const period = hour >= 12 ? "PM" : "AM";
        const formattedMinute = minute === 0 ? "00" : "30";

        timeSlots.push(`${hour12}:${formattedMinute} ${period}`);
    }
}

function to24HourTime(slot) {
    const [time, period] = slot.split(" ");
    const [hourRaw, minute] = time.split(":");
    let hour = parseInt(hourRaw, 10);

    if (period === "PM" && hour !== 12) {
        hour += 12;
    }

    if (period === "AM" && hour === 12) {
        hour = 0;
    }

    return `${String(hour).padStart(2, "0")}:${minute}:00`;
}

function toUiAppointment(apiAppointment) {
    const start = new Date(apiAppointment.start_time);

    return {
        id: apiAppointment.id,
        doctor: apiAppointment.provider_name,
        date: start.toISOString().slice(0, 10),
        time: start.toLocaleTimeString("en-US", {
            hour: "numeric",
            minute: "2-digit",
            hour12: true,
        }),
        reason: apiAppointment.reason,
        status: apiAppointment.status,
    };
}

function UpcomingAppointments() {
    const navigate = useNavigate();

    const [appointments, setAppointments] = useState([]);
    const [editingAppointment, setEditingAppointment] = useState(null);

    useEffect(() => {
        loadAppointments();
    }, []);

    const loadAppointments = async () => {
        const accessToken = localStorage.getItem("access_token");

        if (!accessToken) {
            navigate("/");
            return;
        }

        try {
            const items = await apiGet("/api/v1/appointments", accessToken);
            const mapped = items.map(toUiAppointment);
            setAppointments(mapped);
            localStorage.setItem("appointments", JSON.stringify(mapped));
        } catch (error) {
            alert(error.message || "Unable to load appointments");
        }
    };

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const upcomingAppointments = appointments
        .filter((appointment) => {
            if (appointment.status === "canceled") {
                return false;
            }

            const appointmentDate = new Date(`${appointment.date}T00:00:00`);
            return appointmentDate >= today;
        })
        .sort((a, b) => new Date(a.date) - new Date(b.date));

    const pastAppointments = appointments
        .filter((appointment) => {
            if (appointment.status === "canceled") {
                return false;
            }

            const appointmentDate = new Date(`${appointment.date}T00:00:00`);
            return appointmentDate < today;
        })
        .sort((a, b) => new Date(b.date) - new Date(a.date));

    const cancelAppointment = async (id) => {
        const accessToken = localStorage.getItem("access_token");

        if (!accessToken) {
            navigate("/");
            return;
        }

        try {
            await apiPost(`/api/v1/appointments/${id}/cancel`, {}, accessToken);
            await loadAppointments();
        } catch (error) {
            alert(error.message || "Unable to cancel appointment");
        }
    };

    const startEditing = (appointment) => {
        setEditingAppointment({ ...appointment });
    };

    const handleEditChange = (e) => {
        const { name, value } = e.target;

        setEditingAppointment((previous) => ({
            ...previous,
            [name]: value,
        }));
    };

    const saveEditedAppointment = async (e) => {
        e.preventDefault();

        const accessToken = localStorage.getItem("access_token");

        if (!accessToken) {
            navigate("/");
            return;
        }

        try {
            const startTime = `${editingAppointment.date}T${to24HourTime(editingAppointment.time)}`;
            const endTime = new Date(
                new Date(startTime).getTime() + 30 * 60 * 1000
            ).toISOString();

            await apiPut(
                `/api/v1/appointments/${editingAppointment.id}`,
                {
                    provider_name: editingAppointment.doctor,
                    start_time: new Date(startTime).toISOString(),
                    end_time: endTime,
                    reason: editingAppointment.reason,
                    status: "scheduled",
                },
                accessToken
            );

            setEditingAppointment(null);
            await loadAppointments();
        } catch (error) {
            alert(error.message || "Unable to save appointment changes");
        }
    };

    const cancelEditing = () => {
        setEditingAppointment(null);
    };

    return (
        <div className="appointments-page">
            <div className="appointments-header">
                <div className="header-left">
                    <FaArrowLeft
                        className="back-icon"
                        onClick={() => navigate("/dashboard")}
                    />

                    <h2>Upcoming Appointments</h2>
                </div>
            </div>

            <div className="appointments-content">
                <section className="appointment-section">
                    <div className="section-title">
                        <FaCalendarAlt />
                        <h3>Upcoming Appointments</h3>
                    </div>

                    {upcomingAppointments.length > 0 ? (
                        <div className="appointments-list">
                            {upcomingAppointments.map((appointment) => (
                                <div className="appointment-item" key={appointment.id}>
                                    <div className="appointment-icon">
                                        <FaUserMd />
                                    </div>

                                    <div className="appointment-info">
                                        <h4>{appointment.doctor}</h4>

                                        <p>
                                            <FaCalendarAlt />
                                            {formatDate(appointment.date)}
                                        </p>

                                        <p>
                                            <FaClock />
                                            {appointment.time}
                                        </p>

                                        <p>
                                            <strong>Reason:</strong> {appointment.reason}
                                        </p>
                                    </div>

                                    <div className="appointment-actions">
                                        <button
                                            className="edit-appointment-btn"
                                            onClick={() => startEditing(appointment)}
                                        >
                                            <FaEdit />
                                            Edit
                                        </button>

                                        <button
                                            className="cancel-appointment-btn"
                                            onClick={() => cancelAppointment(appointment.id)}
                                        >
                                            Cancel
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="no-appointments">
                            <p>You don't have any upcoming appointments.</p>

                            <button
                                className="new-appointment-btn"
                                onClick={() => navigate("/appointments")}
                            >
                                <FaPlus />
                                Book Appointment
                            </button>
                        </div>
                    )}
                </section>

                <section className="appointment-section">
                    <div className="section-title">
                        <FaCalendarAlt />
                        <h3>Past Appointments</h3>
                    </div>

                    {pastAppointments.length > 0 ? (
                        <div className="appointments-list">
                            {pastAppointments.map((appointment) => (
                                <div className="appointment-item past" key={appointment.id}>
                                    <div className="appointment-icon">
                                        <FaUserMd />
                                    </div>

                                    <div className="appointment-info">
                                        <h4>{appointment.doctor}</h4>

                                        <p>
                                            <FaCalendarAlt />
                                            {formatDate(appointment.date)}
                                        </p>

                                        <p>
                                            <FaClock />
                                            {appointment.time}
                                        </p>

                                        <p>
                                            <strong>Reason:</strong> {appointment.reason}
                                        </p>
                                    </div>

                                    <span className="past-label">Completed</span>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="no-appointments">
                            <p>No past appointments.</p>
                        </div>
                    )}
                </section>
            </div>

            {editingAppointment && (
                <div className="edit-modal-overlay">
                    <div className="edit-modal">
                        <h3>Edit Appointment</h3>

                        <form onSubmit={saveEditedAppointment}>
                            <div className="form-group">
                                <label>Doctor</label>

                                <input
                                    type="text"
                                    name="doctor"
                                    value={editingAppointment.doctor}
                                    onChange={handleEditChange}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label>Date</label>

                                <input
                                    type="date"
                                    name="date"
                                    value={editingAppointment.date}
                                    onChange={handleEditChange}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label>Time</label>

                                <select
                                    name="time"
                                    value={editingAppointment.time}
                                    onChange={handleEditChange}
                                    required
                                >
                                    <option value="">Select a time</option>

                                    {timeSlots.map((time) => (
                                        <option key={time} value={time}>
                                            {time}
                                        </option>
                                    ))}
                                </select>
                            </div>

                            <div className="form-group">
                                <label>Reason for Appointment</label>

                                <textarea
                                    name="reason"
                                    value={editingAppointment.reason}
                                    onChange={handleEditChange}
                                    required
                                />
                            </div>

                            <div className="edit-modal-actions">
                                <button
                                    type="button"
                                    className="close-edit-btn"
                                    onClick={cancelEditing}
                                >
                                    Cancel
                                </button>

                                <button type="submit" className="save-edit-btn">
                                    Save Changes
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}

function formatDate(dateString) {
    const date = new Date(`${dateString}T00:00:00`);

    return date.toLocaleDateString("en-US", {
        month: "long",
        day: "numeric",
        year: "numeric",
    });
}

export default UpcomingAppointments;
