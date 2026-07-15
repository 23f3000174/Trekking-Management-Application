<template>
  <div id="app">
    <NavBar :key="$route.path" />

    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'

export default {
  name: 'App',
  components: {
    NavBar,
  },
}
</script>

<style scoped></style>
