DROP TABLE IF EXISTS resorts;

CREATE TABLE resorts (
    resort_id       VARCHAR(80) PRIMARY KEY,
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
    vertical        VARCHAR(10),
    resort_open     BOOLEAN
);

DROP TABLE IF EXISTS forecasts;

CREATE TABLE forecasts (
    resort_id                   VARCHAR(80),
    forecast_time               VARCHAR(20),
    sum_historic_faux_days      REAL,
    sum_forecast_snow           REAL,
    sum_historic_snow           REAL,
    fp1_date                    VARCHAR(20),
    fp1_day_short               VARCHAR(3),
    fp1_day_long                VARCHAR(10),
    fp1_max_temp                REAL,
    fp1_min_temp                REAL,
    fp1_conditions              VARCHAR(20),
    fp1_fs_conditions           VARCHAR(8),
    fp2_date                    VARCHAR(20),
    fp2_day_short               VARCHAR(3),
    fp2_day_long                VARCHAR(10),
    fp2_max_temp                REAL,
    fp2_min_temp                REAL,
    fp2_conditions              VARCHAR(20),
    fp2_fs_conditions           VARCHAR(8),
    fp3_date                    VARCHAR(20),
    fp3_day_short               VARCHAR(3),
    fp3_day_long                VARCHAR(10),
    fp3_max_temp                REAL,
    fp3_min_temp                REAL,
    fp3_conditions              VARCHAR(20),
    fp3_fs_conditions           VARCHAR(8),
    fp4_date                    VARCHAR(20),
    fp4_day_short               VARCHAR(3),
    fp4_day_long                VARCHAR(10),
    fp4_max_temp                REAL,
    fp4_min_temp                REAL,
    fp4_conditions              VARCHAR(20),
    fp4_fs_conditions           VARCHAR(8),
    fp5_date                    VARCHAR(20),
    fp5_day_short               VARCHAR(3),
    fp5_day_long                VARCHAR(10),
    fp5_max_temp                REAL,
    fp5_min_temp                REAL,
    fp5_conditions              VARCHAR(20),
    fp5_fs_conditions           VARCHAR(8),
    fp6_date                    VARCHAR(20),
    fp6_day_short               VARCHAR(3),
    fp6_day_long                VARCHAR(10),
    fp6_max_temp                REAL,
    fp6_min_temp                REAL,
    fp6_conditions              VARCHAR(20),
    fp6_fs_conditions           VARCHAR(8),
    fp7_date                    VARCHAR(20),
    fp7_day_short               VARCHAR(3),
    fp7_day_long                VARCHAR(10),
    fp7_max_temp                REAL,
    fp7_min_temp                REAL,
    fp7_conditions              VARCHAR(20),
    fp7_fs_conditions           VARCHAR(8),
    FOREIGN KEY (resort_id) REFERENCES resorts(resort_id)
);

DROP TABLE IF EXISTS raw_forecasts;

CREATE TABLE raw_forecasts (
    resort_id                   VARCHAR(80),
    forecast_time               VARCHAR(20),
    forecast_data               TEXT
);