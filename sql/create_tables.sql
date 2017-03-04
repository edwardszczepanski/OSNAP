/*
 * user_pk is a serial primary key for more flexibility rather than using the username value.
 * username and password have been limited to 16 characters as per the project description.
 * Only one table was created as I don't see a big reason to have two separate tables.
 * Much of the design of this schema is coming directly from earlier assignments. Although
 * the LOST database schema is no longer being enforced I still think it is a good idea to
 * follow much of the same principles. I may have to remove some stuff in the future.
 */
CREATE TABLE roles (
    role_pk SERIAL PRIMARY KEY,
    title VARCHAR(32)
);

CREATE TABLE users(
    user_pk SERIAL PRIMARY KEY, 
    role_fk INTEGER REFERENCES roles(role_pk) NOT NULL,
    username VARCHAR(16) UNIQUE NOT NULL,
    password VARCHAR(16) NOT NULL
);

CREATE TABLE facilities (
    facility_pk SERIAL PRIMARY KEY,
    fcode VARCHAR(6),
    common_name VARCHAR(32),
    location VARCHAR(128)
);

CREATE TABLE assets (
    asset_pk SERIAL PRIMARY KEY,
    facility_fk INTEGER REFERENCES facilities(facility_pk) NOT NULL,
    asset_tag VARCHAR(16),
    description TEXT,
    disposed BOOLEAN
);

CREATE TABLE asset_at (
    asset_fk INTEGER REFERENCES assets(asset_pk) NOT NULL,
    facility_fk INTEGER REFERENCES facilities(facility_pk) NOT NULL,
    arrive_dt TIMESTAMP,
    depart_dt TIMESTAMP
);

CREATE TABLE requests (
    asset_fk INTEGER REFERENCES assets(asset_pk) NOT NULL,
    user_fk INTEGER REFERENCES users(user_pk) NOT NULL,
    src_fk INTEGER REFERENCES facilities(facility_pk) NOT NULL,
    dest_fk INTEGER REFERENCES facilities(facility_pk) NOT NULL,
    request_dt TIMESTAMP,
    approve_dt TIMESTAMP,
    approved BOOLEAN NOT NULL
);

CREATE TABLE in_transit (
    src_fk INTEGER REFERENCES facilities(facility_pk) NOT NULL,
    dest_fk INTEGER REFERENCES facilities(facility_pk) NOT NULL,
    load_dt TIMESTAMP,
    unload_dt TIMESTAMP
);


INSERT INTO roles (role_pk, title) VALUES (1, 'Facilities Officer');
INSERT INTO roles (role_pk, title) VALUES (2, 'Logistics Officer');
