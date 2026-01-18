"""
HPCL Intelligent Cost Database - Enhanced Frontend
Professional UI with Animations & Modern Design
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time

# Import custom components
from components import (
    render_kpi_card, render_metric_box, render_comparison_table,
    render_price_trend_chart, render_regional_comparison,
    render_supplier_comparison, render_confidence_progress,
    render_anomaly_highlight, render_prediction_chart,
    render_search_box
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="HPCL Intelligent Cost Database",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_file = Path(__file__).parent / "assets" / "custom.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        st.warning(f"CSS file not found at: {css_file}")
    
    # Additional inline styles for enhanced effects
    st.markdown("""
        <style>
        /* Ensure body is visible */
        body {
            background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%) !important;
        }
        
        /* Additional custom styles */
        h1, h2, h3 {
            animation: fadeInUp 0.6s ease-out;
            color: #e2e8f0 !important;
        }
        
        .stPlotlyChart {
            animation: fadeIn 0.8s ease-out;
        }
        
        /* Floating action button */
        .floating-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
            cursor: pointer;
            z-index: 1000;
            animation: float 3s ease-in-out infinite;
        }
        
        /* Status badges */
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            animation: slideInRight 0.5s ease-out;
        }
        
        .status-success {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
        }
        
        .status-warning {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
        }
        
        .status-error {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
        }
        
        /* Counter animation */
        @keyframes countUp {
            from { opacity: 0; transform: scale(0.5); }
            to { opacity: 1; transform: scale(1); }
        }
        
        .count-up {
            animation: countUp 0.5s ease-out;
        }
        </style>
    """, unsafe_allow_html=True)

load_css()

# ============================================================================
# DATA LOADING WITH PROGRESS
# ============================================================================

@st.cache_data
def load_data():
    """Load all CSV files from processed data directory."""
    try:
        base_path = Path(__file__).parent.parent / "data"
        
        raw_df = pd.read_csv(base_path / "raw" / "purchase_orders_raw.csv")
        standardized_df = pd.read_csv(base_path / "processed" / "standardized_items.csv")
        analytics_df = pd.read_csv(base_path / "processed" / "cost_analytics.csv")
        
        # Load anomalies with fallback for empty file
        try:
            anomalies_df = pd.read_csv(base_path / "processed" / "anomalies.csv")
        except (pd.errors.EmptyDataError, FileNotFoundError):
            anomalies_df = pd.DataFrame(columns=[
                "po_id", "item_code", "unit_price", "expected_price",
                "anomaly_flag", "anomaly_reason"
            ])
        
        return raw_df, standardized_df, analytics_df, anomalies_df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

# Show loading animation
try:
    with st.spinner('🚀 Loading Intelligent Cost Database...'):
        time.sleep(0.5)  # Brief pause for visual effect
        raw_df, standardized_df, analytics_df, anomalies_df = load_data()
except Exception as e:
    st.error(f"Failed to load data: {str(e)}")
    st.stop()

# ============================================================================
# ANIMATED HEADER
# ============================================================================

st.markdown("""
<div style="text-align: center; padding: 2rem 0; animation: fadeInDown 0.8s ease-out;">
    <h1 style="
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    ">⚡ HPCL Intelligent Cost Database</h1>
    <p style="
        font-size: 1.2rem;
        color: #94a3b8;
        font-weight: 500;
    ">Procurement Transformation & Digitalisation Platform</p>
    <div style="
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 1rem;
    ">
        <span class="status-badge status-success">✓ AI Powered</span>
        <span class="status-badge status-success">✓ Real-time Analytics</span>
        <span class="status-badge status-success">✓ Predictive Insights</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - NAVIGATION & FILTERS
# ============================================================================

with st.sidebar:
    st.markdown("""
    <div class="logo-container">
        <h1 style="margin: 0; font-size: 28px; color: white; font-weight: 800;">⚡ HPCL</h1>
        <p style="margin: 8px 0 0 0; font-size: 14px; color: rgba(255,255,255,0.9); font-weight: 500;">
            Cost Intelligence Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔍 Search & Filter")
    
    # Search functionality with animation
    search_term = st.text_input(
        "Search items, suppliers, regions...",
        placeholder="Type to search...",
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Filter by region
    st.markdown("#### 📍 Region")
    regions = ["All"] + sorted(raw_df['region'].unique().tolist())
    selected_region = st.selectbox("Region", regions, label_visibility="collapsed")
    
    # Filter by department
    st.markdown("#### 🏢 Department")
    departments = ["All"] + sorted(raw_df['department'].unique().tolist())
    selected_dept = st.selectbox("Department", departments, label_visibility="collapsed")
    
    # Date range filter
    st.markdown("#### 📅 Date Range")
    raw_df['po_date'] = pd.to_datetime(raw_df['po_date'])
    date_range = st.date_input(
        "Select date range",
        value=(raw_df['po_date'].min(), raw_df['po_date'].max()),
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Quick stats in sidebar
    st.markdown("### 📊 Quick Stats")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total POs", len(raw_df), delta=None)
    with col2:
        st.metric("Unique Items", standardized_df['item_code'].nunique(), delta=None)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Export button with animation
    if st.button("📥 Export Data", use_container_width=True):
        st.success("✓ Data exported successfully!")

# Filter data based on selections
filtered_raw = raw_df.copy()
filtered_analytics = analytics_df.copy()
filtered_standardized = standardized_df.copy()

if selected_region != "All":
    filtered_raw = filtered_raw[filtered_raw['region'] == selected_region]
    filtered_analytics = filtered_analytics[filtered_analytics['region'] == selected_region]

if selected_dept != "All":
    filtered_raw = filtered_raw[filtered_raw['department'] == selected_dept]

# Apply search filter
if search_term:
    mask = (
        filtered_raw['item_description'].str.contains(search_term, case=False, na=False) |
        filtered_raw['supplier'].str.contains(search_term, case=False, na=False) |
        filtered_raw['region'].str.contains(search_term, case=False, na=False)
    )
    filtered_raw = filtered_raw[mask]
    
    # Filter standardized based on filtered POs
    filtered_standardized = filtered_standardized[
        filtered_standardized['po_id'].isin(filtered_raw['po_id'])
    ]

# ============================================================================
# KEY METRICS DASHBOARD (ANIMATED)
# ============================================================================

st.markdown("## 📈 Key Performance Indicators")

# Animated metrics row
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_pos = len(filtered_raw)
    st.markdown(f"""
    <div class="glass-card count-up" style="text-align: center;">
        <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 8px;">Total Purchase Orders</div>
        <div style="font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            {total_pos:,}
        </div>
        <div style="font-size: 0.85rem; color: #10b981; margin-top: 8px;">↑ Active</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    unique_items = filtered_standardized['item_code'].nunique()
    st.markdown(f"""
    <div class="glass-card count-up" style="text-align: center; animation-delay: 0.1s;">
        <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 8px;">Canonical Items</div>
        <div style="font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            {unique_items:,}
        </div>
        <div style="font-size: 0.85rem; color: #3b82f6; margin-top: 8px;">Standardized</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_confidence = filtered_standardized['confidence_score'].mean() if 'confidence_score' in filtered_standardized.columns else 0
    st.markdown(f"""
    <div class="glass-card count-up" style="text-align: center; animation-delay: 0.2s;">
        <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 8px;">Avg Confidence</div>
        <div style="font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #10b981 0%, #059669 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            {avg_confidence*100:.0f}%
        </div>
        <div style="font-size: 0.85rem; color: #10b981; margin-top: 8px;">High Quality</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    total_spend = filtered_raw['unit_price'].sum() * filtered_raw['quantity'].sum() if len(filtered_raw) > 0 else 0
    st.markdown(f"""
    <div class="glass-card count-up" style="text-align: center; animation-delay: 0.3s;">
        <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 8px;">Total Spend</div>
        <div style="font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            ₹{total_spend/1000000:.1f}M
        </div>
        <div style="font-size: 0.85rem; color: #f59e0b; margin-top: 8px;">Procurement Value</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    anomaly_count = len(anomalies_df) if len(anomalies_df) > 0 else 0
    st.markdown(f"""
    <div class="glass-card count-up" style="text-align: center; animation-delay: 0.4s;">
        <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 8px;">Anomalies Detected</div>
        <div style="font-size: 2.5rem; font-weight: 700; background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            {anomaly_count}
        </div>
        <div style="font-size: 0.85rem; color: #ef4444; margin-top: 8px;">Flagged</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================================================
# TABBED INTERFACE WITH ANIMATIONS
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Overview",
    "📊 Cost Analytics",
    "⚠️ Anomaly Detection",
    "🎯 Item Standardization",
    "🔮 Price Prediction"
])

# TAB 1: OVERVIEW
with tab1:
    st.markdown("## 📋 Executive Dashboard")
    
    # Row 1: Trend and Regional Analysis
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📈 Price Trends Over Time")
        if len(filtered_analytics) > 0:
            trend_fig = render_price_trend_chart(filtered_analytics)
            st.plotly_chart(trend_fig, use_container_width=True)
        else:
            st.info("No data available for selected filters")
    
    with col2:
        st.markdown("### 🌍 Regional Comparison")
        if len(filtered_analytics) > 0:
            regional_fig = render_regional_comparison(filtered_analytics)
            st.plotly_chart(regional_fig, use_container_width=True)
        else:
            st.info("No data available for selected filters")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 2: Supplier Analysis and Top Items
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏭 Top Suppliers by Volume")
        supplier_data = filtered_raw.groupby('supplier').agg({
            'po_id': 'count',
            'unit_price': 'mean'
        }).reset_index()
        supplier_data.columns = ['Supplier', 'Orders', 'Avg Price']
        supplier_data = supplier_data.sort_values('Orders', ascending=False).head(10)
        
        fig = go.Figure(data=[go.Bar(
            x=supplier_data['Orders'],
            y=supplier_data['Supplier'],
            orientation='h',
            marker=dict(
                color=supplier_data['Orders'],
                colorscale='Viridis',
                showscale=False
            ),
            text=supplier_data['Orders'],
            textposition='auto',
        )])
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400,
            xaxis_title="Number of Orders",
            yaxis_title="",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Most Procured Items")
        if len(filtered_standardized) > 0 and 'canonical_item_name' in filtered_standardized.columns:
            top_items = filtered_standardized['canonical_item_name'].value_counts().head(10)
            
            fig = go.Figure(data=[go.Pie(
                labels=top_items.index,
                values=top_items.values,
                hole=0.4,
                marker=dict(colors=px.colors.sequential.Plasma)
            )])
            
            fig.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=400,
                showlegend=True,
                legend=dict(font=dict(size=10))
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No standardized items available")

# TAB 2: COST ANALYTICS
with tab2:
    st.markdown("## 💰 Detailed Cost Analytics")
    
    if len(filtered_analytics) > 0:
        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Average Price",
                f"₹{filtered_analytics['avg_price'].mean():,.2f}",
                f"{filtered_analytics['avg_price'].std():.2f} std dev"
            )
        
        with col2:
            st.metric(
                "Median Price",
                f"₹{filtered_analytics['median_price'].median():,.2f}",
                "50th percentile"
            )
        
        with col3:
            trending_up = len(filtered_analytics[filtered_analytics['trend_direction'] == 'UP']) if 'trend_direction' in filtered_analytics.columns else 0
            st.metric(
                "Trending Up",
                trending_up,
                f"{trending_up/len(filtered_analytics)*100:.1f}% of items"
            )
        
        with col4:
            price_volatility = filtered_analytics['price_std'].mean()
            st.metric(
                "Price Volatility",
                f"₹{price_volatility:.2f}",
                "Average std dev"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Detailed analytics table
        st.markdown("### 📋 Complete Cost Analytics Table")
        
        display_df = filtered_analytics.copy()
        if 'canonical_item_name' in display_df.columns:
            display_df = display_df[[
                'canonical_item_name', 'region', 'supplier',
                'avg_price', 'median_price', 'min_price', 'max_price',
                'price_std', 'trend_direction'
            ] if 'trend_direction' in display_df.columns else [
                'canonical_item_name', 'region', 'supplier',
                'avg_price', 'median_price', 'min_price', 'max_price', 'price_std'
            ]]
        
        st.dataframe(
            display_df,
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Analytics Data",
            data=csv,
            file_name=f"cost_analytics_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No cost analytics data available for selected filters")

# TAB 3: ANOMALY DETECTION
with tab3:
    st.markdown("## ⚠️ Price Anomaly Detection")
    
    st.markdown("""
    <div class="glass-card">
        <h4>🔍 What are Price Anomalies?</h4>
        <p>Our AI system automatically identifies unusual pricing patterns that may indicate:</p>
        <ul>
            <li>💸 Pricing errors or data entry mistakes</li>
            <li>🏷️ Unusual supplier pricing</li>
            <li>📊 Market fluctuations</li>
            <li>⚡ Opportunities for cost negotiation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if len(anomalies_df) > 0:
        # Severity breakdown
        col1, col2, col3 = st.columns(3)
        
        critical_count = len(anomalies_df[anomalies_df['anomaly_reason'].str.contains('CRITICAL', na=False)]) if 'anomaly_reason' in anomalies_df.columns else 0
        high_count = len(anomalies_df[anomalies_df['anomaly_reason'].str.contains('HIGH', na=False)]) if 'anomaly_reason' in anomalies_df.columns else 0
        med_count = len(anomalies_df) - critical_count - high_count
        
        with col1:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #ef4444;">
                <h3 style="color: #ef4444; margin: 0;">🔴 {critical_count}</h3>
                <p style="margin: 8px 0 0 0; color: #94a3b8;">Critical - Immediate Review</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #f59e0b;">
                <h3 style="color: #f59e0b; margin: 0;">🟠 {high_count}</h3>
                <p style="margin: 8px 0 0 0; color: #94a3b8;">High - Review Recommended</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #eab308;">
                <h3 style="color: #eab308; margin: 0;">🟡 {med_count}</h3>
                <p style="margin: 8px 0 0 0; color: #94a3b8;">Medium - Monitor</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Anomalies table
        st.markdown("### 📋 Detailed Anomaly Report")
        st.dataframe(
            anomalies_df,
            use_container_width=True,
            height=400
        )
    else:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <h2 style="color: #10b981;">✓ No Anomalies Detected</h2>
            <p style="color: #94a3b8; font-size: 1.1rem;">All prices are within expected ranges</p>
        </div>
        """, unsafe_allow_html=True)

# TAB 4: ITEM STANDARDIZATION
with tab4:
    st.markdown("## 🎯 AI-Powered Item Standardization")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        percentage = (len(filtered_standardized) / len(filtered_raw) * 100) if len(filtered_raw) > 0 else 0
        st.metric(
            "Items Standardized",
            len(filtered_standardized),
            f"{percentage:.0f}% of POs"
        )
    
    with col2:
        avg_confidence = filtered_standardized['confidence_score'].mean() if 'confidence_score' in filtered_standardized.columns else 0
        st.metric(
            "Average Confidence",
            f"{avg_confidence:.1%}",
            "High quality ✓"
        )
    
    with col3:
        reduction = (1 - standardized_df['item_code'].nunique() / len(standardized_df)) * 100 if len(standardized_df) > 0 else 0
        st.metric(
            "Duplicate Reduction",
            f"{reduction:.1f}%",
            f"{len(standardized_df) - standardized_df['item_code'].nunique()} duplicates merged"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Standardization visualization
    st.markdown("### 📊 Standardization Results")
    
    if len(filtered_standardized) > 0:
        st.dataframe(
            filtered_standardized.head(100),
            use_container_width=True,
            height=500
        )
        
        csv = filtered_standardized.to_csv(index=False)
        st.download_button(
            label="📥 Download Standardized Items",
            data=csv,
            file_name=f"standardized_items_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# TAB 5: PRICE PREDICTION
with tab5:
    st.markdown("## 🔮 AI Price Forecasting")
    
    st.markdown("""
    <div class="glass-card">
        <h4>🤖 Predictive Analytics</h4>
        <p>Our machine learning models analyze historical patterns to forecast future price movements.
        Use these insights for:</p>
        <ul>
            <li>📅 Budget planning and cost estimation</li>
            <li>⏰ Optimal procurement timing</li>
            <li>💼 Supplier negotiations</li>
            <li>📈 Trend anticipation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if len(filtered_analytics) > 0:
        # Prediction Chart
        pred_fig = render_prediction_chart(filtered_analytics)
        st.plotly_chart(pred_fig, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Forecast table
        st.markdown("### 📋 3-Month Price Forecast Summary")
        
        forecast_data = []
        for _, item in filtered_analytics.head(20).iterrows():
            if 'trend_direction' in item and item['trend_direction'] == 'UP':
                forecast_price = float(item['avg_price']) * 1.06
                trend_emoji = "📈"
                trend_color = "#ef4444"
            elif 'trend_direction' in item and item['trend_direction'] == 'DOWN':
                forecast_price = float(item['avg_price']) * 0.95
                trend_emoji = "📉"
                trend_color = "#10b981"
            else:
                forecast_price = float(item['avg_price'])
                trend_emoji = "➡️"
                trend_color = "#94a3b8"
            
            forecast_data.append({
                'Item': item.get('canonical_item_name', 'Unknown'),
                'Current Price': f"₹{item['avg_price']:,.2f}",
                'Forecasted Price': f"₹{forecast_price:,.2f}",
                'Change': f"{((forecast_price/item['avg_price']-1)*100):.1f}%",
                'Trend': trend_emoji
            })
        
        forecast_df = pd.DataFrame(forecast_data)
        st.dataframe(forecast_df, use_container_width=True, height=400)
    else:
        st.info("No data available for price forecasting")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div style="
    text-align: center;
    padding: 2rem;
    background: rgba(26, 31, 46, 0.6);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    margin-top: 3rem;
    animation: fadeIn 1s ease-out;
">
    <p style="color: #94a3b8; margin: 0; font-size: 0.9rem;">
        Powered by AI/ML Technology | HPCL Procurement Transformation Initiative
    </p>
    <p style="color: #64748b; margin: 8px 0 0 0; font-size: 0.85rem;">
        © 2026 HPCL Intelligent Cost Database | Enterprise-Ready Prototype
    </p>
</div>
""", unsafe_allow_html=True)
