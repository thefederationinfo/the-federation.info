<template>
    <main>
        <header class="main-header">
            <div class="main-title">
                <h1><a href="/">The Federation</a></h1>
                <h2>Welcome to the new social web</h2>
            </div>
            <div class="flex">
                <div class="col4">
                    <div class="tile valign-wrapper">
                        1 <strong>Protocol</strong>
                    </div>
                </div>
                <div class="col4">
                    <div class="tile valign-wrapper">
                        5 <strong>Projects</strong>
                    </div>
                </div>
                <div class="col4">
                    <div class="tile valign-wrapper">
                        100 <strong>Nodes</strong>
                    </div>
                </div>
                <div class="col4">
                    <div class="tile valign-wrapper">
                        10000 <strong>Users</strong>
                    </div>
                </div>
                <div class="col4">
                    <div class="tile valign-wrapper">
                        ONE <strong>Network</strong>
                    </div>
                </div>
            </div>
        </header>

        <section class="tile">
            <header>
                <h2>What is The Federation?</h2>
            </header>
            <div>
                <div class="flex">
                    <div class="col2">
                        <p>
                            The Federation refers to a global social network composed of nodes talking together.
                            Each of them is an installation of software which supports one of the federated social web
                            protocols.
                        </p>
                        <div class="center">
                            <a href="/nodes" class="btn btn-primary">Nodes list</a>
                        </div>
                    </div>
                    <div class="col2">
                        <ul>
                            <li>Nodes: <strong>100</strong></li>
                            <li>Users: <strong>10000</strong></li>
                            <li>Last 6 months active users: <strong>6000</strong></li>
                            <li>Last month active users: <strong>2000</strong></li>
                            <li>Posts: <strong>200000</strong></li>
                            <li>Comments: <strong>300000</strong></li>
                        </ul>
                        <div><strong>Disclaimer:</strong> These counts do not reflect the whole network due to the
                            opt-in nature of the statistics.
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!--{% include "charts/_stats_with_selectors.njk" %}-->

        <section class="tile">
            <header>
                <h2>diaspora* - Friendica - GangGo - Hubzilla - Socialhome</h2>
                <h3>Discover the projects which are composing the federation</h3>
            </header>
            <div class="overflow-x">
                <table>
                    <thead>
                        <tr>
                            <th>Project</th>
                            <th><a href="/diaspora">diaspora*</a></th>
                            <th><a href="/friendica">Friendica</a></th>
                            <th><a href="/ganggo">GangGo</a></th>
                            <th><a href="/hubzilla">Hubzilla</a></th>
                            <th><a href="/socialhome">Socialhome</a></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <th>First release date</th>
                            <td>11-2010</td>
                            <td>07-2010</td>
                            <td>02-2017</td>
                            <td>08-2015</td>
                            <td>07-2017</td>
                        </tr>
                        <tr>
                            <th>Nodes</th>
                            <td>21</td>
                            <td>21</td>
                            <td>23</td>
                            <td>43</td>
                            <td>344</td>
                        </tr>
                        <tr>
                            <th>Users</th>
                            <td>44</td>
                            <td>243</td>
                            <td>233</td>
                            <td>32</td>
                            <td>2232</td>
                        </tr>
                        <tr>
                            <th>Official website</th>
                            <td><a href="https://diasporafoundation.org"
                                   target="_blank">diasporafoundation.org</a></td>
                            <td><a href="http://friendi.ca"
                                   target="_blank">friendi.ca</a></td>
                            <td><a href="https://ganggo.github.io"
                                   target="_blank">ganggo.github.io</a></td>
                            <td><a href="https://hubzilla.org"
                                   target="_blank">hubzilla.org</a></td>
                            <td><a href="https://socialhome.network"
                                   target="_blank">socialhome.network</a></td>
                        </tr>
                        <tr>
                            <th>Source code</th>
                            <td><a href="https://github.com" target="_blank">Github</a></td>
                            <td><a href="https://github.com" target="_blank">Github</a></td>
                            <td><a href="https://github.com" target="_blank">Github</a></td>
                            <td><a href="https://github.com" target="_blank">Github</a></td>
                            <td><a href="https://github.com" target="_blank">Github</a></td>
                        </tr>
                        <tr>
                            <th>Licence</th>
                            <td>AGPL</td>
                            <td>AGPL</td>
                            <td>GPLv3</td>
                            <td>MIT</td>
                            <td>AGPL</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>
        <section class="tile">
            <header>
                <h2>Be part of our world</h2>
            </header>
            <div class="flex">
                <div class="col2">
                    <h3>Host yourself</h3>
                    <p>You want to install your own node? Awesome! Choose a project and follow an installation
                        guide.</p>
                    <p>
                        <a href="https://wiki.diasporafoundation.org/Installation" target="_blank">diaspora*</a>
                        -
                        <a href="https://github.com/friendica/friendica/blob/master/INSTALL.txt" target="_blank">Friendica</a>
                        -
                        <a href="https://github.com/redmatrix/hubzilla/blob/master/install/INSTALL.txt" target="_blank">Hubzilla</a>
                        -
                        <a href="http://socialhome.readthedocs.io/en/latest/installation.html" target="_blank">Socialhome</a>
                    </p>
                </div>
                <div class="col2">
                    <h3>I already have my node!</h3>
                    <p>
                        Yay! Welcome in the crew! To see your node included in this website, please go to <code>https://the-federation.info/register/&lt;yournode.tld&gt;</code>.
                        After some seconds, you should see your pod added. After that, daily updates happen once per 24
                        hours (some minutes past midnight EET).
                    </p>
                </div>
            </div>
        </section>
    </main>
</template>

<script>
export default {
    name: "IndexContent",
}
</script>

<style scoped>

</style>
