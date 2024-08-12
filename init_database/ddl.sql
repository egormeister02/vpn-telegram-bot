CREATE SCHEMA main;

CREATE TABLE main.users (
    user_id integer NOT NULL PRIMARY KEY,
    user_nm varchar NOT NULL,
    balance_rub integer NOT NULL
);

CREATE TABLE main.servers (
    server_ip varchar NOT NULL PRIMARY KEY,
    region varchar NOT NULL,
    status varchar NOT NULL
);

CREATE TABLE main.connections (
    connection_id integer NOT NULL PRIMARY KEY,
    user_id integer NOT NULL,
    server_ip varchar NOT NULL,
    date_from_dttm timestamp NOT NULL,
    date_to_dttm timestamp NOT NULL,
    FOREIGN KEY (user_id) REFERENCES main.users (user_id),
    FOREIGN KEY (server_ip) REFERENCES main.servers (server_ip)
);
