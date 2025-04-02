// src/pages/RegisterPage.js

import React, { useState } from "react";
import './RegisterPage.css';

function RegisterPage() {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('');
  const [unitNumber, setUnitNumber] = useState('');

  const handleRegister = (e) => {
    e.preventDefault();
    const registrationData = {
      fullName,
      email,
      phone,
      password,
      role,
      ...(role === "EMT" && { unitNumber })
    };
    console.log("Registration:", registrationData);
  };

  return (
    <div className="register-container">
      <div className="register-box">
        <h2 className="register-header">Register</h2>
        <form onSubmit={handleRegister} className="register-form">
          <input
            type="text"
            className="form-input"
            placeholder="Full Name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            required
          />
          <input
            type="email"
            className="form-input"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="tel"
            className="form-input"
            placeholder="Phone Number"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
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

          <select
            className="form-input"
            value={role}
            onChange={(e) => setRole(e.target.value)}
            required
          >
            <option value="">Select Role</option>
            <option value="EMT">EMT</option>
            <option value="Dispatcher">Dispatcher</option>
          </select>

          {role === "EMT" && (
            <input
              type="text"
              className="form-input"
              placeholder="Unit Number"
              value={unitNumber}
              onChange={(e) => setUnitNumber(e.target.value)}
              required
            />
          )}

          <button type="submit" className="submit-button" aria-label="Register"></button>
        </form>
      </div>
    </div>
  );
}

export default RegisterPage;
