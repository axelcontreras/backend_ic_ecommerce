CREATE DATABASE tempdb;

  CREATE TABLE IF NOT EXISTS tempdb.items (
        codigo SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        talla VARCHAR(50),
        color VARCHAR(50),
        precio NUMERIC(10, 2),
        cantidad INTEGER,
        imagen VARCHAR(255)
     );