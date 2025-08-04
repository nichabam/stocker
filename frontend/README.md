# Stocker - React Frontend

A modern React frontend for the Stocker Cafe Inventory Management System, replacing the original Streamlit interface.

## Features

### Authentication
- Secure JWT-based authentication system
- User registration and login functionality
- Username normalization (converted to lowercase)
- Password hashing with bcrypt
- Persistent authentication using localStorage
- Protected routes with token verification

### Dashboard
- Real-time statistics overview
- Quick metrics: Total Items, Low Stock Items, Categories, Today's Restocks
- Recent activity feed showing latest stock counts

### Category Management
- **View Categories**: Browse all categories with expandable details
- **Create Category**: Add new categories with optional descriptions
- **Edit Categories**: Update existing categories or delete them
- Full CRUD operations with error handling

### Item Management
- **View Items**: Browse all items with filtering options
  - Filter by low stock items
  - Filter by category
  - Visual indicators for stock levels
- **Create Item**: Add new items with category assignment
- **Edit Items**: Update existing items or delete them
- Preview functionality when creating items

### Stock Management
- **Stock Overview**: View current stock levels organized by category
  - Visual indicators for low stock items
  - Detailed stock information
- **Log Stock Counts**: Update stock quantities for items
  - Pre-filled with current stock levels
  - Optional notes and staff name tracking

### Analytics Dashboard
- **ML Predictions**: Restock date predictions and stock life estimates
- **Cost Optimization**: Optimal restocking quantities and cost analysis
- **Sales Performance**: Sales trends and performance metrics
- **Menu Optimization**: Recommendations for menu items based on sales data
- **Dashboard Summary**: Comprehensive analytics overview

## Technology Stack

- **React 18** - Modern React with hooks
- **React Router** - Client-side routing
- **Axios** - HTTP client for API communication
- **React Icons** - Icon library
- **CSS Grid/Flexbox** - Modern responsive layout
- **Local Storage** - Persistent authentication
- **JWT Tokens** - Secure authentication

## Installation & Setup

1. **Install Dependencies**
   ```bash
   cd frontend
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

- **Authentication**: Login, register, token verification
- **Categories**: CRUD operations for categories
- **Items**: CRUD operations for items
- **Stock Records**: Logging and retrieving stock counts
- **Restock Records**: Logging and retrieving restock data
- **Analytics**: ML predictions, cost optimization, sales performance

## Project Structure

```
frontend/
├── public/
│   ├── index.html
│   ├── manifest.json
│   ├── favicon.ico
│   └── favicon.svg
├── src/
│   ├── components/
│   │   ├── Login.js              # Authentication component
│   │   ├── Layout.js             # Main layout with sidebar
│   │   ├── Dashboard.js          # Main dashboard
│   │   ├── CategoryManagement.js # Category CRUD operations
│   │   ├── ItemManagement.js     # Item CRUD operations
│   │   ├── StockManagement.js    # Stock tracking
│   │   └── Analytics.js          # ML analytics dashboard
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
| Authentication | Session-based | JWT + Context |
| Navigation | Page-based | React Router |
| State Management | Session state | React hooks |
| UI Components | Streamlit widgets | Custom React components |
| Styling | Streamlit themes | Custom CSS |
| API Communication | Python requests | Axios |
| Responsive Design | Limited | Full responsive |
| ML Analytics | Basic | Advanced with predictions |

## Usage

1. **Register/Login**: Create an account or login with existing credentials
2. **Dashboard**: View overview and recent activity
3. **Categories**: Manage item categories
4. **Items**: Manage inventory items
5. **Stock Management**: Track and update stock levels
6. **Analytics**: View ML predictions and performance metrics

## Development Notes

- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Loading States**: Loading indicators for better UX
- **Form Validation**: Client-side validation with helpful error messages
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, professional interface with consistent styling
- **Security**: JWT tokens, password hashing, username normalization

## Backend Compatibility

This React frontend is designed to work with your existing FastAPI backend. It uses the same API endpoints and data structures as the original Streamlit frontend, with additional authentication and analytics endpoints.

## Future Enhancements

- Real-time updates using WebSockets
- Advanced analytics and charts
- Export functionality for reports
- Mobile app version
- Multi-user support with role-based access
- Advanced filtering and search capabilities
- Multi-tenant architecture for user data isolation 