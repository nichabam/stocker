# Stocker - React Frontend

A modern React frontend for the Stocker Cafe Inventory Management System, replacing the original Streamlit interface.

## Features

### 🔐 Authentication
- Simple login system with hardcoded credentials (cafe/stock2024)
- Persistent authentication using localStorage
- Protected routes

### 📊 Dashboard
- Real-time statistics overview
- Quick metrics: Total Items, Low Stock Items, Categories, Today's Restocks
- Recent activity feed showing latest stock counts

### 📂 Category Management
- **View Categories**: Browse all categories with expandable details
- **Create Category**: Add new categories with optional descriptions
- **Edit Categories**: Update existing categories or delete them
- Full CRUD operations with error handling

### 📦 Item Management
- **View Items**: Browse all items with filtering options
  - Filter by low stock items
  - Filter by category
  - Visual indicators for stock levels
- **Create Item**: Add new items with category assignment
- **Edit Items**: Update existing items or delete them
- Preview functionality when creating items

### 📦 Stock Management
- **Stock Overview**: View current stock levels organized by category
  - Visual indicators for low stock items
  - Detailed stock information
- **Log Stock Counts**: Update stock quantities for items
  - Pre-filled with current stock levels
  - Optional notes and staff name tracking

## Technology Stack

- **React 18** - Modern React with hooks
- **React Router** - Client-side routing
- **Axios** - HTTP client for API communication
- **React Icons** - Icon library
- **CSS Grid/Flexbox** - Modern responsive layout
- **Local Storage** - Persistent authentication

## Installation & Setup

1. **Install Dependencies**
   ```bash
   cd frontend_v2
   npm install
   ```

2. **Start Development Server**
   ```bash
   npm start
   ```

3. **Build for Production**
   ```bash
   npm run build
   ```

## API Configuration

The frontend connects to the FastAPI backend at `http://localhost:8000`. Make sure your backend is running before starting the frontend.

The API client (`src/utils/apiClient.js`) handles all communication with the backend and includes:

- **Categories**: CRUD operations for categories
- **Items**: CRUD operations for items
- **Stock Records**: Logging and retrieving stock counts
- **Restock Records**: Logging and retrieving restock data

## Project Structure

```
frontend_v2/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Login.js              # Authentication component
│   │   ├── Layout.js             # Main layout with sidebar
│   │   ├── Dashboard.js          # Main dashboard
│   │   ├── CategoryManagement.js # Category CRUD operations
│   │   ├── ItemManagement.js     # Item CRUD operations
│   │   └── StockManagement.js    # Stock tracking
│   ├── contexts/
│   │   └── AuthContext.js        # Authentication context
│   ├── utils/
│   │   └── apiClient.js          # API communication
│   ├── App.js                    # Main app with routing
│   ├── index.js                  # React entry point
│   └── index.css                 # Global styles
├── package.json
└── README.md
```

## Key Features Comparison with Streamlit

| Feature | Streamlit | React |
|---------|-----------|-------|
| Authentication | Session-based | Context + localStorage |
| Navigation | Page-based | React Router |
| State Management | Session state | React hooks |
| UI Components | Streamlit widgets | Custom React components |
| Styling | Streamlit themes | Custom CSS |
| API Communication | Python requests | Axios |
| Responsive Design | Limited | Full responsive |

## Usage

1. **Login**: Use credentials `cafe` / `stock2024`
2. **Dashboard**: View overview and recent activity
3. **Categories**: Manage item categories
4. **Items**: Manage inventory items
5. **Stock Management**: Track and update stock levels

## Development Notes

- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Loading States**: Loading indicators for better UX
- **Form Validation**: Client-side validation with helpful error messages
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, professional interface with consistent styling

## Backend Compatibility

This React frontend is designed to work with your existing FastAPI backend. It uses the same API endpoints and data structures as the original Streamlit frontend.

## Future Enhancements

- Real-time updates using WebSockets
- Advanced analytics and charts
- Export functionality for reports
- Mobile app version
- Multi-user support with proper authentication
- Advanced filtering and search capabilities 