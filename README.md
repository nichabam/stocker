# Stocker
A comprehensive inventory management system designed for small stores and coffee shops. It helps store owners manage supplies, track usage, make informed restocking decisions, and leverage machine learning for predictive analytics.

## Features

### Core Inventory Management
- Track stock levels for different categories (e.g., Milk, Coffee Beans, Packaging)
- Add, update, and view stock items with detailed information
- Set restock thresholds and view low-stock alerts
- Comprehensive stock history tracking with notes and staff attribution

### Authentication & Security
- Secure JWT-based user authentication system
- User registration and login with password hashing
- Username normalization for consistent data storage
- Protected API endpoints and frontend routes

### Machine Learning Analytics
- **Restock Predictions**: Predict when items need restocking based on usage patterns
- **Stock Life Estimation**: Calculate how long current stock will last
- **Cost Optimization**: Determine optimal restocking quantities for cost efficiency
- **Sales Performance Analysis**: Track sales trends and identify underperforming items
- **Menu Optimization**: AI-powered recommendations for menu adjustments

### Modern Web Interface
- React-based frontend with responsive design
- Real-time dashboard with key metrics
- Advanced filtering and search capabilities
- Professional UI with consistent styling

## Tech Stack

### Backend
- **Python FastAPI** - Modern, fast web framework
- **PostgreSQL** - Production-ready, scalable database
- **SQLAlchemy** - Database ORM
- **JWT Authentication** - Secure token-based auth
- **Machine Learning** - Pandas, NumPy, Scikit-learn for analytics

### Frontend
- **React 18** - Modern React with hooks
- **React Router** - Client-side routing
- **Axios** - HTTP client for API communication
- **CSS Grid/Flexbox** - Responsive layout

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. PostgreSQL Setup
Make sure PostgreSQL is installed and running on your system.

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS (with Homebrew):**
```bash
brew install postgresql
brew services start postgresql
```

### 3. Database Configuration
Create a `.env` file in the project root:
```bash
# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/stocker
```

**Customize the DATABASE_URL:**
- `postgres`: username (default PostgreSQL user)
- `password`: your PostgreSQL password
- `localhost`: database host
- `5432`: PostgreSQL port (default)
- `stocker`: database name

### 4. Setup Database
```bash
python reset_database.py
```

### 5. Run the Backend
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 6. Run the Frontend
```bash
cd frontend
npm install
npm start
```

The React app will be available at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info

### Core Inventory
- `GET /categories/` - List all categories
- `POST /categories/` - Create a new category
- `GET /items/` - List all items
- `POST /items/` - Create a new item
- `GET /stock/` - Get stock history
- `POST /stock/` - Log stock count

### Analytics
- `GET /analytics/restock-predictions` - Get restock predictions
- `GET /analytics/cost-optimization` - Get cost optimization data
- `GET /analytics/sales-performance` - Get sales performance metrics
- `GET /analytics/menu-recommendations` - Get menu optimization suggestions

## Project Structure

```
stock-ai/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Database models
│   ├── auth.py              # Authentication utilities
│   ├── ml_analytics.py      # Machine learning analytics
│   ├── routes/              # API route handlers
│   └── database.py          # Database configuration
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── contexts/        # React contexts
│   │   └── utils/           # Utility functions
│   └── package.json
├── requirements.txt          # Python dependencies
├── reset_database.py        # Database reset script
└── README.md
```

## Key Features

### Inventory Management
- Complete CRUD operations for categories and items
- Stock tracking with historical data
- Restock management with cost tracking
- Low stock alerts and notifications

### Analytics & ML
- Predictive restock scheduling
- Cost optimization algorithms
- Sales performance analysis
- Menu optimization recommendations

### Security
- JWT token authentication
- Password hashing with bcrypt
- Username normalization
- Protected API endpoints

### User Experience
- Modern React interface
- Responsive design
- Real-time updates
- Intuitive navigation

## Development

### Database Management
```bash
# Reset database (drops all tables and recreates)
python reset_database.py
```

### API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation.

### Frontend Development
```bash
cd frontend
npm start  # Development server
npm run build  # Production build
```

<!-- ## Deployment (Future)

The application is designed for AWS deployment with:
- EC2 instance for backend hosting
- RDS for PostgreSQL database
- S3 for static file storage
- CloudFront for content delivery

## Other Future Enhancements

- Real-time updates with WebSockets
- Advanced analytics dashboard
- Export functionality for reports
- Mobile app version
- Multi-tenant architecture
- Role-based access control
- Advanced ML models for better predictions -->
