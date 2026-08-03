import "./Register.css";

import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import Button from "../../components/Button/Button";
import Input from "../../components/Input/Input";


function Register() {

  const navigate = useNavigate();

  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [address, setAddress] = useState("");
  const [dob, setDob] = useState("");
  const [gender, setGender] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");


  const handleRegister = (e) => {
    e.preventDefault();


    const user = {
      firstName,
      lastName,
      address,
      dob,
      gender,
      email,
      phone,
      password
    };


    localStorage.setItem(
      "user",
      JSON.stringify(user)
    );


    alert("Account Created Successfully!");

    navigate("/");
  };


  return (
    <div className="register-page">

      <div className="register-card">

        <h2>Create Account</h2>


        <form onSubmit={handleRegister}>


          <Input
            type="text"
            placeholder="First Name"
            value={firstName}
            onChange={(e)=>setFirstName(e.target.value)}
          />


          <Input
            type="text"
            placeholder="Last Name"
            value={lastName}
            onChange={(e)=>setLastName(e.target.value)}
          />


          <Input
            type="text"
            placeholder="Address"
            value={address}
            onChange={(e)=>setAddress(e.target.value)}
          />


          <Input
            type="date"
            value={dob}
            onChange={(e)=>setDob(e.target.value)}
          />


          <select
            className="Gender"
            value={gender}
            onChange={(e)=>setGender(e.target.value)}
          >

            <option value="">
              Select Gender
            </option>

            <option value="female">
              Female
            </option>

            <option value="male">
              Male
            </option>

            <option value="non-binary">
              Non-binary
            </option>

            <option value="prefer-not-to-say">
              Prefer not to say
            </option>

          </select>


          <Input
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e)=>setEmail(e.target.value)}
          />


          <Input
            type="tel"
            placeholder="Phone Number"
            value={phone}
            onChange={(e)=>setPhone(e.target.value)}
          />


          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e)=>setPassword(e.target.value)}
          />


          <Button text="Register"/>


        </form>


        <p>
          Already have an account?

          <Link to="/">
            Login
          </Link>

        </p>


      </div>

    </div>
  );
}


export default Register;