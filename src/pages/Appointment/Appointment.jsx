import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Appointment.css";
import { FaArrowLeft, FaCalendarAlt } from "react-icons/fa";

function Appointment() {
    const navigate = useNavigate();

    const [doctor, setDoctor] = useState("");
    const [date, setDate] = useState("");
    const [time, setTime] = useState("");
    const [reason, setReason] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();

        const newAppointment = {
            id: Date.now(),
            doctor,
            date,
            time,
            reason
        };

        // Get existing appointments
        const existingAppointments =
            JSON.parse(localStorage.getItem("appointments")) || [];

        // Add new appointment
        existingAppointments.push(newAppointment);

        // Save all appointments
        localStorage.setItem(
            "appointments",
            JSON.stringify(existingAppointments)
        );

        // Go to dashboard
        navigate("/dashboard");
    };

    return (
        <div className="appointment-page">

            <div className="appointment-card">

                <header>

                    <FaArrowLeft
                        className="back-icon"
                        onClick={() => navigate("/dashboard")}
                    />

                    <h2>Book Appointment</h2>

                </header>


                <form
                    className="appointment-form"
                    onSubmit={handleSubmit}
                >

                    {/* Doctor */}

                    <div className="form-group">

                        <label>Select Doctor</label>

                        <select
                            value={doctor}
                            onChange={(e) => setDoctor(e.target.value)}
                            required
                        >

                            <option value="">
                                Select a doctor
                            </option>

                            <option value="Dr. Sarah Smith (General Physician)">
                                Dr. Sarah Smith (General Physician)
                            </option>

                            <option value="Dr. John Williams (Cardiologist)">
                                Dr. John Williams (Cardiologist)
                            </option>

                            <option value="Dr. Emily Davis (Dermatologist)">
                                Dr. Emily Davis (Dermatologist)
                            </option>

                            <option value="Dr. Michael Brown (Pediatrician)">
                                Dr. Michael Brown (Pediatrician)
                            </option>

                        </select>

                    </div>


                    {/* Date */}

                    <div className="form-group">

                        <label>Date</label>

                        <div className="date-input">

                            <input
                                type="date"
                                value={date}
                                onChange={(e) => setDate(e.target.value)}
                                required
                            />

                            <FaCalendarAlt className="calendar-icon" />

                        </div>

                    </div>


                    {/* Time */}

                    <div className="form-group">

                        <label>Time</label>

                        <select
                            value={time}
                            onChange={(e) => setTime(e.target.value)}
                            required
                        >

                            <option value="">
                                Select a time
                            </option>

                            <option value="10:00 AM">
                                10:00 AM
                            </option>

                            <option value="11:00 AM">
                                11:00 AM
                            </option>

                            <option value="12:00 PM">
                                12:00 PM
                            </option>

                            <option value="1:00 PM">
                                1:00 PM
                            </option>

                            <option value="2:00 PM">
                                2:00 PM
                            </option>

                            <option value="3:00 PM">
                                3:00 PM
                            </option>

                        </select>

                    </div>


                    {/* Reason */}

                    <div className="form-group">

                        <label>Reason for Visit</label>

                        <textarea
                            rows="5"
                            placeholder="Enter reason for visit..."
                            value={reason}
                            onChange={(e) => setReason(e.target.value)}
                            required
                        />

                    </div>


                    {/* Book */}

                    <button
                        type="submit"
                        className="book-btn"
                    >
                        Book Appointment
                    </button>


                    {/* Cancel */}

                    <button
                        type="button"
                        className="cancel-btn"
                        onClick={() => navigate("/dashboard")}
                    >
                        Cancel
                    </button>

                </form>

            </div>

        </div>
    );
}

export default Appointment;

