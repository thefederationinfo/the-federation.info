<template>
    <main>
        <header class="main-header">
            <div class="main-title">
                <h1>The nodes</h1>
            </div>
        </header>
        <section class="tile">
            <header>
                <h2>List of nodes composing The Federation</h2>
            </header>
            <div>
                <p>You can also access a list of nodes for each project using the global menu on the left.</p>
                <div class="overflow-x">
                    <NodesTable />
                </div>
            </div>
        </section>
    </main>
</template>

<script>
import NodesTable from "./NodesTable"

export default {
    name: "NodesContent",
    components: {NodesTable},
}
</script>
