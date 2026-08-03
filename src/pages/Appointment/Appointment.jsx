import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Appointment.css";
import { FaArrowLeft, FaCalendarAlt } from "react-icons/fa";

function Appointment() {
    const navigate = useNavigate();

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

        <form className="appointment-form">

          <div className="form-group">
            <label>Select Doctor</label>

            <select>
              <option>Dr. Sarah Smith (General Physician)</option>
              <option>Dr. John Williams (Cardiologist)</option>
              <option>Dr. Emily Davis (Dermatologist)</option>
              <option>Dr. Michael Brown (Pediatrician)</option>
            </select>
          </div>

          <div className="form-group">
            <label>Date</label>

            <div className="date-input">
              <input type="date" />
              <FaCalendarAlt className="calendar-icon" />
            </div>
          </div>

          <div className="form-group">
            <label>Time</label>

            <select>
              <option>10:00 AM</option>
              <option>11:00 AM</option>
              <option>12:00 PM</option>
              <option>1:00 PM</option>
              <option>2:00 PM</option>
              <option>3:00 PM</option>
            </select>
          </div>

          <div className="form-group">
            <label>Reason for Visit</label>

            <textarea
              rows="5"
              placeholder="Enter reason for visit..."
            ></textarea>
          </div>

          <button className="book-btn">
            Book Appointment
          </button>

          <button
            type="button"
            className="cancel-btn"
          >
            Cancel
          </button>

        </form>

      </div>
    </div>
  );
}

export default Appointment;