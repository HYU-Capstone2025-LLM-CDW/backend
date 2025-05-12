SELECT * FROM person;
SELECT * FROM person;
SELECT * FROM person;
SELECT * FROM person;
SELECT * FROM person WHERE person_id IN (SELECT person_id FROM death);
SELECT * FROM person WHERE person_id IN (SELECT person_id FROM death);
SELECT * FROM person;
SELECT * FROM person WHERE person_id NOT IN (SELECT person_id FROM death);
SELECT * FROM person;
