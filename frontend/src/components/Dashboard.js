import React, { useState, useEffect } from 'react';
import { FaCoffee, FaExclamationTriangle, FaTags, FaBoxes } from 'react-icons/fa';
import apiClient from '../utils/apiClient';

const Dashboard = () => {
  const [data, setData] = useState({
    items: [],
    categories: [],
    stockRecords: [],
    restockRecords: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [items, categories, stockRecords, restockRecords] = await Promise.all([
        apiClient.getItems(),
        apiClient.getCategories(),
        apiClient.getStockRecords(),
        apiClient.getRestockRecords()
      ]);

      setData({
        items: items || [],
        categories: categories || [],
        stockRecords: stockRecords || [],
        restockRecords: restockRecords || []
      });
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error('Dashboard data error:', err);
    } finally {
      setLoading(false);
    }
  };

  const roundNumber = (value) => {
    if (value === null || value === undefined) return 0.0;
    return Math.round(parseFloat(value) * 10) / 10;
  };

  const getLowStockItemsCount = () => {
    return data.items.filter(item => 
      roundNumber(item.quantity) <= roundNumber(item.restock_threshold)
    ).length;
  };

  const getTodayRestocksCount = () => {
    const today = new Date().toISOString().split('T')[0];
    return data.restockRecords.filter(record => 
      record.date && record.date.startsWith(today)
    ).length;
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <div>Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger">
        {error}
      </div>
    );
  }

  return (
    <div>
      <div style={{ marginBottom: '30px' }}>
        <h1 style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
          <FaCoffee style={{ marginRight: '10px', color: '#007bff' }} />
          ☕ Stocker - Cafe Inventory Management
        </h1>
        <hr />
      </div>

      {/* Quick Stats */}
      <div className="grid grid-4" style={{ marginBottom: '30px' }}>
        <div className="card stats-card">
          <FaCoffee size={24} style={{ color: '#007bff', marginBottom: '10px' }} />
          <h3>{data.items.length}</h3>
          <p>Total Items</p>
        </div>

        <div className="card stats-card">
          <FaExclamationTriangle size={24} style={{ color: '#dc3545', marginBottom: '10px' }} />
          <h3>{getLowStockItemsCount()}</h3>
          <p>Low Stock Items</p>
        </div>

        <div className="card stats-card">
          <FaTags size={24} style={{ color: '#28a745', marginBottom: '10px' }} />
          <h3>{data.categories.length}</h3>
          <p>Categories</p>
        </div>

        <div className="card stats-card">
          <FaBoxes size={24} style={{ color: '#ffc107', marginBottom: '10px' }} />
          <h3>{getTodayRestocksCount()}</h3>
          <p>Today's Restocks</p>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="card">
        <h3>Recent Activity</h3>
        {data.stockRecords.length > 0 ? (
          <div>
            <p style={{ marginBottom: '15px', color: '#666' }}>Recent stock counts:</p>
            {data.stockRecords.slice(0, 5).map((record, index) => {
              const quantity = roundNumber(record.quantity);
              const staffName = record.staff_name || 'Unknown';
              const itemName = record.item_name || 'Unknown';
              const date = record.date || 'Unknown';

              return (
                <div key={index} style={{ 
                  padding: '10px', 
                  borderBottom: index < 4 ? '1px solid #eee' : 'none',
                  display: 'flex',
                  alignItems: 'center'
                }}>
                  <span style={{ marginRight: '10px' }}>•</span>
                  <span>
                    {staffName && staffName !== 'Unknown' 
                      ? `${itemName}: ${quantity} (by ${staffName}) on ${date}`
                      : `${itemName}: ${quantity} on ${date}`
                    }
                  </span>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="alert alert-info">
            No stock records found. Start by logging some stock counts!
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard; 