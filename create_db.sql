CREATE DATABASE text_to_pic;
CREATE USER admin_1 WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE text_to_pic TO admin_1;
GRANT ALL ON SCHEMA public TO admin_1;
GRANT ALL ON SCHEMA public TO public;
ALTER DATABASE text_to_pic OWNER TO admin_1;
