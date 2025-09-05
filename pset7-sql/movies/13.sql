-- CS50 pset7: Movies - Problem 13
-- List the names of all people who starred in a movie in which Kevin Bacon also starred
SELECT DISTINCT name FROM people 
JOIN stars ON people.id = stars.person_id 
WHERE stars.movie_id IN (
    SELECT movie_id FROM stars 
    JOIN people ON stars.person_id = people.id 
    WHERE name = 'Kevin Bacon' AND birth = 1958
) AND name != 'Kevin Bacon';
