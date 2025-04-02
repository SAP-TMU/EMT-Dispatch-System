// src/pages/LandingPage.js

import React from "react";

function LandingPage() {
  return (
    <div className="centered-container">
      <h1>🚑 EMS Dispatcher System</h1>
      <p>Welcome to the Emergency Medical Services interface.</p>
      <p>Please login or register to continue.</p>

      <div style={{ marginTop: "2rem" }}>
        <button style={{ marginRight: "1rem", padding: "8px 16px" }}>
          Login
        </button>
        <button style={{ padding: "8px 16px" }}>
          Register
        </button>
      </div>
    </div>
  );
}

export default LandingPage;
