-- Reusable validation checks for the synthetic surgical registry.
-- These queries are written to be portable across common SQL engines with minor date-function adjustments.

-- 1. Follow-up completion by scheduled visit window.
select
    p.cohort,
    f.day_target,
    count(*) as planned,
    sum(case when f.status = 'completed' then 1 else 0 end) as completed,
    sum(case when f.status <> 'completed' then 1 else 0 end) as missed
from followups f
join participants p
    on p.participant_id = f.participant_id
group by
    p.cohort,
    f.day_target
order by
    p.cohort,
    f.day_target;

-- 2. Serious events without notification.
select
    p.cohort,
    count(*) as serious_events,
    sum(case when ae.notified_on is null then 1 else 0 end) as unnotified_serious_events
from adverse_events ae
join procedures pr
    on pr.procedure_id = ae.procedure_id
join participants p
    on p.participant_id = pr.participant_id
where ae.serious = true
group by
    p.cohort;

-- 3. Module consistency between procedure cohort and module table.
select
    pr.procedure_id,
    pr.cohort,
    case
        when pr.cohort = 'breast' and bm.procedure_id is null then 'MODULE_MISSING'
        when pr.cohort = 'nerve' and nm.procedure_id is null then 'MODULE_MISSING'
        when pr.cohort = 'wound' and wm.procedure_id is null then 'MODULE_MISSING'
        else 'OK'
    end as module_check
from procedures pr
left join breast_module bm
    on bm.procedure_id = pr.procedure_id
left join nerve_module nm
    on nm.procedure_id = pr.procedure_id
left join wound_module wm
    on wm.procedure_id = pr.procedure_id;

-- 4. Follow-up records with missing visit detail after completion.
select
    followup_id,
    participant_id,
    day_target,
    status,
    visit_on,
    function_score
from followups
where status = 'completed'
  and (visit_on is null or function_score is null);

-- 5. Dashboard query counts by rule.
select
    rule_id,
    count(*) as query_count
from challenge_queries
group by
    rule_id
order by
    rule_id;
