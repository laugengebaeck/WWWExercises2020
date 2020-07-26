<template>
  <div>
    <div id="landing-container" class="container-onepage-height">
      <div>
      </div>
      <div id="landing" class="container container-onepage">
        <div class="row">
          <div class="col-md-12 col">
            <div class="row-aligned-content">
              <h2>Vue Playground</h2>
              <p>Something we created just for you!</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="container">
      <h3>Congratulations <icon name="thumbs-up"></icon></h3>
      <p>You managed it to compile your (first) Vue application!</p>

      <h3>Tasks list (19 Points)</h3>
      <p>
        This list covers only the tasks for the Vue application. Please look at the <code>plain</code> directory to see the other tasks.
      </p>

      <ul>
        <li>
          Look around the source code of this repo (you probably have already done this) and answer the questions stated on <router-link to="questions">the questions page</router-link> (5 Points).
        </li>
        <li>
          Resolve all Todos on the <router-link to="api">API page</router-link> (14 Points).
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data () {
    return {}
  }
}
</script>

<style lang="scss" scoped>
  @import '../style/bootstrap-component-include';

  .container-onepage-height {
    height: calc(100vh - 55px);
  }

  .container-onepage {
    height: calc(100vh - 55px);
    display: table;

    .row {
      display: table-row;

      .col {
        display: table-cell;
        vertical-align: middle;
        min-height: 0;
        .row-aligned-content {

          text-align: center;

          img {
            margin-bottom: 20px;
            max-width: 80%;
          }
        }
      }
    }
  }

  #landing {
    > div {
      background-color: rgba(0, 0, 0, 0.3);
    }

    color: #FFFFFF;
  }

  #landing-img {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    object-fit: cover;
  }

  #landing-container {
    background-size: cover;
    background-image: url("../assets/images/landing.jpg");
    margin-bottom: 25px;
    position: relative;
    overflow: hidden;
  }
</style>
