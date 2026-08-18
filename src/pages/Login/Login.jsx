import "./Login.css";

import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import Button from "../../components/Button/Button";
import Input from "../../components/Input/Input";

import { FaHeartbeat } from "react-icons/fa";


function Login(){

  const navigate = useNavigate();


  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");



  const handleLogin = (e)=>{

    e.preventDefault();


    const savedUser = JSON.parse(
      localStorage.getItem("user")
    );


    if(!savedUser){

      alert("No account found. Please register first.");

      return;
    }


    if(
      email === savedUser.email &&
      password === savedUser.password
    ){

      localStorage.setItem(
        "loggedInUser",
        JSON.stringify(savedUser)
      );


      alert("Login Successful!");

      navigate("/dashboard");


    }else{

      alert("Incorrect Email or Password");

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


<Link to="/Register">

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