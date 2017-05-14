[![Stories in Ready](https://badge.waffle.io/jaywink/the-federation.info.png?label=ready&title=Ready)](https://waffle.io/jaywink/the-federation.info) [![chat on freenode](https://img.shields.io/badge/chat-on%20freenode-brightgreen.svg)](http://webchat.freenode.net?channels=%23thefederation&uio=d4) [![Chat on Gitter](https://badges.gitter.im/the-federation-info/Lobby.svg)](https://gitter.im/the-federation-info/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

# The-Federation.info

Statistics hub and node list for The Federation (diaspora*, Friendica, Hubzilla).

## Requirements

* Node 4.x
* Python 3.x
* MySQL/MariaDB

## Database creation

Something like this:

    create database diasporahub;
    create user diasporahub@localhost identified by 'putnicepasswordhere';
    grant all on diasporahub.* to diasporahub@localhost;

Copy src/config.js.example to src/config.js and edit proper values there.

## Installation

### Node

The 4.x LTS version has been tested. For Ubuntu, [follow this guide](https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions). Other systems follow [NodeJS](https://nodejs.org/en/download/) docs.

Install then the Node packages

    npm install

### Python

Python 3 should hopefully be shipped in your system, if not, [install it](https://www.python.org/downloads/).

Create [a virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) using the Python 3 executable and activate it.

The Python dependencies need some system packages. For Ubuntu, this will work, for other systems, find the relevant packages and install.

    sudo apt-get install python3-dev libmysqlclient-dev

Install dependencies in your activated virtualenv:

    pip install -r python-requirements.txt

## Running

Make sure correct Python virtualenv is active. Then in the application abse directory;

    node src/app.js

The app will be running at [http://127.0.0.1:4730](http://127.0.0.1:4730). You can change the port in the `src/config.js` file if you want.

## We need data

Things wont look nice without any data, so register a node, for example this in a browser:

    http://127.0.0.1:4730/register/iliketoast.net

Check the front page and there should be a node listed.

## Development

### Sass

If you want to touch the CSS part of the-federation, you need to modify the .scss files in `static/stylesheet` and then compile site.scss to site.css.
There is a [node compiler](https://github.com/sass/node-sass) or a [python compiler](https://github.com/dahlia/libsass-python). More about the [Sass](http://sass-lang.com/) extension of the CSS language.

## Authors

* Jason Robinson / @jaywink / https://jasonrobinson.me
* Flaburgan / @Flaburgan

## License

AGPLv3
