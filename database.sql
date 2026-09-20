-- Change the database name to match the "name" value in settings.ini
CREATE DATABASE IF NOT EXISTS your_database_name;
USE your_database_name;

CREATE TABLE final (
    id VARCHAR(255) NOT NULL,
    name VARCHAR(255) PRIMARY KEY,
    class TEXT NOT NULL,
    mechanism TEXT NOT NULL,
    source VARCHAR(255) NOT NULL,
    sequence TEXT NOT NULL
);
