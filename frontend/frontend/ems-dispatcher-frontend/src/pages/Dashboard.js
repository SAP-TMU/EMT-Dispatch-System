import React, { useState } from 'react';
import AddItemModal from '../components/AddItemModal';
import DeleteItemModal from '../components/DeleteItemModal';
import UpdateItemModal from '../components/UpdateItemModal';
import { FaPlus, FaTrashAlt, FaEdit } from 'react-icons/fa';
import './DashboardPage.css';
import { dummyEmergencies, dummyHospitals, dummyEMTs } from '../data/dummyData';

const DashboardPage = () => {
  const [emergencies, setEmergencies] = useState(dummyEmergencies);
  const [hospitals, setHospitals] = useState(dummyHospitals);
  const [emts, setEmts] = useState(dummyEMTs);

  const [modalSection, setModalSection] = useState(null);
  const [deleteSection, setDeleteSection] = useState(null);
  const [updateSection, setUpdateSection] = useState(null);
  const [itemToDelete, setItemToDelete] = useState(null);
  const [itemToUpdate, setItemToUpdate] = useState(null);

  const handleAdd = (data) => {
    if (modalSection === 'emergencies') {
      setEmergencies((prev) => [...prev, data]);
    } else if (modalSection === 'hospitals') {
      setHospitals((prev) => [...prev, data]);
    } else if (modalSection === 'emts') {
      setEmts((prev) => [...prev, data]);
    }
  };

  const handleDelete = () => {
    if (deleteSection === 'emergencies') {
      setEmergencies(emergencies.filter((e) => e !== itemToDelete));
    } else if (deleteSection === 'hospitals') {
      setHospitals(hospitals.filter((h) => h !== itemToDelete));
    } else if (deleteSection === 'emts') {
      setEmts(emts.filter((emt) => emt !== itemToDelete));
    }
    setDeleteSection(null);
    setItemToDelete(null);
  };

  const handleUpdate = (updatedData) => {
    if (updateSection === 'emergencies') {
      setEmergencies((prev) => prev.map(e => e === itemToUpdate ? updatedData : e));
    } else if (updateSection === 'hospitals') {
      setHospitals((prev) => prev.map(h => h === itemToUpdate ? updatedData : h));
    } else if (updateSection === 'emts') {
      setEmts((prev) => prev.map(emt => emt === itemToUpdate ? updatedData : emt));
    }
    setUpdateSection(null);
    setItemToUpdate(null);
  };

  const handleOpenDeleteModal = (item, section) => {
    setDeleteSection(section);
    setItemToDelete(item);
  };

  const handleOpenUpdateModal = (item, section) => {
    setUpdateSection(section);
    setItemToUpdate(item);
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-sections">
        {/* Active Emergencies */}
        <div className="section-box">
          <div className="section-header">
            <h3>🚨 Active Emergencies</h3>
            <FaPlus className="add-icon" onClick={() => setModalSection('emergencies')} />
          </div>
          <div className="cards">
            {emergencies.map((e, i) => (
              <div key={i} className="card">
                <FaEdit className="update-icon" onClick={() => handleOpenUpdateModal(e, 'emergencies')} />
                <FaTrashAlt className="delete-icon" onClick={() => handleOpenDeleteModal(e, 'emergencies')} />
                <strong>{e.title}</strong>
                <p>📍 {e.location}</p>
                <p>🚑 Unit: {e.unit}</p>
                <p>⏱️ ETA: {e.eta}</p>
                <p><strong>Priority:</strong> {e.priority}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Hospital Status */}
        <div className="section-box">
          <div className="section-header">
            <h3>🏥 Hospital Status</h3>
            <FaPlus className="add-icon" onClick={() => setModalSection('hospitals')} />
          </div>
          <div className="cards">
            {hospitals.map((h, i) => (
              <div key={i} className="card">
                <FaEdit className="update-icon" onClick={() => handleOpenUpdateModal(h, 'hospitals')} />
                <FaTrashAlt className="delete-icon" onClick={() => handleOpenDeleteModal(h, 'hospitals')} />
                <strong>{h.name}</strong>
                <p>Capacity: {h.capacity}</p>
                <p>Beds Available: {h.beds}</p>
                <span className={`badge ${h.status.toLowerCase()}`}>{h.status}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Available EMT Units */}
        <div className="section-box full-width">
          <div className="section-header">
            <h3>🚑 Available EMT Units</h3>
            <FaPlus className="add-icon" onClick={() => setModalSection('emts')} />
          </div>
          <div className="emt-grid">
            {emts.map((emt, i) => (
              <div key={i} className="card emt-card">
                <FaEdit className="update-icon" onClick={() => handleOpenUpdateModal(emt, 'emts')} />
                <FaTrashAlt className="delete-icon" onClick={() => handleOpenDeleteModal(emt, 'emts')} />
                <strong>{emt.id}</strong>
                <p>Status: {emt.status}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Modals */}
      {modalSection && (
        <AddItemModal
          section={modalSection}
          onClose={() => setModalSection(null)}
          onConfirmAdd={handleAdd}
        />
      )}
      {deleteSection && (
        <DeleteItemModal
          section={deleteSection}
          item={itemToDelete}
          onClose={() => { setDeleteSection(null); setItemToDelete(null); }}
          onConfirmDelete={handleDelete}
        />
      )}
      {updateSection && (
        <UpdateItemModal
          section={updateSection}
          item={itemToUpdate}
          onClose={() => { setUpdateSection(null); setItemToUpdate(null); }}
          onConfirmUpdate={handleUpdate}
        />
      )}
    </div>
  );
};

export default DashboardPage;
