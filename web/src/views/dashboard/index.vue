<template>
  <div class="dashboard-container">
    <div class="titlebox">
      <img src="https://raw.githubusercontent.com/Xuanfq/AutoRunX/master/favicon.ico" alt="AutoRunX" class="logo">
      <div class="title">AutoRunX App Admin</div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Dashboard',
  components: {

  },
  data() {
    return {
    }
  },
  computed: {
    ...mapGetters([
    ])
  },
  created() {
  }
}
</script>
<style>
.titlebox{
  margin-top: 200px;
}
.titlebox .logo{
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100px;
  height: 100px;
  margin: auto;
}
.titlebox .title{
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 32px;
  font-weight: 800;
  font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
}
</style>
