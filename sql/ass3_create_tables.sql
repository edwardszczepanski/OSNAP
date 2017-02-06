CREATE TABLE assets(
    fcode varchar(128),
    asset_tag varchar(128),
    src_facility varchar(128),
    dest_facility varchar(128),
    arrive_date timestamp,
    depart_date timestamp,
    expunge_date timestamp
);
