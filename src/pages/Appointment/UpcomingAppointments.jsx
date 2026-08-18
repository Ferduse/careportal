import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./UpcomingAppointments.css";

import {
    FaArrowLeft,
    FaCalendarAlt,
    FaClock,
    FaUserMd,
    FaPlus,
    FaEdit
} from "react-icons/fa";

const timeSlots = [];

for (let hour = 8; hour <= 17; hour++) {

    for (let minute = 0; minute < 60; minute += 30) {

        // Don't add times after 5:00 PM
        if (hour === 17 && minute > 0) {
            continue;
        }

        const hour12 = hour > 12 ? hour - 12 : hour;
        const period = hour >= 12 ? "PM" : "AM";

        const formattedMinute =
            minute === 0 ? "00" : "30";

        timeSlots.push(
            `${hour12}:${formattedMinute} ${period}`
        );
    }
}


function UpcomingAppointments() {

    const navigate = useNavigate();

    const [appointments, setAppointments] = useState([]);

    // Appointment currently being edited
    const [editingAppointment, setEditingAppointment] = useState(null);


    // Load appointments
    useEffect(() => {

        loadAppointments();

    }, []);


    const loadAppointments = () => {

        const savedAppointments =
            JSON.parse(localStorage.getItem("appointments")) || [];

        setAppointments(savedAppointments);

    };


    // Today's date
    const today = new Date();
    today.setHours(0, 0, 0, 0);


    // Upcoming appointments
    const upcomingAppointments = appointments
        .filter((appointment) => {

            const appointmentDate =
                new Date(appointment.date + "T00:00:00");

            return appointmentDate >= today;

        })
        .sort((a, b) => {

            return new Date(a.date) - new Date(b.date);

        });


    // Past appointments
    const pastAppointments = appointments
        .filter((appointment) => {

            const appointmentDate =
                new Date(appointment.date + "T00:00:00");

            return appointmentDate < today;

        })
        .sort((a, b) => {

            return new Date(b.date) - new Date(a.date);

        });


    // Cancel appointment
    const cancelAppointment = (id) => {

        const updatedAppointments =
            appointments.filter(
                (appointment) => appointment.id !== id
            );

        localStorage.setItem(
            "appointments",
            JSON.stringify(updatedAppointments)
        );

        setAppointments(updatedAppointments);

    };


    // Start editing
    const startEditing = (appointment) => {

        setEditingAppointment({
            ...appointment
        });

    };


    // Handle edit form changes
    const handleEditChange = (e) => {

        const { name, value } = e.target;

        setEditingAppointment((previous) => ({
            ...previous,
            [name]: value
        }));

    };


    // Save edited appointment
    const saveEditedAppointment = (e) => {

        e.preventDefault();

        const updatedAppointments = appointments.map(
            (appointment) => {

                if (appointment.id === editingAppointment.id) {

                    return editingAppointment;

                }

                return appointment;

            }
        );


        localStorage.setItem(
            "appointments",
            JSON.stringify(updatedAppointments)
        );

        setAppointments(updatedAppointments);

        // Close edit form
        setEditingAppointment(null);

    };


    // Cancel editing
    const cancelEditing = () => {

        setEditingAppointment(null);

    };


    return (

        <div className="appointments-page">


            {/* Header */}

            <div className="appointments-header">

                <div className="header-left">

                    <FaArrowLeft
                        className="back-icon"
                        onClick={() => navigate("/dashboard")}
                    />

                    <h2>
                        Upcoming Appointments
                    </h2>

                </div>

            </div>



            {/* Main Content */}

            <div className="appointments-content">


                {/* Upcoming Appointments */}

                <section className="appointment-section">

                    <div className="section-title">

                        <FaCalendarAlt />

                        <h3>
                            Upcoming Appointments
                        </h3>

                    </div>


                    {upcomingAppointments.length > 0 ? (

                        <div className="appointments-list">

                            {upcomingAppointments.map(
                                (appointment) => (

                                    <div
                                        className="appointment-item"
                                        key={appointment.id}
                                    >

                                        <div className="appointment-icon">

                                            <FaUserMd />

                                        </div>


                                        <div className="appointment-info">

                                            <h4>
                                                {appointment.doctor}
                                            </h4>


                                            <p>

                                                <FaCalendarAlt />

                                                {formatDate(
                                                    appointment.date
                                                )}

                                            </p>


                                            <p>

                                                <FaClock />

                                                {appointment.time}

                                            </p>


                                            <p>

                                                <strong>
                                                    Reason:
                                                </strong>{" "}

                                                {appointment.reason}

                                            </p>

                                        </div>


                                        {/* Buttons */}

                                        <div className="appointment-actions">

                                            <button
                                                className="edit-appointment-btn"
                                                onClick={() =>
                                                    startEditing(
                                                        appointment
                                                    )
                                                }
                                            >

                                                <FaEdit />

                                                Edit

                                            </button>


                                            <button
                                                className="cancel-appointment-btn"
                                                onClick={() =>
                                                    cancelAppointment(
                                                        appointment.id
                                                    )
                                                }
                                            >
                                                Cancel
                                            </button>

                                        </div>

                                    </div>

                                )
                            )}

                        </div>

                    ) : (

                        <div className="no-appointments">

                            <p>
                                You don't have any upcoming
                                appointments.
                            </p>

                            <button
                                className="new-appointment-btn"
                                onClick={() =>
                                    navigate("/appointments")
                                }
                            >

                                <FaPlus />

                                Book Appointment

                            </button>

                        </div>

                    )}

                </section>



                {/* Past Appointments */}

                <section className="appointment-section">

                    <div className="section-title">

                        <FaCalendarAlt />

                        <h3>
                            Past Appointments
                        </h3>

                    </div>


                    {pastAppointments.length > 0 ? (

                        <div className="appointments-list">

                            {pastAppointments.map(
                                (appointment) => (

                                    <div
                                        className="appointment-item past"
                                        key={appointment.id}
                                    >

                                        <div className="appointment-icon">

                                            <FaUserMd />

                                        </div>


                                        <div className="appointment-info">

                                            <h4>
                                                {appointment.doctor}
                                            </h4>


                                            <p>

                                                <FaCalendarAlt />

                                                {formatDate(
                                                    appointment.date
                                                )}

                                            </p>


                                            <p>

                                                <FaClock />

                                                {appointment.time}

                                            </p>


                                            <p>

                                                <strong>
                                                    Reason:
                                                </strong>{" "}

                                                {appointment.reason}

                                            </p>

                                        </div>


                                        <span className="past-label">
                                            Completed
                                        </span>

                                    </div>

                                )
                            )}

                        </div>

                    ) : (

                        <div className="no-appointments">

                            <p>
                                No past appointments.
                            </p>

                        </div>

                    )}

                </section>

            </div>



            {/* EDIT APPOINTMENT MODAL */}

            {editingAppointment && (

                <div className="edit-modal-overlay">

                    <div className="edit-modal">

                        <h3>
                            Edit Appointment
                        </h3>


                        <form onSubmit={saveEditedAppointment}>


                            {/* Doctor */}

                            <div className="form-group">

                                <label>
                                    Doctor
                                </label>

                                <input
                                    type="text"
                                    name="doctor"
                                    value={
                                        editingAppointment.doctor
                                    }
                                    onChange={handleEditChange}
                                    required
                                />

                            </div>


                            {/* Date */}

                            <div className="form-group">

                                <label>
                                    Date
                                </label>

                                <input
                                    type="date"
                                    name="date"
                                    value={
                                        editingAppointment.date
                                    }
                                    onChange={handleEditChange}
                                    required
                                />

                            </div>


                            {/* Time */}

                            <div className="form-group">

                                <label>
                                    Time
                                </label>

                                <select
                                    name="time"
                                    value={editingAppointment.time}
                                    onChange={handleEditChange}
                                    required
                                >
                                    <option value="">
                                        Select a time
                                    </option>

                                    {timeSlots.map((time) => (
                                        <option
                                            key={time}
                                            value={time}
                                        >
                                            {time}
                                        </option>
                                    ))}
                                </select>

                            </div>


                            {/* Reason */}

                            <div className="form-group">

                                <label>
                                    Reason for Appointment
                                </label>

                                <textarea
                                    name="reason"
                                    value={
                                        editingAppointment.reason
                                    }
                                    onChange={handleEditChange}
                                    required
                                />

                            </div>


                            {/* Modal Buttons */}

                            <div className="edit-modal-actions">

                                <button
                                    type="button"
                                    className="close-edit-btn"
                                    onClick={cancelEditing}
                                >
                                    Cancel
                                </button>


                                <button
                                    type="submit"
                                    className="save-edit-btn"
                                >
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


// Format date
function formatDate(dateString) {

    const date = new Date(
        dateString + "T00:00:00"
    );

    return date.toLocaleDateString("en-US", {
        month: "long",
        day: "numeric",
        year: "numeric"
    });

}


export default UpcomingAppointments;