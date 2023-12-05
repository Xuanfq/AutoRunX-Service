<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.action" :placeholder="$t('actionLog.action')" style="width: 200px;" class="filter-item"
        @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.action_type" :placeholder="$t('actionLog.actionType')" style="width: 200px;"
        class="filter-item" @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.mark" :placeholder="$t('actionLog.mark')" style="width: 200px;" class="filter-item"
        @keyup.enter.native="handleFilter" />
      <el-button v-waves class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-search"
        @click="handleFilter">
        {{ $t('actionLog.search') }}
      </el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download"
        @click="handleDownload">
        {{ $t('actionLog.export') }}
      </el-button>
      <el-checkbox v-model="showOwner" class="filter-item" style="margin-left:15px;" @change="tableKey = tableKey + 1">
        {{ $t('actionLog.owner') }}
      </el-checkbox>
      <el-checkbox v-model="showUpdateTime" class="filter-item" style="margin-left:15px;"
        @change="tableKey = tableKey + 1">
        {{ $t('actionLog.updateTime') }}
      </el-checkbox>
      <el-checkbox v-model="showCreateTime" class="filter-item" style="margin-left:15px;"
        @change="tableKey = tableKey + 1">
        {{ $t('actionLog.createTime') }}
      </el-checkbox>
    </div>

    <el-table ref="appTable" :key="tableKey" v-loading="listLoading" :data="list" border fit highlight-current-row
      style="width: 100%;" height="600px" :row-class-name="tableRowClassName"
      :default-sort="tableDefaultSort">
      <el-table-column :label="$t('actionLog.action')" fixed="left" prop="action" :sortable="true" width="350px"
        align="center">
        <template slot-scope="{row}">
          <el-tooltip :content="row.action" effect="dark" placement="bottom">
            <span>{{ row.action }}</span>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column :label="$t('actionLog.id')" prop="id" :sortable="false" align="center" width="300" >
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('actionLog.actionType')" prop="action_type" :sortable="true" width="180px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.action_type }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('actionLog.actionData')" prop="action_data" :sortable="true" width="500px" align="left">
        <template slot-scope="{row}">
          <el-tooltip :content="row.action_data" effect="dark" placement="bottom">
            <span>{{ row.action_data }}</span>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column :label="$t('actionLog.mark')" prop="mark" :sortable="true" width="180px" align="center">
        <template slot-scope="{row}">
          <el-tooltip :content="row.mark" effect="dark" placement="bottom">
            <span>{{ row.mark }}</span>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column v-if="showOwner" prop="owner" :sortable="true" :label="$t('actionLog.owner')" width="110px"
        align="center">
        <template slot-scope="{row}">
          <span>{{ row.owner }}</span>
        </template>
      </el-table-column>
      <el-table-column v-if="showUpdateTime" :sortable="true" prop="update_time" :label="$t('actionLog.updateTime')"
        width="150px" align="center" :formatter="timestampFormatter">
      </el-table-column>
      <el-table-column v-if="showCreateTime" :sortable="true" prop="create_time" :label="$t('actionLog.createTime')"
        width="150px" align="center" :formatter="timestampFormatter">
      </el-table-column>
    </el-table>

    <pagination v-show="total > 0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit"
      @pagination="getList" />

  </div>
</template>

<script>
import { getActionLog } from '@/api/action-log'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import { mapGetters } from 'vuex'

export default {
  name: 'ActionLog',
  components: { Pagination },
  directives: { waves },
  filters: {
  },
  data() {
    return {
      tableKey: 0,
      tableDefaultSort: { prop: 'create_time', order: 'descending' },
      tableHeight: 500,
      list: null,
      total: 0,
      listLoading: false,
      listQuery: {
        page: 1,
        limit: 20,
        action: undefined,
        mark: undefined,
        action_type: undefined
      },
      showOwner: false,
      showUpdateTime: false,
      showCreateTime: true,
      downloadLoading: false
    }
  },
  computed: {
    ...mapGetters([
      'serverBaseUrl'
    ])
  },
  created() {
    this.getList()
    this.freshTimer = setInterval(() => {
      this.getList(false)
    }, 15000)
  },
  mounted() {
  },
  destroyed() {
    clearInterval(this.freshTimer)
  },
  methods: {
    getList(setLoading = true) {
      if (setLoading) this.listLoading = true
      getActionLog(this.listQuery).then(response => {
        console.log(response)
        this.list = response.data.list
        this.total = response.data.total
        this.$nextTick(() => {
          // fix misalignment of table 
          this.$refs.appTable.doLayout()
        });
        this.listLoading = false
      }, (err) => {
        this.listLoading = false
        this.notify(null, err)
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    tableRowClassName({ row, rowIndex }) {
      return ''
    },
    notify(res = null, err = null) {
      if (res) {
        this.$notify({
          title: res.flag ? this.$t('actionLog.success') : this.$t('actionLog.fail'),
          message: res.data || '',
          type: res.flag ? 'success' : 'error',
          duration: 2000
        })
      } else if (err) {
        this.$notify({
          title: this.$t('actionLog.fail'),
          message: err.data,
          type: 'error',
          duration: 2000
        })
      }
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['id', 'action', 'owner', 'action_type', 'action_data', 'mark', 'update_time', 'create_time']
        const filterVal = ['id', 'action', 'owner', 'action_type', 'action_data', 'mark', 'update_time', 'create_time']
        const data = this.formatJson(filterVal)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'table-list'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal) {
      return this.list.map(v => filterVal.map(j => {
        if (String(j).endsWith('time')) {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    timestampFormatter(row,col,cellValue,index){
      return parseTime(cellValue)
    },
  }
}
</script>
<style scoped>
::v-deep .el-table .warning-row {
  background: oldlace;
}

::v-deep .el-table .success-row {
  background: #f0f9eb;
}

::v-deep .el-table .danger-row {
  background: #ffc9c9;
}

::v-deep .el-table .info-row {
  background: rgba(236, 245, 255);
}

::v-deep .el-table .primary-row {
  background: rgb(236, 246, 255);
}

.filter-container {
  vertical-align: center;
}

.filter-container .filter-item:nth-of-type(n+2) {
  margin-left: 10px;
}

.small-padding {
  padding: 5px;
}

.edit-input {
  padding-right: 100px;
}

.cancel-btn {
  position: absolute;
  margin: auto;
  right: 15px;
}

/* .el-table__body-wrapper .cell span {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.el-table__body-wrapper .cell:hover span {
  overflow: visible;
  white-space: normal;
} */
</style>
