# Data Dictionary

The dashboard uses processed summary tables exported by `pipeline/build_registry_dataset.py`.

## `cohort_counts`

| Field | Description |
| --- | --- |
| `cohort` | Registry module: breast, nerve, or wound. |
| `participant_count` | Number of simulated participants in the module. |

## `followup_by_cohort`

| Field | Description |
| --- | --- |
| `cohort` | Registry module. |
| `day_target` | Scheduled follow-up window in days. |
| `planned` | Planned follow-up visits. |
| `completed` | Completed follow-up visits. |
| `missed` | Planned visits not completed. |

## `ae_by_cohort`

| Field | Description |
| --- | --- |
| `cohort` | Registry module. |
| `event_count` | Adverse event records. |
| `serious_count` | Serious event flags. |
| `unnotified_serious_count` | Serious events without notification. |

## `challenge_queries_by_rule`

| Field | Description |
| --- | --- |
| `rule_id` | Data quality rule identifier. |
| `query_count` | Number of records flagged by the rule. |

## `field_completeness`

| Field | Description |
| --- | --- |
| `table_name` | Source table name. |
| `field_name` | Field evaluated for completeness. |
| `nonmissing` | Count of populated values. |
| `rows` | Total rows assessed. |
| `missing` | Count of missing values. |
