CREATE OR REPLACE FUNCTION node_count_by_date()
RETURNS SETOF count_by_date AS $$
    SELECT date, COUNT(id) as count from thefederation_stat WHERE node_id IS NOT NULL AND node_id IS NOT NULL AND date > NOW() - INTERVAL '1 year' GROUP BY date
$$ LANGUAGE sql STABLE;
