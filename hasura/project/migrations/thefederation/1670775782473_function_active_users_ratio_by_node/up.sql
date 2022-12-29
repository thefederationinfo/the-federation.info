CREATE
OR REPLACE FUNCTION active_users_ratio_by_node(nodeId integer)
RETURNS SETOF count_by_date AS $$
SELECT
  date,
  SUM(users_monthly) :: float / SUM(users_total) as count
from
  thefederation_stat
WHERE
  node_id = nodeId
  AND date > NOW() - INTERVAL '1 year'
group by
  date $$ LANGUAGE sql STABLE;
