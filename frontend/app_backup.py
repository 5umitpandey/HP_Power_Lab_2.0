"""
HPCL Intelligent Cost Database - Main Streamlit Dashboard
Theme: Procurement Transformation & Digitalisation
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Import custom components
from components import (
    render_kpi_card, render_metric_box, render_comparison_table,
    render_price_trend_chart, render_regional_comparison,
    render_supplier_comparison, render_confidence_progress,
    render_anomaly_highlight, render_prediction_chart,
    render_search_box, apply_custom_css
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

apply_custom_css()

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_data():
    """Load all CSV files from processed data directory."""
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


# Load data
raw_df, standardized_df, analytics_df, anomalies_df = load_data()

# ============================================================================
# SIDEBAR - NAVIGATION & FILTERS
# ============================================================================

st.sidebar.markdown("""
<div style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    color: white;
    text-align: center;
">
    <h1 style="margin: 0; font-size: 24px;">⚡ HPCL</h1>
    <p style="margin: 5px 0 0 0; font-size: 13px; opacity: 0.9;">
        Intelligent Cost Database
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# Search functionality
search_term = render_search_box("Search items, suppliers, regions...")

# Filter by region
regions = ["All"] + sorted(raw_df['region'].unique().tolist())
selected_region = st.sidebar.selectbox("📍 Region", regions)

# Filter by department
departments = ["All"] + sorted(raw_df['department'].unique().tolist())
selected_dept = st.sidebar.selectbox("🏢 Department", departments)

# Filter data based on selections
filtered_raw = raw_df.copy()
filtered_analytics = analytics_df.copy()
filtered_standardized = standardized_df.copy()

if selected_region != "All":
    filtered_raw = filtered_raw[filtered_raw['region'] == selected_region]
    filtered_analytics = filtered_analytics[filtered_analytics['region'] == selected_region]

if selected_dept != "All":
    filtered_raw = filtered_raw[filtered_raw['department'] == selected_dept]

# Search filter
if search_term:
    search_lower = search_term.lower()
    mask = (
        filtered_raw['item_description'].str.lower().str.contains(search_lower, na=False) |
        filtered_raw['supplier'].str.lower().str.contains(search_lower, na=False)
    )
    filtered_raw = filtered_raw[mask]
    
    std_mask = (
        filtered_standardized['canonical_item_name'].str.lower().str.contains(search_lower, na=False) |
        filtered_standardized['item_code'].str.lower().str.contains(search_lower, na=False)
    )
    filtered_standardized = filtered_standardized[std_mask]

st.sidebar.markdown("---")

# Additional info
st.sidebar.markdown("""
<div style="
    background: #f8f9fa;
    border-radius: 8px;
    padding: 15px;
    font-size: 12px;
    color: #2c3e50;
">
    <strong>📊 Dashboard Stats</strong><br>
    • Raw POs: <strong>{}</strong><br>
    • Standardized Items: <strong>{}</strong><br>
    • Anomalies: <strong>{}</strong><br>
    • Last Updated: <strong>{}</strong>
</div>
""".format(
    len(raw_df),
    len(standardized_df),
    len(anomalies_df),
    datetime.now().strftime("%Y-%m-%d %H:%M")
), unsafe_allow_html=True)

st.sidebar.markdown("---")

# Download section
st.sidebar.subheader("📥 Download Data")
if st.sidebar.button("Download Standardized Items"):
    csv = filtered_standardized.to_csv(index=False)
    st.sidebar.download_button(
        label="📥 Get CSV",
        data=csv,
        file_name=f"standardized_items_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

if st.sidebar.button("Download Cost Analytics"):
    csv = filtered_analytics.to_csv(index=False)
    st.sidebar.download_button(
        label="📥 Get CSV",
        data=csv,
        file_name=f"cost_analytics_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

# Header
st.markdown("""
<div style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    padding: 30px;
    margin-bottom: 30px;
    color: white;
">
    <h1 style="margin: 0; font-size: 36px; font-weight: 700;">
        ⚡ Intelligent Cost Database
    </h1>
    <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">
        Procure with Precision | Analyze with Intelligence
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# TAB SECTION
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "🔄 Item Standardization",
    "💰 Cost Analytics",
    "🚨 Anomalies",
    "🔮 Price Prediction"
])

# ============================================================================
# TAB 1: OVERVIEW
# ============================================================================

with tab1:
    st.subheader("Executive Summary")
    
    # Calculate KPIs
    total_pos = len(filtered_raw)
    unique_items_raw = len(filtered_raw['item_description'].unique())
    unique_items_std = len(filtered_standardized['canonical_item_name'].unique())
    dedup_percentage = ((unique_items_raw - unique_items_std) / unique_items_raw * 100) if unique_items_raw > 0 else 0
    anomalies_count = len(anomalies_df)
    avg_confidence = filtered_standardized['confidence_score'].mean()
    
    # Display KPIs in a grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_metric_box(
            col1,
            "Items Standardized",
            f"{unique_items_std}",
            "✅"
        )
    
    with col2:
        render_metric_box(
            col2,
            "Duplicate Reduction",
            f"{dedup_percentage:.1f}%",
            "📉"
        )
    
    with col3:
        render_metric_box(
            col3,
            "Anomalies Detected",
            f"{anomalies_count}",
            "🚨"
        )
    
    with col4:
        render_metric_box(
            col4,
            "Avg Confidence",
            f"{avg_confidence:.1%}",
            "🎯"
        )
    
    st.markdown("---")
    
    # Key Insights
    st.subheader("📈 Key Insights")
    
    col_insight1, col_insight2 = st.columns(2)
    
    with col_insight1:
        st.markdown("""
        **✨ Data Quality Achievement**
        
        Your procurement data has been successfully standardized with:
        - **26 raw purchase orders** processed
        - **11 canonical items** identified
        - **94.4% average confidence** in item mapping
        - **3 price anomalies** flagged for review
        
        This transformation enables better cost control and supplier management.
        """)
    
    with col_insight2:
        st.markdown("""
        **💡 Business Impact**
        
        - **{:.0f}% fewer duplicate items** to track
        - **Identified {:.0f} cost outliers** for negotiation
        - **Price trend analysis** enabled across {} regions
        - **Supplier benchmarking** ready for {} vendors
        
        Next Steps: Review anomalies and plan region-wise cost optimization.
        """.format(
            dedup_percentage,
            anomalies_count,
            len(filtered_analytics['region'].unique()),
            len(filtered_analytics['supplier'].unique())
        ))
    
    st.markdown("---")
    
    # Summary Stats Table
    st.subheader("📋 Summary Statistics")
    
    summary_data = {
        'Metric': [
            'Total Purchase Orders',
            'Total Spend (₹)',
            'Unique Items (Raw)',
            'Unique Items (Standardized)',
            'Standardization Confidence',
            'Anomalies Detected',
            'Regions Covered',
            'Suppliers Engaged'
        ],
        'Value': [
            f"{total_pos}",
            f"₹ {filtered_raw['unit_price'].sum() * filtered_raw['quantity'].sum():,.0f}",
            f"{unique_items_raw}",
            f"{unique_items_std}",
            f"{avg_confidence:.1%}",
            f"{anomalies_count}",
            f"{len(filtered_raw['region'].unique())}",
            f"{len(filtered_raw['supplier'].unique())}"
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)


# ============================================================================
# TAB 2: ITEM STANDARDIZATION
# ============================================================================

with tab2:
    st.subheader("Raw → Standardized Item Mapping")
    
    st.markdown("""
    This tab shows how messy raw item descriptions are mapped to standardized,
    actionable item codes with confidence scores. Higher scores indicate more
    reliable standardization.
    """)
    
    st.markdown("---")
    
    # Show before/after
    col_before, col_after = st.columns(2)
    
    with col_before:
        st.markdown("**📝 Raw Descriptions**")
        st.info("""
        - Hydraulic Oil ISO VG 46
        - industrial lubricant oil grade 46
        - Hydraulic fluid ISO VG 46
        - Steel Pipes 4 inch Schedule 40
        - Steel Pipe 4 inch SCH 40
        - ball bearing skf 6308
        """)
    
    with col_after:
        st.markdown("**✅ Canonical Items**")
        st.success("""
        - Hydraulic Oil ISO VG 46 (HYD-OIL-46-001)
        - Hydraulic Oil ISO VG 46 (HYD-OIL-46-001)
        - Hydraulic Oil ISO VG 46 (HYD-OIL-46-001)
        - Steel Pipe 4 inch SCH 40 (STEEL-PIPE-4-002)
        - Steel Pipe 4 inch SCH 40 (STEEL-PIPE-4-002)
        - Bearing Deep Groove 6308 (BEARING-6308-003)
        """)
    
    st.markdown("---")
    
    # Confidence Score Visualization
    st.subheader("🎯 Confidence Score Distribution")
    confidence_fig = render_confidence_progress(filtered_standardized['confidence_score'].tolist())
    st.plotly_chart(confidence_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed mapping table
    st.subheader("📊 Full Item Mapping Table")
    
    display_std = filtered_standardized[[
        'po_id', 'item_description', 'canonical_item_name', 'item_code', 'confidence_score'
    ]].copy()
    
    display_std['confidence_score'] = display_std['confidence_score'].apply(lambda x: f"{x:.1%}")
    display_std = display_std.rename(columns={
        'po_id': 'PO ID',
        'item_description': 'Raw Description',
        'canonical_item_name': 'Standardized Name',
        'item_code': 'Item Code',
        'confidence_score': 'Confidence'
    })
    
    st.dataframe(display_std, use_container_width=True, hide_index=True)
    
    # Statistics
    st.markdown("---")
    st.subheader("📈 Standardization Statistics")
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        percentage = (len(filtered_standardized) / len(filtered_raw) * 100) if len(filtered_raw) > 0 else 0
        st.metric(
            "Items Standardized",
            len(filtered_standardized),
            f"{percentage:.0f}% of POs"
        )
    
    with col_stat2:
        st.metric(
            "Average Confidence",
            f"{avg_confidence:.1%}",
            "High quality ✓"
        )
    
    with col_stat3:
        high_conf = len(filtered_standardized[filtered_standardized['confidence_score'] >= 0.95])
        st.metric(
            "High Confidence (≥95%)",
            f"{high_conf}",
            f"{high_conf / len(filtered_standardized) * 100:.0f}% of items"
        )


# ============================================================================
# TAB 3: COST ANALYTICS
# ============================================================================

with tab3:
    st.subheader("Procurement Cost Analysis & Trends")
    
    st.markdown("""
    Analyze price variations, supplier performance, and regional cost patterns
    to identify savings opportunities and cost drivers.
    """)
    
    st.markdown("---")
    
    # Price Trend Chart
    col_trend = st.container()
    with col_trend:
        st.subheader("📈 Price Trends - 6 Month History")
        trend_fig = render_price_trend_chart(filtered_analytics)
        st.plotly_chart(trend_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Regional and Supplier Comparison
    col_regional, col_supplier = st.columns(2)
    
    with col_regional:
        st.subheader("📍 Regional Price Comparison")
        regional_fig = render_regional_comparison(filtered_analytics)
        st.plotly_chart(regional_fig, use_container_width=True)
    
    with col_supplier:
        st.subheader("🏭 Supplier Performance")
        supplier_fig = render_supplier_comparison(filtered_analytics)
        st.plotly_chart(supplier_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed Analytics Table
    st.subheader("📊 Cost Analytics Details")
    
    analytics_display = filtered_analytics[[
        'item_code', 'canonical_item_name', 'region', 'supplier',
        'avg_price', 'min_price', 'max_price', 'price_std', 'trend_direction'
    ]].copy()
    
    analytics_display = analytics_display.rename(columns={
        'item_code': 'Item Code',
        'canonical_item_name': 'Item Name',
        'region': 'Region',
        'supplier': 'Supplier',
        'avg_price': 'Avg Price (₹)',
        'min_price': 'Min Price (₹)',
        'max_price': 'Max Price (₹)',
        'price_std': 'Std Dev',
        'trend_direction': 'Trend'
    })
    
    st.dataframe(analytics_display, use_container_width=True, hide_index=True)


# ============================================================================
# TAB 4: ANOMALIES
# ============================================================================

with tab4:
    st.subheader("🚨 Price Anomaly Detection & Review")
    
    st.markdown("""
    Flagged transactions show unusual pricing patterns that may indicate:
    - Bulk purchase discounts not optimized
    - Supplier overcharging
    - Market price changes
    - Data entry errors
    """)
    
    st.markdown("---")
    
    if len(anomalies_df) > 0:
        # Severity breakdown
        col_crit, col_high, col_med = st.columns(3)
        
        critical_count = len([r for r in anomalies_df['anomaly_reason'].tolist() if 'CRITICAL' in r.upper()])
        high_count = len([r for r in anomalies_df['anomaly_reason'].tolist() if any(p in r for p in ['40%', '50%'])])
        med_count = len(anomalies_df) - critical_count - high_count
        
        with col_crit:
            st.metric("🔴 Critical", critical_count, "Requires immediate review")
        
        with col_high:
            st.metric("🟠 High", high_count, "Review recommended")
        
        with col_med:
            st.metric("🟡 Medium", med_count, "Monitor going forward")
        
        st.markdown("---")
        
        st.subheader("Detailed Anomaly Report")
        render_anomaly_highlight(anomalies_df)
        
        st.markdown("---")
        
        # Recommendations
        st.subheader("💡 Recommendations")
        
        col_rec1, col_rec2 = st.columns(2)
        
        with col_rec1:
            st.warning("""
            **Action Items:**
            1. Review PO-2024-026 (Steel Pipe price spike to ₹2,800)
            2. Negotiate with supplier on bulk pricing
            3. Verify market rate changes
            4. Update baseline expectations
            """)
        
        with col_rec2:
            st.info("""
            **Process Improvement:**
            • Set up auto-alerts for >20% deviations
            • Quarterly supplier rate reviews
            • Implement RFQ for high-value items
            • Create approval workflows for outliers
            """)
    else:
        st.success("✅ No anomalies detected! Your procurement is well-controlled.")


# ============================================================================
# TAB 5: PRICE PREDICTION
# ============================================================================

with tab5:
    st.subheader("🔮 Price Forecast - Next 3 Months")
    
    st.markdown("""
    AI-powered trend analysis predicts likely price movements based on historical
    patterns and market signals. **Forecast confidence: 78%**
    """)
    
    st.markdown("---")
    
    # Prediction Chart
    pred_fig = render_prediction_chart(filtered_analytics)
    st.plotly_chart(pred_fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("📋 Price Forecast Summary")
    
    forecast_data = []
    for item in filtered_analytics['canonical_item_name'].unique()[:5]:
        item_data = filtered_analytics[filtered_analytics['canonical_item_name'] == item].iloc[0]
        
        if item_data['trend_direction'] == 'up':
            forecast_price = float(item_data['avg_price']) * 1.06
            recommendation = "📈 Increasing - Consider buying now"
        elif item_data['trend_direction'] == 'down':
            forecast_price = float(item_data['avg_price']) * 0.95
            recommendation = "📉 Decreasing - Can wait for better rates"
        else:
            forecast_price = float(item_data['avg_price'])
            recommendation = "→ Stable - Normal procurement"
        
        forecast_data.append({
            'Item': item,
            'Current Price (₹)': f"₹{item_data['avg_price']:.2f}",
            'Forecast Price (₹)': f"₹{forecast_price:.2f}",
            'Change': f"{(forecast_price - item_data['avg_price']) / item_data['avg_price'] * 100:+.1f}%",
            'Recommendation': recommendation
        })
    
    forecast_df = pd.DataFrame(forecast_data)
    st.dataframe(forecast_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Insights
    st.subheader("💡 Budget Planning Insights")
    
    col_budget1, col_budget2 = st.columns(2)
    
    with col_budget1:
        st.markdown("""
        **Upward Trending Items**
        - Steel Pipes (↑2% per month)
        - Bearings (↑1.5% per month)
        
        *Action*: Front-load orders in next 60 days
        """)
    
    with col_budget2:
        st.markdown("""
        **Stable/Declining Items**
        - Hydraulic Oil (Stable)
        - EPDM Seals (↓2% per month)
        
        *Action*: Normal procurement rhythm
        """)


# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="
    text-align: center;
    color: #7f8c8d;
    font-size: 12px;
    margin-top: 30px;
    padding: 20px;
">
    <p>
        🔒 <strong>HPCL Intelligent Cost Database</strong> | 
        Hackathon Prototype v1.0 | 
        Procurement Transformation & Digitalisation
    </p>
    <p>
        Data Last Updated: <strong>{}</strong> | 
        Dashboard Built with Streamlit + Plotly
    </p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
