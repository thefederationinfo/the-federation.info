[![Stories in Ready](https://badge.waffle.io/jaywink/the-federation.info.png?label=ready&title=Ready)](https://waffle.io/jaywink/the-federation.info)
# The-Federation.info

Statistics hub and node list for The Federation (diaspora*, Friendica, Hubzilla/Redmatrix).

## Database creation

Something like this (MariaDB/MySQL example):

    create database diasporahub;
    create user diasporahub@localhost identified by 'putnicepasswordhere';
    grant all on diasporahub.* to diasporahub@localhost;

Copy src/config.js.example to src/config.js and edit proper values there.

## Installation

Node stuff;

    npm install
    
Python stuff (2.x required);

    pip install -r python-requirements.txt

## Running

Make sure correct Python virtualenv is active, if any. Then;

    node src/app.js

## Author

Jason Robinson / @jaywink / https://jasonrobinson.me / https://iliketoast.net/u/jaywink

## License

AGPLv3
