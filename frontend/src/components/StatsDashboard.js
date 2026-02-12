import React, { useState, useEffect } from 'react';
import { ambulanceAPI } from '../api';

const StatsDashboard = () => {
  const [stats, setStats] = useState({
    total_hospitals: 5,
    pending_count: 0,
    accepted_count: 0,
    response_time: '~2min',
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchStats();
    // Auto-refresh every 15 seconds
    const interval = setInterval(fetchStats, 15000);
    return () => clearInterval(interval);
  }, []);

  const fetchStats = async () => {
    try {
      const result = await ambulanceAPI.getStats();
      setStats(result.data);
    } catch (err) {
      console.error('Failed to fetch stats:', err);
    }
  };

  const statCards = [
    {
      icon: '🏥',
      label: 'Total Hospitals',
      value: stats.total_hospitals,
      color: 'from-blue-500 to-blue-600',
      delay: '0s',
    },
    {
      icon: '📋',
      label: 'Pending Requests',
      value: stats.pending_count,
      color: 'from-yellow-500 to-yellow-600',
      delay: '0.1s',
    },
    {
      icon: '✅',
      label: 'Accepted Today',
      value: stats.accepted_count,
      color: 'from-green-500 to-green-600',
      delay: '0.2s',
    },
    {
      icon: '⚡',
      label: 'Avg Response Time',
      value: stats.response_time,
      color: 'from-purple-500 to-purple-600',
      delay: '0.3s',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {statCards.map((card, index) => (
        <div
          key={index}
          style={{ animationDelay: card.delay }}
          className="animate-fadeIn"
        >
          <div className={`bg-gradient-to-br ${card.color} rounded-lg shadow-lg p-6 text-white hover:shadow-xl transition-all duration-300 transform hover:scale-105 cursor-pointer`}>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm opacity-90 mb-1">{card.label}</p>
                <p className="text-3xl font-bold">{card.value}</p>
              </div>
              <div className="text-4xl opacity-75">{card.icon}</div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default StatsDashboard;
