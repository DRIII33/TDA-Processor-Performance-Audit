#INSTALL PACKAGES
!pip install pandas

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- Configuration ---
NUM_RECORDS = 150
REPORT_DATE = datetime(2025, 10, 31)
PROJECT_NAME = "TDA Processor Performance Audit"

# Define 20 synthetic processors and their bulk commodities
processors = {
    f'PROC_610{i:02}': {
        'products': {
            'US_CHICKEN_BR_BULK': {'allocation_min': 100000, 'allocation_max': 200000},
            'US_BEEF_GR_BULK': {'allocation_min': 80000, 'allocation_max': 150000},
            'US_CHEESE_BULK': {'allocation_min': 50000, 'allocation_max': 120000}
        }
    }
    for i in range(1, 21)
}

# Commodity Names
commodity_names = {
    'US_CHICKEN_BR_BULK': 'Bulk Chicken Breast',
    'US_BEEF_GR_BULK': 'Bulk Ground Beef',
    'US_CHEESE_BULK': 'Bulk Cheddar Cheese'
}

# --- Data Generation Function ---
def generate_processor_data(processors, report_date, num_records):
    """Generates synthetic processor MPR data."""
    data = []

    # Track the agreement ID to ensure unique assignment per product/processor
    agreement_counter = 1000

    # Iterate to create records
    for i in range(num_records):
        proc_id = random.choice(list(processors.keys()))
        product_id = random.choice(list(processors[proc_id]['products'].keys()))

        # 1. Determine Allocation (fixed per agreement/product)
        alloc_range = processors[proc_id]['products'][product_id]
        allocation_lbs = random.randint(alloc_range['allocation_min'], alloc_range['allocation_max'])

        # 2. Determine Monthly Target (based on a typical 12-month agreement)
        target_lbs_mtd = round(allocation_lbs / 12, 2)

        # 3. Determine LBS Processed MTD (Introduce risk/underperformance)
        # 20% chance of high performance (1.0 to 1.3x target)
        # 60% chance of typical/low performance (0.5 to 1.0x target)
        # 20% chance of very poor performance (0.1 to 0.5x target)

        rand_performance = random.random()
        if rand_performance < 0.2:
            multiplier = random.uniform(1.0, 1.3)
        elif rand_performance < 0.8:
            multiplier = random.uniform(0.5, 1.0)
        else:
            multiplier = random.uniform(0.1, 0.5)

        lbs_processed_mtd = round(target_lbs_mtd * multiplier, 2)

        # 4. Determine Days Held Inventory (Introduce holding risk)
        # 20% chance of > 90 days (high compliance risk)
        # 80% chance of < 90 days (low/normal risk)

        rand_hold = random.random()
        if rand_hold < 0.2:
            # High-risk holding time (90 to 150 days)
            days_held = random.randint(90, 150)
        else:
            # Low-risk holding time (30 to 89 days)
            days_held = random.randint(30, 89)

        # 5. Calculate Current Inventory (simulated, starting high)
        # A simple model: start with high inventory and subtract MTD processed.
        # This simplifies the complex WBSCM logic for portfolio demo.
        initial_inventory = allocation_lbs / 2 # Assume they've drawn down half their allocation
        bulk_inventory_lbs = round(initial_inventory - (i * 10) - lbs_processed_mtd, 2) # Simulate monthly usage

        # Ensure inventory is not negative
        bulk_inventory_lbs = max(500.0, bulk_inventory_lbs)

        data.append({
            'Report_ID': f'{proc_id}_{report_date.strftime("%Y%m")}_{i:03}',
            'Processor_ID': proc_id,
            'Agreement_ID': f'AGR_2025_{agreement_counter}',
            'Product_ID': product_id,
            'Product_Name': commodity_names[product_id],
            'Report_Date': report_date.strftime('%Y-%m-%d'),
            'Bulk_Inventory_LBS': bulk_inventory_lbs,
            'LBS_Processed_MTD': lbs_processed_mtd,
            'Allocation_LBS': allocation_lbs,
            'Target_LBS_MTD': target_lbs_mtd,
            'Days_Held_Inventory': days_held
        })
        agreement_counter += 1

    return pd.DataFrame(data)

# --- Execution ---
df_processor = generate_processor_data(processors, REPORT_DATE, NUM_RECORDS)

# Save to CSV
FILE_NAME = "Processor_Performance_Synthetic_Data.csv"
df_processor.to_csv(FILE_NAME, index=False)

print(f"Synthetic data generated and saved to {FILE_NAME} ({len(df_processor)} records).")

# Display first few rows and summary
print("\nDataFrame Head:")
print(df_processor.head().to_markdown(index=False, numalign="left", stralign="left"))
print("\nDataFrame Info:")
df_processor.info()
