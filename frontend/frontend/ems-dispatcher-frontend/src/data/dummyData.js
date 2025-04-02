// src/data/dummyData.js

export const dummyEmergencies = [
    { title: 'Cardiac Emergency', location: '123 Main St', unit: 'EMT-A1', eta: '4 min', priority: 5 },
    { title: 'Traffic Accident', location: '456 Oak Ave', unit: 'EMT-B3', eta: '8 min', priority: 3 },
  ];
  
  export const dummyHospitals = [
    { name: 'Central Hospital', capacity: '85%', beds: 4, status: 'Available' },
    { name: "St. Mary's Medical", capacity: '92%', beds: 2, status: 'Critical' },
    { name: 'County General', capacity: '75%', beds: 6, status: 'Available' },
  ];
  
  export const dummyEMTs = [
    { id: 'EMT-A2', status: 'Ready' },
    { id: 'EMT-B1', status: 'Ready' },
    { id: 'EMT-C1', status: 'Ready' },
    { id: 'EMT-D2', status: 'Ready' },
  ];
  