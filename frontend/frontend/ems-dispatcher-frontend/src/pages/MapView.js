// src/pages/MapView.js

import React, { useState } from "react";
import { GoogleMap, Marker } from "@react-google-maps/api";
import { getCustomPinsData, getCustomIconUrl } from "../utils/customPins";
import mapStyles from "../mapStyles";

const containerStyle = {
  width: "75vw",
  height: "75vh",
  margin: "20px auto",
  borderRadius: "10px",
  boxShadow: "0 0 10px rgba(0, 0, 0, 0.2)",
};

const tmuCoordinates = { lat: 43.6532, lng: -79.3832 };

const MapView = () => {
  const allPins = getCustomPinsData();
  const [filter, setFilter] = useState("all");

  const filteredPins =
    filter === "all"
      ? allPins
      : allPins.filter((pin) => pin.type.toLowerCase() === filter);

  return (
    <div style={{ textAlign: "center", paddingTop: "20px" }}>

      {/* Filter buttons */}
      <div style={{ marginBottom: "10px" }}>
        {["all", "ambulance", "hospital", "request"].map((type) => (
          <button
            key={type}
            onClick={() => setFilter(type)}
            style={{
              margin: "0 5px",
              padding: "8px 16px",
              borderRadius: "6px",
              border: "1px solid #ccc",
              backgroundColor: filter === type ? "#007bff" : "#fff",
              color: filter === type ? "#fff" : "#000",
              cursor: "pointer",
            }}
          >
            {type.charAt(0).toUpperCase() + type.slice(1)}
          </button>
        ))}
      </div>

      {/* Map (no LoadScript here!) */}
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={tmuCoordinates}
        zoom={15}
        options={{ styles: mapStyles }}
      >
        {filteredPins.map((pin) => (
          <Marker
            key={pin.id}
            position={{ lat: pin.lat, lng: pin.lng }}
            icon={{
              url: getCustomIconUrl(pin.type),
              scaledSize: new window.google.maps.Size(35, 35),
            }}
          />
        ))}
      </GoogleMap>
    </div>
  );
};

export default MapView;
