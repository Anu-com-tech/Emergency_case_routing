import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const ambulanceAPI = {
  findHospital: (patientType, emergencyType, needs) =>
    api.post('/ambulance/find-hospital', {
      patient_type: patientType,
      emergency_type: emergencyType,
      needs: needs,
    }),
  checkStatus: (requestId) =>
    api.post('/ambulance/check-status', {
      request_id: requestId,
    }),
  getStats: () =>
    api.get('/ambulance/stats'),
};

export const hospitalAPI = {
  getPendingRequests: () =>
    api.get('/hospital/pending-requests'),
  acceptRequest: (requestId) =>
    api.post('/hospital/accept-request', {
      request_id: requestId,
    }),
  rejectRequest: (requestId) =>
    api.post('/hospital/reject-request', {
      request_id: requestId,
    }),
};

export const hospitalsAPI = {
  getAll: () =>
    api.get('/hospitals/'),
};

export default api;
