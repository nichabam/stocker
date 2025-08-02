import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

class APIClient {
  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
    });
  }

  // Helper method to handle API calls
  async makeRequest(method, endpoint, params = {}) {
    try {
      const response = await this.api.request({
        method,
        url: endpoint,
        params,
      });
      return response.data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // Categories
  async getCategories() {
    return this.makeRequest('GET', '/categories/');
  }

  async createCategory(name) {
    return this.makeRequest('POST', '/categories/', { name });
  }

  async updateCategory(categoryId, name, description = null) {
    const params = { name };
    if (description !== null) {
      params.description = description;
    }
    return this.makeRequest('PUT', `/categories/${categoryId}`, params);
  }

  async deleteCategory(categoryId) {
    return this.makeRequest('DELETE', `/categories/${categoryId}`);
  }

  // Items
  async getItems() {
    return this.makeRequest('GET', '/items/');
  }

  async getItem(itemId) {
    return this.makeRequest('GET', `/items/${itemId}`);
  }

  async createItem(name, unit, restockThreshold, categoryId) {
    return this.makeRequest('POST', '/items/', {
      name,
      unit,
      restock_threshold: restockThreshold,
      category_id: categoryId,
    });
  }

  async updateItem(itemId, updates) {
    return this.makeRequest('PUT', `/items/${itemId}`, updates);
  }

  async deleteItem(itemId) {
    return this.makeRequest('DELETE', `/items/${itemId}`);
  }

  async getItemsByCategory(categoryId) {
    return this.makeRequest('GET', `/items/category/${categoryId}`);
  }

  // Stock Records
  async getStockRecords() {
    return this.makeRequest('GET', '/stock/');
  }

  async logStock(itemId, quantity, notes = null, staffName = null) {
    const params = { item_id: itemId, quantity };
    if (notes) params.notes = notes;
    if (staffName) params.staff_name = staffName;
    return this.makeRequest('POST', '/stock/', params);
  }

  async getStockRecordsForItem(itemId) {
    return this.makeRequest('GET', `/stock/item/${itemId}`);
  }

  // Restock Records
  async getRestockRecords() {
    return this.makeRequest('GET', '/restocks/');
  }

  async logRestock(itemId, restockAmount, supplier = null, notes = null) {
    const params = { item_id: itemId, restock_amount: restockAmount };
    if (supplier) params.supplier = supplier;
    if (notes) params.notes = notes;
    return this.makeRequest('POST', '/restocks/', params);
  }

  async getRestockRecordsForItem(itemId) {
    return this.makeRequest('GET', `/restocks/item/${itemId}`);
  }
}

export default new APIClient(); 