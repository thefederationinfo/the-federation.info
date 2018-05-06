<template>
    <div>
        <a
            id="drawer-icon"
            href="#drawer-opened"
        />
        <nav
            id="menu"
            class="tile"
        >
            <a
                class="close-drawer"
                href="#"
            >
                x
            </a>
            <ul>
                <li><router-link to="/">Home</router-link></li>
                <li><router-link to="/nodes">Nodes list</router-link></li>
                <li><router-link to="/#projects">Projects</router-link></li>
                <li><router-link to="/#protocols">Protocols</router-link></li>
                <li><router-link to="/info">Info</router-link></li>
            </ul>
        </nav>
    </div>
</template>

<script>
export default {
    name: "Drawer",
}
</script>

<style scoped>

</style>
