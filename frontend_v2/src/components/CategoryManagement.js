import React, { useState, useEffect } from 'react';
import { FaFolder, FaPlus, FaEdit, FaTrash } from 'react-icons/fa';
import apiClient from '../utils/apiClient';

const CategoryManagement = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('view');
  const [formData, setFormData] = useState({
    name: '',
    description: ''
  });
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getCategories();
      setCategories(data || []);
    } catch (err) {
      setError('Failed to load categories');
      console.error('Categories error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCategory = async (e) => {
    e.preventDefault();
    if (!formData.name.trim()) {
      setError('Category name is required!');
      return;
    }

    try {
      await apiClient.createCategory(formData.name.trim());
      setSuccessMessage(`✅ Category '${formData.name}' created successfully!`);
      setFormData({ name: '', description: '' });
      fetchCategories();
    } catch (err) {
      setError('❌ Failed to create category. Please try again.');
    }
  };

  const handleUpdateCategory = async (e) => {
    e.preventDefault();
    if (!selectedCategory) return;

    try {
      await apiClient.updateCategory(
        selectedCategory.id,
        formData.name.trim(),
        formData.description.trim() || null
      );
      setSuccessMessage('✅ Category updated successfully!');
      setSelectedCategory(null);
      setFormData({ name: '', description: '' });
      fetchCategories();
    } catch (err) {
      setError('❌ Failed to update category. Please try again.');
    }
  };

  const handleDeleteCategory = async (categoryId) => {
    if (!window.confirm('Are you sure you want to delete this category?')) return;

    try {
      await apiClient.deleteCategory(categoryId);
      setSuccessMessage('✅ Category deleted successfully!');
      fetchCategories();
    } catch (err) {
      setError('❌ Failed to delete category. Make sure it has no items.');
    }
  };

  const handleEditCategory = (category) => {
    setSelectedCategory(category);
    setFormData({
      name: category.name,
      description: category.description || ''
    });
    setActiveTab('edit');
  };

  const clearMessages = () => {
    setError('');
    setSuccessMessage('');
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <div>Loading categories...</div>
      </div>
    );
  }

  return (
    <div>
      <div style={{ marginBottom: '30px' }}>
        <h1 style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
          <FaFolder style={{ marginRight: '10px', color: '#007bff' }} />
          📂 Category Management
        </h1>
      </div>

      {/* Tabs */}
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'view' ? 'active' : ''}`}
          onClick={() => { setActiveTab('view'); clearMessages(); }}
        >
          📋 View Categories
        </button>
        <button
          className={`tab ${activeTab === 'create' ? 'active' : ''}`}
          onClick={() => { setActiveTab('create'); clearMessages(); }}
        >
          ➕ Create Category
        </button>
        <button
          className={`tab ${activeTab === 'edit' ? 'active' : ''}`}
          onClick={() => { setActiveTab('edit'); clearMessages(); }}
        >
          ✏️ Edit Categories
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

      {/* View Categories Tab */}
      <div className={`tab-content ${activeTab === 'view' ? 'active' : ''}`}>
        <div className="card">
          <h3>All Categories</h3>
          {categories.length > 0 ? (
            categories.map((category) => (
              <div key={category.id} className="expander">
                <div className="expander-header">
                  <span>📁 {category.name}</span>
                  <button
                    className="btn btn-danger"
                    onClick={() => handleDeleteCategory(category.id)}
                    style={{ padding: '5px 10px', fontSize: '12px' }}
                  >
                    <FaTrash style={{ marginRight: '5px' }} />
                    Delete
                  </button>
                </div>
                <div className="expander-content">
                  <div className="grid grid-3">
                    <div>
                      <strong>Name:</strong> {category.name}
                    </div>
                    <div>
                      <strong>ID:</strong> {category.id}
                    </div>
                    <div>
                      <strong>Description:</strong> {category.description || 'No description'}
                    </div>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="alert alert-info">
              No categories found. Create your first category in the 'Create Category' tab!
            </div>
          )}
        </div>
      </div>

      {/* Create Category Tab */}
      <div className={`tab-content ${activeTab === 'create' ? 'active' : ''}`}>
        <div className="card">
          <h3>Create New Category</h3>
          <form onSubmit={handleCreateCategory}>
            <div className="form-group">
              <label>Category Name</label>
              <input
                type="text"
                className="form-control"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="e.g., Beverages, Dairy, Snacks"
                required
              />
            </div>
            <div className="form-group">
              <label>Description (optional)</label>
              <textarea
                className="form-control"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                placeholder="Describe what items belong in this category"
                rows="3"
              />
            </div>
            <button type="submit" className="btn btn-primary">
              Create Category
            </button>
          </form>
        </div>
      </div>

      {/* Edit Categories Tab */}
      <div className={`tab-content ${activeTab === 'edit' ? 'active' : ''}`}>
        <div className="card">
          <h3>Edit Categories</h3>
          {categories.length > 0 ? (
            <div>
              <div className="form-group">
                <label>Select Category to Edit:</label>
                <select
                  className="form-control"
                  value={selectedCategory?.id || ''}
                  onChange={(e) => {
                    const category = categories.find(c => c.id === parseInt(e.target.value));
                    if (category) {
                      handleEditCategory(category);
                    }
                  }}
                >
                  <option value="">Select a category...</option>
                  {categories.map((category) => (
                    <option key={category.id} value={category.id}>
                      {category.name}
                    </option>
                  ))}
                </select>
              </div>

              {selectedCategory && (
                <form onSubmit={handleUpdateCategory}>
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
                    <label>New Description</label>
                    <textarea
                      className="form-control"
                      value={formData.description}
                      onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                      rows="3"
                    />
                  </div>
                  <div className="grid grid-2">
                    <button type="submit" className="btn btn-primary">
                      Update Category
                    </button>
                    <button
                      type="button"
                      className="btn btn-danger"
                      onClick={() => handleDeleteCategory(selectedCategory.id)}
                    >
                      Delete Category
                    </button>
                  </div>
                </form>
              )}
            </div>
          ) : (
            <div className="alert alert-info">
              No categories to edit. Create some categories first!
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CategoryManagement; 