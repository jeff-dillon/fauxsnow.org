/*
    Resort table creation and data loading script.
*/

DROP TABLE IF EXISTS resorts;

CREATE TABLE resorts (
    resort_id       VARCHAR(80),
    resort_name     VARCHAR(80),
    logo_file_name  VARCHAR(80),
    state_full      VARCHAR(80),
    state_short     VARCHAR(2),
    address_full    VARCHAR(256),
    lat             VARCHAR(80),
    lon             VARCHAR(80),
    main_url        VARCHAR(256),
    conditions_url  VARCHAR(256),
    map_url         VARCHAR(256),
    acres           VARCHAR(10),
    trails          VARCHAR(10),
    lifts           VARCHAR(10),
    vertical        VARCHAR(10)
);