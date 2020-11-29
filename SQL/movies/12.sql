SELECT title FROM movies
JOIN stars
ON movies.id = stars.movie_id
Join people
ON stars.person_id = people.id
WHERE name == "Johnny Depp" or name == "Helena Bonham Carter"
GROUP BY title
HAVING COUNT(*) > 1;