/*
 * Asset Tables :%s/foo/bar/g
 */

CREATE TABLE products(
    product_pk serial primary key,
    vendor varchar(128),
    description varchar(128),
    alt_description varchar(128)
);

CREATE TABLE assets(
    asset_pk serial primary key,
    product_fk integer REFERENCES products (product_pk),
    asset_tag varchar(128),
    description varchar(128),
    alt_description varchar(128)
);

CREATE TABLE vehicles(
    vehicle_pk serial primary key,
    asset_fk integer REFERENCES assets(asset_pk)
);

CREATE TABLE facilities(
    facility_pk serial primary key,
    fcode varchar(128),
    common_name varchar(128),
    location varchar(128)
);

CREATE TABLE asset_at(
    asset_fk integer REFERENCES assets(asset_pk),
    facility_fk integer REFERENCES facilities(facility_pk),
    arrive_dt timestamp,
    depart_dt timestamp
);

CREATE TABLE convoys(
    convoy_pk serial primary key,
    request varchar(128),
    source_fk varchar(128),
    dest_fk varchar(128),
    depart_dt timestamp,
    arrive_dt timestamp
);

CREATE TABLE used_by(
    vehicle_fk integer REFERENCES vehicles(vehicle_pk),
    convoy_fk integer REFERENCES convoys(convoy_pk)
);

CREATE TABLE asset_on(
    asset_fk integer REFERENCES assets(asset_pk),
    convoy_fk integer REFERENCES convoys(convoy_pk),
    load_dt timestamp,
    unload_dt timestamp
);

/*
 * User Tables
 */

CREATE TABLE users(
    user_pk serial primary key,
    username varchar(128),
    active boolean
);

CREATE TABLE roles(
    role_pk serial primary key,
    title varchar(128)
);

CREATE TABLE user_is(
    vehicle_fk integer REFERENCES vehicles(vehicle_pk),
    role_fk integer REFERENCES roles(role_pk)
);

CREATE TABLE user_supports(
    user_fk integer REFERENCES users(user_pk),
    facility_fk integer REFERENCES facilities(facility_pk)
);

/*
 * Security Tables
 */

CREATE TABLE levels(
    level_pk serial primary key,
    abbrv varchar(128),
    comment varchar(128)
);


CREATE TABLE compartments(
    compartment_pk serial primary key,
    abbrv varchar(128),
    comment varchar(128)
);

CREATE TABLE security_tags(
    tag_pk serial primary key,
    level_fk integer REFERENCES levels(level_pk),
    compartment_fk integer REFERENCES compartments(compartment_pk),
    user_fk integer REFERENCES users(user_pk),
    product_fk integer REFERENCES products(product_pk),
    asset_fk integer REFERENCES assets(asset_pk)
);

