import React, { useState, useEffect } from 'react';
import { hospitalAPI } from '../api';

const HospitalPanel = ({ onRefresh }) => {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [actionLoading, setActionLoading] = useState({});

  useEffect(() => {
    fetchPendingRequests();
    // Auto-refresh every 10 seconds
    const interval = setInterval(fetchPendingRequests, 10000);
    return () => clearInterval(interval);
  }, []);

  const fetchPendingRequests = async () => {
    setLoading(true);
    try {
      const result = await hospitalAPI.getPendingRequests();
      setRequests(result.data.requests);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch requests');
    } finally {
      setLoading(false);
    }
  };

  const handleAccept = async (requestId) => {
    setActionLoading(prev => ({ ...prev, [requestId]: 'accepting' }));
    try {
      await hospitalAPI.acceptRequest(requestId);
      fetchPendingRequests();
      onRefresh();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to accept request');
    } finally {
      setActionLoading(prev => ({ ...prev, [requestId]: null }));
    }
  };

  const handleReject = async (requestId) => {
    setActionLoading(prev => ({ ...prev, [requestId]: 'rejecting' }));
    try {
      await hospitalAPI.rejectRequest(requestId);
      fetchPendingRequests();
      onRefresh();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to reject request');
    } finally {
      setActionLoading(prev => ({ ...prev, [requestId]: null }));
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-xl overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-500 to-pink-600 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-3xl">🏥</span>
            <div>
              <h2 className="text-2xl font-bold text-white">Hospital Admin Panel</h2>
              <p className="text-purple-100 text-sm">Manage emergency requests</p>
            </div>
          </div>
          <button
            onClick={fetchPendingRequests}
            className="px-3 py-2 bg-white bg-opacity-20 text-white rounded-lg hover:bg-opacity-30 transition-all duration-200 text-sm font-semibold"
          >
            🔄 Refresh
          </button>
        </div>
      </div>

      <div className="p-6">
        {/* Error Message */}
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            ⚠️ {error}
          </div>
        )}

        {/* Loading State */}
        {loading && requests.length === 0 && (
          <div className="text-center py-8">
            <div className="inline-block animate-spin text-3xl">⌛</div>
            <p className="text-gray-600 mt-2">Loading pending requests...</p>
          </div>
        )}

        {/* Empty State */}
        {!loading && requests.length === 0 && (
          <div className="text-center py-12 bg-gradient-to-b from-green-50 to-transparent rounded-lg">
            <div className="text-5xl mb-3">✓</div>
            <h3 className="text-lg font-semibold text-gray-700 mb-1">No Pending Requests</h3>
            <p className="text-gray-600">All emergency requests have been processed</p>
          </div>
        )}

        {/* Requests List */}
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {requests.map((request, index) => (
            <div
              key={request.id}
              className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-all duration-200 animate-fadeIn"
              style={{ animationDelay: `${index * 50}ms` }}
            >
              {/* Request Header */}
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xl">
                      {request.patient_type === 'Serious' ? '🔴' : '🟢'}
                    </span>
                    <h3 className="font-bold text-gray-800">
                      Request #{request.id}
                    </h3>
                    <span className="text-xs px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full font-semibold">
                      {request.status}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mt-1">
                    Time: {new Date(request.created_at).toLocaleTimeString()}
                  </p>
                </div>
              </div>

              {/* Request Details Grid */}
              <div className="grid grid-cols-2 gap-3 mb-4 text-sm bg-gray-50 p-3 rounded-lg">
                <div>
                  <p className="text-gray-600">Patient Type</p>
                  <p className="font-semibold text-gray-800">{request.patient_type}</p>
                </div>
                <div>
                  <p className="text-gray-600">Emergency Type</p>
                  <p className="font-semibold text-gray-800">{request.emergency_type}</p>
                </div>
              </div>

              {/* Medical Needs */}
              <div className="mb-4">
                <p className="text-sm text-gray-600 mb-2 font-semibold">Medical Requirements:</p>
                <div className="flex flex-wrap gap-2">
                  <span className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded-full">
                    🛏️ Bed
                  </span>
                  {request.need_icu && (
                    <span className="text-xs px-2 py-1 bg-purple-100 text-purple-800 rounded-full">
                      🏥 ICU
                    </span>
                  )}
                  {request.need_oxygen && (
                    <span className="text-xs px-2 py-1 bg-cyan-100 text-cyan-800 rounded-full">
                      💨 Oxygen
                    </span>
                  )}
                  {request.need_ventilator && (
                    <span className="text-xs px-2 py-1 bg-indigo-100 text-indigo-800 rounded-full">
                      🫁 Ventilator
                    </span>
                  )}
                </div>
              </div>

              {/* Hospital Info */}
              <div className="mb-4 p-2 bg-blue-50 rounded-lg text-sm">
                <p className="text-gray-600">Assigned Hospital</p>
                <p className="font-semibold text-blue-600">{request.hospital_name}</p>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-2">
                <button
                  onClick={() => handleAccept(request.id)}
                  disabled={actionLoading[request.id] === 'accepting'}
                  className="flex-1 px-3 py-2 bg-gradient-to-r from-green-500 to-green-600 text-white font-semibold rounded-lg hover:shadow-lg hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
                >
                  {actionLoading[request.id] === 'accepting' ? '⏳ Accepting...' : '✓ Accept'}
                </button>
                <button
                  onClick={() => handleReject(request.id)}
                  disabled={actionLoading[request.id] === 'rejecting'}
                  className="flex-1 px-3 py-2 bg-gradient-to-r from-red-500 to-red-600 text-white font-semibold rounded-lg hover:shadow-lg hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
                >
                  {actionLoading[request.id] === 'rejecting' ? '⏳ Rejecting...' : '✗ Reject'}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default HospitalPanel;
