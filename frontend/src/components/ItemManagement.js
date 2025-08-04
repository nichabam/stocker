import React, { useState, useEffect } from 'react';
import { FaBox, FaPlus, FaEdit, FaTrash, FaExclamationTriangle } from 'react-icons/fa';
import apiClient from '../utils/apiClient';

const ItemManagement = () => {
  const [items, setItems] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('view');
  const [formData, setFormData] = useState({
    name: '',
    unit: '',
    restockThreshold: 5.0,
    categoryId: ''
  });
  const [selectedItem, setSelectedItem] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');
  const [filters, setFilters] = useState({
    showLowStock: false,
    categoryFilter: 'All Categories'
  });

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

  const handleCreateItem = async (e) => {
    e.preventDefault();
    if (!formData.name.trim() || !formData.unit.trim()) {
      setError('Item name and unit are required!');
      return;
    }

    try {
      await apiClient.createItem(
        formData.name.trim(),
        formData.unit.trim(),
        roundNumber(formData.restockThreshold),
        parseInt(formData.categoryId)
      );
      setSuccessMessage(`✅ Item '${formData.name}' created successfully!`);
      setFormData({
        name: '',
        unit: '',
        restockThreshold: 5.0,
        categoryId: ''
      });
      fetchData();
    } catch (err) {
      setError('❌ Failed to create item. Please try again.');
    }
  };

  const handleUpdateItem = async (e) => {
    e.preventDefault();
    if (!selectedItem) return;

    try {
      await apiClient.updateItem(selectedItem.id, {
        name: formData.name.trim(),
        unit: formData.unit.trim(),
        restock_threshold: roundNumber(formData.restockThreshold),
        category_id: parseInt(formData.categoryId)
      });
      setSuccessMessage('✅ Item updated successfully!');
      setSelectedItem(null);
      setFormData({
        name: '',
        unit: '',
        restockThreshold: 5.0,
        categoryId: ''
      });
      fetchData();
    } catch (err) {
      setError('❌ Failed to update item. Please try again.');
    }
  };

  const handleDeleteItem = async (itemId) => {
    if (!window.confirm('Are you sure you want to delete this item?')) return;

    try {
      await apiClient.deleteItem(itemId);
      setSuccessMessage('✅ Item deleted successfully!');
      fetchData();
    } catch (err) {
      setError('❌ Failed to delete item. Please try again.');
    }
  };

  const handleEditItem = (item) => {
    setSelectedItem(item);
    setFormData({
      name: item.name,
      unit: item.unit,
      restockThreshold: roundNumber(item.restock_threshold),
      categoryId: item.category_id.toString()
    });
    setActiveTab('edit');
  };

  const getFilteredItems = () => {
    let filtered = items;

    if (filters.showLowStock) {
      filtered = filtered.filter(item => 
        roundNumber(item.quantity) <= roundNumber(item.restock_threshold)
      );
    }

    if (filters.categoryFilter !== 'All Categories') {
      filtered = filtered.filter(item => 
        item.category_name === filters.categoryFilter
      );
    }

    return filtered;
  };

  const clearMessages = () => {
    setError('');
    setSuccessMessage('');
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <div>Loading items...</div>
      </div>
    );
  }

  const filteredItems = getFilteredItems();

  return (
    <div>
      <div style={{ marginBottom: '30px' }}>
        <h1 style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
          <FaBox style={{ marginRight: '10px', color: '#007bff' }} />
          📦 Item Management
        </h1>
      </div>

      {/* Tabs */}
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'view' ? 'active' : ''}`}
          onClick={() => { setActiveTab('view'); clearMessages(); }}
        >
          📋 View Items
        </button>
        <button
          className={`tab ${activeTab === 'create' ? 'active' : ''}`}
          onClick={() => { setActiveTab('create'); clearMessages(); }}
        >
          ➕ Create Item
        </button>
        <button
          className={`tab ${activeTab === 'edit' ? 'active' : ''}`}
          onClick={() => { setActiveTab('edit'); clearMessages(); }}
        >
          ✏️ Edit Items
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

      {/* View Items Tab */}
      <div className={`tab-content ${activeTab === 'view' ? 'active' : ''}`}>
        <div className="card">
          <h3>All Items</h3>
          
          {/* Filters */}
          <div className="grid grid-2" style={{ marginBottom: '20px' }}>
            <div>
              <label>
                <input
                  type="checkbox"
                  checked={filters.showLowStock}
                  onChange={(e) => setFilters({ ...filters, showLowStock: e.target.checked })}
                  style={{ marginRight: '8px' }}
                />
                Show only low stock items
              </label>
            </div>
            <div>
              <label>Filter by category:</label>
              <select
                className="form-control"
                value={filters.categoryFilter}
                onChange={(e) => setFilters({ ...filters, categoryFilter: e.target.value })}
              >
                <option value="All Categories">All Categories</option>
                {categories.map((category) => (
                  <option key={category.id} value={category.name}>
                    {category.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {filteredItems.length > 0 ? (
            filteredItems.map((item) => {
              const quantity = roundNumber(item.quantity);
              const unit = item.unit;
              const threshold = roundNumber(item.restock_threshold);
              const isLowStock = quantity <= threshold;

              return (
                <div key={item.id} className="expander">
                  <div className="expander-header">
                    <span>📦 {item.name} - {quantity} {unit}</span>
                    <button
                      className="btn btn-danger"
                      onClick={() => handleDeleteItem(item.id)}
                      style={{ padding: '5px 10px', fontSize: '12px' }}
                    >
                      <FaTrash style={{ marginRight: '5px' }} />
                      Delete
                    </button>
                  </div>
                  <div className="expander-content">
                    <div className="grid grid-3">
                      <div>
                        <strong>Name:</strong> {item.name}
                      </div>
                      <div>
                        <strong>Category:</strong> {item.category_name}
                      </div>
                      <div>
                        <strong>Unit:</strong> {unit}
                      </div>
                      <div>
                        <strong>Current Stock:</strong> {quantity} {unit}
                      </div>
                      <div>
                        <strong>Restock Threshold:</strong> {threshold} {unit}
                      </div>
                      <div>
                        {isLowStock ? (
                          <span style={{ color: '#dc3545' }}>
                            <FaExclamationTriangle style={{ marginRight: '5px' }} />
                            ⚠️ Low Stock
                          </span>
                        ) : (
                          <span style={{ color: '#28a745' }}>
                            ✅ Good Stock
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              );
            })
          ) : (
            <div className="alert alert-info">
              No items found. Create your first item in the 'Create Item' tab!
            </div>
          )}
        </div>
      </div>

      {/* Create Item Tab */}
      <div className={`tab-content ${activeTab === 'create' ? 'active' : ''}`}>
        <div className="card">
          <h3>Create New Item</h3>
          {categories.length > 0 ? (
            <form onSubmit={handleCreateItem}>
              <div className="grid grid-2">
                <div>
                  <div className="form-group">
                    <label>Item Name</label>
                    <input
                      type="text"
                      className="form-control"
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      placeholder="e.g., Coffee Beans, Milk, Sugar"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Unit</label>
                    <input
                      type="text"
                      className="form-control"
                      value={formData.unit}
                      onChange={(e) => setFormData({ ...formData, unit: e.target.value })}
                      placeholder="e.g., kg, L, pieces"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Restock Threshold</label>
                    <input
                      type="number"
                      className="form-control"
                      value={formData.restockThreshold}
                      onChange={(e) => setFormData({ ...formData, restockThreshold: parseFloat(e.target.value) })}
                      min="0"
                      step="0.1"
                      required
                    />
                  </div>
                </div>
                <div>
                  <div className="form-group">
                    <label>Category</label>
                    <select
                      className="form-control"
                      value={formData.categoryId}
                      onChange={(e) => setFormData({ ...formData, categoryId: e.target.value })}
                      required
                    >
                      <option value="">Select a category...</option>
                      {categories.map((category) => (
                        <option key={category.id} value={category.id}>
                          {category.name}
                        </option>
                      ))}
                    </select>
                  </div>
                  
                  {/* Preview */}
                  <div style={{ padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
                    <h4>Preview:</h4>
                    <p><strong>Name:</strong> {formData.name}</p>
                    <p><strong>Unit:</strong> {formData.unit}</p>
                    <p><strong>Threshold:</strong> {roundNumber(formData.restockThreshold)}</p>
                    <p><strong>Category:</strong> {
                      categories.find(c => c.id === parseInt(formData.categoryId))?.name || 'Not selected'
                    }</p>
                  </div>
                </div>
              </div>
              <button type="submit" className="btn btn-primary">
                Create Item
              </button>
            </form>
          ) : (
            <div className="alert alert-warning">
              ⚠️ No categories found. Please create categories first!
            </div>
          )}
        </div>
      </div>

      {/* Edit Items Tab */}
      <div className={`tab-content ${activeTab === 'edit' ? 'active' : ''}`}>
        <div className="card">
          <h3>Edit Items</h3>
          {items.length > 0 ? (
            <div>
              <div className="form-group">
                <label>Select Item to Edit:</label>
                <select
                  className="form-control"
                  value={selectedItem?.id || ''}
                  onChange={(e) => {
                    const item = items.find(i => i.id === parseInt(e.target.value));
                    if (item) {
                      handleEditItem(item);
                    }
                  }}
                >
                  <option value="">Select an item...</option>
                  {items.map((item) => (
                    <option key={item.id} value={item.id}>
                      {item.name}
                    </option>
                  ))}
                </select>
              </div>

              {selectedItem && (
                <form onSubmit={handleUpdateItem}>
                  <div className="grid grid-2">
                    <div>
                      <div className="form-group">
                        <label>New Name</label>
                        <input
                          type="text"
                          className="form-control"
                          value={formData.name}
                          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                          required
                        />
                      </div>
                      <div className="form-group">
                        <label>New Unit</label>
                        <input
                          type="text"
                          className="form-control"
                          value={formData.unit}
                          onChange={(e) => setFormData({ ...formData, unit: e.target.value })}
                          required
                        />
                      </div>
                      <div className="form-group">
                        <label>New Threshold</label>
                        <input
                          type="number"
                          className="form-control"
                          value={formData.restockThreshold}
                          onChange={(e) => setFormData({ ...formData, restockThreshold: parseFloat(e.target.value) })}
                          min="0"
                          step="0.1"
                          required
                        />
                      </div>
                    </div>
                    <div>
                      <div className="form-group">
                        <label>New Category</label>
                        <select
                          className="form-control"
                          value={formData.categoryId}
                          onChange={(e) => setFormData({ ...formData, categoryId: e.target.value })}
                          required
                        >
                          {categories.map((category) => (
                            <option key={category.id} value={category.id}>
                              {category.name}
                            </option>
                          ))}
                        </select>
                      </div>
                    </div>
                  </div>
                  <div className="grid grid-2">
                    <button type="submit" className="btn btn-primary">
                      Update Item
                    </button>
                    <button
                      type="button"
                      className="btn btn-danger"
                      onClick={() => handleDeleteItem(selectedItem.id)}
                    >
                      Delete Item
                    </button>
                  </div>
                </form>
              )}
            </div>
          ) : (
            <div className="alert alert-info">
              No items to edit. Create some items first!
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ItemManagement; 