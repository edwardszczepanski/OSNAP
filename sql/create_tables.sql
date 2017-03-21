/*
 * user_pk is a serial primary key for more flexibility rather than using the username value.
 * username and password have been limited to 16 characters as per the project description.
 * Only one table was created as I don't see a big reason to have two separate tables.
 * Much of the design of this schema is coming directly from earlier assignments. Although
 * the LOST database schema is no longer being enforced I still think it is a good idea to
 * follow much of the same principles. I may have to remove some stuff in the future.
 * This has been updated for revision #3. After last assignment I had some technical debt so that was difficult to fix. Not so much here, but in my SQL queries. I had a location foreign key in assets, which doesn't really make sense... Fixed now.
 * I made my requests and in_transit two separate tables. in_transit is associated with requests. It is a one-to-one relationship. Pretty simple. All in_transit holds really is start and end dates.
 * Requests holds most of the information. I think it is a pretty solid data model.
 */
CREATE TABLE roles (
    role_pk SERIAL PRIMARY KEY,
    title VARCHAR(32)
);

CREATE TABLE users(
    user_pk SERIAL PRIMARY KEY, 
    role_fk INTEGER REFERENCES roles(role_pk) NOT NULL,
    username VARCHAR(16) UNIQUE NOT NULL,
    password VARCHAR(16) NOT NULL,
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE facilities (
    facility_pk SERIAL PRIMARY KEY,
    fcode VARCHAR(6),
    common_name VARCHAR(32),
    location VARCHAR(128)
);

CREATE TABLE assets (
    asset_pk SERIAL PRIMARY KEY,
    asset_tag VARCHAR(16),
    description TEXT,
    disposed BOOLEAN DEFAULT FALSE
);

CREATE TABLE asset_at (
    asset_fk INTEGER REFERENCES assets(asset_pk) NOT NULL,
    facility_fk INTEGER REFERENCES facilities(facility_pk) NOT NULL,
    arrive_dt TIMESTAMP,
    depart_dt TIMESTAMP
);

CREATE TABLE requests (
    request_pk SERIAL PRIMARY KEY,
    asset_fk INTEGER REFERENCES assets(asset_pk) NOT NULL,
    user_fk INTEGER REFERENCES users(user_pk) NOT NULL,
    src_fk INTEGER REFERENCES facilities(facility_pk) NOT NULL,
    dest_fk INTEGER REFERENCES facilities(facility_pk) NOT NULL,
    request_dt TIMESTAMP,
    approve_dt TIMESTAMP,
    approved BOOLEAN NOT NULL,
    approve_user_fk INTEGER REFERENCES users(user_pk)
);

CREATE TABLE in_transit (
    in_transit_pk SERIAL PRIMARY KEY,
    request_fk INTEGER REFERENCES requests(request_pk) NOT NULL,
    load_dt TIMESTAMP,
    unload_dt TIMESTAMP
);

INSERT INTO roles (role_pk, title) VALUES (1, 'Facilities Officer');
INSERT INTO roles (role_pk, title) VALUES (2, 'Logistics Officer');
