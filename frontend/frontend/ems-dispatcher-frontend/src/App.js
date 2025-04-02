import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Header from "./components/Header";
import MapView from "./pages/MapView";
import DashboardPage from "./pages/Dashboard";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import EMTHome from "./pages/EMTHome";

function App() {
  const [userRole, setUserRole] = useState(null);

  const headerTitle =
    userRole === "Dispatcher"
      ? "EMS Dispatcher"
      : userRole === "EMT"
      ? "EMT Dashboard"
      : "";

  return (
    <Router>
      <div className="centered-container">
        {userRole && (
          <Header
            userRole={userRole}
            setUserRole={setUserRole}
            title={headerTitle}
          />
        )}

        <Routes>
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="/login" element={<LoginPage setUserRole={setUserRole} />} />
          <Route path="/register-page" element={<RegisterPage />} />
          <Route
            path="/map"
            element={userRole === "Dispatcher" ? <MapView /> : <Navigate to="/login" />}
          />
          <Route
            path="/dashboard"
            element={userRole === "Dispatcher" ? <DashboardPage /> : <Navigate to="/login" />}
          />
          <Route
            path="/emt-home"
            element={userRole === "EMT" ? <EMTHome /> : <Navigate to="/login" />}
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
