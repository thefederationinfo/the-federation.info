CREATE OR REPLACE FUNCTION node_count_per_date_by_platform_id(platformId integer)
RETURNS SETOF count_by_date AS $$
    SELECT stat.date, COUNT(stat.id) as count FROM thefederation_stat as stat INNER JOIN thefederation_node as node ON stat.node_id = node.id WHERE stat.date > NOW() - INTERVAL '1 year' AND node.last_success > NOW() - INTERVAL '1 Month' AND node.platform_id = platformId GROUP BY stat.date
$$ LANGUAGE sql STABLE;
