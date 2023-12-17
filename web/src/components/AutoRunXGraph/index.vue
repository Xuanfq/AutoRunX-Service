<template>
    <div ref="arxgraph" :id="id" class="container" :style="customStyle">
        <div v-if="minimapShow" :id="minimapId" class="minimap" :style="minimapStyle">
        </div>
        <div v-if="toolbarShow" class="toolbar horizontal topcenter">
            <div v-if="toolbar.fileGroup.show" class="toolbar-group ">
                <div v-if="toolbar.fileGroup.importLocalDataShow" class="toolbar-item svg-icon" @click="importLocalData">
                    <img class="toolbar-item-image" src="./index/icons/svg/folder.svg" alt="">
                </div>
                <div v-if="toolbar.fileGroup.exportCloudDataShow" class="toolbar-item svg-icon" @click="exportCloudData">
                    <img class="toolbar-item-image" src="./index/icons/svg/save-cloud.svg" alt="">
                </div>
                <div v-if="toolbar.fileGroup.exportLocalDataShow" class="toolbar-item svg-icon" @click="exportLocalData">
                    <img class="toolbar-item-image" src="./index/icons/svg/save-local.svg" alt="">
                </div>
                <div v-if="toolbar.fileGroup.exportLocalPictureShow" class="toolbar-item svg-icon"
                    @click="g6DownloadFullImage">
                    <img class="toolbar-item-image" src="./index/icons/svg/picture.svg" alt="">
                </div>
            </div>
            <div v-if="toolbar.viewGroup.show" class="toolbar-group ">
                <div class="toolbar-item svg-icon" @click="g6ZoomIn">
                    <img class="toolbar-item-image" src="./index/icons/svg/add.svg" alt="">
                </div>
                <div class="toolbar-item svg-icon" @click="g6ZoomOut">
                    <img class="toolbar-item-image" src="./index/icons/svg/sub.svg" alt="">
                </div>
                <div class="toolbar-item svg-icon" @click="g6FocusItem">
                    <img class="toolbar-item-image" src="./index/icons/svg/locate.svg" alt="">
                </div>
                <div class="toolbar-item svg-icon" @click="g6FitView">
                    <img class="toolbar-item-image" src="./index/icons/svg/fitview.svg" alt="">
                </div>
                <div class="toolbar-item svg-icon" @click="g6FitCenter">
                    <img class="toolbar-item-image" src="./index/icons/svg/home.svg" alt="">
                </div>
            </div>
            <div v-if="toolbar.graphGroup.show" class="toolbar-group ">
                <div class="toolbar-item svg-icon" @click="undo">
                    <img class="toolbar-item-image" src="./index/icons/svg/undo.svg" alt="">
                </div>
                <div class="toolbar-item svg-icon" @click="redo">
                    <img class="toolbar-item-image" src="./index/icons/svg/redo.svg" alt="">
                </div>
            </div>
        </div>
    </div>
</template>
  
<script>
import { Utils } from './index/index.js'
import ARXGraph from "./AutoRunXGraph/index"

export default {
    name: 'AutoRunXGraph',
    props: {
        lang: {
            type: String,
            default: 'zh',
        },
        name: {
            type: String,
            default: 'AutoRunXGraph',
        },
        id: {
            type: String,
            default: () => {
                return Math.random().toString()
            }
        },
        graphWidth: {
            type: Number,
            default: () => {
                return null
            }
        },
        graphHight: {
            type: Number,
            default: () => {
                return null
            }
        },
        initData: {
            type: Object,
            default: () => {
                return {}
            }
        },
        customStyle: {
            type: Object,
            default: () => {
                return {
                    'background-color': ''
                }
            }
        },
        minimapShow: {
            type: Boolean,
            default: true,
        },
        minimapStyle: {
            type: Object,
            default: () => {
                return {
                }
            }
        },
        toolbarShow: {
            type: Boolean,
            default: true,
        },
        toolbar: {
            type: Object,
            default: () => {
                return {
                    fileGroup: {
                        show: true,
                        importLocalDataShow: true,
                        importLocalDataFileFormat: '.arxc,.json',
                        exportLocalDataShow: true,
                        exportLocalDataFileFormat: '.arxc',
                        exportCloudDataShow: false,
                        exportCloudDataCallback: null,  //params: config
                        exportLocalPictureShow: true,
                    },
                    viewGroup: {
                        show: true,
                        fitViewPadding: [100, 50],
                    },
                    graphGroup: {
                        show: true,
                    }
                }
            }
        },
        textWaterMarker: {
            type: Array,
            default: () => {
                return []
            }
        },
        autoResize: {
            type: Boolean,
            default: true
        },
        onInitComplete: {
            type: Function,  //param: graph
            default: null
        },
        onRequestAddNode: {
            type: Function,  //param: data, addNodeCallback
            default: null
        },
        onRequestEditNodeAttr: {
            type: Function,  //param: data, editNodeAttrCallback
            default: null
        },
        onRequestChangeNodeLang: {
            type: Function,  //param: data, editNodeAttrCallback
            default: null
        },
        onRequestShowMessage: {
            type: Function,  //param: data
            default: null
        },
    },
    watch: {
        lang(val, oldV) {
            if (val == 'zh' || val == 'en' || val == 'es' || val == 'ja') {
                this.changeLang(val)
            }
        },
        graphWidth(val, oldV) {
            this.g6ChangeSize()
        },
        graphHight(val, oldV) {
            this.g6ChangeSize()
        },
        textWaterMarker(val, oldV) {
            this.g6SetTextWaterMarker()
        },
    },
    data() {
        return {
            minimapId: Math.random().toString(),
            graph: null,
            observer: null,
        }
    },
    computed: {
    },
    mounted() {
        this.graph = ARXGraph.initGraph(this.id, this.graphWidth, this.graphHight, this.minimapId, this.initData)
        if (this.onInitComplete) {
            this.onInitComplete(this.graph)
        }
        // ========================= AutoRunXGraph API Event =========================
        ARXGraph.Event.on("rqAddNode#" + this.id, this, (data) => {
            if (this.onRequestAddNode) {
                this.onRequestAddNode(data, this.addNode)
            }
        })
        ARXGraph.Event.on("rqEditNodeAttr#" + this.id, this, (data) => {
            if (this.onRequestEditNodeAttr) {
                this.onRequestEditNodeAttr(data, this.editNodeAttr)
            }
        })
        ARXGraph.Event.on("rqChangeNodeLang#" + this.id, this, (data) => {
            if (this.onRequestChangeNodeLang) {
                this.onRequestChangeNodeLang(data, this.editNodeAttr)
            }
        })
        ARXGraph.Event.on("rqShowMessage#" + this.id, this, (data) => {
            if (this.onRequestShowMessage) {
                this.onRequestShowMessage(data)
            }
        })
        // ========================= AutoRunXGraph ResizeObserver =========================
        this.observer = new ResizeObserver(() => {
            const width = this.$refs.arxgraph.offsetWidth
            const height = this.$refs.arxgraph.offsetHeight
            if (this.autoResize) {
                this.g6ChangeSize(width, height)
            }
        })
        this.observer.observe(this.$refs.arxgraph, { box: "border-box" })
        // ========================= Others =========================
        this.g6SetTextWaterMarker()
    },
    beforeDestroy() {
        if (this.observer) {
            this.observer.disconnect()
        }
    },
    methods: {
        // ========================= G6 Source API About =========================
        g6ZoomIn() {
            const zoom = this.graph.getZoom()
            this.graph.zoomTo(zoom + 0.1)
        },
        g6ZoomOut() {
            const zoom = this.graph.getZoom()
            this.graph.zoomTo(zoom - 0.1)
        },
        g6FocusItem() {
            const nodes = this.graph.findAllByState('node', 'selected');
            if (nodes.length > 0) {
                this.graph.focusItem(nodes[0], true, {
                    easing: 'easeCubic',
                    duration: 400,
                })
            }
        },
        g6FitView() {
            this.graph.fitView(this.toolbar.viewGroup.fitViewPadding)
        },
        g6FitCenter() {
            this.graph.fitCenter()
        },
        g6ChangeSize(width, height) {
            if (width && height) {
                this.graph.changeSize(width, height)
            } else {
                this.graph.changeSize(this.graphWidth, this.graphHight)
            }
        },
        g6SetTextWaterMarker() {
            this.graph.setTextWaterMarker(this.textWaterMarker)
        },
        g6DownloadFullImage() {
            const imageConfig = { padding: [50, 100, 50, 100] }
            if (this.customStyle['background-color']) {
                imageConfig['backgroundColor'] = this.customStyle['background-color']
            }
            this.graph.downloadFullImage(this.name, 'image/png', imageConfig);
        },
        // ========================= AutoRunXGraph API About =========================
        // ========== Event
        addNode(data) {
            ARXGraph.Event.emit("addNode#" + this.id, data)
        },
        editNodeAttr(data) {
            ARXGraph.Event.emit("editNodeAttr#" + this.id, data)
        },
        // ========== Not Event
        saveConfig() {
            return ARXGraph.saveConfig(null, null, this.id)  //return config
        },
        loadConfig(config) {
            return ARXGraph.loadConfig(this.id, config)  //return config
        },
        changeLang(lang) {
            ARXGraph.changeLang(lang)
        },
        undo() {
            ARXGraph.undo(this.id)
        },
        redo() {
            ARXGraph.redo(this.id)
        },
        // ========================= Additional Function =========================
        importLocalData() {
            Utils.File.uploadFile(this.toolbar.fileGroup.importLocalDataFileFormat, (data) => {
                const config = JSON.parse(data)
                this.loadConfig(config)
            })
        },
        exportLocalData() {
            const config = this.saveConfig()
            Utils.File.downloadFile(this.name + this.toolbar.fileGroup.exportLocalDataFileFormat, JSON.stringify(config))
        },
        exportCloudData() {
            const config = this.saveConfig()
            if (this.toolbar.fileGroup.exportCloudDataCallback) {
                this.toolbar.fileGroup.exportCloudDataCallback(config)
            }
        },
    }
}
</script>
  
<style scoped>
.container {
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden;
}

.minimap {
    position: absolute;
    top: 16px;
    right: 16px;
    background-color: rgba(44, 44, 44, 0.175);
    -webkit-box-shadow: 0px 0px 13px 9px rgba(62, 66, 66, 0.07);
    -moz-box-shadow: 0px 0px 13px 9px rgba(62, 66, 66, 0.07);
    box-shadow: 0px 0px 13px 9px rgba(62, 66, 66, 0.07);
}

.toolbar {
    user-select: none;
}

.toolbar.horizontal.topleft {
    position: absolute;
    top: 16px;
    left: 16px;
}

.toolbar.horizontal.topcenter {
    position: absolute;
    top: 16px;
    left: 50%;
    transform: translateX(-50%);
}

.toolbar.horizontal.bottomleft {
    position: absolute;
    top: 100%;
    left: 16px;
    transform: translateY(-56px);
}

.toolbar.horizontal.bottomcenter {
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%) translateY(-56px);
}

.toolbar.vertical.lefttop {
    position: absolute;
    top: 16px;
    left: 16px;
}

.toolbar.vertical.leftcenter {
    position: absolute;
    top: 50%;
    left: 16px;
    transform: translateY(-50%);
}

.toolbar.vertical.rightcenter {
    position: absolute;
    top: 50%;
    left: 100%;
    transform: translateX(-56px) translateY(-50%);
}

.toolbar.horizontal .toolbar-group {
    display: inline-block;
    padding: 5px 0;
    margin-right: 8px;
    margin-bottom: 8px;
    border-radius: 3px;
    background-color: white;
    -webkit-box-shadow: 0px 0px 13px 3px rgba(62, 66, 66, 0.07);
    -moz-box-shadow: 0px 0px 13px 3px rgba(62, 66, 66, 0.07);
    box-shadow: 0px 0px 13px 3px rgba(62, 66, 66, 0.07);
}

.toolbar.horizontal .toolbar-group .toolbar-item {
    display: inline-block;
    padding: 2px 10px;
}

.toolbar.horizontal .toolbar-group .toolbar-item:nth-child(n+2) {
    border-left: 1px solid rgb(219, 219, 219);
}

.toolbar.vertical .toolbar-group {
    padding: 0 5px;
    margin-right: 8px;
    margin-bottom: 8px;
    border-radius: 3px;
    background-color: white;
    -webkit-box-shadow: 0px 0px 13px 3px rgba(62, 66, 66, 0.07);
    -moz-box-shadow: 0px 0px 13px 3px rgba(62, 66, 66, 0.07);
    box-shadow: 0px 0px 13px 3px rgba(62, 66, 66, 0.07);
}

.toolbar.vertical .toolbar-group .toolbar-item {
    padding: 10px 2px;
}

.toolbar.vertical .toolbar-group .toolbar-item:nth-child(n+2) {
    border-top: 1px solid rgb(219, 219, 219);
}

.svg-icon {
    /* width: 1em;
    height: 1em; */
    vertical-align: -0.35em;
    display: inline;
    fill: currentColor;
    overflow: hidden;
}

.toolbar-item-image {
    width: 17px;
    height: 17px;
    background-color: rgb(255, 255, 255);
    margin-top: 3.5px;
}

.svg-icon:hover img {
    filter: sepia(100%);
}
</style>
  