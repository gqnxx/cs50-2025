-- CS50 pset7: Fiftyville Mystery
-- Keep a log of any SQL queries you execute as you solve the mystery.

-- The CS50 Duck has been stolen! The town of Fiftyville has called upon you to solve the mystery of the stolen duck. 
-- Authorities believe that the thief stole the duck and then, shortly afterwards, took a flight out of town with the help of an accomplice. 
-- Your goal is to identify:
-- - Who the thief is
-- - What city the thief escaped to
-- - Who the thief's accomplice is

-- All you know is that the theft took place on July 28, 2021 and that it took place on Humphrey Street.

-- Step 1: Check the crime scene reports for July 28, 2021 on Humphrey Street
SELECT description FROM crime_scene_reports 
WHERE year = 2021 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

-- Result shows: Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. 
-- Interviews were conducted with three witnesses who were present at the scene – each of their interview transcripts mentions the bakery.

-- Step 2: Check interviews mentioning bakery on July 28, 2021
SELECT name, transcript FROM interviews 
WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE '%bakery%';

-- Key findings from interviews:
-- Ruth: Thief got into a car in the bakery parking lot within 10 minutes of theft (10:15-10:25am)
-- Eugene: Thief was withdrawing money from ATM on Leggett Street earlier that morning
-- Raymond: Thief was on phone for less than a minute, planning to take earliest flight out of Fiftyville tomorrow (July 29)

-- Step 3: Check bakery security logs between 10:15-10:25am on July 28
SELECT activity, license_plate, hour, minute FROM bakery_security_logs 
WHERE year = 2021 AND month = 7 AND day = 28 
AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = 'exit';

-- Step 4: Check ATM transactions on Leggett Street on July 28
SELECT account_number, amount FROM atm_transactions 
WHERE year = 2021 AND month = 7 AND day = 28 
AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

-- Step 5: Check phone calls on July 28 that were less than 60 seconds
SELECT caller, receiver, duration FROM phone_calls 
WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;

-- Step 6: Check flights from Fiftyville on July 29 (earliest flight)
SELECT id, destination_airport_id, hour, minute FROM flights 
WHERE year = 2021 AND month = 7 AND day = 29 
AND origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
ORDER BY hour, minute LIMIT 1;

-- Step 7: Cross-reference all evidence
-- Find people who match ALL criteria:
-- 1. License plate from bakery parking lot (10:15-10:25am exit)
-- 2. Bank account with ATM withdrawal on Leggett Street
-- 3. Phone call < 60 seconds on July 28
-- 4. Passenger on earliest flight July 29

-- Get suspects from license plates
SELECT DISTINCT people.name, people.phone_number, people.passport_number 
FROM people 
JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate 
WHERE bakery_security_logs.year = 2021 AND bakery_security_logs.month = 7 AND bakery_security_logs.day = 28 
AND bakery_security_logs.hour = 10 AND bakery_security_logs.minute >= 15 AND bakery_security_logs.minute <= 25 
AND bakery_security_logs.activity = 'exit';

-- Cross-reference with ATM transactions
SELECT DISTINCT people.name, people.phone_number, people.passport_number 
FROM people 
JOIN bank_accounts ON people.id = bank_accounts.person_id 
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number 
JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate 
WHERE atm_transactions.year = 2021 AND atm_transactions.month = 7 AND atm_transactions.day = 28 
AND atm_transactions.atm_location = 'Leggett Street' AND atm_transactions.transaction_type = 'withdraw'
AND bakery_security_logs.year = 2021 AND bakery_security_logs.month = 7 AND bakery_security_logs.day = 28 
AND bakery_security_logs.hour = 10 AND bakery_security_logs.minute >= 15 AND bakery_security_logs.minute <= 25 
AND bakery_security_logs.activity = 'exit';

-- Cross-reference with phone calls
SELECT DISTINCT people.name, people.phone_number, people.passport_number 
FROM people 
JOIN bank_accounts ON people.id = bank_accounts.person_id 
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number 
JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate 
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE atm_transactions.year = 2021 AND atm_transactions.month = 7 AND atm_transactions.day = 28 
AND atm_transactions.atm_location = 'Leggett Street' AND atm_transactions.transaction_type = 'withdraw'
AND bakery_security_logs.year = 2021 AND bakery_security_logs.month = 7 AND bakery_security_logs.day = 28 
AND bakery_security_logs.hour = 10 AND bakery_security_logs.minute >= 15 AND bakery_security_logs.minute <= 25 
AND bakery_security_logs.activity = 'exit'
AND phone_calls.year = 2021 AND phone_calls.month = 7 AND phone_calls.day = 28 
AND phone_calls.duration < 60;

-- Final step: Check who was on the earliest flight
-- This should narrow down to the thief
SELECT people.name 
FROM people 
JOIN passengers ON people.passport_number = passengers.passport_number 
JOIN flights ON passengers.flight_id = flights.id 
JOIN bank_accounts ON people.id = bank_accounts.person_id 
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number 
JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate 
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE flights.year = 2021 AND flights.month = 7 AND flights.day = 29 
AND flights.origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
AND flights.hour = 8 AND flights.minute = 20  -- Earliest flight time
AND atm_transactions.year = 2021 AND atm_transactions.month = 7 AND atm_transactions.day = 28 
AND atm_transactions.atm_location = 'Leggett Street' AND atm_transactions.transaction_type = 'withdraw'
AND bakery_security_logs.year = 2021 AND bakery_security_logs.month = 7 AND bakery_security_logs.day = 28 
AND bakery_security_logs.hour = 10 AND bakery_security_logs.minute >= 15 AND bakery_security_logs.minute <= 25 
AND bakery_security_logs.activity = 'exit'
AND phone_calls.year = 2021 AND phone_calls.month = 7 AND phone_calls.day = 28 
AND phone_calls.duration < 60;

-- Find the accomplice (person who received the phone call)
SELECT people.name 
FROM people 
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE phone_calls.caller = (
    -- Phone number of the thief (Bruce)
    SELECT people.phone_number 
    FROM people 
    JOIN passengers ON people.passport_number = passengers.passport_number 
    JOIN flights ON passengers.flight_id = flights.id 
    JOIN bank_accounts ON people.id = bank_accounts.person_id 
    JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number 
    JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate 
    JOIN phone_calls pc ON people.phone_number = pc.caller
    WHERE flights.year = 2021 AND flights.month = 7 AND flights.day = 29 
    AND flights.origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
    AND flights.hour = 8 AND flights.minute = 20
    AND atm_transactions.year = 2021 AND atm_transactions.month = 7 AND atm_transactions.day = 28 
    AND atm_transactions.atm_location = 'Leggett Street' AND atm_transactions.transaction_type = 'withdraw'
    AND bakery_security_logs.year = 2021 AND bakery_security_logs.month = 7 AND bakery_security_logs.day = 28 
    AND bakery_security_logs.hour = 10 AND bakery_security_logs.minute >= 15 AND bakery_security_logs.minute <= 25 
    AND bakery_security_logs.activity = 'exit'
    AND pc.year = 2021 AND pc.month = 7 AND pc.day = 28 AND pc.duration < 60
)
AND phone_calls.year = 2021 AND phone_calls.month = 7 AND phone_calls.day = 28 
AND phone_calls.duration < 60;

-- Find the destination city
SELECT city 
FROM airports 
WHERE id = (
    SELECT destination_airport_id 
    FROM flights 
    WHERE year = 2021 AND month = 7 AND day = 29 
    AND origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
    AND hour = 8 AND minute = 20
);

-- SOLUTION:
-- The thief is: Bruce
-- The accomplice is: Robin  
-- The destination city is: New York City
