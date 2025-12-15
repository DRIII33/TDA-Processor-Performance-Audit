#INSTALL PACKAGES
import pandas as pd
from google.colab import auth
from google.cloud import bigquery

# 05_Processor_Audit_Ranking.ipynb
# Purpose: Connects to the BigQuery Audit View, performs final risk segmentation,
#          and generates the prioritized 06_Audit_Action_List.csv for TDA analysts.

import pandas as pd
from google.colab import auth
from google.cloud import bigquery

# --- Configuration ---
PROJECT_ID = "driiiportfolio"
DATASET_ID = "tda_processor_data"
VIEW_ID = "processor_audit_view"
OUTPUT_FILE = "06_Audit_Action_List.csv"

# --- 1. Authenticate and Connect to BigQuery ---
print("Authenticating to Google Cloud...")
auth.authenticate_user()
client = bigquery.Client(project=PROJECT_ID)
print("Authentication successful.")

# --- 2. SQL Query to Fetch Prioritized Data ---
# Select all records flagged for TDA action, including the core metrics.
# ORDER BY: 
# 1. Audit Flag (Critical flags first, e.g., using a CASE statement or numeric code)
# 2. DPI (Lowest DPI first)
# 3. Bulk Inventory (Largest volume first)

sql_query = f"""
SELECT
    Processor_ID,
    Product_Name,
    Agreement_ID,
    Audit_Action_Flag,
    Drawdown_Performance_Index,
    Days_Held_Inventory,
    Bulk_Inventory_LBS,
    Target_LBS_MTD
FROM
    `{PROJECT_ID}.{DATASET_ID}.{VIEW_ID}`
WHERE
    -- Filter out records that are fully compliant (optional but speeds up triage list)
    Audit_Action_Flag != 'PERFORMING'
ORDER BY
    -- Prioritize the most severe flags first (RED > ORANGE > YELLOW)
    CASE Audit_Action_Flag
        WHEN 'LOW DPI: IMMEDIATE AUDIT' THEN 1
        WHEN 'HIGH HOLD RISK: AGREEMENT REVIEW' THEN 2
        WHEN 'WATCHLIST: SLOW DRAWDOWN' THEN 3
        ELSE 4
    END,
    Drawdown_Performance_Index ASC, -- Sort by worst performance (lowest DPI)
    Bulk_Inventory_LBS DESC          -- Break ties by largest volume at risk
"""

# --- 3. Run Query and Load into Pandas DataFrame ---
print(f"Fetching data from BigQuery view: {VIEW_ID}...")
df_audit = client.query(sql_query).to_dataframe()

print(f"Data fetched successfully. Total records for audit: {len(df_audit)}")

# --- 4. Python-Based Secondary Risk Segmentation (Example of Python Value-Add) ---
# Create a final prioritization rank based on combined factors
df_audit['Risk_Score_Combined'] = (
    (1 - df_audit['Drawdown_Performance_Index']) * 100 
    + (df_audit['Days_Held_Inventory'] / 90) * 50
)

df_audit = df_audit.sort_values(
    by=['Risk_Score_Combined', 'Bulk_Inventory_LBS'], 
    ascending=[False, False]
).reset_index(drop=True)

# Add a simple sequential TDA Action Priority column
df_audit.insert(0, 'TDA_Priority_Rank', range(1, 1 + len(df_audit)))


# --- 5. Generate the Final CSV Deliverable ---
# Select only the columns needed for the TDA analyst's audit list
df_audit_list = df_audit[[
    'TDA_Priority_Rank',
    'Audit_Action_Flag',
    'Processor_ID',
    'Product_Name',
    'Agreement_ID',
    'Bulk_Inventory_LBS',
    'Drawdown_Performance_Index',
    'Days_Held_Inventory'
]]

df_audit_list.to_csv(OUTPUT_FILE, index=False)

print(f"\nAudit Action List generated: {OUTPUT_FILE} ({len(df_audit_list)} records).")
print("\nFirst 5 prioritized audit items:")
print(df_audit_list.head().to_markdown(index=False, numalign="left", stralign="left"))
