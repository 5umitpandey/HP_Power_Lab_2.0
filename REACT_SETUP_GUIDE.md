# 🚀 HPCL Intelligent Cost Database - Modern React Frontend

## ✨ New Features

- **Beautiful Modern UI** with animated gradient backgrounds
- **Framer Motion** animations for smooth transitions
- **Tailwind CSS** for responsive design
- **React + Vite** for blazing fast development
- **Interactive Charts** with Recharts
- **Glass morphism** design elements
- **Animated statistics** cards
- **Real-time data** from Flask API backend

---

## 📋 Prerequisites

- Node.js (v18 or higher)
- Python 3.8+
- npm or yarn

---

## 🔧 Installation & Setup

### 1️⃣ Install Backend Dependencies

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies (if not in venv, activate it first)
pip install flask flask-cors pandas numpy
# Or use the requirements file:
pip install -r requirements.txt
```

### 2️⃣ Install Frontend Dependencies

```bash
# Navigate to React frontend directory
cd ../frontend-react

# Install Node modules
npm install
```

---

## 🎯 Running the Application

### Step 1: Start the Flask API Backend

Open a terminal and run:

```bash
# From the backend directory
cd backend
python api.py
```

The API will start on `http://localhost:5000`

### Step 2: Start the React Frontend

Open another terminal and run:

```bash
# From the frontend-react directory
cd frontend-react
npm run dev
```

The frontend will start on `http://localhost:3000`

---

## 🌐 Access the Application

Open your browser and navigate to:
```
http://localhost:3000
```

---

## 📂 Project Structure

```
intelligent-cost-database/
├── backend/
│   ├── api.py                 # Flask REST API
│   └── requirements.txt       # Python dependencies
│
├── frontend-react/
│   ├── src/
│   │   ├── components/
│   │   │   ├── BackgroundAnimation.jsx
│   │   │   ├── Navigation.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ItemsTable.jsx
│   │   │   ├── Analytics.jsx
│   │   │   └── Anomalies.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
└── data/
    └── processed/
        ├── standardized_items.csv
        ├── cost_analytics.csv
        └── anomalies.csv
```

---

## 🎨 Features Overview

### 🏠 Dashboard
- **Real-time KPI cards** with animated statistics
- **Trend indicators** (up/down arrows)
- **Animated progress bars**
- **Quick action buttons**

### 📊 Items Table
- **Searchable** and **paginated** data table
- **Smooth animations** on load
- **Confidence score** visualizations
- **Category tags**

### 📈 Analytics
- **Interactive bar charts** for price trends
- **Pie charts** for supplier distribution
- **Trend cards** with directional indicators
- **Supplier performance** metrics

### ⚠️ Anomalies
- **Severity-based filtering** (High, Medium, Low)
- **Color-coded alerts**
- **Detailed anomaly** information
- **Deviation percentage** tracking

---

## 🎨 Design System

### Color Palette
- **Primary**: Purple gradient (#667eea to #764ba2)
- **Secondary**: Pink gradient (#f093fb to #4facfe)
- **Background**: Dark slate with animated orbs
- **Glass**: Transparent backdrop blur effects

### Animations
- **Fade in/out** transitions
- **Slide up/down** effects
- **Hover** scale effects
- **Floating** elements
- **Gradient shifts**

---

## 🔌 API Endpoints

- `GET /api/health` - Health check
- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/items` - Paginated items list
- `GET /api/analytics` - Cost analytics data
- `GET /api/anomalies` - Price anomalies
- `GET /api/price-trends` - Price trend data
- `GET /api/suppliers` - Supplier statistics
- `GET /api/categories` - Category distribution

---

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Utility-first CSS
- **Framer Motion** - Animation library
- **Recharts** - Chart library
- **Axios** - HTTP client
- **Lucide React** - Icon library

### Backend
- **Flask** - Web framework
- **Flask-CORS** - CORS handling
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing

---

## 📝 Development Tips

### Hot Reload
Both frontend and backend support hot reload:
- **Frontend**: Vite HMR automatically updates on file changes
- **Backend**: Flask debug mode reloads on code changes

### Build for Production

```bash
# Frontend
cd frontend-react
npm run build

# This creates an optimized production build in the dist/ folder
```

### Environment Variables
Create a `.env` file in frontend-react for custom configurations:
```
VITE_API_URL=http://localhost:5000
```

---

## 🐛 Troubleshooting

### Port Already in Use
If port 3000 or 5000 is busy:
- Change frontend port in `vite.config.js`
- Change backend port in `api.py`

### CORS Errors
Make sure Flask-CORS is installed:
```bash
pip install flask-cors
```

### Module Not Found
Reinstall dependencies:
```bash
# Frontend
cd frontend-react
npm install

# Backend
cd backend
pip install -r requirements.txt
```

---

## 🎉 Features Comparison

| Feature | Old (Streamlit) | New (React) |
|---------|----------------|-------------|
| UI Framework | Streamlit | React + Tailwind |
| Animations | Limited | Full Framer Motion |
| Customization | Limited | Highly customizable |
| Performance | Server-side | Client-side (faster) |
| Responsiveness | Basic | Advanced responsive |
| Background | Static | Animated gradients |
| Loading States | Basic | Beautiful skeletons |

---

## 📧 Support

For issues or questions, refer to the project documentation or check the console logs for debugging information.

---

## 🌟 Enjoy Your New Beautiful Dashboard!

The new React frontend provides a modern, animated, and highly interactive experience compared to the previous Streamlit version. Happy coding! 🎨✨
