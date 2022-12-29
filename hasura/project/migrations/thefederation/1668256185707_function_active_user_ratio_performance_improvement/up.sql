CREATE OR REPLACE FUNCTION public.active_users_ratio()
 RETURNS SETOF count_by_date
 LANGUAGE sql
 STABLE
AS $function$
    SELECT date, SUM(users_monthly)::float / SUM(users_total) as count from thefederation_stat WHERE node_id IS NOT NULL AND date > NOW() - INTERVAL '1 year' group by date
$function$;
