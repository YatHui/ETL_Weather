DROP TABLE IF EXISTS weather_forecast;

CREATE TABLE IF NOT EXISTS weather_forecast(
	weather_id SERIAL PRIMARY KEY,
	date VARCHAR(11),
	time VARCHAR(6),
	temperature FLOAt,
);

INSERT INTO weather_forecast(date, time, temperature)
VALUES(validDate, validTime, temperature)