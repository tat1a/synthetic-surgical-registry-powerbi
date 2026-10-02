# Project 4 Power BI Handoff

## Current deliverable

Project: Synthetic Surgical Registry Power BI report

Latest package:

- Final review package: `Project4_PowerBI_FINAL_OpenMe_2026-10-02.zip`
- Final working folder: `C:\Users\Tati\Desktop\Project4_PowerBI_FINAL_OpenMe`
- Power BI entry file: `C:\Users\Tati\Desktop\Project4_PowerBI_FINAL_OpenMe\Synthetic_Surgical_Registry.pbip`
- The final package uses `model.bim` / TMSL format for better Power BI Desktop compatibility.

## Scope

This report uses a simulated registry dataset for presentation and workflow review. It contains no real patients, no MIMIC data, and no restricted source data. It is separate from the MIMIC-IV research roadmap.

## Report pages

1. `Registry Operations`
   - Participants by module
   - Follow-up completion by scheduled visit day
   - Operational KPI cards

2. `Data Quality & Queries`
   - Challenge queries by rule
   - Field completeness table
   - Serious event flags and query KPI cards

## Data summary

- 300 simulated participant records.
- Three synthetic modules/cohorts: breast, nerve, wound.
- 1,200 planned follow-up visits across 30, 90, 180, and 365 day targets.
- 1,012 completed follow-up visits.
- 52 adverse event records.
- 5 serious event flags.
- 188 missing follow-up-related cells in the field-completeness audit.
- 30 challenge queries across six quality rules.

## Current status

Technical checks completed locally:

- Power BI project JSON files parse successfully.
- Required schema metadata is present in the `.pbip`, `.pbir`, and `.pbism` entry files.
- The previous invalid `dataType: text` issue is no longer present.
- Base theme resources are registered in `report.json`, which resolves the earlier report-load failure.
- No Git repository is initialized in this local Project 4 folder.

## Opening checklist

1. Open `C:\Users\Tati\Desktop\Project4_PowerBI_FINAL_OpenMe\Synthetic_Surgical_Registry.pbip`.
2. If Power BI Desktop asks to apply project changes, apply them.
3. If Power BI shows the banner `Some of the tables have incomplete or no data`, click `Refresh`.
4. If an error message appears, capture the full message before closing it.

## Hold before GitHub

Do not upload to GitHub until the full Power BI project is reviewed and explicitly approved.

