<template>
  <div id="app">
    <div id="nav">
      <Search />
    </div>
  </div>
</template>

<script>
import Search from "./components/Search.vue";

export default {
  name: "app",
  components: {
    Search
  },
  data: function () {
    return {
      hasResult: false
    };
  }
};
</script>

<style lang="less">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
