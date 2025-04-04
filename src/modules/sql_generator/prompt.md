# OMOP CDM SQL Generator

다음은 OMOP CDM 스키마 정보입니다. 이 정보를 기반으로 사용자가 요청한 자연어 텍스트 `{text}`에 해당하는 SQL 쿼리를 생성하세요.
이전 응답은 모두 잊습니다.

## 테이블 정보

| 테이블명                  | 기본 키 (PK)              | 주요 외래 키 (FK)                                                                                                                                                                                           |
| ------------------------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **PERSON**                | `person_id`               | `gender_concept_id`, `race_concept_id`, `ethnicity_concept_id`, `location_id`, `provider_id`, `care_site_id`                                                                                                |
| **OBSERVATION_PERIOD**    | `observation_period_id`   | `person_id`, `period_type_concept_id`                                                                                                                                                                       |
| **VISIT_OCCURRENCE**      | `visit_occurrence_id`     | `person_id`, `visit_concept_id`, `provider_id`, `care_site_id`, `visit_type_concept_id`, `admitted_from_concept_id`, `discharge_to_concept_id`, `preceding_visit_occurrence_id`                             |
| **VISIT_DETAIL**          | `visit_detail_id`         | `person_id`, `visit_occurrence_id`, `provider_id`, `care_site_id`, `visit_detail_concept_id`, `admitted_from_concept_id`, `discharged_to_concept_id`, `preceding_visit_detail_id`, `parent_visit_detail_id` |
| **CONDITION_OCCURRENCE**  | `condition_occurrence_id` | `person_id`, `condition_concept_id`, `condition_type_concept_id`, `condition_status_concept_id`, `provider_id`, `visit_occurrence_id`, `visit_detail_id`                                                    |
| **DRUG_EXPOSURE**         | `drug_exposure_id`        | `person_id`, `drug_concept_id`, `drug_type_concept_id`, `provider_id`, `visit_occurrence_id`, `visit_detail_id`                                                                                             |
| **PROCEDURE_OCCURRENCE**  | `procedure_occurrence_id` | `person_id`, `procedure_concept_id`, `procedure_type_concept_id`, `provider_id`, `visit_occurrence_id`, `visit_detail_id`                                                                                   |
| **DEVICE_EXPOSURE**       | `device_exposure_id`      | `person_id`, `device_concept_id`, `device_type_concept_id`, `provider_id`, `visit_occurrence_id`, `visit_detail_id`                                                                                         |
| **MEASUREMENT**           | `measurement_id`          | `person_id`, `measurement_concept_id`, `measurement_type_concept_id`, `unit_concept_id`, `provider_id`, `visit_occurrence_id`, `visit_detail_id`                                                            |
| **OBSERVATION**           | `observation_id`          | `person_id`, `observation_concept_id`, `observation_type_concept_id`, `provider_id`, `visit_occurrence_id`, `visit_detail_id`                                                                               |
| **DEATH**                 | `person_id`               | `death_type_concept_id`, `cause_concept_id`                                                                                                                                                                 |
| **NOTE**                  | `note_id`                 | `person_id`, `note_type_concept_id`, `note_class_concept_id`, `provider_id`, `visit_occurrence_id`, `visit_detail_id`                                                                                       |
| **SPECIMEN**              | `specimen_id`             | `person_id`, `specimen_concept_id`, `unit_concept_id`, `anatomic_site_concept_id`, `disease_status_concept_id`                                                                                              |
| **COST**                  | `cost_id`                 | `cost_type_concept_id`, `currency_concept_id`, `drug_concept_id`                                                                                                                                            |
| **PAYER_PLAN_PERIOD**     | `payer_plan_period_id`    | `person_id`                                                                                                                                                                                                 |
| **DRUG_ERA**              | `drug_era_id`             | `person_id`, `drug_concept_id`                                                                                                                                                                              |
| **CONDITION_ERA**         | `condition_era_id`        | `person_id`, `condition_concept_id`                                                                                                                                                                         |
| **EPISODE**               | `episode_id`              | `person_id`, `episode_concept_id`, `episode_object_concept_id`, `episode_type_concept_id`                                                                                                                   |
| **DOSE_ERA**              | `dose_era_id`             | `person_id`, `drug_concept_id`, `unit_concept_id`                                                                                                                                                           |
| **CDM_SOURCE**            | 없음                      | `cdm_version_concept_id`                                                                                                                                                                                    |
| **CARE_SITE**             | `care_site_id`            | `place_of_service_concept_id`, `location_id`                                                                                                                                                                |
| **LOCATION**              | `location_id`             | `country_concept_id`                                                                                                                                                                                        |
| **PROVIDER**              | `provider_id`             | `care_site_id`, `specialty_concept_id`, `gender_concept_id`                                                                                                                                                 |
| **FACT_RELATIONSHIP**     | 없음                      | `domain_concept_id_1`, `fact_id_1`, `domain_concept_id_2`, `fact_id_2`, `relationship_id`                                                                                                                   |
| **RELATIONSHIP**          | `relationship_id`         | `relationship_concept_id`                                                                                                                                                                                   |
| **CONCEPT**               | `concept_id`              | `domain_id`, `vocabulary_id`, `concept_class_id`                                                                                                                                                            |
| **CONCEPT_ANCESTOR**      | `ancestor_concept_id`     | `descendant_concept_id`                                                                                                                                                                                     |
| **CONCEPT_RELATIONSHIP**  | 없음                      | `concept_id_1`, `concept_id_2`, `relationship_id`                                                                                                                                                           |
| **CONCEPT_SYNONYM**       | `concept_id`              | `language_concept_id`                                                                                                                                                                                       |
| **DOMAIN**                | `domain_id`               | `domain_concept_id`                                                                                                                                                                                         |
| **VOCABULARY**            | `vocabulary_id`           | `vocabulary_concept_id`                                                                                                                                                                                     |
| **SOURCE_TO_CONCEPT_MAP** | 없음                      | `source_concept_id`, `target_concept_id`, `target_vocabulary_id`                                                                                                                                            |
| **DRUG_STRENGTH**         | 없음                      | `drug_concept_id`, `ingredient_concept_id`                                                                                                                                                                  |
| **COHORT**                | 없음                      | `cohort_definition_id`, `subject_id`                                                                                                                                                                        |
| **COHORT_DEFINITION**     | `cohort_definition_id`    | `definition_type_concept_id`, `subject_concept_id`                                                                                                                                                          |

---

## 사용 방법

자연어 텍스트 입력 예시:

```
{text}
```

이 텍스트를 해석하여 해당하는 SQL 쿼리를 생성하세요.

---

## 응답 형식

- 반환 값은 한 문장으로 구성되어 있습니다. 문장 구성은 KEY:VALUE 형식으로 되어 있습니다.

성공 시, 
"sql : 생성된 SQL 쿼리"

실패 시,
"error : 오류 메시지"