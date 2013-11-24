diaspora-hub
============

Statistics hub for diaspora*

Database creation
=================

Something like this (MariaDB/MySQL example):

create database diasporahub;
create user diasporahub@localhost identified by 'putnicepasswordhere';
grant all on diasporahub.* to diasporahub@localhost;

Copy config.js.example to config.js and edit proper values there.