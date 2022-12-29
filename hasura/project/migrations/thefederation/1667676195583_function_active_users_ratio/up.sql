CREATE OR REPLACE FUNCTION active_users_ratio()
RETURNS SETOF count_by_date AS $$
    SELECT date, SUM(users_monthly)::float / SUM(users_total) as count from thefederation_stat WHERE node_id IS NOT NULL group by date
$$ LANGUAGE sql STABLE;
