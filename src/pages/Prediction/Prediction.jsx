
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Prediction.css";
import { FaArrowLeft } from "react-icons/fa";


const Prediction = () => {

  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    age: "",
    gender: "",
    hypertension: "",
    heart_disease: "",
    bmi: "",
    HbA1c_level: "",
    blood_glucose_level: "",
    smoking_history: "",
  });

  const [result, setResult] = useState(null);


  const handleChange = (e) => {

    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

  };


  const handleSubmit = (e) => {

    e.preventDefault();


    // Data that will eventually be sent to your backend
    const payload = {
      age: parseInt(formData.age),
      gender: formData.gender,
      hypertension: formData.hypertension === "true",
      heart_disease: formData.heart_disease === "true",
      bmi: parseFloat(formData.bmi),
      HbA1c_level: parseFloat(formData.HbA1c_level),
      blood_glucose_level: parseInt(formData.blood_glucose_level),
      smoking_history: formData.smoking_history,
    };


    console.log("Prediction payload:", payload);


    /*
      TEMPORARY RESULT

      Your backend team will eventually replace this
      with the actual prediction returned from the API.
    */
    const riskLevel = "Medium";


    // Create a new risk result
    const newRiskResult = {

      id: Date.now(),

      risk: riskLevel,

      date: new Date().toLocaleDateString("en-US", {
        month: "long",
        day: "numeric",
        year: "numeric"
      }),

      // Save the information used for the prediction
      ...payload

    };


    // Get previous risk results
    const previousResults =
      JSON.parse(localStorage.getItem("riskResults")) || [];


    // Add newest result to the beginning
    const updatedResults = [
      newRiskResult,
      ...previousResults
    ];


    // Save results
    localStorage.setItem(
      "riskResults",
      JSON.stringify(updatedResults)
    );


    // Display result on this page
    setResult(riskLevel);

  };


  return (

    <div className="prediction-container">

      <div className="prediction-card">


        <header>

          <FaArrowLeft
            className="back-icon"
            onClick={() => navigate("/dashboard")}
          />

          <h2>
            Enter Your Health Information
          </h2>

        </header>


        <form onSubmit={handleSubmit}>

          <div className="form-grid">


            {/* Age */}

            <div className="form-group">

              <label>
                Age
              </label>

              <input
                type="number"
                name="age"
                value={formData.age}
                onChange={handleChange}
                placeholder="45"
                required
              />

            </div>


            {/* Gender */}

            <div className="form-group">

              <label>
                Gender
              </label>

              <select
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                required
              >

                <option value="">
                  Select Gender
                </option>

                <option value="gender_Female">
                  Female
                </option>

                <option value="gender_Male">
                  Male
                </option>

                <option value="gender_Other">
                  Other
                </option>

              </select>

            </div>


            {/* Hypertension */}

            <div className="form-group">

              <label>
                Hypertension
              </label>

              <select
                name="hypertension"
                value={formData.hypertension}
                onChange={handleChange}
                required
              >

                <option value="">
                  Select
                </option>

                <option value="true">
                  Yes
                </option>

                <option value="false">
                  No
                </option>

              </select>

            </div>


            {/* Heart Disease */}

            <div className="form-group">

              <label>
                Heart Disease
              </label>

              <select
                name="heart_disease"
                value={formData.heart_disease}
                onChange={handleChange}
                required
              >

                <option value="">
                  Select
                </option>

                <option value="true">
                  Yes
                </option>

                <option value="false">
                  No
                </option>

              </select>

            </div>


            {/* BMI */}

            <div className="form-group">

              <label>
                BMI (kg/m²)
              </label>

              <input
                type="number"
                step="0.1"
                name="bmi"
                value={formData.bmi}
                onChange={handleChange}
                placeholder="27.4"
                required
              />

            </div>


            {/* HbA1c */}

            <div className="form-group">

              <label>
                HbA1c Level
              </label>

              <input
                type="number"
                step="0.1"
                name="HbA1c_level"
                value={formData.HbA1c_level}
                onChange={handleChange}
                placeholder="6.5"
                required
              />

            </div>


            {/* Blood Glucose */}

            <div className="form-group">

              <label>
                Blood Glucose Level (mg/dL)
              </label>

              <input
                type="number"
                name="blood_glucose_level"
                value={formData.blood_glucose_level}
                onChange={handleChange}
                placeholder="140"
                required
              />

            </div>


            {/* Smoking History */}

            <div className="form-group">

              <label>
                Smoking History
              </label>

              <select
                name="smoking_history"
                value={formData.smoking_history}
                onChange={handleChange}
                required
              >

                <option value="">
                  Select
                </option>

                <option value="smoking_history_No">
                  No
                </option>

                <option value="smoking_history_current">
                  Current
                </option>

                <option value="smoking_history_ever">
                  Ever
                </option>

                <option value="smoking_history_former">
                  Former
                </option>

                <option value="smoking_history_never">
                  Never
                </option>

                <option value="smoking_history_not_current">
                  Not Current
                </option>

              </select>

            </div>


          </div>


          <button
            type="submit"
            className="predict-btn"
          >
            Predict Risk
          </button>

        </form>


        {/* Prediction Result */}
        {result && (
        <div className="result-card">

            <h3>Prediction Result</h3>

            <div className="result-content">

                <div className={`risk-badge ${result.toLowerCase()}`}>
                    {result} Risk
                </div>

                <button
                    className="dashboard-btn"
                    onClick={() => navigate("/dashboard")}
                >
                    Return to Dashboard
                </button>

            </div>

            {/* <p className="disclaimer">
                This prediction is for informational purposes only and is not a medical diagnosis.
            </p> */}

        </div>
    )}

      </div>

    </div>

  );

};


export default Prediction;

