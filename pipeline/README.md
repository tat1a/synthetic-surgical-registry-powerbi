# Registry Data Pipeline

This folder documents the data preparation workflow behind the Power BI dashboard.

The workflow is intentionally reproducible and uses only simulated registry records. It does not use real patient data, MIMIC-IV data, or restricted clinical source data.

## Files

- `01_schema.sql`: relational schema for registry participants, procedures, module-specific records, follow-up visits, adverse events, and quality queries.
- `02_quality_checks.sql`: validation queries for follow-up completeness, module consistency, serious event notification, and field completeness.
- `build_registry_dataset.py`: deterministic Python pipeline that builds synthetic records and exports dashboard-ready summary tables.

## Outputs

Running the Python pipeline creates the following files in `data/processed/`:

- `cohort_counts.csv`
- `followup_by_cohort.csv`
- `ae_by_cohort.csv`
- `challenge_queries_by_rule.csv`
- `field_completeness.csv`

These tables match the reporting grain used in the Power BI dashboard.

## Run

```bash
python pipeline/build_registry_dataset.py
```
