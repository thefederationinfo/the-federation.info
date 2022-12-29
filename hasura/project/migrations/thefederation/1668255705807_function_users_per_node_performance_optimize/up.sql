CREATE OR REPLACE FUNCTION public.users_per_node()
 RETURNS SETOF count_by_date
 LANGUAGE sql
 STABLE
AS $function$
    SELECT date, FLOOR(AVG(users_total)) as count from thefederation_stat WHERE node_id IS NOT NULL AND date > NOW() - INTERVAL '1 year' group by date
$function$;
