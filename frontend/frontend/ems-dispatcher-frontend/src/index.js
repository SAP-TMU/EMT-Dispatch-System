// src/index.js

import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";
import { LoadScript } from "@react-google-maps/api";

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <LoadScript
      googleMapsApiKey={process.env.REACT_APP_GOOGLE_MAPS_API_KEY}
      libraries={[]}  // You can add "places" or "marker" here if needed
    >
      <App />
    </LoadScript>
  </React.StrictMode>
);
