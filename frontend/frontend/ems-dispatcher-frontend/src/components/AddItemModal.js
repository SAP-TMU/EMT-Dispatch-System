// src/components/AddItemModal.js
import React, { useState } from 'react';
import './AddItemModal.css';

const AddItemModal = ({ section, onClose, onConfirmAdd }) => {
  const [formData, setFormData] = useState({});
  const [confirming, setConfirming] = useState(false);

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = () => {
    setConfirming(true);
  };

  const confirm = () => {
    onConfirmAdd(formData);
    onClose();
  };

  const cancel = () => {
    setConfirming(false);
  };

  const renderFields = () => {
    switch (section) {
      case 'emergencies':
        return (
          <>
            <input name="title" placeholder="Title" onChange={handleChange} />
            <input name="location" placeholder="Location" onChange={handleChange} />
            <input name="unit" placeholder="Unit" onChange={handleChange} />
            <input name="eta" placeholder="ETA" onChange={handleChange} />
            <select name="priority" onChange={handleChange}>
              <option value="">Select Priority (1–5)</option>
              <option value="1">1 (Lowest)</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5 (Highest)</option>
            </select>

          </>
        );
      case 'hospitals':
        return (
          <>
            <input name="name" placeholder="Hospital Name" onChange={handleChange} />
            <input name="capacity" placeholder="Capacity (e.g. 85%)" onChange={handleChange} />
            <input name="beds" placeholder="Beds Available" onChange={handleChange} />
            <select name="status" onChange={handleChange}>
              <option value="">Select Status</option>
              <option value="Available">Available</option>
              <option value="Critical">Critical</option>
            </select>
          </>
        );
      case 'emts':
        return (
          <>
            <input name="id" placeholder="EMT ID (e.g. EMT-X1)" onChange={handleChange} />
            <select name="status" onChange={handleChange}>
              <option value="">Select Status</option>
              <option value="Ready">Ready</option>
              <option value="Busy">Busy</option>
            </select>
          </>
        );
      default:
        return null;
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-box">
        <button className="close-btn" onClick={onClose}>✖</button>
        {!confirming ? (
          <>
            <h3>Add New {section.slice(0, 1).toUpperCase() + section.slice(1)}</h3>
            <div className="form-fields">{renderFields()}</div>
            <button className="modal-btn" onClick={handleSubmit}>Add</button>
          </>
        ) : (
          <>
            <p>Are you sure you want to add this?</p>
            <div className="confirm-btns">
              <button className="modal-btn" onClick={confirm}>Yes</button>
              <button className="modal-btn cancel" onClick={cancel}>No</button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default AddItemModal;
