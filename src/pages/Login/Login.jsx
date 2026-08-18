import "./Login.css";

import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import Button from "../../components/Button/Button";
import Input from "../../components/Input/Input";
import { apiGet, apiPost } from "../../api/client";

import { FaHeartbeat } from "react-icons/fa";


function Login(){

  const navigate = useNavigate();


  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");



  const handleLogin = async (e)=>{

    e.preventDefault();


    try {
      const tokenData = await apiPost("/api/v1/auth/login", {
        email,
        password,
      });

      localStorage.setItem("access_token", tokenData.access_token);
      localStorage.setItem("refresh_token", tokenData.refresh_token);

      const user = await apiGet("/api/v1/auth/me", tokenData.access_token);
      const firstName = user.full_name.split(" ")[0] || user.full_name;

      localStorage.setItem(
        "user",
        JSON.stringify({
          id: user.id,
          email: user.email,
          full_name: user.full_name,
          firstName,
        })
      );

      localStorage.setItem("isLoggedIn", "true");

      alert("Login successful!");
      navigate("/dashboard");
    } catch (error) {
      alert(error.message || "Login failed");
    }

  };



return(

<div className="login-page">

<div className="login-card">


<div className="logo">

<FaHeartbeat 
size={60} 
color="#2563eb"
/>


<h2>
Healthcare Appointment
</h2>


<p>
Diagnostic Assistant
</p>

</div>



<h3>
Welcome Back
</h3>



<form onSubmit={handleLogin}>


<Input
type="email"
placeholder="Email"
value={email}
onChange={(e)=>setEmail(e.target.value)}
/>



<Input
type="password"
placeholder="Password"
value={password}
onChange={(e)=>setPassword(e.target.value)}
/>



<Button text="Login"/>


</form>



<p>

New Here?


<Link to="/register">

 Register

</Link>


</p>



</div>

</div>

)

}


export default Login;

//  Genesiszol@gmail.com
// Yukarizoldyck