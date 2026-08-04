import { useEffect, useState } from "react";
import { NavLink } from "react-router-dom";
import { FaArrowLeft, FaShieldAlt } from "react-icons/fa";
import "./RiskHistory.css";

function RiskHistory() {

    const [results, setResults] = useState([]);

    useEffect(() => {

        const savedResults =
            JSON.parse(localStorage.getItem("riskResults")) || [];

        setResults(savedResults);

    }, []);

    return (

        <div className="risk-history-page">

            <div className="history-header">

                <NavLink to="/dashboard">
                    <FaArrowLeft />
                </NavLink>

                <h2>Risk History</h2>

            </div>

            {results.length === 0 ? (

                <div className="empty-history">

                    <FaShieldAlt size={40} />

                    <h3>No Risk Results Yet</h3>

                    <p>
                        Complete a diabetes risk assessment
                        to see your results here.
                    </p>

                </div>

            ) : (

                <div className="history-list">

                    {results.map((result) => (

                        <div
                            className="history-card"
                            key={result.id}
                        >

                            <div className="history-icon">
                                <FaShieldAlt size={30} />
                            </div>

                            <div className="history-info">

                                <h3>
                                    Diabetes Risk
                                </h3>

                                <p>
                                    Risk Level:
                                    <span className="risk">
                                        {result.risk}
                                    </span>
                                </p>

                                <p>
                                    {result.date}
                                </p>

                            </div>

                        </div>

                    ))}

                </div>

            )}

        </div>
    );
}

export default RiskHistory;