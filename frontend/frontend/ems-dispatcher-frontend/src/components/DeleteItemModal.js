// src/components/DeleteItemModal.js
import React from 'react';
import './DeleteItemModal.css';

const DeleteItemModal = ({ section, item, onClose, onConfirmDelete }) => {
  return (
    <div className="modal-overlay">
      <div className="modal-box">
        <button className="close-btn" onClick={onClose}>✖</button>
        <h3>Delete this {section.slice(0, 1).toUpperCase() + section.slice(1)}?</h3>
        <p>{item.name || item.id}</p>  {/* Display only the name or ID */}
        <div className="confirm-btns">
          <button className="modal-btn" onClick={onConfirmDelete}>Yes</button>
          <button className="modal-btn cancel" onClick={onClose}>No</button>
        </div>
      </div>
    </div>
  );
};

export default DeleteItemModal;
