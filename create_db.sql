-- PostgreSQL --

--Create a new database
CREATE DATABASE text_to_pic; 

--Create username and password 
CREATE USER admin_1 WITH PASSWORD 'password';

--Gives the user admin_1 full permissions
GRANT ALL PRIVILEGES ON DATABASE text_to_pic TO admin_1;
GRANT ALL ON SCHEMA public TO admin_1;
GRANT ALL ON SCHEMA public TO public;
ALTER DATABASE text_to_pic OWNER TO admin_1;
