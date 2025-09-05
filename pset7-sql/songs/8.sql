-- 8.sql: Lists the names of the songs that feature other artists
SELECT name FROM songs WHERE name LIKE '%feat.%' OR name LIKE '%ft.%' OR name LIKE '%featuring%';
