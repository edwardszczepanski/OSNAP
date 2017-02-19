
/*
 * user_pk is a serial primary key for more flexibility rather than using the username value.
 * username and password have been limited to 16 characters as per the project description.
 * Only one table was created as I don't see a big reason to have two separate tables.
 */
CREATE TABLE users(
    user_pk serial primary key, 
    username varchar(16),
    password varchar(16)
);
