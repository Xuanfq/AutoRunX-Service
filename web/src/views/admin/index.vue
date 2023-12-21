<template>
  <div class="tab-container">
    <el-tabs v-model="activeName" style="margin-top:15px;" type="border-card">
      <el-tab-pane v-for="item in tabMapOptions" :key="item.key" :label="item.label" :name="item.key">
        <keep-alive>
          <div v-if="item.key == 'Node'">
            <el-row>
              <el-button type="danger" @click="triggerSyncNodes" round :loading="isSyncingNodes">Sync Nodes</el-button>
            </el-row>
          </div>
        </keep-alive>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { syncNodes } from '@/api/node.js'
export default {
  name: 'Admin',
  components: {},
  data() {
    return {
      tabMapOptions: [
        { label: 'Node', key: 'Node' },
      ],
      activeName: 'Node',
      isSyncingNodes: false,
    }
  },
  watch: {
    activeName(val) {
      this.$router.push(`${this.$route.path}?tab=${val}`)
    }
  },
  created() {
    // init the default selected tab
    const tab = this.$route.query.tab
    if (tab) {
      this.activeName = tab
    }
  },
  methods: {
    triggerSyncNodes() {
      this.$confirm('Continue to Sync Nodes?', 'Tips', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancle',
        type: 'warning'
      }).then(() => {
        this.isSyncingNodes = true
        let params = { lang: this.language == 'zh' ? 'zh' : 'en' }
        syncNodes(params).then((res) => {
          if (res.flag) {
            let data = res.data
            this.$message({
              type: 'success',
              message: 'Sync Success!'
            })
          } else {
            this.$message({
              type: 'error',
              message: res.data
            })
          }
          this.isSyncingNodes = false
        }, (err) => {
          this.$message({
            type: 'error',
            message: err.data
          })
          this.isSyncingNodes = false
        })
      }).catch(() => {

      })
    },
  }
}
</script>

<style scoped>
.tab-container {
  margin: 30px;
}
</style>
