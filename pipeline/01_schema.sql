-- Synthetic surgical registry relational schema.
-- This schema is for a simulated reporting workflow and contains no real patient data.

create table participants (
    participant_id varchar(16) primary key,
    cohort varchar(32) not null,
    age_band varchar(16) not null,
    enrolled_on date not null
);

create table procedures (
    procedure_id varchar(16) primary key,
    participant_id varchar(16) not null references participants(participant_id),
    cohort varchar(32) not null,
    procedure_on date not null,
    procedure_type varchar(64) not null
);

create table breast_module (
    procedure_id varchar(16) primary key references procedures(procedure_id),
    intent varchar(32) not null,
    laterality varchar(16) not null,
    implant_used boolean not null
);

create table nerve_module (
    procedure_id varchar(16) primary key references procedures(procedure_id),
    injury_level varchar(32) not null,
    technique varchar(32) not null,
    target_function varchar(48) not null
);

create table wound_module (
    procedure_id varchar(16) primary key references procedures(procedure_id),
    region varchar(32) not null,
    coverage varchar(32) not null,
    defect_size varchar(16) not null
);

create table followups (
    followup_id varchar(20) primary key,
    participant_id varchar(16) not null references participants(participant_id),
    day_target integer not null,
    due_on date not null,
    status varchar(16) not null,
    visit_on date,
    function_score integer,
    constraint followups_day_target_chk check (day_target in (30, 90, 180, 365)),
    constraint followups_status_chk check (status in ('completed', 'missed', 'pending'))
);

create table adverse_events (
    event_id varchar(20) primary key,
    procedure_id varchar(16) not null references procedures(procedure_id),
    event_on date not null,
    term varchar(64) not null,
    severity varchar(16) not null,
    serious boolean not null,
    notified_on date
);

create table challenge_queries (
    query_id varchar(20) primary key,
    participant_id varchar(16) not null references participants(participant_id),
    rule_id varchar(48) not null,
    query_status varchar(16) not null,
    created_on date not null
);
