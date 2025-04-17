SELECT person_id, year_of_birth 
FROM person 
WHERE gender_concept_id = 8532 AND year_of_birth > 2010;

SELECT person_id, death_date, cause_concept_id 
FROM death;

SELECT person_id, condition_start_date 
FROM condition_occurrence 
WHERE condition_concept_id = 320128;

SELECT person_id, drug_exposure_start_date 
FROM drug_exposure 
WHERE drug_concept_id = 40170911;

SELECT person_id, measurement_date, value_as_number 
FROM measurement 
WHERE measurement_concept_id = 37003487 
  AND measurement_date BETWEEN '2020-01-01' AND '2020-12-31';

SELECT person_id, visit_start_date, visit_end_date 
FROM visit_occurrence 
WHERE DATE_PART('day', visit_end_date - visit_start_date) > 7;

SELECT person_id, procedure_date 
FROM procedure_occurrence 
WHERE procedure_date BETWEEN '2021-01-01' AND '2021-12-31';

SELECT person_id 
FROM observation_period 
WHERE DATE_PART('day', observation_period_end_date - observation_period_start_date) >= 365;

SELECT person_id 
FROM device_exposure 
WHERE device_exposure_end_date IS NULL;

SELECT care_site_id, COUNT(*) 
FROM visit_occurrence 
GROUP BY care_site_id;

SELECT person_id, race_concept_id 
FROM person 
WHERE race_concept_id IS NOT NULL;

SELECT * 
FROM drug_exposure 
WHERE visit_occurrence_id = 12345;

SELECT DISTINCT person_id 
FROM procedure_occurrence;

SELECT person_id, value_as_number 
FROM measurement 
WHERE value_as_number < range_low OR value_as_number > range_high;

SELECT * 
FROM condition_occurrence 
WHERE condition_status_concept_id IS NOT NULL;

SELECT person_id, COUNT(*) 
FROM drug_exposure 
GROUP BY person_id 
HAVING COUNT(*) > 1;

SELECT * 
FROM visit_occurrence 
WHERE visit_start_date BETWEEN '2022-01-01' AND '2022-01-31';

SELECT AVG(DATE_PART('day', visit_end_date - visit_start_date)) 
FROM visit_occurrence;

SELECT DISTINCT d.person_id 
FROM drug_exposure d 
JOIN procedure_occurrence p ON d.person_id = p.person_id;

SELECT person_id 
FROM measurement 
WHERE measurement_concept_id = 3004249;