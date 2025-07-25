# **Stocker**  
A lightweight stock tracking and analytics tool designed for **small stores and coffee shops**. It helps store owners manage supplies, track usage, and make informed restocking decisions.

---

## **Features**
- ✅ Track stock levels for different categories (e.g., Milk, Coffee Beans, Packaging)  
- ✅ Add, update, and view stock items  
- ✅ Set **restock thresholds** and view low-stock alerts  
- ✅ Basic usage analytics for decision-making  
- ✅ Simple and lightweight — perfect for small businesses

---

## **Tech Stack**
- **Backend:** Python (FastAPI)  
- **Database:** PostgreSQL (production-ready, scalable)  
- **Hosting:** AWS Free Tier (EC2 instance)  

*Future upgrades:* Predictive analytics, and a front-end dashboard.

---

## **Setup Instructions**

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
python setup_database.py
```

### 5. Run the Application
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

---

## **API Endpoints**

- `GET /` - Health check
- `POST /categories/` - Create a new category
- `GET /categories/` - List all categories

*More endpoints coming soon...*
