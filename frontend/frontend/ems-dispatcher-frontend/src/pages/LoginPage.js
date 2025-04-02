// src/pages/LoginPage.js

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import './Login.css';
import { users } from "../data/dummyUsers"; // Make sure this matches your filename

function LoginPage({ setUserRole }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    const foundUser = users.find(
      (user) => user.email === email && user.password === password
    );

    if (foundUser) {
      setUserRole(foundUser.role);
      if (foundUser.role === "Dispatcher") {
        navigate("/dashboard");
      } else {
        navigate("/emt-home");
      }
    } else {
      alert("Invalid credentials");
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2 className="login-header">Login</h2>
        <form onSubmit={handleSubmit} className="login-form">
          <input
            type="email"
            className="form-input"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            className="form-input"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit" className="submit-button" aria-label="Login"></button>
        </form>
        <p className="register-link">
          Don't have an account? <a href="/register-page">Register here</a>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;
