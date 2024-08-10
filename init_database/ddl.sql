CREATE SCHEMA main;

CREATE OR REPLACE TABLE main.users (

    user_id integer NOT NULL PRIMARY KEY,
    user_nm varchar NOT NULL,
    user_balance integer NOT NULL
);

INSERT INTO main.users (user_id, user_nm, user_balance) VALUES 
(1, 'John', 1000);