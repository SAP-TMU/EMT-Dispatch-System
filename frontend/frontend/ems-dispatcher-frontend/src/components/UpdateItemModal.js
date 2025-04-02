// src/components/UpdateItemModal.js
import React, { useState, useEffect } from 'react';
import './UpdateItemModal.css';

const UpdateItemModal = ({ section, item, onClose, onConfirmUpdate }) => {
  const [formData, setFormData] = useState({});

  useEffect(() => {
    setFormData(item);  // Pre-fill form with current item data
  }, [item]);

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = () => {
    onConfirmUpdate(formData);
  };

  return (
    <div className="modal-overlay">
      <div className="modal-box">
        <button className="close-btn" onClick={onClose}>✖</button>
        <h3>Update {section.slice(0, 1).toUpperCase() + section.slice(1)}</h3>
        <div className="form-fields">
          {section === 'emergencies' && (
            <>
              <input name="title" value={formData.title} onChange={handleChange} placeholder="Title" />
              <input name="location" value={formData.location} onChange={handleChange} placeholder="Location" />
              <input name="unit" value={formData.unit} onChange={handleChange} placeholder="Unit" />
              <input name="eta" value={formData.eta} onChange={handleChange} placeholder="ETA" />
              <select name="priority" value={formData.priority} onChange={(e) =>setFormData((prev) => ({ ...prev, priority: Number(e.target.value) }))}>
                <option value="">Select Priority (1–5)</option>
                <option value="1">1 (Lowest)</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5 (Highest)</option>
              </select>
            </>
          )}
          {section === 'hospitals' && (
            <>
              <input name="name" value={formData.name} onChange={handleChange} placeholder="Hospital Name" />
              <input name="capacity" value={formData.capacity} onChange={handleChange} placeholder="Capacity" />
              <input name="beds" value={formData.beds} onChange={handleChange} placeholder="Beds Available" />
              <select name="status" value={formData.status} onChange={handleChange}>
                <option value="Available">Available</option>
                <option value="Critical">Critical</option>
              </select>
            </>
          )}
          {section === 'emts' && (
            <>
              <input name="id" value={formData.id} onChange={handleChange} placeholder="EMT ID" />
              <select name="status" value={formData.status} onChange={handleChange}>
                <option value="Ready">Ready</option>
                <option value="Busy">Busy</option>
              </select>
            </>
          )}
        </div>
        <div className="modal-buttons">
          <button className="confirm-button" onClick={handleSubmit}>Confirm Update</button>
          <button className="cancel-button" onClick={onClose}>Cancel</button>
        </div>
      </div>
    </div>
  );
};

export default UpdateItemModal;
