-- Run this only to create the database outside of the bfx server (it already exists on the server)
-- This table exists within the dpatel95 database since I couldn't create a separate one

-- Create database
CREATE DATABASE IF NOT EXISTS dpatel95;

-- Switch to the database
USE dpatel95;

-- Format for table created in mysql database on server
CREATE TABLE final (
    id VARCHAR(255) NOT NULL,
    name VARCHAR(255) PRIMARY KEY,
    class TEXT NOT NULL,
    mechanism TEXT NOT NULL,
    source VARCHAR(255) NOT NULL,
    sequence TEXT NOT NULL,
);