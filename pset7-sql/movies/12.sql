-- CS50 pset7: Movies - Problem 12
-- List the titles of all movies in which both Johnny Depp and Helena Bonham Carter starred
SELECT title FROM movies 
JOIN stars s1 ON movies.id = s1.movie_id 
JOIN people p1 ON s1.person_id = p1.id 
JOIN stars s2 ON movies.id = s2.movie_id 
JOIN people p2 ON s2.person_id = p2.id 
WHERE p1.name = 'Johnny Depp' AND p2.name = 'Helena Bonham Carter';
