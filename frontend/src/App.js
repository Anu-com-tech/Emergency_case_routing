import React, { useState, useEffect } from 'react';
import AmbulancePanel from './components/AmbulancePanel';
import HospitalPanel from './components/HospitalPanel';
import StatsDashboard from './components/StatsDashboard';

function App() {
  const [refreshKey, setRefreshKey] = useState(0);
  const [userType, setUserType] = useState(null);

  const handleRefresh = () => {
    setRefreshKey(prev => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-gradient-to-r from-blue-600 to-purple-600 shadow-xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="text-3xl">🚑</div>
              <div>
                <h1 className="text-2xl font-bold text-white">Emergency Routing System</h1>
                <p className="text-blue-100 text-sm">Hospital Emergency Case Routing & Matching</p>
              </div>
            </div>
            <button
              onClick={handleRefresh}
              className="px-4 py-2 bg-white bg-opacity-20 text-white rounded-lg hover:bg-opacity-30 transition-all duration-200 font-semibold"
            >
              🔄 Refresh
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Dashboard */}
        <StatsDashboard key={refreshKey} />

        {/* Dual Panel Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          {/* Left Panel - Ambulance Staff */}
          <div className="animate-slideInLeft">
            <AmbulancePanel key={refreshKey} onRefresh={handleRefresh} />
          </div>

          {/* Right Panel - Hospital Admin */}
          <div className="animate-slideInRight">
            <HospitalPanel key={refreshKey} onRefresh={handleRefresh} />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-16 bg-gray-900 text-white py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-gray-400">
            Emergency Routing System © 2024 | Optimizing Emergency Response & Hospital Resource Utilization
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
