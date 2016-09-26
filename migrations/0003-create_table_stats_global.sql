create table if not exists diasporahub.global_stats (
    id int(10) not null auto_increment primary key,
    date date,
    total_users int(10),
    active_users_halfyear int(10),
    active_users_monthly int(10),
    local_posts int(10),
    new_users int(10),
    new_posts int(10)
);