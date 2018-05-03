<template>
    <div>
        <Drawer />
        <IndexContent />
        <Footer />
    </div>
</template>

<script>
import Drawer from "./common/Drawer"
import Footer from "./common/Footer"
import IndexContent from "./IndexContent";

export default {
    name: 'IndexPage',
    components: {IndexContent, Footer, Drawer},
}
</script>

<style scoped>

</style>
