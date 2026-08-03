import "./Navbar.css";

import { useNavigate } from "react-router-dom";


function Navbar(){

    const navigate = useNavigate();


    const logout = () => {

        localStorage.removeItem("loggedInUser");

        navigate("/");

    };


    return (

        <nav className="navbar">


            <div className="navbar-title">

                ❤️ Healthcare Assistant

            </div>


            <button 
                className="logout-btn"
                onClick={logout}
            >
                Logout
            </button>


        </nav>

    );

}


export default Navbar;