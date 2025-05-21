You are a clinical data SQL expert.

Your job is to convert a Korean-language epidemiological question into a SQL query  
that follows the OMOP Common Data Model using MSSQL syntax.

- Return your response in the following format only:  
If SQL is successfully generated:  
`sql: <your_sql_query_here>`  

If the question cannot be answered:  
`error: <brief explanation>`  

---

```sql
CREATE TABLE [project].[person](
	[person_id] [varchar](8) NOT NULL,
	[gender_concept_id] [int] NULL,
	[year_of_birth] [int] NULL,
	[month_of_birth] [int] NULL,
	[day_of_birth] [int] NULL,
	[birth_datetime] [date] NOT NULL,
	[race_concept_id] [int] NULL,
	[ethnicity_concept_id] [int] NULL,
	[location_id] [int] NULL,
	[provider_id] [int] NULL,
	[care_site_id] [int] NULL,
	[person_source_value] [varchar](50) NULL,
	[gender_source_value] [varchar](50) NULL,
	[gender_source_concept_id] [int] NULL,
	[race_source_value] [varchar](50) NULL,
	[race_source_concept_id] [int] NULL,
	[ethnicity_source_value] [varchar](50) NULL,
	[ethnicity_source_concept_id] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[person_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
```

Example rows:
```sql
select * from person limit 3;
-- person_id | gender_concept_id | year_of_birth | race_concept_id | ethnicity_concept_id
-- 101       | 8507              | 1950          | 8527            | 38003563
-- 102       | 8532              | 1980          | 8515            | 38003564
-- 103       | 8506              | 2000          | 8657            | 38003565
```

---


```sql
CREATE TABLE [project].[condition_occurrence](
	[condition_occurrence_id] [int] NULL,
	[person_id] [varchar](8) NOT NULL,
	[condition_concept_id] [varchar](50) NULL,
	[condition_start_date] [date] NULL,
	[condition_start_datetime] [datetime] NULL,
	[condition_end_date] [date] NULL,
	[condition_end_datetime] [datetime] NULL,
	[condition_type_concept_id] [int] NOT NULL,
	[condition_status_concept_id] [varchar](50) NULL,
	[stop_reason] [varchar](50) NULL,
	[provider_id] [varchar](50) NULL,
	[visit_occurrence_id] [int] NULL,
	[visit_detail_id] [int] NULL,
	[condition_source_value] [varchar](50) NULL,
	[condition_source_concept_id] [int] NULL,
	[condition_status_source_value] [varchar](50) NULL
) ON [PRIMARY]

```

Example rows:
```sql
```

---

```sql
CREATE TABLE [project].[drug_exposure](
	[drug_exposure_id] [int] NULL,
	[person_id] [varchar](8) NULL,
	[drug_concept_id] [varchar](10) NULL,
	[drug_exposure_start_date] [date] NOT NULL,
	[drug_exposure_start_datetime] [datetime] NOT NULL,
	[drug_exposure_end_date] [date] NULL,
	[drug_exposure_end_datetime] [datetime] NULL,
	[verbatim_end_date] [date] NULL,
	[drug_type_concept_id] [int] NULL,
	[stop_reason] [text] NULL,
	[refills] [int] NULL,
	[quantity] [float] NULL,
	[days_supply] [int] NULL,
	[sig] [varchar](4000) NULL,
	[route_concept_id] [varchar](4) NULL,
	[lot_number] [text] NULL,
	[provider_id] [varchar](10) NULL,
	[visit_occurrence_id] [int] NULL,
	[visit_detail_id] [int] NULL,
	[drug_source_value] [varchar](10) NULL,
	[drug_source_concept_id] [varchar](10) NULL,
	[route_source_value] [varchar](4) NULL,
	[dose_unit_source_value] [varchar](5) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
```
Example rows:
```sql
```

---


```sql
CREATE TABLE [project].[measurement](
	[measurement_id] [int] NULL,
	[person_id] [varchar](8) NULL,
	[measurement_concept_id] [varchar](10) NULL,
	[measurement_date] [date] NOT NULL,
	[measurement_datetime] [date] NOT NULL,
	[measurement_time] [text] NULL,
	[measurement_type_concept_id] [int] NULL,
	[operator_concept_id] [int] NULL,
	[value_as_number] [varchar](50) NULL,
	[value_as_concept_id] [text] NULL,
	[unit_concept_id] [varchar](100) NULL,
	[range_low] [varchar](10) NULL,
	[range_high] [varchar](10) NULL,
	[provider_id] [varchar](10) NULL,
	[visit_occurrence_id] [int] NULL,
	[visit_detail_id] [int] NULL,
	[measurement_source_value] [varchar](10) NULL,
	[measurement_source_concept_id] [varchar](500) NULL,
	[unit_source_value] [varchar](100) NULL,
	[value_source_value] [varchar](50) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
```

Example rows:
```sql
```

---
```sql
CREATE TABLE [project].[visit_occurrence](
	[visit_occurrence_id] [int] NULL,
	[person_id] [varchar](8) NULL,
	[visit_concept_id] [int] NULL,
	[visit_start_date] [date] NULL,
	[visit_start_datetime] [datetime] NULL,
	[visit_end_date] [date] NULL,
	[visit_end_datetime] [datetime] NULL,
	[visit_type_concept_id] [int] NULL,
	[provider_id] [varchar](50) NULL,
	[care_site_id] [int] NULL,
	[visit_source_value] [varchar](50) NULL,
	[visit_source_concept_id] [int] NULL,
	[admitting_source_concept_id] [int] NULL,
	[admitting_source_value] [varchar](50) NULL,
	[discharge_to_concept_id] [int] NULL,
	[discharge_to_source_value] [varchar](50) NULL,
	[preceding_visit_occurrence_id] [text] NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
```

Example rows:
```sql
```

---

```sql
CREATE TABLE [project].[drug](
	[drug_exposure_id] [int] NULL,
	[person_id] [varchar](8) NULL,
	[drug_concept_id] [varchar](10) NULL,
	[drug_exposure_start_date] [varchar](10) NULL,
	[drug_exposure_start_datetime] [varchar](8) NULL,
	[drug_exposure_end_date] [varchar](10) NULL,
	[drug_exposure_end_datetime] [text] NULL,
	[verbatim_end_date] [text] NULL,
	[drug_type_concept_id] [int] NULL,
	[stop_reason] [text] NULL,
	[refills] [text] NULL,
	[quantity] [float] NULL,
	[days_supply] [int] NULL,
	[sig] [varchar](4000) NULL,
	[route_concept_id] [varchar](4) NULL,
	[lot_number] [text] NULL,
	[provider_id] [char](3) NULL,
	[visit_occurrence_id] [char](19) NULL,
	[visit_detail_id] [char](15) NULL,
	[drug_source_value] [varchar](10) NULL,
	[drug_source_concept_id] [varchar](10) NULL,
	[route_source_value] [varchar](4) NULL,
	[dose_unit_source_value] [varchar](5) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

```

Example rows:
```sql
```

---

Using valid MSSQL, answer the following questions for the tables provided above only.  
Return output in one of the following formats:

```text
sql : <sql query>
error : <brief explanation>
```  

Question : {text}