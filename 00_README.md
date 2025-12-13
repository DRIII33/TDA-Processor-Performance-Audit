# TDA-Processor-Performance-Audit

## Project Title
TDA Processor Performance and Drawdown Efficiency Audit

## Project Goal
To develop a system for the Texas Department of Agriculture (TDA) Food & Nutrition (F&N) Division to proactively monitor and audit USDA Food Processor performance by calculating a Drawdown Performance Index (DPI). This system identifies processors who are inefficiently holding bulk commodity inventory for too long, creating supply chain bottlenecks and non-compliance risk, enabling TDA analysts to intervene with corrective actions.

## Business Problem Addressed
The TDA Data Analyst role requires monitoring Processor Monthly Performance Reports (MPR). The problem is that static inventory reports do not fully capture processing *efficiency* or *bottleneck risk*. A processor may be compliant with their agreement but still holding high volumes of bulk commodity inventory for an excessive duration, which impedes the overall supply chain and future commodity allocation.

## Framework
**CRISP-DM (Cross-Industry Standard Process for Data Mining)**

## Key Deliverables
1.  **Data Generation & Cleansing (Google Colab/Python):** Creation of a realistic synthetic dataset modeling 20 different processor agreements and their monthly processing metrics.
2.  **Data Preparation & Transformation (Google BigQuery/SQL):** Development of an optimized SQL view to calculate core audit metrics, including `Days_Held_Inventory` and the **Drawdown Performance Index (DPI)**.
3.  **Analysis & Reporting (Looker Studio/Executive Summary):** A two-page dashboard mockup to visualize processor risk, performance against target rates, and compliance flags for agreement review.

## Tools Used
* **Data Generation & Logic:** Python (Pandas, NumPy, random) in Google Colab
* **Data Storage & Transformation:** Google BigQuery (Standard SQL)
* **Visualization & Reporting:** Looker Studio (Mockup)
