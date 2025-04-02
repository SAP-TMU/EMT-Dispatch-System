import React, { useEffect, useState } from "react";
import {
  GoogleMap,
  Marker,
  DirectionsRenderer,
  useJsApiLoader
} from "@react-google-maps/api";
import {
  emtId,
  emtInitialLocation,
  callerInfo,
  hospitalInfo
} from "../data/dummyEmtData";
import "./EMTHome.css";

const containerStyle = {
  width: "100%",
  height: "100%",
};

const center = emtInitialLocation;

function EMTHome() {
  const [status, setStatus] = useState("En Route");
  const [pendingStatus, setPendingStatus] = useState("");
  const [showConfirmPopup, setShowConfirmPopup] = useState(false);
  const [assignmentPopup, setAssignmentPopup] = useState(true);
  const [requestAccepted, setRequestAccepted] = useState(null);
  const [directions, setDirections] = useState(null);
  const [currentLocation] = useState(emtInitialLocation);

  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
  });

  useEffect(() => {
    let timer;
    if (assignmentPopup) {
      timer = setTimeout(() => {
        if (requestAccepted === null) {
          setAssignmentPopup(false);
          console.log("Request auto-declined");
        }
      }, 10000);
    }
    return () => clearTimeout(timer);
  }, [assignmentPopup, requestAccepted]);

  useEffect(() => {
    if (!isLoaded) return;

    const directionsService = new window.google.maps.DirectionsService();

    const origin = status === "On Scene" ? callerInfo.location : currentLocation;
    const destination = status === "On Scene" ? hospitalInfo.location : callerInfo.location;

    directionsService.route(
      {
        origin,
        destination,
        travelMode: window.google.maps.TravelMode.DRIVING,
      },
      (result, resultStatus) => {
        if (resultStatus === "OK") {
          setDirections(result);
        }
      }
    );
  }, [status, isLoaded]);

  const handleStatusChange = (e) => {
    setPendingStatus(e.target.value);
    setShowConfirmPopup(true);
  };

  const confirmStatusChange = () => {
    setStatus(pendingStatus);
    setShowConfirmPopup(false);
  };

  const handleAccept = () => {
    setRequestAccepted(true);
    setAssignmentPopup(false);
  };

  const handleDecline = () => {
    setRequestAccepted(false);
    setAssignmentPopup(false);
  };

  if (!isLoaded) return <p>Loading map...</p>;

  return (
    <div className="emt-home-container">
      
      <div className="map-container">
        <GoogleMap mapContainerStyle={containerStyle} center={center} zoom={13}>
          <Marker position={currentLocation} label={{ text: "🚑", fontSize: "20px" }} />
          <Marker position={callerInfo.location} label={{ text: "📍", fontSize: "20px" }} />
          {status === "On Scene" && (
            <Marker position={hospitalInfo.location} label={{ text: "🏥", fontSize: "20px" }} />
          )}
          {directions && (
            <DirectionsRenderer
              directions={directions}
              options={{ suppressMarkers: true }}
            />
          )}
        </GoogleMap>
      </div>

      <div className="info-grid">
        <div className="info-card">
          <h4>🧍 Caller Info</h4>
          <p><strong>Name:</strong> {callerInfo.name}</p>
          <p><strong>Age:</strong> {callerInfo.age}</p>
          <p><strong>Diagnosis:</strong> {callerInfo.diagnosis}</p>
          <p><strong>Priority:</strong> {callerInfo.priority}</p>
        </div>

        <div className="info-card">
          <h4>📟 EMT Status</h4>
          <select onChange={handleStatusChange} value={status}>
            <option>En Route</option>
            <option>On Scene</option>
            <option>Transporting</option>
            <option>At Hospital</option>
            <option>Available</option>
          </select>
        </div>

        <div className="info-card">
          <h4>🕒 EMT Info</h4>
          <p><strong>ID:</strong> {emtId}</p>
          <p><strong>Time:</strong> {new Date().toLocaleTimeString()}</p>
          <p><strong>Lat:</strong> {currentLocation.lat.toFixed(4)}</p>
          <p><strong>Lng:</strong> {currentLocation.lng.toFixed(4)}</p>
        </div>
      </div>

      {/* Confirm Status Popup */}
      {showConfirmPopup && (
        <div className="popup">
          <div className="popup-box">
            <p>Change status to <strong>{pendingStatus}</strong>?</p>
            <div className="popup-btns">
              <button onClick={confirmStatusChange}>Yes</button>
              <button onClick={() => setShowConfirmPopup(false)}>No</button>
            </div>
          </div>
        </div>
      )}

      {/* Assignment Popup */}
      {assignmentPopup && (
        <div className="popup">
          <div className="popup-box">
            <p><strong>🚨 New Dispatch Assignment</strong></p>
            <div className="popup-btns">
              <button onClick={handleAccept}>Accept</button>
              <button onClick={handleDecline}>Decline</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default EMTHome;
