<template>
    <div>
        <Drawer />
        <NodesContent />
        <Footer />
    </div>
</template>

<script>
import Drawer from "./Drawer"
import Footer from "./Footer"
import NodesContent from "./NodesContent"

export default {
    name: 'NodesPage',
    components: {NodesContent, Footer, Drawer},
}
</script>

<style scoped>

</style>
