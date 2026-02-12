import React, { useState } from 'react';
import { ambulanceAPI } from '../api';

const AmbulancePanel = ({ onRefresh }) => {
  const [formData, setFormData] = useState({
    patient_type: '',
    emergency_type: '',
    needs: {
      bed: true,
      icu: false,
      oxygen: false,
      ventilator: false,
    },
  });

  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [requestId, setRequestId] = useState('');
  const [statusResult, setStatusResult] = useState(null);
  const [checkingStatus, setCheckingStatus] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
    setError(null);
  };

  const handleCheckboxChange = (field) => {
    if (field === 'bed') return; // Bed is mandatory
    setFormData(prev => ({
      ...prev,
      needs: {
        ...prev.needs,
        [field]: !prev.needs[field],
      },
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.patient_type || !formData.emergency_type) {
      setError('Please select both Patient Type and Emergency Type');
      return;
    }

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const result = await ambulanceAPI.findHospital(
        formData.patient_type,
        formData.emergency_type,
        formData.needs
      );
      setResponse(result.data);
      setRequestId(result.data.request_id);
      onRefresh();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to find hospital');
    } finally {
      setLoading(false);
    }
  };

  const handleCheckStatus = async (e) => {
    e.preventDefault();
    
    if (!requestId) {
      setError('Please enter a Request ID');
      return;
    }

    setCheckingStatus(true);
    setError(null);

    try {
      const result = await ambulanceAPI.checkStatus(parseInt(requestId));
      setStatusResult(result.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to check status');
    } finally {
      setCheckingStatus(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-xl overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-500 to-blue-600 px-6 py-4">
        <div className="flex items-center gap-3">
          <span className="text-3xl">🚑</span>
          <div>
            <h2 className="text-2xl font-bold text-white">Ambulance Staff Panel</h2>
            <p className="text-blue-100 text-sm">Find nearest hospital for emergency</p>
          </div>
        </div>
      </div>

      <div className="p-6">
        {/* Find Hospital Form */}
        <form onSubmit={handleSubmit} className="space-y-4 mb-8">
          {/* Patient Type */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Patient Type <span className="text-red-500">*</span>
            </label>
            <select
              name="patient_type"
              value={formData.patient_type}
              onChange={handleInputChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">-- Select Patient Type --</option>
              <option value="Normal">🟢 Normal</option>
              <option value="Serious">🔴 Serious</option>
            </select>
          </div>

          {/* Emergency Type */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Emergency Type <span className="text-red-500">*</span>
            </label>
            <select
              name="emergency_type"
              value={formData.emergency_type}
              onChange={handleInputChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">-- Select Emergency Type --</option>
              <option value="Accident">🚗 Accident</option>
              <option value="Attack">💔 Attack</option>
              <option value="Respiratory">🫁 Respiratory</option>
            </select>
          </div>

          {/* Patient Needs */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              Patient Needs <span className="text-red-500">*</span>
            </label>
            <div className="space-y-2">
              {/* Bed - Always checked */}
              <label className="flex items-center gap-3 p-2 bg-gray-50 rounded-lg">
                <input
                  type="checkbox"
                  checked={true}
                  disabled
                  className="w-4 h-4 text-blue-600 rounded cursor-not-allowed"
                />
                <span className="text-gray-700">🛏️ Bed (Mandatory)</span>
              </label>

              {/* ICU */}
              <label className="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg cursor-pointer transition">
                <input
                  type="checkbox"
                  checked={formData.needs.icu}
                  onChange={() => handleCheckboxChange('icu')}
                  className="w-4 h-4 text-blue-600 rounded cursor-pointer"
                />
                <span className="text-gray-700">🏥 ICU</span>
              </label>

              {/* Oxygen */}
              <label className="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg cursor-pointer transition">
                <input
                  type="checkbox"
                  checked={formData.needs.oxygen}
                  onChange={() => handleCheckboxChange('oxygen')}
                  className="w-4 h-4 text-blue-600 rounded cursor-pointer"
                />
                <span className="text-gray-700">💨 Oxygen</span>
              </label>

              {/* Ventilator */}
              <label className="flex items-center gap-3 p-2 hover:bg-gray-50 rounded-lg cursor-pointer transition">
                <input
                  type="checkbox"
                  checked={formData.needs.ventilator}
                  onChange={() => handleCheckboxChange('ventilator')}
                  className="w-4 h-4 text-blue-600 rounded cursor-pointer"
                />
                <span className="text-gray-700">🫁 Ventilator</span>
              </label>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
              ⚠️ {error}
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full px-4 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white font-semibold rounded-lg hover:shadow-lg hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? '🔍 Searching...' : '🔍 Find Nearest Hospital'}
          </button>
        </form>

        {/* Response */}
        {response && (
          <div className="mb-8 p-4 bg-green-50 border border-green-200 rounded-lg animate-fadeIn">
            <div className="flex items-start gap-3">
              <span className="text-3xl">✓</span>
              <div className="flex-1">
                <h3 className="font-bold text-green-900 mb-2">Request Sent Successfully!</h3>
                <div className="space-y-2 bg-white p-3 rounded-lg">
                  <p className="text-gray-700">
                    <strong>🏥 Hospital:</strong> {response.hospital_name}
                  </p>
                  <p className="text-gray-700">
                    <strong>📍 Distance:</strong> {response.distance} km
                  </p>
                  <p className="text-gray-700">
                    <strong>🆔 Request ID:</strong> #{response.request_id}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Check Status Section */}
        <div className="border-t pt-6">
          <h3 className="font-semibold text-gray-700 mb-4">📊 Check Request Status</h3>
          <form onSubmit={handleCheckStatus} className="flex gap-2">
            <input
              type="number"
              value={requestId}
              onChange={(e) => setRequestId(e.target.value)}
              placeholder="Enter Request ID..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button
              type="submit"
              disabled={checkingStatus}
              className="px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-all disabled:opacity-50"
            >
              {checkingStatus ? 'Checking...' : 'Check'}
            </button>
          </form>

          {statusResult && (
            <div className="mt-4 p-4 rounded-lg animate-fadeIn" style={{
              backgroundColor: statusResult.status === 'Accepted' ? '#ECFDF5' : statusResult.status === 'Rejected' ? '#FEF2F2' : '#FFFBEB',
              borderColor: statusResult.status === 'Accepted' ? '#10B981' : statusResult.status === 'Rejected' ? '#EF4444' : '#F59E0B',
              borderWidth: '1px'
            }}>
              <div className="flex items-start gap-3">
                <span className="text-2xl">
                  {statusResult.status === 'Accepted' ? '✓' : statusResult.status === 'Rejected' ? '✗' : '⏳'}
                </span>
                <div className="flex-1">
                  <h4 className="font-bold mb-1">
                    {statusResult.status === 'Accepted' ? 'Request Accepted! 🎉' : statusResult.status === 'Rejected' ? 'Request Rejected' : 'Request Pending'}
                  </h4>
                  <p className="text-sm mb-2">
                    Hospital: <strong>{statusResult.hospital_name}</strong>
                  </p>
                  <p className="text-sm">
                    Status: <strong>{statusResult.status}</strong>
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AmbulancePanel;
