/*
 * Asset Tables
 */
CREATE TABLE products(
    product_pk integer,
    vendor varchar(128),
    description varchar(128),
    alt_description varchar(128),
    PRIMARY KEY(product_pk));

CREATE TABLE assets(
    asset_pk integer,
    product_fk integer,
    asset_tag varchar(128),
    description varchar(128),
    alt_description varchar(128),
    PRIMARY KEY(asset_pk),
    FOREIGN KEY(product_fk) REFERENCES products);

CREATE TABLE vehicles(
    vehicle_pk integer,
    asset_fk integer,
    PRIMARY KEY(vehicle_pk),
    FOREIGN KEY(asset_fk) REFERENCES assets);

CREATE TABLE facilities(
    facility_pk integer,
    fcode varchar(128),
    common_name varchar(128),
    location varchar(128),
    PRIMARY KEY(facility_pk));

CREATE TABLE convoys(
    convoy_pk integer,
    facility_fk integer,
    arrive_dt date,
    depart_dt date,
    PRIMARY KEY(convoy_pk),
    FOREIGN KEY(facility_fk) REFERENCES facilities);

CREATE TABLE used_by(
    vehicle_fk integer,
    convoy_fk integer,
    FOREIGN KEY(vehicle_fk) REFERENCES vehicles,
    FOREIGN KEY(convoy_fk) REFERENCES convoys);

CREATE TABLE asset_on(
    vehicle_fk integer,
    convoy_fk integer,
    FOREIGN KEY(vehicle_fk) REFERENCES vehicles,
    FOREIGN KEY(convoy_fk) REFERENCES convoys);

/*
 * User Tables
 */

CREATE TABLE users(
    user_pk integer,
    username varchar(128),
    active boolean,
    PRIMARY KEY(user_pk));

CREATE TABLE roles(
    role_pk integer,
    title varchar(128),
    PRIMARY KEY(role_pk));

CREATE TABLE user_is(
    vehicle_fk integer,
    role_fk integer,
    FOREIGN KEY(vehicle_fk) REFERENCES vehicles,
    FOREIGN KEY(role_fk) REFERENCES roles);

CREATE TABLE user_supports(
    user_fk integer,
    facility_fk integer,
    FOREIGN KEY(user_fk) REFERENCES users,
    FOREIGN KEY(facility_fk) REFERENCES facilities);

/*
 * Security Tables
 */

CREATE TABLE levels(
    level_pk integer,
    abbrv varchar(128),
    comment varchar(128),
    PRIMARY KEY(level_pk));


CREATE TABLE compartments(
    compartment_pk integer,
    abbrv varchar(128),
    comment varchar(128),
    PRIMARY KEY(compartment_Pk));

CREATE TABLE security_tags(
    tag_pk integer,
    level_fk integer,
    compartment_fk integer,
    user_fk integer,
    product_fk integer,
    asset_fk integer,
    PRIMARY KEY(tag_pk),
    FOREIGN KEY(level_fk) REFERENCES levels,
    FOREIGN KEY(compartment_fk) REFERENCES compartments,
    FOREIGN KEY(user_fk) REFERENCES users,
    FOREIGN KEY(product_fk) REFERENCES products,
    FOREIGN KEY(asset_fk) REFERENCES assets);

