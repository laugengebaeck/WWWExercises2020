<template>
  <b-navbar toggleable="md" type="dark" class="navbar-dark sticky-top bg-dark">
    <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
    <b-navbar-brand to="/" class="navbar-brand">
      <img src="../assets/images/logo.png" id="navbar-logo">
      <span class="d-none d-sm-inline">Vue</span> Playground
    </b-navbar-brand>

    <b-collapse is-nav id="nav_collapse">
      <b-navbar-nav>
        <b-nav-item to="/home"><icon name="home" scale="1.2" class="symbol"></icon> Home</b-nav-item>
        <b-nav-item to="/questions"><icon name="question" scale="1.2" class="symbol"></icon> Questions</b-nav-item>
        <b-nav-item to="/api"><icon name="cogs" scale="1.2" class="symbol"></icon> API</b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  name: 'Navbar'
}
</script>

<style lang="scss" scoped>
  @import '../style/bootstrap-component-include';

  .symbol {
    margin-top: -5px;
    vertical-align: middle;
  }

  .sticky-top {
    z-index: 100;
  }

  #navbar-logo {
    $navbar-logo-height: 40px;
    $navbar-logo-mb: -5px;

    margin-top: 25px - $navbar-logo-mb - $navbar-logo-height;
    height: $navbar-logo-height;
    margin-bottom: $navbar-logo-mb;
  }
</style>
