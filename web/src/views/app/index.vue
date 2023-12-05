<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.name" :placeholder="$t('app.name')" style="width: 200px;" class="filter-item"
        @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.mark" :placeholder="$t('app.mark')" style="width: 200px;" class="filter-item"
        @keyup.enter.native="handleFilter" />
      <el-input v-model="listQuery.run_time_error" :placeholder="$t('app.runTimeError')" style="width: 200px;"
        class="filter-item" @keyup.enter.native="handleFilter" />
      <el-button v-waves class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-search"
        @click="handleFilter">
        {{ $t('app.search') }}
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit"
        @click="handleShowDialogForm('create', 'name')">
        {{ $t('app.add') }}
      </el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download"
        @click="handleDownload">
        {{ $t('app.export') }}
      </el-button>
      <el-checkbox v-model="showOwner" class="filter-item" style="margin-left:15px;" @change="tableKey = tableKey + 1">
        {{ $t('app.owner') }}
      </el-checkbox>
      <el-checkbox v-model="showUpdateTime" class="filter-item" style="margin-left:15px;"
        @change="tableKey = tableKey + 1">
        {{ $t('app.updateTime') }}
      </el-checkbox>
      <el-checkbox v-model="showCreateTime" class="filter-item" style="margin-left:15px;"
        @change="tableKey = tableKey + 1">
        {{ $t('app.createTime') }}
      </el-checkbox>
    </div>

    <el-table ref="appTable" :key="tableKey" @cell-dblclick="handleCellDbClick" v-loading="listLoading" :data="list"
      border fit highlight-current-row style="width: 100%;" height="600" :row-class-name="tableRowClassName"
      :default-sort="tableDefaultSort">
      <el-table-column :label="$t('app.name')" fixed="left" prop="name" :sortable="true" width="200px" align="center">
        <template slot-scope="{row}">
          <el-tooltip :content="$t('app.doubleClickEdit')" effect="dark" placement="bottom">
            <span>{{ row.name }}</span>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column :label="$t('app.id')" prop="id" :sortable="false" align="center" width="300px">
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('app.uploadRunConfig')" prop="upload_run_config" :sortable="true" width="180px"
        align="center" :formatter="booleanFormatter">
      </el-table-column>
      <el-table-column :label="$t('app.planStartTime')" prop="plan_start_time" :sortable="true" width="150px"
        align="center" :formatter="timestampFormatter">
      </el-table-column>
      <el-table-column :label="$t('app.startTime')" prop="start_running_time" :sortable="true" width="150px"
        align="center" :formatter="timestampFormatter">
      </el-table-column>
      <el-table-column :label="$t('app.endTime')" prop="end_running_time" :sortable="true" width="150px" align="center"
        :formatter="timestampFormatter">
      </el-table-column>
      <el-table-column :label="$t('app.abortTime')" prop="abort_running_time" :sortable="true" width="150px"
        align="center" :formatter="timestampFormatter">
      </el-table-column>
      <el-table-column :label="$t('app.runTimeError')" prop="run_time_error" :sortable="true" width="150px"
        align="center">
        <template slot-scope="{row}">
          <span>{{ row.run_time_error }}</span>
        </template>
      </el-table-column>
      <el-table-column :label="$t('app.mark')" prop="mark" :sortable="true" width="150px" align="center">
        <template slot-scope="{row}">
          <el-tooltip :content="$t('app.doubleClickEdit')" effect="dark" placement="bottom">
            <span>{{ row.mark }}</span>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column v-if="showOwner" prop="owner" :sortable="true" :label="$t('app.owner')" width="110px"
        align="center">
        <template slot-scope="{row}">
          <span>{{ row.owner }}</span>
        </template>
      </el-table-column>
      <el-table-column v-if="showUpdateTime" :sortable="true" prop="update_time" :label="$t('app.updateTime')"
        width="150px" align="center" :formatter="timestampFormatter">
      </el-table-column>
      <el-table-column v-if="showCreateTime" sortable prop="create_time" :label="$t('app.createTime')" width="150px"
        align="center" :formatter="timestampFormatter">
      </el-table-column>
      <el-table-column :label="$t('app.actions')" fixed="right" align="center" width="440px"
        class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button-group>
            <el-tooltip :content="$t('app.uploadRunConfig')" effect="dark" placement="bottom">
              <el-button
                :disabled="row.plan_start_time && row.plan_start_time > 0 || row.start_running_time && row.start_running_time > 0"
                size="mini" type="primary" @click="handleShowDialogForm('edit', 'run_config_file', row)"
                icon="el-icon-upload2" round>
              </el-button>
            </el-tooltip>
            <el-tooltip :content="$t('app.planToStart')" effect="dark" placement="bottom">
              <el-button :disabled="!row.upload_run_config || row.start_running_time && row.start_running_time > 0"
                size="mini" type="warning" @click="handleShowDialogForm('edit', 'plan_start_time', row)"
                icon="el-icon-time" round>
              </el-button>
            </el-tooltip>
            <el-tooltip :content="$t('app.start')" effect="dark" placement="bottom">
              <el-button :disabled="!row.upload_run_config || row.start_running_time && row.start_running_time > 0"
                size="mini" type="success" @click="handleStartApp(row)" icon="el-icon-video-play" round>
              </el-button>
            </el-tooltip>
            <el-tooltip :content="$t('app.runRealTimeMonitor')" effect="dark" placement="bottom">
              <el-button :disabled="!(row.start_running_time > 0 && !row.end_running_time)" size="mini" type="info"
                @click="showXterm(row)" icon="el-icon-s-platform" round>
              </el-button>
            </el-tooltip>
            <el-tooltip :content="$t('app.abort')" effect="dark" placement="bottom">
              <el-button :disabled="!row.start_running_time || row.end_running_time > 0" size="mini" type="danger"
                @click="handleAbortApp(row)" round>
                <svg-icon iconClass="video-stop"></svg-icon>
              </el-button>
            </el-tooltip>
            <el-tooltip :content="$t('app.downloadResult')" effect="dark" placement="bottom">
              <el-button :disabled="!row.end_running_time" size="mini" type="primary"
                @click="handleDownloadAppResult(row)" icon="el-icon-download" round>
              </el-button>
            </el-tooltip>
            <el-tooltip :content="$t('app.deleteApp')" effect="dark" placement="bottom">
              <el-button
                :disabled="row.start_running_time && !row.end_running_time || !row.end_running_time && row.plan_start_time > 0"
                size="mini" type="danger" @click="handleDeleteApp(row)" icon="el-icon-delete" round>
              </el-button>
            </el-tooltip>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total > 0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit"
      @pagination="getList" />

    <el-dialog :title="$t('app.' + dialogFormAction + '')" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="{ [dialogFormItem]: rules[dialogFormItem] }" :model="temp" label-position="left"
        label-width="70px" style="width: 400px; margin-left:50px;">
        <el-form-item v-if="dialogFormItem == 'name'" :label="$t('app.name')" prop="name">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item v-if="dialogFormItem == 'run_config_file'" :label="$t('app.uploadRunConfig')"
          prop="run_config_file">
          <el-upload action="string" drag :http-request="uploadRunConfig" name="run_config_file" :show-file-list="false"
            :data="{ id: temp.id }" accept=".json, .arxc">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">{{ $t('app.dragFileHereOrClickUpload') }}</div>
          </el-upload>
        </el-form-item>
        <el-form-item v-if="dialogFormItem == 'plan_start_time'" :label="$t('app.planStartTime')" prop="plan_start_time">
          <el-date-picker v-model="temp.plan_start_time" type="datetime" placeholder="Please pick a date" />
        </el-form-item>
        <el-form-item v-if="dialogFormItem == 'mark'" :label="$t('app.mark')" prop="mark">
          <el-input v-model="temp.mark" :autosize="{ minRows: 2, maxRows: 4 }" type="textarea"
            placeholder="Please input" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          {{ $t('app.cancel') }}
        </el-button>
        <el-button type="primary" @click="handleDialogFormAction()">
          {{ $t('app.confirm') }}
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :title="$t('app.runRealTimeMonitor') + ': ' + dialogXtermApp" :visible.sync="dialogXtermVisible" top="4vh"
      width="70%" @close="closeXterm">
      <div ref="terminal" id="terminal" />
    </el-dialog>

  </div>
</template>

<script>
import {
  getApp, addApp, deleteApp, updateAppName, updateAppMark, updateAppRunconfigUpload,
  updateAppRunconfigDelete, updateAppPlanstart, updateAppStart, updateAppAbort, downloadAppRusult
} from '@/api/app'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import { mapGetters } from 'vuex'
import 'xterm/css/xterm.css'
import { Terminal } from 'xterm'
import { FitAddon } from 'xterm-addon-fit'
import { AttachAddon } from 'xterm-addon-attach'

export default {
  name: 'App',
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
        name: undefined,
        mark: undefined,
        run_time_error: undefined
      },
      showOwner: false,
      showUpdateTime: false,
      showCreateTime: true,
      temp: {
        id: undefined,
        name: undefined,
        owner: undefined,
        upload_run_config: undefined,
        plan_start_time: undefined,
        start_running_time: undefined,
        end_running_time: undefined,
        abort_running_time: undefined,
        run_time_error: undefined,
        mark: undefined,
        update_time: undefined,
        create_time: undefined
      },
      socket: null,
      xterm: null,
      dialogXtermVisible: false,
      dialogXtermApp: '',
      dialogFormVisible: false,
      dialogFormItem: 'name',
      dialogFormAction: '',
      rules: {
        name: [{ required: true, message: 'title is required', trigger: 'blur' }],
        plan_start_time: [{ type: 'date', required: true, message: 'timestamp is required', trigger: 'change' }],
        mark: [{ required: false, message: 'type is required', trigger: 'blur' }]
      },
      downloadLoading: false
    }
  },
  computed: {
    ...mapGetters([
      'token',
    ])
  },
  created() {
    this.getList()
    this.freshTimer = setInterval(() => {
      this.getList(false)
    }, 15000)
  },
  destroyed() {
    clearInterval(this.freshTimer)
  },
  methods: {
    getList(setLoading = true) {
      if (setLoading) this.listLoading = true
      getApp(this.listQuery).then(response => {
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
    resetTemp() {
      this.temp = {
        id: undefined,
        name: '',
        owner: undefined,
        upload_run_config: undefined,
        plan_start_time: undefined,
        start_running_time: undefined,
        end_running_time: undefined,
        abort_running_time: undefined,
        run_time_error: undefined,
        mark: '',
        update_time: undefined,
        create_time: undefined
      }
    },
    handleCellDbClick(row, column, cell, event) {
      console.log(row, column, cell, event)
      const item = column.property
      if (item === 'name' || item === 'mark') {
        this.handleShowDialogForm('edit', item, row)
      }
    },
    handleShowDialogForm(action, item, row) {
      if (action === 'create') {
        this.resetTemp()
        this.dialogFormAction = 'create'
        this.dialogFormItem = 'name'
        this.dialogFormVisible = true
        this.$nextTick(() => {
          this.$refs['dataForm'].clearValidate()
        })
      } else if (action === 'edit') {
        this.temp = Object.assign({}, row) // copy obj
        console.log(row)
        for (const k in this.temp) {
          if (String(k).endsWith('time')) {
            this.temp[k] = this.temp[k] ? new Date(this.temp[k]) : new Date(new Date().getTime() + 5 * 60 * 1000)
          }
        }
        this.dialogFormAction = 'edit'
        this.dialogFormItem = item
        this.dialogFormVisible = true
        this.$nextTick(() => {
          this.$refs['dataForm'].clearValidate()
        })
      }
    },
    handleDialogFormAction() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          if (this.dialogFormAction === 'create') {
            const data = { data: { name: this.temp.name } }
            addApp(data).then((res) => {
              this.notify(res)
              this.handleDataUpdate()
            }, (err) => {
              this.notify(null, err)
            })
          } else if (this.dialogFormAction === 'edit') {
            if (this.dialogFormItem === 'name') {
              const data = { data: { id: this.temp.id, name: this.temp.name } }
              updateAppName(data).then((res) => {
                this.notify(res)
                this.handleDataUpdate()
              }, (err) => {
                this.notify(null, err)
              })
            } else if (this.dialogFormItem === 'mark') {
              const data = { data: { id: this.temp.id, mark: this.temp.mark } }
              updateAppMark(data).then((res) => {
                this.notify(res)
                this.handleDataUpdate()
              }, (err) => {
                this.notify(null, err)
              })
            } else if (this.dialogFormItem === 'plan_start_time') {
              const data = { data: { id: this.temp.id, plan_start_time: this.temp.plan_start_time.getTime() } }
              updateAppPlanstart(data).then((res) => {
                this.notify(res)
                this.handleDataUpdate()
              }, (err) => {
                this.notify(null, err)
              })
            } else {
              this.handleDataUpdate()
            }
          } else {
            this.handleDataUpdate()
          }
        }
      })
    },
    handleDataUpdate() {
      this.dialogFormVisible = false
      this.getList()
    },
    uploadRunConfig(param) {
      console.log(param)
      const formData = new FormData()
      formData.append('run_config_file', param.file)
      updateAppRunconfigUpload(this.temp.id, formData).then(res => {
        this.notify(res)
        this.handleDataUpdate()
      }).catch(err => {
        this.notify(null, err)
      })
    },
    handleStartApp(row) {
      const data = { data: { id: row.id } }
      updateAppStart(data).then((res) => {
        this.notify(res)
        this.handleDataUpdate()
      }, (err) => {
        this.notify(null, err)
      })
    },
    handleAbortApp(row) {
      const data = { data: { id: row.id } }
      updateAppAbort(data).then((res) => {
        this.notify(res)
        this.handleDataUpdate()
      }, (err) => {
        this.notify(null, err)
      })
    },
    handleDownloadAppResult(row) {
      const data = { id: row.id }
      downloadAppRusult(data).then((res) => {
        this.notify(res)
        this.handleDataUpdate()
      }, (err) => {
        this.notify(null, err)
      })
    },
    handleDeleteApp(row) {
      this.$confirm(this.$t('app.confirm') + ' ' + this.$t('app.deleteApp') + ': ' + row.id + ' ?', 'Tip', {
        confirmButtonText: this.$t('app.confirm'),
        cancelButtonText: this.$t('app.cancel'),
        type: 'warning'
      }).then(() => {
        const data = { data: { id: row.id } }
        deleteApp(data).then((res) => {
          this.notify(res)
          this.handleDataUpdate()
        }, (err) => {
          this.notify(null, err)
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: this.$t('app.cancel')
        })
      })
    },
    showXterm(row) {
      const ACCEPT_SIGNAL = '^^^^^^^^^^ACCEPT^^^^^^^^^^'
      const REFUSE_SIGNAL = '^^^^^^^^^^REFUSE^^^^^^^^^^'
      this.xterm = new Terminal({
        rendererType: "canvas", //渲染类型
        rows: 40, //行数
        cols: 130, // 不指定行数，自动回车后光标从下一行开始
        convertEol: true, //启用时，光标将设置为下一行的开头
        // scrollback: 50, //终端中的回滚量
        disableStdin: true, //是否应禁用输入
        windowsMode: true, // 根据窗口换行
        cursorStyle: "underline", //光标样式
        cursorBlink: true, //光标闪烁
        theme: {
          foreground: "#ECECEC", //字体
          background: "#000000", //背景色
          cursor: "help", //设置光标
          lineHeight: 20,
        },
      })
      this.socket = new WebSocket('ws://localhost:8765/api/app/appmonitor/' + row.id)   // 带 token 发起连接
      this.socket.onopen = () => {
        this.socket.send(this.token)  // auth
        this.socket.onmessage = (event) => {
          let data = event.data
          if (data == ACCEPT_SIGNAL) {
            this.dialogXtermVisible = true
            this.dialogXtermApp = row.name
            // const attachAddon = new AttachAddon(this.socket)
            // const fitAddon = new FitAddon() // 全屏插件
            // this.term.loadAddon(attachAddon)
            // this.term.loadAddon(fitAddon)
            this.$nextTick(() => {
              this.xterm.open(document.getElementById('terminal'))
              // fitAddon.fit()
              this.xterm.focus()
            })
          } else {
            if (this.xterm) {
              this.xterm.write(data)
            } else {
              this.closeXterm(false)
            }
          }
        }
      }
      this.socket.onclose = () => {
        // this.$message({
        //   type: 'info',
        //   message: 'Connect close'
        // })
        this.closeXterm(false)
      }
      this.socket.onerror = (err) => {
        this.$message({
          type: 'error',
          message: 'Connect error:' + err
        })
        this.closeXterm(false)
      }
    },
    closeXterm(closeVisible = true) {
      if (this.socket) this.socket.close()
      if (closeVisible) this.dialogXtermVisible = false
      this.xterm.dispose()
      this.socket = null
    },
    tableRowClassName({ row, rowIndex }) {
      if (row.start_running_time && !row.end_running_time) {
        return 'running-row'
      } else if (row.run_time_error !== '') {
        return 'danger-row'
      } else if (row.abort_running_time) {
        return 'warning-row'
      } else if (row.end_running_time) {
        return 'success-row'
      }else if (row.upload_run_config){
        return 'ready-row'
      }
      return ''
    },
    notify(res = null, err = null) {
      if (res) {
        this.$notify({
          title: res.flag ? this.$t('app.success') : this.$t('app.fail'),
          message: res.data || '',
          type: res.flag ? 'success' : 'error',
          duration: 2000
        })
      } else if (err) {
        this.$notify({
          title: this.$t('app.fail'),
          message: err.data,
          type: 'error',
          duration: 2000
        })
      }
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['id', 'name', 'owner', 'plan_start_time', 'start_running_time', 'end_running_time', 'abort_running_time', 'run_time_error', 'mark', 'update_time', 'create_time']
        const filterVal = ['id', 'name', 'owner', 'plan_start_time', 'start_running_time', 'end_running_time', 'abort_running_time', 'run_time_error', 'mark', 'update_time', 'create_time']
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
    timestampFormatter(row, col, cellValue, index) {
      return parseTime(cellValue)
    },
    booleanFormatter(row, col, cellValue, index) {
      return cellValue ? this.$t('app.true') : this.$t('app.false')
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

::v-deep .el-table .running-row {
  background: #ffc9c9;
}

::v-deep .el-table .danger-row {
  background: #ffc9c9c8;
}

::v-deep .el-table .ready-row {
  background: rgba(255, 232, 232, 0.898);
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
