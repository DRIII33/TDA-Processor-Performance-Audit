Below is a **clean, GitHub-ready Markdown version** of your file.
All LaTeX-style text has been normalized so it **renders correctly in GitHub Markdown** (inline math uses backticks or plain text where appropriate, and block equations are converted to readable Markdown formulas).

---

```markdown
# TDA Processor Performance and Drawdown Efficiency Audit  
## Business Context

The Texas Department of Agriculture (TDA) Food & Nutrition (F&N) Division administers the USDA Foods program, which includes the critical **Further Processing (FP)** component. This program relies on third-party food processors to convert USDA bulk commodities (e.g., bulk chicken, ground beef) into end-products (e.g., chicken patties, beef crumbles) for Contracting Entities (CEs) such as schools.

The success of the TDA F&N Division depends on the efficient and compliant flow of these commodities. This project enhances the data analyst’s ability to audit the performance of external processors.

---

## Business Problem: Processor Bottleneck and Performance Risk

The Data Analyst role requires routine analysis of **Processor Monthly Performance Reports (MPRs)** to ensure compliance. However, simply checking reported inventory balances is insufficient for effective supply chain oversight.

The core issue is the **inefficient utilization of bulk inventory by processors**, creating two interconnected risks:

### 1. Contract Non-Compliance

Processors operate under a **State Participation Agreement** that defines performance expectations, including drawdown rates and inventory management standards. Sustained processing below contractual targets constitutes a breach of performance requirements, triggering TDA intervention and potential corrective action.

### 2. Supply Chain Bottleneck and Risk of Spoilage

When a processor holds large quantities of bulk inventory for extended periods:

- **Supply bottlenecks occur**  
  Allocated inventory is effectively removed from statewide availability, limiting TDA’s ability to reallocate commodities to other CEs.

- **Spoilage and loss risk increases**  
  Extended storage increases the likelihood of quality degradation, expiration beyond best-by dates, or physical damage—resulting in wasted federal resources.

For audit purposes, **excessive duration** is defined as holding inventory for **90 days or more**, signaling a failure in fulfillment or production scheduling.

---

## Solution: Drawdown Performance Index (DPI)

To move beyond static compliance checks, this project introduces the **Drawdown Performance Index (DPI)**—a composite metric that quantifies processor efficiency and compliance risk.

The DPI incorporates both:
- Monthly processing performance
- Length of time inventory is held

---

## DPI Calculation Formula

**Drawdown Performance Index (DPI):**

```

DPI = (LBS Processed MTD / Target LBS MTD) × (1 / Compliance Multiplier)

```

---

## Component Definitions

| Component | Description | Calculation / Logic |
|--------|-------------|-------------------|
| **LBS Processed MTD** | Pounds of bulk commodity processed month-to-date (from MPR). | Raw reported value |
| **Target LBS MTD** | Contractual monthly processing target. | Allocation LBS ÷ 12 (or contract term) |
| **Compliance Multiplier** | Penalty applied for excessive inventory holding time. | If Days Held ≥ 90 → 1.5 |
| | | Else → 1.0 |

---

## DPI Interpretation and Required Action

The DPI provides a clear, data-driven trigger for TDA analysts to initiate technical assistance or enforcement actions.

| DPI Value | Compliance Multiplier | Interpretation | Required TDA Action |
|--------|----------------------|----------------|--------------------|
| ≥ 1.0 | 1.0 | Highly efficient and compliant. Meeting or exceeding targets with acceptable holding time. | **PERFORMING** |
| 0.75 ≤ DPI < 1.0 | 1.0 | Acceptable but below target processing rate. | **WATCHLIST: SLOW DRAWDOWN** |
| < 0.75 | 1.0 or 1.5 | **Low performance failure.** Severe under-processing, with holding-time penalty if applicable. | **LOW DPI: IMMEDIATE AUDIT** |
| Any value | 1.5 | **High hold risk.** Inventory held 90 days or more regardless of recent activity. | **HIGH HOLD RISK: AGREEMENT REVIEW** |

---

## Strategic Impact

By implementing the DPI, TDA F&N transforms its MPR review process from a passive compliance check into an **active, risk-segmented audit framework**, ensuring efficient utilization of USDA Foods and proactive mitigation of processor performance risks statewide.
```

---

