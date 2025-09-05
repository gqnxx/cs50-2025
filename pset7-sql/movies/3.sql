-- CS50 pset7: Movies - Problem 3
-- List the titles of all movies released in or after 2018, in alphabetical order
SELECT title FROM movies 
WHERE year >= 2018 
ORDER BY title;
