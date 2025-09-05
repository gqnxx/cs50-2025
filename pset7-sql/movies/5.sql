-- CS50 pset7: Movies - Problem 5
-- List the titles and release years of all Harry Potter movies, in chronological order
SELECT title, year FROM movies 
WHERE title LIKE 'Harry Potter%' 
ORDER BY year;
