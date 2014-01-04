diaspora-hub
============

(Unofficial) statistics hub for diaspora*

Check information and how to add your pod: http://pods.jasonrobinson.me

Database creation
=================

Something like this (MariaDB/MySQL example):

    create database diasporahub;
    create user diasporahub@localhost identified by 'putnicepasswordhere';
    grant all on diasporahub.* to diasporahub@localhost;

Copy config.js.example to config.js and edit proper values there.

Installation
============

Node stuff;

    npm install
    
Python stuff (2.x required);

    sudo pip install MySQL-python

Author
======

[Jason Robinson](https://github.com/jaywink)

[Me on diaspora*](https://iliketoast.net/u/jaywink)

Like this?
==========

Please donate via the options at the end of [the hub page](http://pods.jasonrobinson.me).

License
=======

AGPLv3