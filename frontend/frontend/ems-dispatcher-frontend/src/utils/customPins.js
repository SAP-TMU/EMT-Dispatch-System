// src/utils/customPins.js

// Utility to return icon based on pin type
export const getCustomIconUrl = (type) => {
  switch (type) {
    case "ambulance":
      return process.env.PUBLIC_URL + "/icons/ambulance.png";
    case "hospital":
      return process.env.PUBLIC_URL + "/icons/hospital.png";
    case "request":
      return process.env.PUBLIC_URL + "/icons/request.png";
    default:
      return process.env.PUBLIC_URL + "/icons/default.png";
  }
};

// Example pin data
export const getCustomPinsData = () => [
  {
    id: 1,
    type: "ambulance",
    lat: 43.6532,
    lng: -79.3832,
    name: "Ambulance 1",
  },
  {
    id: 2,
    type: "hospital",
    lat: 43.6542,
    lng: -79.3842,
    name: "Hospital A",
  },
  {
    id: 3,
    type: "request",
    lat: 43.6562,
    lng: -79.3862,
    name: "Emergency Request 1",
  },
];
