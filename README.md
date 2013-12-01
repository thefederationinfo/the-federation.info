diaspora-hub
============

(Unofficial) statistics hub for diaspora*

http://pods.jasonrobinson.me

Database creation
=================

Something like this (MariaDB/MySQL example):

    create database diasporahub;
    create user diasporahub@localhost identified by 'putnicepasswordhere';
    grant all on diasporahub.* to diasporahub@localhost;

Copy config.js.example to config.js and edit proper values there.
