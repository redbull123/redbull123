-- KPI 1 — Attach Success Rate (ASR) por hora
WITH hourly_stats AS (
    SELECT
        date_trunc('hour', "timestamp") as event_hour,
        COUNT(*) as total_attempts,
        SUM(CASE WHEN result = 'success' THEN 1 ELSE 0 END) as successful_attempts
    FROM eventos
    WHERE event_type = 'attach'
    GROUP BY 1
)
SELECT
    event_hour,
    total_attempts,
    successful_attempts,
    ROUND(CAST(100.0 * successful_attempts / total_attempts AS NUMERIC), 2) as asr_percent
FROM hourly_stats
ORDER BY event_hour;

-- KPI 2 — Top 10 eNodeBs con más fallos (HOSR)
SELECT
    enodeb_id,
    COUNT(*) as total_handovers,
    SUM(CASE WHEN result = 'failure' THEN 1 ELSE 0 END) as failed_handovers,
    ROUND(CAST(100.0 * SUM(CASE WHEN result = 'failure' THEN 1 ELSE 0 END) / COUNT(*) AS NUMERIC), 2) as failure_rate
FROM eventos
WHERE event_type = 'handover'
GROUP BY enodeb_id
ORDER BY failed_handovers DESC
LIMIT 10;

-- KPI 3 — Distribución de duración por tipo de evento
SELECT
    event_type,
    AVG(CAST(duration_ms AS INTEGER)) as avg_duration,
    MIN(CAST(duration_ms AS INTEGER)) as min_duration,
    MAX(CAST(duration_ms AS INTEGER)) as max_duration
FROM eventos
GROUP BY event_type;
