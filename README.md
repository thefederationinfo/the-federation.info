# The-Federation.info

[![Join the Matrix room](https://img.shields.io/matrix/the-federation:matrix.org?label=matrix)](https://matrix.to/#/#the-federation:matrix.org)
[![](https://img.shields.io/badge/license-AGPLv3-green.svg)](https://tldrlegal.com/license/gnu-affero-general-public-license-v3-(agpl-3.0))

<a href="https://codeberg.org/thefederationinfo/the-federation.info">
    <img alt="Get it on Codeberg" src="https://codeberg.org/Codeberg/GetItOnCodeberg/media/branch/main/get-it-on-neon-blue.png" height="60">
</a>

---

Tracking various projects using the ActivityPub, Matrix, Diaspora, OStatus and other protocols.

Site found at: https://the-federation.info

## How to get your platform listed

Just implement the .well-known [NodeInfo](http://nodeinfo.diaspora.software/) endpoint to your project.

Matrix instances are scraped with a dedicated scraper since they don't (yet) provide generic metadata.

### OK, I've done that, what now?

Register your node here, for example `https://the-federation.info/register/mynode.tld`. If it is a success, you're good! If your platform is new, or you want to update an existing platform information, raise an issue providing the following:

* URL to code
* Description
* Display name
* Code license
* Icon
* URL to install guide
* Tagline
* URL to official website

If it's closed source, leave out link to code and install guide. Icon can be any size, currently only using 16px. Possibly will have a larger image at some point on the platform page. Tagline is a kind of short one sentence marketing line, see other platforms.

### Code of Conduct

While interactions on our site is not possible, we expect sites we list to have a humane code of conduct in place. Should sites who fail to ban content that can be found generally harmful, that node will be blocked from listing here.

Harmful content can be, but not limited to, malware, graphical material of minorities, abusive images, hateful content, racist content and climate denialism. The admins of this site reserve the right to decide case by case on blocking of nodes. Please report any nodes violating our terms to the admins.

## Tech stack

* Node 16
* Python 3.6
* Django 2.0
* PostgreSQL
* Vue 2
* Webpack
* Hasura (GraphQL)

## Development

> Note the Graphql Django Backend is deprecated, use the Hasura Service instead!

### Dependencies

``` bash
pip install -U pip setuptools pip-tools
pip-sync dev-requirements.txt
```

### DB

``` bash
sudo su - postgres
createuser -s -P thefederation  # give password 'thefederation'
createdb -O thefederation thefederation
exit
python manage.py migrate
```

### Hasura

Hasura-Console: http://localhost:8090/console
Password: myadminsecretkey <- this is the default password for development

If you want to create migrations you have to use the hasura cli:

```bash
cd hasura/project
hasura console --admin-secret "myadminsecretkey" --endpoint "http://localhost:8090"
```

The second command opens your default browser with the hasura console.
Every change you made with the database it creates automatically migrations for you.

To create a fresh schema.graphql:

```bash
yarn gq http://localhost:8090/v1/graphql -H "X-Hasura-Admin-Secret: myadminsecretkey" --introspect > schema.graphql
```

and delete non wanted information.

## Frontend

### Build Setup

``` bash
# install dependencies
yarn

# serve with hot reload at localhost:8080
yarn dev

# build for production with minification
yarn build
```

## Authors

* Jason Robinson / @jaywink / https://jasonrobinson.me / `@jaywink:federator.dev`
* Flaburgan / @Flaburgan

See [other awesome contributors](https://github.com/thefederationinfo/the-federation.info/graphs/contributors)!

## License

Source code: AGPLv3

### Third party

This product includes GeoLite2 data created by MaxMind, available from https://www.maxmind.com.
