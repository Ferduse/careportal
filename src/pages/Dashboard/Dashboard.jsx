import { Link, NavLink, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import "./Dashboard.css";
import { apiGet } from "../../api/client";

import {
    FaHome,
    FaCalendarAlt,
    FaFileMedical,
    FaChartBar,
    FaCalendarCheck,
    FaShieldAlt,
    FaClipboard
} from "react-icons/fa";


function Dashboard() {

    const navigate = useNavigate();


    // Store appointments
    const [appointments, setAppointments] = useState([]);


    // Store latest risk result
    const [latestRisk, setLatestRisk] = useState(null);


    // Store medical history
    const [medicalHistory, setMedicalHistory] = useState({
        conditions: [],
        medications: [],
        allergies: [],
        surgeries: [],
        lastCheckup: ""
    });


    // Store logged-in user
    const [user, setUser] = useState(null);


    // Load dashboard information
    useEffect(() => {
        const loadDashboard = async () => {
            const accessToken = localStorage.getItem("access_token");

            if (!accessToken) {
                navigate("/");
                return;
            }

            try {
                const me = await apiGet("/api/v1/auth/me", accessToken);
                const firstName = me.full_name.split(" ")[0] || me.full_name;

                const userSnapshot = {
                    id: me.id,
                    email: me.email,
                    full_name: me.full_name,
                    firstName,
                };

                setUser(userSnapshot);
                localStorage.setItem("user", JSON.stringify(userSnapshot));

                const apiAppointments = await apiGet("/api/v1/appointments", accessToken);
                const mappedAppointments = apiAppointments
                    .filter((item) => item.status !== "canceled")
                    .map((item) => {
                        const start = new Date(item.start_time);
                        return {
                            id: item.id,
                            doctor: item.provider_name,
                            date: start.toISOString().slice(0, 10),
                            time: start.toLocaleTimeString("en-US", {
                                hour: "numeric",
                                minute: "2-digit",
                                hour12: true,
                            }),
                            reason: item.reason,
                        };
                    });

                setAppointments(mappedAppointments);
                localStorage.setItem("appointments", JSON.stringify(mappedAppointments));

                const predictionHistory = await apiGet("/api/v1/predictions", accessToken);
                if (predictionHistory.length > 0) {
                    const latest = predictionHistory[0];
                    setLatestRisk({
                        id: latest.id,
                        risk: latest.risk_label === "high_risk" ? "High" : "Low",
                        date: new Date(latest.created_at).toLocaleDateString("en-US", {
                            month: "long",
                            day: "numeric",
                            year: "numeric",
                        }),
                    });
                }

                const historyRecords = await apiGet("/api/v1/medical-history", accessToken);
                const summary = {
                    conditions: [],
                    medications: [],
                    allergies: [],
                    surgeries: [],
                    lastCheckup: localStorage.getItem("last_checkup") || "",
                };

                historyRecords.forEach((record) => {
                    const type = ["conditions", "medications", "allergies", "surgeries"].includes(record.condition_name)
                        ? record.condition_name
                        : "conditions";

                    summary[type].push({
                        id: record.id,
                        name: record.notes,
                        dateAdded: record.created_at.slice(0, 10),
                    });
                });

                setMedicalHistory(summary);
                localStorage.setItem("medicalHistory", JSON.stringify(summary));
            } catch (_error) {
                navigate("/");
            }
        };

        loadDashboard();

    }, []);


    // Logout
    const handleLogout = () => {

        // Keep the user's account information saved
        // but mark the user as logged out
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.setItem("isLoggedIn", "false");

        navigate("/");

    };


    // Get today's date
    const today = new Date();

    today.setHours(0, 0, 0, 0);


    // Get upcoming appointments
    const upcomingAppointments = appointments
        .filter((appointment) => {

            const appointmentDate =
                new Date(
                    appointment.date + "T00:00:00"
                );

            return appointmentDate >= today;

        })
        .sort((a, b) => {

            const dateA =
                new Date(
                    a.date + "T00:00:00"
                );

            const dateB =
                new Date(
                    b.date + "T00:00:00"
                );

            return dateA - dateB;

        });


    // Only show the next 3 appointments
    const dashboardAppointments =
        upcomingAppointments.slice(0, 3);


    return (

        <div className="dashboard-container">


            {/* Sidebar */}

            <div className="sidebar">

                <NavLink
                    to="/dashboard"
                    className={({ isActive }) =>
                        isActive
                            ? "side-item active"
                            : "side-item"
                    }
                >

                    <FaHome />

                    <span>
                        Dashboard
                    </span>

                </NavLink>


                <NavLink
                    to="/appointments"
                    className={({ isActive }) =>
                        isActive
                            ? "side-item active"
                            : "side-item"
                    }
                >

                    <FaCalendarAlt />

                    <span>
                        Book Appointment
                    </span>

                </NavLink>


                <NavLink
                    to="/medical-history"
                    className={({ isActive }) =>
                        isActive
                            ? "side-item active"
                            : "side-item"
                    }
                >

                    <FaFileMedical />

                    <span>
                        Medical
                        <br />
                        History
                    </span>

                </NavLink>


                <NavLink
                    to="/prediction"
                    className={({ isActive }) =>
                        isActive
                            ? "side-item active"
                            : "side-item"
                    }
                >

                    <FaChartBar />

                    <span>
                        Risk
                        <br />
                        Prediction
                    </span>

                </NavLink>

                {/* Logout */}

                <button
                    className="side-item logout-side-item"
                    onClick={handleLogout}
                >
                    <span>Logout</span>
                </button>

            </div>



            {/* Main Area */}

            <div className="main-content">


                {/* Navbar */}

              <div className="top-navbar">

                  <h2>
                      Dashboard
                  </h2>

                  <div className="welcome-message">

                      Welcome,{" "}

                      {user?.firstName || "User"}

                  </div>

               </div>



                {/* Dashboard Body */}

                <div className="dashboard-body">

                    <p>
                        Here's your health overview.
                    </p>



                    {/* Upcoming Appointments */}

                    <div className="dashboard-card">

                        <div className="card-icon">

                            <FaCalendarCheck size={45} />

                        </div>


                        <div className="appointment-card-content">

                            <div className="appointment-header">

                                <h3>
                                    Upcoming Appointments
                                </h3>


                                <Link to="/upcoming-appointments">
                                    View All 〉
                                </Link>

                            </div>


                            {dashboardAppointments.length > 0 ? (

                                dashboardAppointments.map(
                                    (appointment) => (

                                        <div
                                            className="upcoming-appointment"
                                            key={appointment.id}
                                        >

                                            <p>
                                                <b>
                                                    {appointment.doctor}
                                                </b>
                                            </p>


                                            <p>

                                                {formatDate(
                                                    appointment.date
                                                )}

                                                {" • "}

                                                {appointment.time}

                                            </p>


                                            <p>
                                                {appointment.reason}
                                            </p>

                                        </div>

                                    )

                                )

                            ) : (

                                <div>

                                    <p>
                                        No upcoming appointments.
                                    </p>


                                    <Link to="/appointments">
                                        Book Appointment 〉
                                    </Link>

                                </div>

                            )}

                        </div>

                    </div>



                    {/* Risk Card */}

                    <div className="dashboard-card">

                        <div className="card-icon">

                            <FaShieldAlt size={45} />

                        </div>


                        <div>

                            <h3>
                                Latest Risk Result
                            </h3>


                            {latestRisk ? (

                                <>

                                    <p>

                                        Diabetes Risk:

                                        <span className="risk">
                                            {latestRisk.risk}
                                        </span>

                                    </p>


                                    <p>
                                        {latestRisk.date}
                                    </p>

                                </>

                            ) : (

                                <>

                                    <p>
                                        No risk assessment yet.
                                    </p>


                                    <p>
                                        Complete your first assessment.
                                    </p>

                                </>

                            )}


                            <NavLink
                                className="dashboard-link"
                                to="/risk-history"
                            >
                                View History 〉
                            </NavLink>

                        </div>

                    </div>



                    {/* Medical History Card */}

                    <div className="dashboard-card">

                        <div className="card-icon">

                            <FaClipboard size={45} />

                        </div>


                        <div>

                            <h3>
                                Medical History Summary
                            </h3>


                            <p>

                                Conditions:&nbsp;

                                <span className="number">

                                    {
                                        medicalHistory
                                            .conditions
                                            .length
                                    }

                                </span>

                            </p>


                            <p>

                                Medications:&nbsp;

                                <span className="number">

                                    {
                                        medicalHistory
                                            .medications
                                            .length
                                    }

                                </span>

                            </p>


                            <p>

                                Allergies:&nbsp;

                                <span className="number">

                                    {
                                        medicalHistory
                                            .allergies
                                            .length
                                    }

                                </span>

                            </p>


                            <p>

                                Surgeries:&nbsp;

                                <span className="number">

                                    {
                                        medicalHistory
                                            .surgeries
                                            .length
                                    }

                                </span>

                            </p>


                            <p>

                                Last Checkup:&nbsp;

                                <span className="date">

                                    {
                                        medicalHistory.lastCheckup

                                            ? formatDate(
                                                medicalHistory.lastCheckup
                                            )

                                            : "Not recorded"
                                    }

                                </span>

                            </p>


                            <Link
                                className="dashboard-link"
                                to="/medical-history"
                            >
                                View Full History 〉
                            </Link>

                        </div>

                    </div>


                </div>

            </div>

        </div>

    );

}


// Format date for display
function formatDate(dateString) {

    const date = new Date(
        dateString + "T00:00:00"
    );

    return date.toLocaleDateString(
        "en-US",
        {
            month: "long",
            day: "numeric",
            year: "numeric"
        }
    );

}


export default Dashboard;


