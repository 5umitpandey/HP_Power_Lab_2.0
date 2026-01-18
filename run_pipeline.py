"""
Master Pipeline Script
Runs the complete data processing pipeline:
1. Item Standardization (AI/ML)
2. Cost Analytics Generation
3. Anomaly Detection

This script should be run whenever new purchase order data is added.
"""

import os
import sys
from pathlib import Path

# Suppress TensorFlow warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

print("=" * 70)
print("HPCL INTELLIGENT COST DATABASE - DATA PROCESSING PIPELINE")
print("=" * 70)

# Step 1: Item Standardization
print("\n[STEP 1/3] Running Item Standardization...")
print("-" * 70)
try:
    # Change to project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Import and run standardization
    sys.path.insert(0, str(project_root / "ai_standardization"))
    from ai_standardization.run_standardization import main as run_standardization
    run_standardization()
except Exception as e:
    print(f"Error in standardization: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 2: Cost Analytics
print("\n[STEP 2/3] Running Cost Analytics Generation...")
print("-" * 70)
try:
    sys.path.insert(0, str(project_root / "ai_analytics"))
    from ai_analytics.run_analytics import main as run_analytics_full
    run_analytics_full()
except Exception as e:
    print(f"Error in analytics: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("PIPELINE COMPLETED SUCCESSFULLY!")
print("=" * 70)
print("\nGenerated files:")
print("  ✓ data/processed/standardized_items.csv")
print("  ✓ data/processed/cost_analytics.csv")
print("  ✓ data/processed/anomalies.csv")
print("\nData is now ready for the dashboard!")
print("=" * 70)
