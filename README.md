# Synthetic Surgical Registry Power BI Dashboard

Professional Power BI dashboard for a simulated surgical registry. The report is designed for operational monitoring, follow-up tracking, adverse event review, and data quality oversight across three registry modules.

![Dashboard preview](assets/dashboard-preview.png)

## Project Overview

This project presents a structured registry dashboard built in Power BI Project format (`.pbip`). It uses simulated data only and does not contain real patient records, MIMIC-IV data, or restricted clinical source data.

The dashboard is organized into two report pages:

- **Registry Operations**: participant volume, follow-up completion, planned visits, event records, module distribution, and visit-window performance.
- **Data Quality & Review Queue**: challenge queries, missing-cell checks, serious event flags, field completeness, review status, and rule-level quality signals.

## Repository Structure

```text
.
├── assets/
│   └── dashboard-preview.png
├── docs/
│   ├── OPEN_POWERBI_FIRST.txt
│   ├── PROJECT4_POWERBI_HANDOFF_legacy.md
│   └── dashboard-preview.html
└── powerbi/
    ├── Project4_Final_Dashboard.pbip
    ├── Project4_Final_Dashboard.Report/
    └── Project4_Final_Dashboard.SemanticModel/
```

## How To Open

1. Open `powerbi/Project4_Final_Dashboard.pbip` in Power BI Desktop.
2. If Power BI asks to apply project changes, choose **Apply**.
3. If Power BI shows a data warning, use **Home > Refresh**.
4. Review both pages: **Registry Operations** and **Data Quality & Review Queue**.

## Dashboard Scope

The dashboard supports:

- high-level registry performance review;
- follow-up completion monitoring;
- adverse event and serious event tracking;
- challenge-query monitoring;
- missingness and field-completeness review;
- presentation-ready registry reporting.

## Data Summary

- 300 simulated participant records
- 3 registry modules
- 1,200 planned follow-up visits
- 1,012 completed follow-up visits
- 52 event records
- 5 serious event flags
- 30 challenge queries

## Notes

This is a review-ready analytics project using synthetic registry data. It is suitable for portfolio review, dashboard design review, and workflow discussion, but not for clinical inference.
