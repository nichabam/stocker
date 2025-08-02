import React, { useState, useEffect } from 'react';
import { FaBoxes, FaExclamationTriangle, FaCheckCircle } from 'react-icons/fa';
import apiClient from '../utils/apiClient';

const StockManagement = () => {
  const [items, setItems] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('overview');
  const [selectedItem, setSelectedItem] = useState(null);
  const [formData, setFormData] = useState({
    quantity: 0,
    notes: '',
    staffName: ''
  });
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [itemsData, categoriesData] = await Promise.all([
        apiClient.getItems(),
        apiClient.getCategories()
      ]);
      setItems(itemsData || []);
      setCategories(categoriesData || []);
    } catch (err) {
      setError('Failed to load data');
      console.error('Data error:', err);
    } finally {
      setLoading(false);
    }
  };

  const roundNumber = (value) => {
    if (value === null || value === undefined) return 0.0;
    return Math.round(parseFloat(value) * 10) / 10;
  };

  const handleLogStock = async (e) => {
    e.preventDefault();
    if (!selectedItem) return;

    try {
      await apiClient.logStock(
        selectedItem.id,
        roundNumber(formData.quantity),
        formData.notes || null,
        formData.staffName || null
      );
      setSuccessMessage('Stock count logged successfully!');
      setFormData({ quantity: 0, notes: '', staffName: '' });
      fetchData(); // Refresh data to get updated quantities
    } catch (err) {
      setError('Failed to log stock count. Please try again.');
    }
  };

  const handleItemSelect = (item) => {
    setSelectedItem(item);
    setFormData({
      quantity: roundNumber(item.quantity),
      notes: '',
      staffName: ''
    });
  };

  const clearMessages = () => {
    setError('');
    setSuccessMessage('');
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <div>Loading stock data...</div>
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div>
        <div style={{ marginBottom: '30px' }}>
          <h1 style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
            <FaBoxes style={{ marginRight: '10px', color: '#007bff' }} />
            📦 Stock Management
          </h1>
        </div>
        <div className="alert alert-info">
          No items found. Create some items first!
        </div>
      </div>
    );
  }

  return (
    <div>
      <div style={{ marginBottom: '30px' }}>
        <h1 style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
          <FaBoxes style={{ marginRight: '10px', color: '#007bff' }} />
          📦 Stock Management
        </h1>
      </div>

      {/* Tabs */}
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => { setActiveTab('overview'); clearMessages(); }}
        >
          📊 Stock Overview
        </button>
        <button
          className={`tab ${activeTab === 'log' ? 'active' : ''}`}
          onClick={() => { setActiveTab('log'); clearMessages(); }}
        >
          📝 Log Stock Counts
        </button>
      </div>

      {/* Messages */}
      {error && (
        <div className="alert alert-danger">
          {error}
        </div>
      )}
      {successMessage && (
        <div className="alert alert-success">
          {successMessage}
        </div>
      )}

      {/* Stock Overview Tab */}
      <div className={`tab-content ${activeTab === 'overview' ? 'active' : ''}`}>
        <div className="card">
          <h3>Current Stock Levels</h3>
          {categories.map((category) => {
            const categoryItems = items.filter(item => item.category_id === category.id);
            
            if (categoryItems.length === 0) return null;

            return (
              <div key={category.id} style={{ marginBottom: '30px' }}>
                <h4 style={{ 
                  borderBottom: '2px solid #007bff', 
                  paddingBottom: '5px',
                  marginBottom: '15px'
                }}>
                  {category.name}
                </h4>
                {categoryItems.map((item) => {
                  const quantity = roundNumber(item.quantity);
                  const unit = item.unit;
                  const threshold = roundNumber(item.restock_threshold);
                  const isLowStock = quantity <= threshold;

                  return (
                    <div key={item.id} className="expander">
                      <div className="expander-header">
                        <span>{item.name} - {quantity} {unit}</span>
                        {isLowStock ? (
                          <span style={{ color: '#dc3545' }}>
                            <FaExclamationTriangle style={{ marginRight: '5px' }} />
                            ⚠️ Low Stock
                          </span>
                        ) : (
                          <span style={{ color: '#28a745' }}>
                            <FaCheckCircle style={{ marginRight: '5px' }} />
                            ✅ Good Stock
                          </span>
                        )}
                      </div>
                      <div className="expander-content">
                        <div className="grid grid-3">
                          <div>
                            <strong>Category:</strong> {item.category_name}
                          </div>
                          <div>
                            <strong>Current Stock:</strong> {quantity} {unit}
                          </div>
                          <div>
                            <strong>Restock Threshold:</strong> {threshold} {unit}
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            );
          })}
        </div>
      </div>

      {/* Log Stock Counts Tab */}
      <div className={`tab-content ${activeTab === 'log' ? 'active' : ''}`}>
        <div className="card">
          <h3>Log Stock Counts</h3>
          
          <div className="form-group">
            <label>Select Item:</label>
            <select
              className="form-control"
              value={selectedItem?.id || ''}
              onChange={(e) => {
                const item = items.find(i => i.id === parseInt(e.target.value));
                if (item) {
                  handleItemSelect(item);
                }
              }}
            >
              <option value="">Select an item...</option>
              {items.map((item) => (
                <option key={item.id} value={item.id}>
                  {item.name} ({item.category_name})
                </option>
              ))}
            </select>
          </div>

          {selectedItem && (
            <div>
              <div style={{ 
                padding: '15px', 
                backgroundColor: '#f8f9fa', 
                borderRadius: '4px',
                marginBottom: '20px'
              }}>
                <h4>Current Stock Information</h4>
                <p><strong>Item:</strong> {selectedItem.name}</p>
                <p><strong>Category:</strong> {selectedItem.category_name}</p>
                <p><strong>Current Stock:</strong> {roundNumber(selectedItem.quantity)} {selectedItem.unit}</p>
                <p><strong>Restock Threshold:</strong> {roundNumber(selectedItem.restock_threshold)} {selectedItem.unit}</p>
              </div>

              <form onSubmit={handleLogStock}>
                <div className="form-group">
                  <label>New Quantity</label>
                  <input
                    type="number"
                    className="form-control"
                    value={formData.quantity}
                    onChange={(e) => setFormData({ ...formData, quantity: parseFloat(e.target.value) })}
                    min="0"
                    step="0.1"
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Notes (optional)</label>
                  <input
                    type="text"
                    className="form-control"
                    value={formData.notes}
                    onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                    placeholder="Add any notes about this stock count"
                  />
                </div>

                <div className="form-group">
                  <label>Staff Name (optional)</label>
                  <input
                    type="text"
                    className="form-control"
                    value={formData.staffName}
                    onChange={(e) => setFormData({ ...formData, staffName: e.target.value })}
                    placeholder="Enter staff name"
                  />
                </div>

                <button type="submit" className="btn btn-primary">
                  Log Stock Count
                </button>
              </form>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default StockManagement; 