
/*
 * user_pk is a serial primary key for more flexibility.
 * username and password have been limited to 16 characters as per the project description
 */
CREATE TABLE users(
    user_pk serial primary key, 
    username varchar(16),
    password varchar(16)
);
