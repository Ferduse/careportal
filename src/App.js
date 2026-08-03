import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login/Login";
import Register from "./pages/Register/Register";
import Dashboard from "./pages/Dashboard/Dashboard";
import Appointment from "./pages/Appointment/Appointment";
import MedicalHistory from "./pages/MedicalHistory/MedicalHistory";
import Prediction from "./pages/Prediction/Prediction";




function App() {

  return (

    <BrowserRouter>

      <Routes>

        {/* Authentication */}
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />


        {/* Patient Pages */}
        <Route path="/dashboard" element={<Dashboard />} />

        <Route path="/appointments" element={<Appointment />} />

        <Route path="/medical-history" element={<MedicalHistory />} />

        <Route path="/prediction" element={<Prediction /> } />


        {/* Temporary Pages */}
        <Route 
          path="/profile" 
          element={<h1>Profile Page</h1>} 
        />


      </Routes>

    </BrowserRouter>

  );

}


export default App;

