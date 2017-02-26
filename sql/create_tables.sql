/*
 * user_pk is a serial primary key for more flexibility rather than using the username value.
 * username and password have been limited to 16 characters as per the project description.
 * Only one table was created as I don't see a big reason to have two separate tables.
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

CREATE TABLE vehicles (
    vehicle_pk SERIAL PRIMARY KEY,
    asset_fk INTEGER REFERENCES assets(asset_pk) NOT NULL
);

CREATE TABLE asset_at (
    asset_fk INTEGER REFERENCES assets(asset_pk) NOT NULL,
    facility_fk INTEGER REFERENCES facilities(facility_pk) NOT NULL,
    arrive_dt TIMESTAMP,
    depart_dt TIMESTAMP
);

CREATE TABLE convoys (
    convoy_pk SERIAL PRIMARY KEY,
    request_id VARCHAR(16),
    src_fk INTEGER REFERENCES facilities(facility_pk) NOT NULL,
    dst_fk INTEGER REFERENCES facilities(facility_pk) NOT NULL,
    arrive_dt TIMESTAMP,
    depart_dt TIMESTAMP
);

CREATE TABLE asset_on (
    asset_fk INTEGER REFERENCES assets(asset_pk) NOT NULL,
    convoy_fk INTEGER REFERENCES convoys(convoy_pk) NOT NULL,
    load_dt TIMESTAMP,
    unload_dt TIMESTAMP
);

