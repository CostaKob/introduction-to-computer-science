SELECT name FROM people
WHERE name IS NOT "Kevin Bacon"
AND people.id IN (SELECT person_id FROM stars
WHERE movie_id IN (SELECT movie_id FROM stars
WHERE person_id IN (SELECT id From people
WHERE name == "Kevin Bacon" AND birth == 1958)))