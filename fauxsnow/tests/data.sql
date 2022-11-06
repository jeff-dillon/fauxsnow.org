INSERT INTO resorts (resort_id, resort_name, logo_file_name, state_full, state_short, address_full, lat, lon, main_url, conditions_url, map_url, acres, trails, lifts, vertical, resort_open)
VALUES ('paoli-peaks','Paoli Peaks','paoli-peaks-logo.svg','Indiana','IN','2798 W. County Road 25 S, Paoli, IN 47454','38.5574763058665','-86.50665478920111','https://www.paolipeaks.com/','https://www.paolipeaks.com/the-mountain/mountain-conditions/lift-and-terrain-status.aspx','https://goo.gl/maps/aA5bWk8ppQsCMBBK9','65','17','8','300', 0);

INSERT INTO resorts (resort_id, resort_name, logo_file_name, state_full, state_short, address_full, lat, lon, main_url, conditions_url, map_url, acres, trails, lifts, vertical, resort_open)
VALUES ('wolf-ridge','Wolf Ridge Ski Resort','wolf-ridge-logo.png','North Carolina','NC','578 Valley View Circle Mars Hill, NC 28754','36.02153540770578','-82.48665163158509','https://skiwolfridgenc.com/','https://skiwolfridgenc.com/the-mountain/snow-report','https://goo.gl/maps/VP2U6nfb4DYPiyvZ8','82','15','5','700', 0);


INSERT INTO forecasts 
(resort_id, forecast_time, sum_historic_faux_days, sum_forecast_snow, 
fp1_date, fp1_day_short, fp1_day_long, fp1_max_temp, fp1_min_temp, fp1_conditions, fp1_fs_conditions,
fp2_date, fp2_day_short, fp2_day_long, fp2_max_temp, fp2_min_temp, fp2_conditions, fp2_fs_conditions,
fp3_date, fp3_day_short, fp3_day_long, fp3_max_temp, fp3_min_temp, fp3_conditions, fp3_fs_conditions,
fp4_date, fp4_day_short, fp4_day_long, fp4_max_temp, fp4_min_temp, fp4_conditions, fp4_fs_conditions,
fp5_date, fp5_day_short, fp5_day_long, fp5_max_temp, fp5_min_temp, fp5_conditions, fp5_fs_conditions,
fp6_date, fp6_day_short, fp6_day_long, fp6_max_temp, fp6_min_temp, fp6_conditions, fp6_fs_conditions,
fp7_date, fp7_day_short, fp7_day_long, fp7_max_temp, fp7_min_temp, fp7_conditions, fp7_fs_conditions)
VALUES 
('paoli-peaks', '2022-11-04T12:00', 3, 2, 
'2022-11-04T00:00', 'T', 'THU 04', 62.3, 46.2, 'light rain showers', '-',
'2022-11-05T00:00', 'F', 'FRI 05', 63.4, 46.2, 'light rain showers', '-',
'2022-11-06T00:00', 'S', 'SAT 06', 68.5, 47.2, 'overcast', '-',
'2022-11-07T00:00', 'S', 'SUN 07', 62.3, 46.2, 'overcast', '-',
'2022-11-08T00:00', 'M', 'MON 08', 42.3, 36.2, 'clear sky', 'icy',
'2022-11-09T00:00', 'T', 'TUE 09', 22.3, 16.2, 'light snow showers', 'snow',
'2022-11-10T00:00', 'W', 'WED 10', 22.3, 16.2, 'light snow showers', 'snow'
 );

