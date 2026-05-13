SELECT * FROM eventos
--KPI 1 — Attach Success Rate (ASR) por hora
WITH by_hour AS(
	SELECT
		TO_CHAR(timestamp, 'YYYY-MM-DD HH24') AS time_by_hour,
		event_type,
		cause_code,
		COUNT(cause_code) OVER(PARTITION BY TO_CHAR(timestamp, 'YYYY-MM-DD HH24')
								ORDER BY event_type) AS Recurrency
	FROM eventos
	WHERE event_type = 'attach'
	),
	total_stat AS(
	SELECT
		time_by_hour,
		event_type,
		cause_code,
		SUM(recurrency) AS total_recurrency
	FROM by_hour
	GROUP BY time_by_hour, event_type, cause_code

	)
SELECT
	time_by_hour,
	event_type,
	cause_code,


--KPI 2 — Top 10 eNodeBs con más fallos (HOSR)

--KPI 3 — Distribución de duración por tipo de evento (percentiles)


--KPI 4 — Detección de anomalías por ventana de tiempo (ROWS BETWEEN)

--KPI 5 — Análisis de causa de fallo (top causas por tipo + CROSSTAB):