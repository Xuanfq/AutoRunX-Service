<template>
    <div ref="root" class="root">
        <div v-if="false" id="header" class="header">
            <el-row type="flex" :gutter="20">
                <el-col :span="8" class="header-left">
                    <img src="" alt="" />
                </el-col>
                <el-col :span="8" class="header-center">
                    <span class="logo-title">AutoRunX</span>
                </el-col>
                <el-col :span="8" class="header-right">
                    <div class="header-item">
                    </div>
                    <div>
                        <a href="https://github.com/Xuanfq/AutoRunX-Creator" target="_blank">
                            <i class="el-icon-github" style="font-size: 32px;"></i>
                        </a>
                    </div>
                </el-col>
            </el-row>
        </div>
        <div ref="arxbox" >
            <arxgraph :style="'position: fixed;top:' + (tagsView ? '84px' : '50px') + ';left: 0;right: 0;bottom: 0;'" ref="arx"
                :autoResize="false" name="AutoRunXGraphPreview" :lang="language" :initData="graphInitData"
                :onRequestAddNode="onRequestAddNode" :onRequestEditNodeAttr="onRequestEditNodeAttr"
                :onRequestChangeNodeLang="onRequestChangeNodeLang" :onRequestShowMessage="onRequestShowMessage" />
        </div>
        <!-- Add Node Dialog -->
        <el-dialog :title="$t('creator.FindNode')" :visible="isShowSearchNodeDialog" width="60%"
            @close="isShowSearchNodeDialog = false" center>
            <el-input :placeholder="$t('creator.EnterAKeywordToSearch')" v-model="searchNodeFilterText">
            </el-input>
            <el-row :gutter="0">
                <el-col :span="12">
                    <div class="dialog-left">
                        <el-tree :data="searchNodeData" :props="searchNodeDefaultProps" :default-expand-all="false"
                            :filter-node-method="triggerSearchNodeFilterNode" :expand-on-click-node="true" accordion
                            @node-click="triggerSearchNodeClickNode" @node-contextmenu="triggerSearchNodeRightClickNode"
                            ref="searchNodeTree">
                        </el-tree>
                    </div>
                </el-col>
                <el-col :span="12" v-loading="searchNodeSelectNodeDocLoading">
                    <div class="dialog-right">
                        <div v-if="!searchNodeSelectNode || !searchNodeSelectNodeDoc">
                            <!-- <el-empty
                                :description="!searchNodeSelectNode ? $t('creator.PleaseSelectNode') : $t('creator.NoNode') + '「' + searchNodeSelectNode.name + '」' + $t('creator.sIntro')">
                            </el-empty> -->
                        </div>
                        <div v-if="searchNodeSelectNode && searchNodeSelectNodeDoc">
                            <vue-markdown :source="searchNodeSelectNodeDoc" :breaks="true" :typographer="true"
                                :linkify="true" :highlight="true"></vue-markdown>
                        </div>
                    </div>
                </el-col>
            </el-row>
            <span slot="footer" class="dialog-footer">
                <el-button @click="isShowSearchNodeDialog = false">{{ $t('creator.Cancel') }}</el-button>
                <el-button :disabled="!searchNodeSelectNode" type="primary"
                    @click="triggerSearchNodeRightClickNode(null, searchNodeSelectNode)">{{ $t('creator.Confirm') }}</el-button>
            </span>
        </el-dialog>
        <!-- Alter Node Attr Dialog -->
        <el-dialog :title="$t('creator.EditProperties')" :visible="isShowEditNodeAttrDrawer" width="60%"
            @close="triggerCloseEditNodeAttrDrawer">
            <el-row :gutter="0">
                <el-col :span="12">
                    <div v-if="editNodeAttrData" class="dialog-left attribute-box">
                        <div class="attribute-title">{{ $t('creator.Input') }}</div>
                        <div v-for="item, index in editNodeAttrData.input_type" :key="index">
                            <div v-if="item.indexOf('bool') > -1" class="attribute-key-value">
                                <div>
                                    <div>{{ editNodeAttrData.input_intro[index] }}</div>
                                </div>
                                <div style="width: 150px;">
                                    <el-switch v-model="editNodeAttrData.input[index]" active-text="True"
                                        inactive-text="False">
                                    </el-switch>
                                </div>
                            </div>
                            <div v-else-if="item.indexOf('int') > -1" class="attribute-key-value">
                                <div>
                                    <div>{{ editNodeAttrData.input_intro[index] }}</div>
                                </div>
                                <div style="width: 150px;">
                                    <el-input-number style="width: 150px;" v-model="editNodeAttrData.input[index]"
                                        size="small" :precision="0"></el-input-number>
                                </div>
                            </div>
                            <div v-else-if="item.indexOf('float') > -1 || item.indexOf('number') > -1"
                                class="attribute-key-value">
                                <div>
                                    <div>{{ editNodeAttrData.input_intro[index] }}</div>
                                </div>
                                <div style="width: 150px;">
                                    <el-input-number style="width: 150px;" v-model="editNodeAttrData.input[index]"
                                        size="small" :precision="2" :step="0.5"></el-input-number>
                                </div>
                            </div>
                            <div v-else class="attribute-key-value">
                                <div>
                                    <div>{{ editNodeAttrData.input_intro[index] }}</div>
                                </div>
                                <div style="width: 150px;">
                                    <el-input v-model="editNodeAttrData.input[index]"
                                        :placeholder="$t('creator.PleaseEnterAString')" type="textarea"></el-input>
                                </div>
                            </div>
                        </div>
                    </div>
                </el-col>
                <el-col :span="12" v-loading="searchNodeSelectNodeDocLoading">
                    <div class="dialog-right">
                        <div v-if="!searchNodeSelectNode || !searchNodeSelectNodeDoc">
                            <!-- <el-empty
                                :description="!searchNodeSelectNode ? $t('creator.PleaseSelectNode') : $t('creator.NoNode') + '「' + searchNodeSelectNode.name + '」' + $t('creator.sIntro')">
                            </el-empty> -->
                        </div>
                        <div v-if="searchNodeSelectNode && searchNodeSelectNodeDoc">
                            <vue-markdown :source="searchNodeSelectNodeDoc" :breaks="true" :typographer="true"
                                :linkify="true" :highlight="true"></vue-markdown>
                        </div>
                    </div>
                </el-col>
            </el-row>
        </el-dialog>
    </div>
</template>
  
<script>
import { mapGetters } from 'vuex'
import arxgraph from '../../components/AutoRunXGraph'
import { getNodeConfig, getNodeReadme, addNodes, syncNodes, deleteNodes } from '@/api/node'

export default {
    name: 'Creator',
    components: {
        arxgraph,
    },
    watch: {
        searchNodeFilterText(val) {
            this.$refs.searchNodeTree.filter(val);
        },
        language(val, valOld) {
            this.changeLang(val)
        }
    },
    data() {
        return {
            // lang: 'zh',
            // Search Node Dialog
            isShowSearchNodeDialog: false,
            searchNodeSelectNode: null,
            searchNodeSelectNodeDoc: null,
            searchNodeSelectNodeDocLoading: false,
            searchNodeFilterText: '',
            searchNodeDefaultProps: { label: 'name', children: 'nodeList' },
            searchNodeData: [{
                type: 'dtio',
                name: '输入输出节点',
                zname: '输入输出节点',
                ename: 'Input/Output Node',
                nodeList: [],
            }, {
                type: 'dtpc',
                name: '数据处理节点',
                zname: '数据处理节点',
                ename: 'Data Processing Node',
                nodeList: [],
            }, {
                type: 'ctrl',
                name: '程序控制节点',
                zname: '程序控制节点',
                ename: 'Program Control Node',
                nodeList: [],
            }, {
                type: 'func',
                name: '程序功能节点',
                zname: '程序功能节点',
                ename: 'Program Function Node',
                nodeList: [],
            }, {
                type: 'evtx',
                name: '事件触发节点',
                zname: '事件触发节点',
                ename: 'Event Emit Node',
                nodeList: [],
            }, {
                type: 'evrx',
                name: '事件发生节点',
                zname: '事件发生节点',
                ename: 'Event Start Node',
                nodeList: [],
            }],
            // Edit Node Attr Dialog
            isShowEditNodeAttrDrawer: false,
            editNodeAttrData: null,
            graph: null,
            graphInitData: {
                nodes: [{
                    "id": "node-start",
                    "name": "开始",
                    "node_name": "evrx-start",
                    "node_type": "evrx",
                    "pre_edge_id": [],
                    "nxt_edge_id": [
                        ""
                    ],
                    "nxt_edge_id_intro": [
                        "下一步: 执行"
                    ],
                    "input": {},
                    "input_type": {},
                    "input_intro": {},
                    "output": {},
                    "output_type": {},
                    "output_intro": {}
                }, {
                    "id": "node-end",
                    "name": "结束",
                    "node_name": "evtx-end",
                    "node_type": "evtx",
                    "pre_edge_id": [],
                    "nxt_edge_id": [],
                    "input": {},
                    "input_type": {},
                    "input_intro": {},
                    "output": {},
                    "output_type": {},
                    "output_intro": {}
                }],
                edges: []
            },
            // ARXGraph Api
            arxAddNode: null,
            arxEditNodeAttr: null,
        }
    },
    computed: {
        ...mapGetters([
            'language',
            'sidebar'
        ]),
        tagsView: {
            get() {
                return this.$store.state.settings.tagsView
            },
            set(val) {
                this.$store.dispatch('settings/changeSetting', {
                    key: 'tagsView',
                    value: val
                })
            }
        },
    },
    created() {
        this.refresh()
    },
    mounted() {
        
    },
    methods: {
        onRequestAddNode(data, addNode) {
            this.rqAddNode = data
            this.arxAddNode = addNode
            this.triggerOpenSearchNodeDialog()
        },
        onRequestEditNodeAttr(data, editNodeAttr) {
            this.editNodeAttrData = data
            this.arxEditNodeAttr = editNodeAttr
            this.isShowEditNodeAttrDrawer = true
            this.triggerSearchNodeClickNode(this.editNodeAttrData)
        },
        onRequestChangeNodeLang(data, editNodeAttrdNode) {
            let params = { lang: this.language=='zh'?'zh':'en', node_name: data.node_name }
            getNodeConfig(params).then((res) => {
                if (res.flag) {
                    if (res.data.length > 0) {
                        data.name = res.data[0].name
                        data.nxt_edge_id_intro = res.data[0].nxt_edge_id_intro
                        data.input_intro = res.data[0].input_intro
                        data.output_intro = res.data[0].output_intro
                        editNodeAttrdNode(data)
                    } else {
                        this.$message({
                            type: 'error',
                            message: 'Server Error'
                        })
                    }
                } else {
                    this.$message({
                        type: 'error',
                        message: res.data
                    })
                }
            }, (err) => {
                this.$message({
                    type: 'error',
                    message: err.data
                })
            })
        },
        onRequestShowMessage(data) {
            this.$message(data)
        },
        // =============================================== language ==================================================
        changeLang(lang) {
            this.refresh()
        },
        // =============================================== refresh ==================================================
        refresh() {
            this.searchNodeData[0]['nodeList'] = []
            this.searchNodeData[1]['nodeList'] = []
            this.searchNodeData[2]['nodeList'] = []
            this.searchNodeData[3]['nodeList'] = []
            this.searchNodeData[4]['nodeList'] = []
            this.searchNodeData[5]['nodeList'] = []
            if(this.language=='zh'){
                for(let i=0;i<6;i++){
                    this.searchNodeData[i].name=this.searchNodeData[i].zname
                }
            }else{
                for(let i=0;i<6;i++){
                    this.searchNodeData[i].name=this.searchNodeData[i].ename
                }
            }
            let params = { lang: this.language=='zh'?'zh':'en' }
            getNodeConfig(params).then((res) => {
                if (res.flag) {
                    let data = res.data
                    data.forEach((item, index) => {
                        if (item.node_type == 'dtio') {
                            this.searchNodeData[0]['nodeList'].push(item)
                        } else if (item.node_type == 'dtpc') {
                            this.searchNodeData[1]['nodeList'].push(item)
                        } else if (item.node_type == 'ctrl') {
                            this.searchNodeData[2]['nodeList'].push(item)
                        } else if (item.node_type == 'func') {
                            this.searchNodeData[3]['nodeList'].push(item)
                        } else if (item.node_type == 'evtx') {
                            this.searchNodeData[4]['nodeList'].push(item)
                        } else if (item.node_type == 'evrx') {
                            this.searchNodeData[5]['nodeList'].push(item)
                        }
                    })
                } else {
                    this.$message({
                        type: 'error',
                        message: res.data
                    })
                }
            }, (err) => {
                this.$message({
                    type: 'error',
                    message: err.data
                })
            })
        },
        // =============================================== find node ==================================================
        triggerSearchNodeFilterNode(value, data) {
            if (!value) return true;
            return data.name.indexOf(value) !== -1 || (data.node_type && data.node_type.indexOf(value) !== -1);
        },
        triggerSearchNodeRightClickNode(e, data, node) {
            if (!data.nodeList) {
                // console.log(data)
                data = JSON.parse(JSON.stringify(data))
                data.id = `node-${data.node_name}-${Date.now()}-${(Math.random() * 1000000 + "").substring(0, 4)}`
                data.x = this.rqAddNode.x
                data.y = this.rqAddNode.y
                // console.log(data.id)
                this.arxAddNode(data)
                this.isShowSearchNodeDialog = false
            }
        },
        triggerSearchNodeClickNode(data, node, vueobj) {
            if (!data.nodeList) {
                // console.log(data)
                data = JSON.parse(JSON.stringify(data))
                this.searchNodeSelectNode = data
                this.searchNodeSelectNodeDocLoading = true
                let params = { lang: this.language=='zh'?'zh':'en', node_name: data.node_name }
                getNodeReadme(params).then((res) => {
                    console.log(res)
                    if (res.flag) {
                        if (res.data.length > 0) {
                            this.searchNodeSelectNodeDoc = res.data[0].readme
                        } else {
                            this.$message({
                                type: 'error',
                                message: 'Server Error'
                            })
                        }
                    } else {
                        this.$message({
                            type: 'error',
                            message: res.data
                        })
                    }
                    this.searchNodeSelectNodeDocLoading = false
                }, (err) => {
                    this.$message({
                        type: 'error',
                        message: err.data
                    })
                    this.searchNodeSelectNodeDocLoading = false
                })
            }
        },
        triggerOpenSearchNodeDialog() {
            this.searchNodeSelectNode = null
            this.searchNodeSelectNodeDoc = null
            this.isShowSearchNodeDialog = true
        },
        triggerCloseEditNodeAttrDrawer() {
            this.arxEditNodeAttr(this.editNodeAttrData)
            this.isShowEditNodeAttrDrawer = false
        },
    }
}
</script>
<style scoped>
.root {
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
    overflow: hidden;
    /* overflow: hidden; */
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
        "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
    color: #606266;
    user-select: none;
}

/* el-menu */
.header-menu .el-menu.el-menu--horizontal {
    border-bottom: 0px solid #e6e6e6;
}

.header-menu .el-menu--horizontal>.el-submenu .el-submenu__title {
    height: 33px;
    line-height: 15px;
    border-bottom: 0px solid rgba(0, 0, 0, 0);
    display: flex;
    align-items: center;
    color: #606266;
}

.header-menu .el-submenu__title {
    padding: 0;
}

.header-menu .el-submenu.is-opened>.el-submenu__title .el-submenu__icon-arrow {
    display: none;
}

.header-menu .el-submenu>.el-submenu__title .el-submenu__icon-arrow {
    display: none;
}

.header-menu .el-menu--horizontal>.el-submenu.is-active .el-submenu__title {
    border-bottom: 0px solid #409EFF;
    color: #303133;
}

#header {
    position: relative;
    height: 37px;
    border-bottom: 1px solid #dfe2e5;
    padding: 11px 0;
    background-color: white;
    color: #606266;
}

.header-left {
    margin: auto 0;
    margin-left: 16px;
    display: flex;
    justify-content: start;
    align-items: center;
}

.header-left .header-item {
    margin-left: 16px;
}

.header-center {
    margin: auto;
    display: flex;
    justify-content: center;
    align-items: center;
}

.header-right {
    margin: auto 0;
    margin-right: 16px;
    display: flex;
    justify-content: end;
    align-items: center;
}

.header-right .header-item {
    margin-right: 16px;
}

.header-right .header-item>:hover,
.header-left .header-item>:hover,
i:hover {
    color: rgb(127, 55, 183);
}


.header-left .header-item:hover,
.header-center .header-item:hover,
.header-right .header-item:hover {
    border-bottom: 0px solid #606266;
}

.header-dropdown-item {
    width: 150px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.header-left img,
.header-right img {
    margin: auto 0;
    width: 33px;
    height: 33px;
}

.logo-title {
    font-weight: bold;
    font-size: x-large;
}

.arxbox.hideSidebar.hideTagsView {
    position: fixed;
    top: 50px;
    left: 54px;
    right: 0;
    bottom: 0;
    display: flex;
    justify-content: center;
    align-items: center;
}

.arxbox.hideSidebar {
    position: fixed;
    top: 84px;
    left: 54px;
    right: 0;
    bottom: 0;
    display: flex;
    justify-content: center;
    align-items: center;
}

.arxbox.hideTagsView {
    position: fixed;
    top: 50px;
    left: 210px;
    right: 0;
    bottom: 0;
    display: flex;
    justify-content: center;
    align-items: center;
}

.arxbox {
    position: fixed;
    top: 84px;
    left: 210px;
    right: 0;
    bottom: 0;
    display: flex;
    justify-content: center;
    align-items: center;
}

.attribute-box {
    padding: 25px;
}

.attribute-box .attribute-title {
    font-size: medium;
    font-weight: 600;
}

.attribute-box .attribute-title:nth-child(n+2) {
    margin-top: 25px;
}

.dialog-left {
    border-right: 1px solid lightgrey;
    padding: 0 20px;
    margin-top: 25px;
    height: 350px;
    overflow-y: scroll;
}

.dialog-right {
    border-left: 1px solid lightgrey;
    padding: 0 20px;
    margin-top: 25px;
    height: 350px;
    overflow-y: scroll;
}
</style>
  