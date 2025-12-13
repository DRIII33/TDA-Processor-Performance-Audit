-- Title: 03_SQL_Processor_Performance_View.sql
-- Description: Creates an analytical view to calculate the Drawdown Performance Index (DPI)
--              and flag compliance risks for Processor Performance Audits.
-- Framework: CRISP-DM (Data Preparation Stage)
-- BigQuery Project ID: driiiportfolio
-- Dataset: tda_processor_data
-- Source Table: processor_raw_data (Loaded from Processor_Performance_Synthetic_Data.csv)

CREATE OR REPLACE VIEW
  `driiiportfolio.tda_processor_data.processor_audit_view` AS
SELECT
  -- Primary Dimensions
  t1.Report_ID,
  t1.Processor_ID,
  t1.Agreement_ID,
  t1.Product_ID,
  t1.Product_Name,
  
  -- Core Metrics
  t1.Bulk_Inventory_LBS,
  t1.LBS_Processed_MTD,
  t1.Allocation_LBS,
  t1.Target_LBS_MTD,
  
  -- Compliance Metric 1: Inventory Hold Time
  t1.Days_Held_Inventory,
  
  -- Compliance Metric 2: Drawdown Rate
  -- Measures the processor's monthly efficiency against their contractual target
  SAFE_DIVIDE(t1.LBS_Processed_MTD, t1.Target_LBS_MTD) AS Drawdown_Rate_Index,
  
  -- Compliance Metric 3: Compliance Multiplier (Penalizes excessive holding time)
  CASE
    WHEN t1.Days_Held_Inventory >= 90 THEN 1.5 -- Severe penalty for holding > 90 days
    ELSE 1.0
  END AS Compliance_Multiplier,
  
  -- Compliance Metric 4: Drawdown Performance Index (DPI)
  -- The final, composite risk score: (Drawdown_Rate / Compliance_Multiplier)
  -- A low DPI indicates both slow processing AND long holding time.
  SAFE_DIVIDE(SAFE_DIVIDE(t1.LBS_Processed_MTD, t1.Target_LBS_MTD),
    CASE
      WHEN t1.Days_Held_Inventory >= 90 THEN 1.5
      ELSE 1.0
    END
  ) AS Drawdown_Performance_Index,
  
  -- Compliance Metric 5: Audit Flag (The primary output for TDA action)
  CASE
    WHEN SAFE_DIVIDE(SAFE_DIVIDE(t1.LBS_Processed_MTD, t1.Target_LBS_MTD),
      CASE
        WHEN t1.Days_Held_Inventory >= 90 THEN 1.5
        ELSE 1.0
      END
    ) < 0.75 THEN 'LOW DPI: IMMEDIATE AUDIT' -- Performance failure
    WHEN t1.Days_Held_Inventory >= 90 THEN 'HIGH HOLD RISK: AGREEMENT REVIEW' -- Time-based failure
    WHEN SAFE_DIVIDE(t1.LBS_Processed_MTD, t1.Target_LBS_MTD) < 1.0 THEN 'WATCHLIST: SLOW DRAWDOWN' -- Below target
    ELSE 'PERFORMING'
  END AS Audit_Action_Flag
  
FROM
  `driiiportfolio.tda_processor_data.processor_raw_data` AS t1

-- Optimization Note: Using SAFE_DIVIDE to prevent division by zero errors, ensuring robust query execution.
