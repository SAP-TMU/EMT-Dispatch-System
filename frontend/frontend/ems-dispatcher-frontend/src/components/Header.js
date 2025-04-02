import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { FaAmbulance } from "react-icons/fa";
import "./Header.css";

function Header({ userRole, setUserRole, title }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    setUserRole(null);
    localStorage.removeItem("userRole");
    navigate("/login");
  };

  return (
    <header className="custom-header">
      <div className="logo-title">
        <FaAmbulance className="logo-icon" />
        <h1>{title}</h1>
      </div>
      <nav className="nav-buttons">
        {userRole === "Dispatcher" && (
          <>
            <Link to="/map" className="nav-btn">Map</Link>
            <Link to="/dashboard" className="nav-btn">Dashboard</Link>
          </>
        )}
        {userRole ? (
          <button className="nav-btn logout" onClick={handleLogout}>Logout</button>
        ) : (
          <Link to="/login" className="nav-btn">Login</Link>
        )}
      </nav>
    </header>
  );
}

export default Header;
