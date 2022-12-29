CREATE OR REPLACE FUNCTION users_per_node()
RETURNS SETOF count_by_date AS $$
    SELECT date, CEIL(AVG(users_total)) as count from thefederation_stat WHERE node_id IS NOT NULL group by date
$$ LANGUAGE sql STABLE;
