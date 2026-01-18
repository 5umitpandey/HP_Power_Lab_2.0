"""
Flask API Backend for Intelligent Cost Database
Serves data to the React frontend
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import pandas as pd
from pathlib import Path
import numpy as np
import os
import sys
import subprocess
from werkzeug.utils import secure_filename
import shutil
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# File upload configuration
UPLOAD_FOLDER = Path(__file__).parent.parent / "data" / "uploads"
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# Data paths
DATA_DIR = Path(__file__).parent.parent / "data" / "processed"
RAW_DATA_DIR = Path(__file__).parent.parent / "data" / "raw"

# Load data
def load_data():
    """Load all processed data files and merge with raw data"""
    try:
        # Load processed data
        standardized = pd.read_csv(DATA_DIR / "standardized_items.csv")
        analytics = pd.read_csv(DATA_DIR / "cost_analytics.csv")
        anomalies = pd.read_csv(DATA_DIR / "anomalies.csv")
        
        # Load raw data to get supplier and price info
        raw_data = pd.read_csv(RAW_DATA_DIR / "purchase_orders_raw.csv")
        
        # Merge standardized with raw data to get complete info
        standardized = standardized.merge(
            raw_data[['po_id', 'unit_price', 'supplier', 'region', 'quantity', 'unit', 'po_date']],
            on='po_id',
            how='left'
        )
        
        # Rename columns to match API expectations
        standardized = standardized.rename(columns={
            'supplier': 'supplier_name',
            'confidence_score': 'standardization_confidence'
        })
        
        print(f"✅ Loaded {len(standardized)} standardized items")
        print(f"✅ Loaded {len(analytics)} analytics records")
        print(f"✅ Loaded {len(anomalies)} anomalies")
        
        return standardized, analytics, anomalies
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None

standardized_df, analytics_df, anomalies_df = load_data()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "API is running"})


@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get overall dashboard statistics"""
    if standardized_df is None or analytics_df is None:
        return jsonify({"error": "Data not loaded"}), 500
    
    stats = {
        "total_items": int(len(standardized_df)),
        "total_suppliers": int(standardized_df['supplier_name'].nunique()),
        "avg_unit_price": float(standardized_df['unit_price'].mean()),
        "avg_confidence": float(standardized_df['standardization_confidence'].mean()),
        "items_with_anomalies": int(len(anomalies_df)) if anomalies_df is not None else 0,
        "total_categories": int(standardized_df['category'].nunique() if 'category' in standardized_df.columns else 0)
    }
    
    return jsonify(stats)


@app.route('/api/items', methods=['GET'])
def get_items():
    """Get all standardized items with pagination"""
    if standardized_df is None:
        return jsonify({"error": "Data not loaded"}), 500
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)
    
    df = standardized_df.copy()
    
    # Search filter
    if search:
        df = df[df['canonical_item_name'].str.contains(search, case=False, na=False) |
                df['supplier_name'].str.contains(search, case=False, na=False)]
    
    # Pagination
    total = len(df)
    start = (page - 1) * per_page
    end = start + per_page
    
    items = df.iloc[start:end].replace({np.nan: None}).to_dict('records')
    
    return jsonify({
        "items": items,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page
    })


@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get cost analytics data"""
    if analytics_df is None:
        return jsonify({"error": "Data not loaded"}), 500
    
    analytics = analytics_df.replace({np.nan: None}).to_dict('records')
    return jsonify(analytics)


@app.route('/api/anomalies', methods=['GET'])
def get_anomalies():
    """Get price anomalies"""
    if anomalies_df is None:
        return jsonify({"error": "Data not loaded"}), 500
    
    anomalies = anomalies_df.replace({np.nan: None}).to_dict('records')
    return jsonify(anomalies)


@app.route('/api/price-trends', methods=['GET'])
def get_price_trends():
    """Get price trend data"""
    if analytics_df is None:
        return jsonify({"error": "Data not loaded"}), 500
    
    # Generate trend data
    trends = []
    for _, row in analytics_df.head(10).iterrows():
        trend_data = {
            "item_name": row.get('canonical_item_name', 'Unknown'),
            "trend_direction": row.get('trend_direction', 'stable'),
            "avg_price": float(row.get('avg_price', 0)),
            "min_price": float(row.get('min_price', 0)),
            "max_price": float(row.get('max_price', 0)),
            "price_variance": float(row.get('price_std', 0))
        }
        trends.append(trend_data)
    
    return jsonify(trends)


@app.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    """Get supplier statistics"""
    if standardized_df is None:
        return jsonify({"error": "Data not loaded"}), 500
    
    supplier_stats = standardized_df.groupby('supplier_name').agg({
        'unit_price': ['mean', 'min', 'max', 'count'],
        'standardization_confidence': 'mean'
    }).reset_index()
    
    supplier_stats.columns = ['supplier', 'avg_price', 'min_price', 'max_price', 'item_count', 'avg_confidence']
    suppliers = supplier_stats.replace({np.nan: None}).head(10).to_dict('records')
    
    return jsonify(suppliers)


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get category distribution"""
    if standardized_df is None or 'category' not in standardized_df.columns:
        return jsonify({"error": "Data not loaded or categories not available"}), 500
    
    category_counts = standardized_df['category'].value_counts().to_dict()
    return jsonify(category_counts)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload and process raw purchase order CSV file"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "Only CSV files are allowed"}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_filename = f"upload_{timestamp}_{filename}"
        filepath = app.config['UPLOAD_FOLDER'] / saved_filename
        file.save(filepath)
        
        # Validate CSV structure
        try:
            df = pd.read_csv(filepath)
            required_columns = ['po_id', 'item_description', 'unit_price', 'quantity', 
                              'unit', 'po_date', 'region', 'department', 'supplier']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                os.remove(filepath)
                return jsonify({
                    "error": f"Missing required columns: {', '.join(missing_columns)}",
                    "required_columns": required_columns
                }), 400
            
            # Backup existing raw data
            raw_data_path = Path(__file__).parent.parent / "data" / "raw" / "purchase_orders_raw.csv"
            if raw_data_path.exists():
                backup_path = Path(__file__).parent.parent / "data" / "raw" / f"purchase_orders_raw_backup_{timestamp}.csv"
                shutil.copy(raw_data_path, backup_path)
            
            # Replace raw data with uploaded file
            shutil.copy(filepath, raw_data_path)
            
            return jsonify({
                "message": "File uploaded successfully",
                "filename": saved_filename,
                "rows": len(df),
                "columns": list(df.columns)
            }), 200
            
        except Exception as e:
            if filepath.exists():
                os.remove(filepath)
            return jsonify({"error": f"Invalid CSV format: {str(e)}"}), 400
            
    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500


@app.route('/api/process', methods=['POST'])
def process_data():
    """Run the complete data processing pipeline"""
    try:
        project_root = Path(__file__).parent.parent
        pipeline_script = project_root / "run_pipeline.py"
        
        if not pipeline_script.exists():
            return jsonify({"error": f"Pipeline script not found at {pipeline_script}"}), 500
        
        # Run the complete pipeline
        result = subprocess.run(
            [sys.executable, str(pipeline_script)],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=300,  # 5 minute timeout
            env={**os.environ, 'PYTHONIOENCODING': 'utf-8', 'TF_CPP_MIN_LOG_LEVEL': '2'}
        )
        
        if result.returncode == 0:
            # Reload data after processing
            global standardized_df, analytics_df, anomalies_df
            standardized_df, analytics_df, anomalies_df = load_data()
            
            return jsonify({
                "message": "Data processed successfully",
                "output": result.stdout,
                "standardized_items": len(standardized_df) if standardized_df is not None else 0,
                "analytics_records": len(analytics_df) if analytics_df is not None else 0,
                "anomalies_found": len(anomalies_df) if anomalies_df is not None else 0
            }), 200
        else:
            return jsonify({
                "error": "Processing failed",
                "output": result.stdout,
                "error_details": result.stderr
            }), 500
            
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Processing timeout (max 5 minutes)"}), 500
    except Exception as e:
        import traceback
        return jsonify({
            "error": f"Processing failed: {str(e)}", 
            "traceback": traceback.format_exc()
        }), 500


@app.route('/api/download-template', methods=['GET'])
def download_template():
    """Download CSV template for raw purchase orders"""
    template_data = {
        'po_id': ['PO001', 'PO002', 'PO003'],
        'item_description': ['Carbon Steel Pipe 100mm', 'Stainless Steel Valve 2 inch', 'Gate Valve CS 50mm'],
        'unit_price': [1200.00, 5000.00, 4500.00],
        'quantity': [10, 5, 3],
        'unit': ['pcs', 'pcs', 'pcs'],
        'po_date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'region': ['North', 'South', 'East'],
        'department': ['Maintenance', 'Production', 'Maintenance'],
        'supplier': ['ABC Metals', 'ValveWorld', 'FlowTech']
    }
    
    df = pd.DataFrame(template_data)
    template_path = UPLOAD_FOLDER / "template_purchase_orders.csv"
    df.to_csv(template_path, index=False)
    
    return send_file(template_path, as_attachment=True, download_name="purchase_orders_template.csv")


if __name__ == '__main__':
    print("🚀 Starting Flask API Server...")
    print("📊 Data loaded successfully!")
    app.run(debug=True, port=5000, host='0.0.0.0')
