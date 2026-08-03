import { Link, NavLink } from "react-router-dom";
import { useState } from "react";
import "./Dashboard.css";
import { 
  FaBars,
  FaUserCircle,
  FaHome,
  FaCalendarAlt,
  FaFileMedical,
  FaChartBar,
  FaCog,
  FaCalendarCheck,
  FaShieldAlt,
  FaClipboard
} from "react-icons/fa";



function Dashboard(){
  const [sidebarOpen, setSidebarOpen] = useState(true);

return (

<div className="dashboard-container">


{/* Sidebar */}

<div className="sidebar">

  <NavLink
    to="/dashboard"
    className={({ isActive }) =>
      isActive ? "side-item active" : "side-item"
    }
  >
    <FaHome />
    <span>Dashboard</span>
  </NavLink>

  <NavLink
    to="/appointments"
    className={({ isActive }) =>
      isActive ? "side-item active" : "side-item"
    }
  >
    <FaCalendarAlt />
    <span>Appointments</span>
  </NavLink>

  <NavLink
    to="/medical-history"
    className={({ isActive }) =>
      isActive ? "side-item active" : "side-item"
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
      isActive ? "side-item active" : "side-item"
    }
  >
    <FaChartBar />
    <span>
      Risk
      <br />
      Prediction
    </span>
  </NavLink>

</div>


{/* Main Area */}

<div className="main-content">



{/* Navbar */}

<div className="menu-btn" onClick={() => setSidebarOpen(!sidebarOpen)}>
    <FaBars size={25} />
    <h2>Dashboard</h2>
</div>






{/* Dashboard Content */}

<div className="dashboard-body">


<h2>
Welcome, Patient!
</h2>


<p>
Here's your health overview.
</p>






{/* Appointment Card */}

<div className="dashboard-card">


<div className="card-icon">

<FaCalendarCheck size={45}/>

</div>



<div>


<h3>
Upcoming Appointment
</h3>


<p>
<b>
Dr. Sarah Smith
</b>
</p>


<p>
May 24, 2025 • 10:00 AM
</p>


<p>
General Physician
</p>


<Link to="/appointments">
View Details 〉
</Link>


</div>


</div>







{/* Risk Card */}

<div className="dashboard-card">


<div className="card-icon">

<FaShieldAlt size={45}/>

</div>




<div>


<h3>
Latest Risk Result
</h3>



<p>
Diabetes Risk:

<span className="risk">
Medium
</span>

</p>



<p>
May 18, 2025
</p>



<a>
View History 〉
</a>



</div>


</div>







{/* Medical History Card */}

<div className="dashboard-card">


<div className="card-icon">

<FaClipboard size={45}/>

</div>




<div>


<h3>
Medical History Summary
</h3>



<p>
Conditions

<span className="number">
2
</span>

</p>



<p>
Medications

<span className="number">
1
</span>

</p>



<p>
Allergies

<span className="number">
1
</span>

</p>



<p>
Surgeries

<span className="number">
0
</span>

</p>



<p>
Last Checkup

<span className="date">
Jan 15, 2025
</span>

</p>



<Link to="/medical-history">
  View Full History 〉
</Link>



</div>


</div>




</div>


</div>


</div>


);

}


export default Dashboard;