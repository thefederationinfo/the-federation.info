alter table diasporahub.pods add column network varchar(80) default "unknown";
alter table diasporahub.pods add column service_facebook int(1) default "0";
alter table diasporahub.pods add column service_twitter int(1) default "0";
alter table diasporahub.pods add column service_tumblr int(1) default "0";
alter table diasporahub.pods add column service_wordpress int(1) default "0";
