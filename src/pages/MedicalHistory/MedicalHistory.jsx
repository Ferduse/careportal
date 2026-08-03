import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./MedicalHistory.css";
import { FaArrowLeft, FaCalendarAlt } from "react-icons/fa";

function MedicalHistory() {
    const navigate = useNavigate();
    
  const [medicalHistory, setMedicalHistory] = useState({
    conditions: "",
    medications: "",
    allergies: "",
    surgeries: "",
    lastCheckup: "",
  });

  const handleChange = (e) => {
    setMedicalHistory({
      ...medicalHistory,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    console.log(medicalHistory);

    alert("Medical history saved successfully!");
  };

  return (
    <div className="page">

      <div className="phone">

      <header>
        <FaArrowLeft
            className="back-icon"
            onClick={() => navigate("/dashboard")}
        />
        <h2>Medical History</h2>
      </header>

        <form onSubmit={handleSubmit}>

          <div className="input-group">
            <label>Past Medical Conditions</label>

            <textarea
              name="conditions"
              placeholder="e.g. Hypertension, Asthma"
              value={medicalHistory.conditions}
              onChange={handleChange}
            />
          </div>

          <div className="input-group">
            <label>Current Medications</label>

            <textarea
              name="medications"
              placeholder="e.g. Metformin 500mg"
              value={medicalHistory.medications}
              onChange={handleChange}
            />
          </div>

          <div className="input-group">
            <label>Allergies</label>

            <textarea
              name="allergies"
              placeholder="e.g. Penicillin, Pollen"
              value={medicalHistory.allergies}
              onChange={handleChange}
            />
          </div>

          <div className="input-group">
            <label>Past Surgeries</label>

            <textarea
              name="surgeries"
              placeholder="e.g. Appendectomy (2018)"
              value={medicalHistory.surgeries}
              onChange={handleChange}
            />
          </div>

          <div className="input-group">
            <label>Last Checkup Date</label>

            <div className="date-input">

              <input
                type="date"
                name="lastCheckup"
                value={medicalHistory.lastCheckup}
                onChange={handleChange}
              />

              <FaCalendarAlt className="calendar-icon" />

            </div>

          </div>

          <button type="submit">
            Save Changes
          </button>

        </form>

      </div>

    </div>
  );
}

export default MedicalHistory;