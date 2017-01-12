# Database migrations

Add migration files to this folder.

Migrations will be executed automatically on starting the app. Executed migrations will be stored in the database table `migration`.

## Naming

    <number>-<migration_name>.<type>

For example:

    001-foo_bar.sql
    002-bar_foo.py

## SQL migrations

Put pure SQL here, it will be run as is.

Do NOT put database names in the SQL statements. A `USE <dbname>; ` will automatically be executed before the SQL!

## Python migrations

Any kind of Python can be run, so technically any script, not just DB related. Script will be executed as is. Use the `src.utils.DBConnection` class to handle DB connections with correct config.
