import requests
from typing import List, Dict, Optional
import streamlit as st

# API configuration
API_BASE_URL = "http://localhost:8000"

class APIClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
    
    def _make_request(self, method: str, endpoint: str, **kwargs):
        """Make HTTP request to API"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")
            return None
    
    # Categories
    def get_categories(self) -> List[Dict]:
        """Get all categories"""
        return self._make_request("GET", "/categories/")
    
    def create_category(self, name: str) -> Dict:
        """Create a new category"""
        return self._make_request("POST", "/categories/", params={"name": name})
    
    # Items
    def get_items(self) -> List[Dict]:
        """Get all items"""
        return self._make_request("GET", "/items/")
    
    def get_item(self, item_id: int) -> Dict:
        """Get specific item"""
        return self._make_request("GET", f"/items/{item_id}")
    
    def create_item(self, name: str, unit: str, restock_threshold: float, category_id: int) -> Dict:
        """Create a new item"""
        return self._make_request("POST", "/items/", params={
            "name": name,
            "unit": unit,
            "restock_threshold": restock_threshold,
            "category_id": category_id
        })
    
    def update_item(self, item_id: int, **kwargs) -> Dict:
        """Update an item"""
        return self._make_request("PUT", f"/items/{item_id}", params=kwargs)
    
    def delete_item(self, item_id: int) -> Dict:
        """Delete an item"""
        return self._make_request("DELETE", f"/items/{item_id}")
    
    def get_items_by_category(self, category_id: int) -> List[Dict]:
        """Get items by category"""
        return self._make_request("GET", f"/items/category/{category_id}")
    
    # Stock Records
    def get_stock_records(self) -> List[Dict]:
        """Get all stock records"""
        return self._make_request("GET", "/stocks/")
    
    def log_stock(self, item_id: int, quantity: float, notes: Optional[str] = None) -> Dict:
        """Log a stock count"""
        params = {"item_id": item_id, "quantity": quantity}
        if notes:
            params["notes"] = notes
        return self._make_request("POST", "/stocks/", params=params)
    
    def get_stock_records_for_item(self, item_id: int) -> List[Dict]:
        """Get stock records for specific item"""
        return self._make_request("GET", f"/stocks/item/{item_id}")
    
    # Restock Records
    def get_restock_records(self) -> List[Dict]:
        """Get all restock records"""
        return self._make_request("GET", "/restocks/")
    
    def log_restock(self, item_id: int, restock_amount: float, supplier: Optional[str] = None, notes: Optional[str] = None) -> Dict:
        """Log a restock"""
        params = {"item_id": item_id, "restock_amount": restock_amount}
        if supplier:
            params["supplier"] = supplier
        if notes:
            params["notes"] = notes
        return self._make_request("POST", "/restocks/", params=params)
    
    def get_restock_records_for_item(self, item_id: int) -> List[Dict]:
        """Get restock records for specific item"""
        return self._make_request("GET", f"/restocks/item/{item_id}")

# Create a global API client instance
api_client = APIClient() 