CREATE
OR REPLACE FUNCTION active_users_ratio_by_platform(platformId integer)
RETURNS SETOF count_by_date AS $$
SELECT
  date,
  SUM(users_monthly) :: float / SUM(users_total) as count
from
  thefederation_stat
WHERE
  platform_id = platformId
  AND date > NOW() - INTERVAL '1 year'
group by
  date $$ LANGUAGE sql STABLE;
