import G6 from "@antv/g6"
import flow_link_img from "./images/lightgreen-right-triangle.png"
import flow_linked_img from "./images/lightgreen-right-triangle-fill.png"
import flow_linkbg_img from "./images/lightgrey-right-triangle-fill.png"
import data_link_img from "./images/grey-circle.png"
import data_linked_img from "./images/grey-circle-fill.png"
import data_linkbg_img from "./images/lightgrey-circle-fill.png"
import node_type_event_img from "./images/green-event-fill.png"
import node_type_flow_img from "./images/blue-flow-fill.png"
import node_type_data_img from "./images/orange-bigdata-fill.png"
import Lang from "./lang"


document.oncontextmenu = (e) => {
	e.preventDefault()
}

var lang = 'zh'

var events = {};

const Event = {
	/**
	 * subscribe
	 */
	on: function on(name, self, callback) {
		var tuple = [self, callback]
		var callbacks = events[name]
		if (Array.isArray(callbacks)) {
			callbacks.push(tuple)
		}
		else {
			events[name] = [tuple]
		}
	},

	/**
	 * Unsubscribe
	 */
	remove: function remove(name, self) {
		var callbacks = events[name]
		if (Array.isArray(callbacks)) {
			events[name] = callbacks.filter((tuple) => {
				return tuple[0] != self
			})
		}
	},

	/**
	 * emit
	 */
	emit: function emit(name, data) {
		var callbacks = events[name]
		if (Array.isArray(callbacks)) {
			callbacks.map((tuple) => {
				var self = tuple[0]
				var callback = tuple[1]
				callback.call(self, data)
			})
		}
	}
}

/**
 * Evaluates the displayed string
 * @param {string} str The string to crop
 * @param {number} maxWidth Maximum width
 * @param {number} fontSize Font size
 * @return {string} The processed string
 */
const UTIL_FITTING_STRING = (str, maxWidth, fontSize) => {
	const UTIL_CALC_STR_LEN = (str) => {
		let len = 0
		for (let i = 0; i < str.length; i++) {
			if (str.charCodeAt(i) > 0) {  // && str.charCodeAt(i) < 128
				len++
			} else {
				len += 2
			}
		}
		return len
	}
	const fontWidth = fontSize * 1.3  // font size + margin
	maxWidth = maxWidth * 2
	const width = UTIL_CALC_STR_LEN(str) * fontWidth
	const ellipsis = "…"
	if (width > maxWidth) {
		const actualLen = Math.floor((maxWidth - 10) / fontWidth)
		const result = str.substring(0, actualLen) + ellipsis
		return result
	}
	return str
}

/**
 * Do objects compare different
 * @param {*} json1 obj1
 * @param {*} json2 obj2
 * @returns 
 */
const UTIL_IS_OBJECT_DIFF = (json1, json2) => {
	const getType = (obj) => {
		return Object.prototype.toString.call(obj).match(/^\[object ([a-zA-Z]*)\]$/)[1]
	}
	const isEmptyObject = (obj) => {
		for (var key in obj) {
			return false
		};
		return true
	}

	if (!json1 && !json2) {
		return false
	} else if (!isEmptyObject(json1) && isEmptyObject(json2)) {
		return true
	} else if (!isEmptyObject(json2) && isEmptyObject(json1)) {
		return true
	}
	for (let k in json2) {
		// Check whether the field exists
		if (json1[k] == undefined) {
			return true
		}
		// Check whether the data types are consistent
		if (getType(json2[k]) == getType(json1[k])) {
			// Compare the Array and Object types
			if (getType(json2[k]) == 'Array' || getType(json2[k]) == 'Object') {
				let result = UTIL_IS_OBJECT_DIFF(json1[k], json2[k])
				if (result) {
					return true
				}
			} else if (json1[k] != json2[k]) { // Compare other types of data
				return true
			}
		} else {
			return true
		}
	}
	for (let k in json1) {
		// Check whether the field exists
		if (json2[k] == undefined) {
			return true
		}
		// Check whether the data types are consistent
		if (getType(json2[k]) == getType(json1[k])) {
			// Compare the Array and Object types
			if (getType(json1[k]) == 'Array' || getType(json1[k]) == 'Object') {
				let result = UTIL_IS_OBJECT_DIFF(json2[k], json1[k])
				if (result) {
					return true
				}
			} else if (json1[k] != json2[k]) { // Compare other types of data
				return true
			}
		} else {
			return true
		}
	}
	return false;
}

const NODE_TYPE_IMAGE_MAP = {
	evtx: node_type_event_img,
	evrx: node_type_event_img,
	ctrl: node_type_flow_img,
	func: node_type_flow_img,
	dtio: node_type_data_img,
	dtpc: node_type_data_img
};

const NODE_TYPE_COLOR_MAP = {
	evtx: 'red',
	evrx: 'green',
	ctrl: 'orange',
	func: 'RoyalBlue',
	dtio: 'DarkCyan',
	dtpc: 'Orchid'
};

const VALUE_TYPE_COLOR_MAP = {
	pre_edge_id: 'lightgreen',
	nxt_edge_id: 'lightgreen',
	number: 'lightpink',
	string: 'lightgrey',
	bool: 'lightskyblue',
	default: 'lightgrey',
}

const FUNC_GET_EDGE_ANCHORPOINT_INDEX = (cfg, anchorPointShapeName) => {
	let isEvrx = FUNC_GET_IS_EVRX_NODE(cfg.node_type)
	let isEvtx = FUNC_GET_IS_EVTX_NODE(cfg.node_type)
	let isFunc = FUNC_GET_IS_FUNC_NODE(cfg.node_type)
	let isCtrl = FUNC_GET_IS_CTRL_NODE(cfg.node_type)
	let index = 0

	// 输入
	if (isCtrl || isFunc || isEvtx) {
		if (anchorPointShapeName.startsWith("pre_edge_id")) {
			return index
		}
		index++
	}
	for (let key in cfg.input) {
		if (anchorPointShapeName.startsWith(`input-${key}`)) {
			return index
		}
		index++
	}

	// 输出
	if (isFunc || isEvrx) {
		if (anchorPointShapeName.startsWith("nxt_edge_id")) {
			return index
		}
		index++
	} else if (isCtrl) {
		for (let i = 0; i < cfg.nxt_edge_id.length; i++) {
			if (anchorPointShapeName.startsWith("nxt_edge_id-" + i + "i")) {
				return index
			}
			index++
		}
	}
	for (let key in cfg.output) {
		if (anchorPointShapeName.startsWith(`output-${key}`)) {
			return index
		}
		index++
	}

	return -1
}

const FUNC_GET_EDGE_ANCHORPOINT_INDEX_FROM_ID = (cfg, id) => {
	let isEvrx = FUNC_GET_IS_EVRX_NODE(cfg.node_type)
	let isEvtx = FUNC_GET_IS_EVTX_NODE(cfg.node_type)
	let isFunc = FUNC_GET_IS_FUNC_NODE(cfg.node_type)
	let isCtrl = FUNC_GET_IS_CTRL_NODE(cfg.node_type)
	let index = 0

	// 输入
	if (isCtrl || isFunc || isEvtx) {
		if (id == null || id == undefined || id == "pre_edge_id") {
			return index
		}
		index++
	}
	for (let key in cfg.input) {
		if (id == `${cfg.id}.input.${key}`) {
			return index
		}
		index++
	}

	// 输出
	if (isFunc || isEvrx) {
		if (id == 0) {
			return index
		}
		index++
	} else if (isCtrl) {
		for (let i = 0; i < cfg.nxt_edge_id.length; i++) {
			if (id == i) {
				return index
			}
			index++
		}
	}
	for (let key in cfg.output) {
		if (id == `${cfg.id}.output.${key}`) {
			return index
		}
		index++
	}

	return -1
}

const FUNC_GET_EDGE_ANCHORPOINT_INDEX_ID = (cfg, anchorPointIndex) => {
	let isEvrx = FUNC_GET_IS_EVRX_NODE(cfg.node_type)
	let isEvtx = FUNC_GET_IS_EVTX_NODE(cfg.node_type)
	let isFunc = FUNC_GET_IS_FUNC_NODE(cfg.node_type)
	let isCtrl = FUNC_GET_IS_CTRL_NODE(cfg.node_type)
	let index = 0

	// 输入
	if (isCtrl || isFunc || isEvtx) {
		if (anchorPointIndex == index) {
			return "pre_edge_id"
		}
		index++
	}
	for (let key in cfg.input) {
		if (anchorPointIndex == index) {
			return `${cfg.id}.input.${key}`
		}
		index++
	}

	// 输出
	if (isFunc || isEvrx) {
		if (anchorPointIndex == index) {
			return 0
		}
		index++
	} else if (isCtrl) {
		for (let i = 0; i < cfg.nxt_edge_id.length; i++) {
			if (anchorPointIndex == index) {
				return i
			}
			index++
		}
	}
	for (let key in cfg.output) {
		if (anchorPointIndex == index) {
			return `${cfg.id}.output.${key}`
		}
		index++
	}

	return null
}

const FUNC_GET_IS_FLOW_NODE = (nodeType) => {
	if (
		nodeType === "evtx" ||
		nodeType === "evrx" ||
		nodeType === "ctrl" ||
		nodeType === "func"
	) {
		return true;
	}
	return false;
}

const FUNC_GET_IS_EVTX_NODE = (nodeType) => {
	if (
		nodeType === "evtx"
	) {
		return true;
	}
	return false;
}

const FUNC_GET_IS_EVRX_NODE = (nodeType) => {
	if (
		nodeType === "evrx"
	) {
		return true;
	}
	return false;
}

const FUNC_GET_IS_CTRL_NODE = (nodeType) => {
	if (
		nodeType === "ctrl"
	) {
		return true;
	}
	return false;
}

const FUNC_GET_IS_FUNC_NODE = (nodeType) => {
	if (
		nodeType === "func"
	) {
		return true;
	}
	return false;
}

G6.registerEdge('cubic-horizontal-end-distance', {
	getPath(item) {
		// console.log(item)
		var points = item;
		var start = points[0];
		var end = points[points.length - 1];
		var hgap = Math.abs(end.x - start.x);
		if (end.x > start.x) {
			hgap = Math.max(hgap, 32 * 7 - hgap * 2)
		} else {
			hgap = 32 * 7 + hgap / 2
		}
		return [['M', start.x, start.y], ['C', start.x + hgap * 1 / 2, start.y, end.x - hgap * 1 / 2, end.y, end.x, end.y]];
	},
	afterDraw(cfg, group) {
		// 获得当前边的第一个图形，这里是边本身的 path
		const shape = group.get('children')[0];
		// 边 path 的起点位置
		const startPoint = shape.getPoint(0);

		// 添加红色 circle 图形
		const circle = group.addShape('circle', {
			attrs: {
				x: startPoint.x,
				y: startPoint.y,
				fill: 'red',
				r: 3,
			},
			// must be assigned in G6 3.3 and later versions. it can be any value you want
			name: 'circle-shape',
		});
		// 对红色圆点添加动画
		circle.animate(
			(ratio) => {
				// 每一帧的操作，入参 ratio：这一帧的比例值（Number）。返回值：这一帧需要变化的参数集（Object）。
				// 根据比例值，获得在边 path 上对应比例的位置。
				const tmpPoint = shape.getPoint(ratio);
				// 返回需要变化的参数集，这里返回了位置 x 和 y
				return {
					x: tmpPoint.x,
					y: tmpPoint.y,
				};
			},
			{
				repeat: false, // 动画重复
				duration: 1500,
				callback: () => {
					circle.hide()
				},
			},
		); // 一次动画的时间长度
	},
	setState(name, value, item) {
		const shape = item.get('keyShape');
		// console.log(name, value, item)
		if (name === 'active' || name === 'selected') {
			if (value) {
				shape.attr('lineWidth', 5);
				shape.get('parent').get('children').forEach((keyShape) => {
					if (keyShape.get('name').startsWith('circle-shape')) {
						keyShape.show()
						keyShape.animate(
							(ratio) => {
								// 每一帧的操作，入参 ratio：这一帧的比例值（Number）。返回值：这一帧需要变化的参数集（Object）。
								// 根据比例值，获得在边 path 上对应比例的位置。
								const tmpPoint = shape.getPoint(ratio);
								// 返回需要变化的参数集，这里返回了位置 x 和 y
								return {
									x: tmpPoint.x,
									y: tmpPoint.y,
								};
							},
							{
								repeat: true, // 动画重复
								duration: 2000,
							},
						); // 一次动画的时间长度
					}
				})
			} else {
				if (!item.hasState('selected') && !item.hasState('active')) {
					shape.attr('lineWidth', 3);
					// 结束动画
					shape.get('parent').get('children').forEach((keyShape) => {
						// console.log(keyShape)
						if (keyShape.get('name').startsWith('circle-shape')) {
							keyShape.hide()
						}
					})
				}
			}
		}
	}
}, 'cubic-horizontal');

G6.registerNode("flow-node", {
	update: undefined,
	draw: (cfg, group) => {
		const KEYSHAPE_WIDTH = 180;
		let KEYSHAPE_HEIGHT = 200;
		const KEYSHAPE_RADIUS = 4;
		const KEYSHAPE_LINEWIDTH = 2;
		const KEYSHAPE_STROKECOLOR = "black";
		const KEYSHAPE_FILLCOLOR = "#130c0e40";
		const TITLEBAR_HEIGHT = 28;
		const TITLEBAR_PADDING = 4;
		const TITLEBAR_COLOR = NODE_TYPE_COLOR_MAP[cfg.node_type];
		const TITLEBAR_TITLECOLOR = "grey";
		const TITLEBAR_STATUSCOLOR = "lightblue";
		const CONTENT_PADDING_X = 4;
		const CONTENT_PADDING_Y = 8;
		const CONTENT_ITEM_HEIGHT = 28;
		const CONTENT_ITEM_PADDING_X = 0;
		const CONTENT_ITEM_PADDING_Y = 2;
		const CONTENT_ITEM_ACTUAL_HEIGHT =
			CONTENT_ITEM_HEIGHT - CONTENT_ITEM_PADDING_Y * 2;

		let isEvtx = FUNC_GET_IS_EVTX_NODE(cfg.node_type)
		let isEvrx = FUNC_GET_IS_EVRX_NODE(cfg.node_type)
		let isFlow = FUNC_GET_IS_FLOW_NODE(cfg.node_type)
		let isFunc = FUNC_GET_IS_FUNC_NODE(cfg.node_type)
		let isCtrl = FUNC_GET_IS_CTRL_NODE(cfg.node_type)

		const keyShape = group.addShape("rect", {
			attrs: {
				x: 0,
				y: 0,
				width: KEYSHAPE_WIDTH,
				height: KEYSHAPE_HEIGHT,
				lineWidth: KEYSHAPE_LINEWIDTH,
				stroke: KEYSHAPE_STROKECOLOR,
				fill: KEYSHAPE_FILLCOLOR,
				fillOpacity: 0.6,
				radius: KEYSHAPE_RADIUS
			},
			name: `${isFlow ? "flow" : "data"}-node-keyshape`
		});
		group.addShape("rect", {
			attrs: {
				x: KEYSHAPE_LINEWIDTH / 2,
				y: KEYSHAPE_LINEWIDTH / 2,
				width: KEYSHAPE_WIDTH - KEYSHAPE_LINEWIDTH,
				height: TITLEBAR_HEIGHT,
				lineWidth: 0,
				fillOpacity: 0.6,
				fill: TITLEBAR_COLOR,
				radius: [KEYSHAPE_RADIUS, KEYSHAPE_RADIUS, 0, 0]
			},
			name: `titlebar-keyshape`,
			draggable: true
		});
		group.addShape("image", {
			attrs: {
				x: KEYSHAPE_LINEWIDTH + TITLEBAR_PADDING,
				y: KEYSHAPE_LINEWIDTH + TITLEBAR_PADDING,
				width:
					TITLEBAR_HEIGHT -
					(KEYSHAPE_LINEWIDTH + TITLEBAR_PADDING) -
					TITLEBAR_PADDING,
				height:
					TITLEBAR_HEIGHT -
					(KEYSHAPE_LINEWIDTH + TITLEBAR_PADDING) -
					TITLEBAR_PADDING,
				img: NODE_TYPE_IMAGE_MAP[cfg.node_type]
			},
			name: `titlebar-typeimage`,
			draggable: true
		});
		group.addShape("text", {
			attrs: {
				text: UTIL_FITTING_STRING(
					cfg.name,
					KEYSHAPE_WIDTH -
					KEYSHAPE_LINEWIDTH * 2 -
					TITLEBAR_HEIGHT * 2 -
					TITLEBAR_PADDING * 4,
					14
				),
				x: TITLEBAR_HEIGHT,
				y: (TITLEBAR_HEIGHT + KEYSHAPE_LINEWIDTH) / 2,
				fill: TITLEBAR_TITLECOLOR,
				textBaseline: "middle",
				fontWeight: 600
			},
			name: `titlebar-nametext`,
			draggable: true
		});
		group.addShape("circle", {
			attrs: {
				x:
					KEYSHAPE_WIDTH -
					KEYSHAPE_LINEWIDTH -
					TITLEBAR_PADDING -
					((TITLEBAR_HEIGHT - TITLEBAR_PADDING * 2) * 2) / 5,
				y:
					KEYSHAPE_LINEWIDTH +
					TITLEBAR_PADDING +
					((TITLEBAR_HEIGHT - TITLEBAR_PADDING * 2) * 2) / 5,
				r: ((TITLEBAR_HEIGHT - TITLEBAR_PADDING * 2) * 2) / 5,
				fill: TITLEBAR_STATUSCOLOR
			},
			name: `titlebar-typecircle`,
			draggable: true
		});

		let appendContentItemStartX =
			CONTENT_PADDING_X + KEYSHAPE_LINEWIDTH;
		let appendContentItemStartY =
			TITLEBAR_HEIGHT + CONTENT_PADDING_Y + KEYSHAPE_LINEWIDTH;

		// 输入
		let inList = [];
		let inNamePrefixList = [];
		let inIntro = []
		let inTypeIsFlow = []
		if (isCtrl || isFunc || isEvtx) {
			inList.push("pre_edge_id");
			inNamePrefixList.push("pre_edge_id")
			inIntro.push(Lang[lang]['execute'])
			inTypeIsFlow.push(true)
		}
		for (let key in cfg.input) {
			inList.push(key);
			inNamePrefixList.push("input-" + key)
			inIntro.push(cfg.input_intro[key])
			inTypeIsFlow.push(cfg.input_type[key].endsWith("edge_id") ? true : false)
		}

		for (let i = 0; i < inList.length; i++) {
			const contentItemGroupX = appendContentItemStartX + CONTENT_ITEM_PADDING_X;
			const contentItemGroupY = appendContentItemStartY + CONTENT_ITEM_PADDING_Y;

			const contentItemGroup = group.addGroup();

			let input_intro = inIntro[i]
			let namePrefix = inNamePrefixList[i]

			let linkimage = data_link_img,
				linkedimage = data_linked_img,
				linkbgimage = data_linkbg_img;
			if (inTypeIsFlow[i]) {
				linkimage = flow_link_img;
				linkedimage = flow_linked_img;
				linkbgimage = flow_linkbg_img;
			}

			contentItemGroup.addShape("image", {
				attrs: {
					x: contentItemGroupX + 4,
					y: contentItemGroupY + 4,
					width: CONTENT_ITEM_ACTUAL_HEIGHT - 8,
					height: CONTENT_ITEM_ACTUAL_HEIGHT - 8,
					img: linkimage
				},
				name: namePrefix + "-linkimage"
			});
			contentItemGroup.addShape("image", {
				attrs: {
					x: contentItemGroupX + 4,
					y: contentItemGroupY + 4,
					width: CONTENT_ITEM_ACTUAL_HEIGHT - 8,
					height: CONTENT_ITEM_ACTUAL_HEIGHT - 8,
					opacity: 0,
					img: linkedimage
				},
				name: namePrefix + "-linkedimage"
			});
			contentItemGroup.addShape("image", {
				attrs: {
					x: contentItemGroupX,
					y: contentItemGroupY,
					width: CONTENT_ITEM_ACTUAL_HEIGHT,
					height: CONTENT_ITEM_ACTUAL_HEIGHT,
					opacity: 0.3,
					img: linkbgimage
				},
				name: namePrefix + "-linkbgimage"
			});
			contentItemGroup.addShape("text", {
				attrs: {
					x: contentItemGroupX + CONTENT_ITEM_ACTUAL_HEIGHT + 4,
					y: contentItemGroupY + CONTENT_ITEM_ACTUAL_HEIGHT / 2,
					textAlign: 'left',
					textBaseline: "middle",
					text: UTIL_FITTING_STRING(
						input_intro,
						KEYSHAPE_WIDTH -
						KEYSHAPE_LINEWIDTH * 2 -
						CONTENT_PADDING_X * 2 -
						CONTENT_ITEM_HEIGHT,
						12
					),
					fill: "grey"
				},
				name: namePrefix + "-linktipstext",
				draggable: true
			});

			appendContentItemStartY += CONTENT_ITEM_HEIGHT
		}

		// 输出
		appendContentItemStartX = KEYSHAPE_WIDTH - KEYSHAPE_LINEWIDTH - CONTENT_PADDING_X;

		let outList = [];
		let outNamePrefix = []
		let outIntro = []
		let outTypeIsFlow = []
		if (isFunc || isEvrx) {
			outList.push("nxt_edge_id");
			outNamePrefix.push("nxt_edge_id")
			outIntro.push(Lang[lang]['nextExecute'])
			outTypeIsFlow.push(true)
		} else if (isCtrl) {
			cfg.nxt_edge_id.forEach((edge_id, i) => {
				outList.push("nxt_edge_id-" + i + "i");
				outNamePrefix.push("nxt_edge_id-" + i + "i")
				outIntro.push(cfg.nxt_edge_id_intro[i])
				outTypeIsFlow.push(true)
			})
		}
		for (let key in cfg.output) {
			outList.push(key);
			outNamePrefix.push("output-" + key)
			outIntro.push(cfg.output_intro[key])
			outTypeIsFlow.push(cfg.output_type[key].endsWith("edge_id") ? true : false)
		}

		for (let i = 0; i < outList.length; i++) {
			const contentItemGroupX = appendContentItemStartX - CONTENT_ITEM_PADDING_X - CONTENT_ITEM_ACTUAL_HEIGHT;
			const contentItemGroupY = appendContentItemStartY + CONTENT_ITEM_PADDING_Y;

			const contentItemGroup = group.addGroup();

			let output_intro = outIntro[i]
			let namePrefix = outNamePrefix[i]

			let linkimage = data_link_img,
				linkedimage = data_linked_img,
				linkbgimage = data_linkbg_img;
			if (outTypeIsFlow[i]) {
				linkimage = flow_link_img;
				linkedimage = flow_linked_img;
				linkbgimage = flow_linkbg_img;
			}

			contentItemGroup.addShape("image", {
				attrs: {
					x: contentItemGroupX + 4,
					y: contentItemGroupY + 4,
					width: CONTENT_ITEM_ACTUAL_HEIGHT - 8,
					height: CONTENT_ITEM_ACTUAL_HEIGHT - 8,
					img: linkimage
				},
				name: namePrefix + "-linkimage"
			});
			contentItemGroup.addShape("image", {
				attrs: {
					x: contentItemGroupX + 4,
					y: contentItemGroupY + 4,
					width: CONTENT_ITEM_ACTUAL_HEIGHT - 8,
					height: CONTENT_ITEM_ACTUAL_HEIGHT - 8,
					opacity: 0,
					img: linkedimage
				},
				name: namePrefix + "-linkedimage"
			});
			contentItemGroup.addShape("image", {
				attrs: {
					x: contentItemGroupX,
					y: contentItemGroupY,
					width: CONTENT_ITEM_ACTUAL_HEIGHT,
					height: CONTENT_ITEM_ACTUAL_HEIGHT,
					opacity: 0.3,
					img: linkbgimage
				},
				name: namePrefix + "-linkbgimage"
			});
			contentItemGroup.addShape("text", {
				attrs: {
					x: contentItemGroupX - 4,
					y: contentItemGroupY + CONTENT_ITEM_ACTUAL_HEIGHT / 2,
					textAlign: "right",
					textBaseline: "middle",
					text: UTIL_FITTING_STRING(
						output_intro,
						KEYSHAPE_WIDTH -
						KEYSHAPE_LINEWIDTH * 2 -
						CONTENT_PADDING_X * 2 -
						CONTENT_ITEM_HEIGHT,
						12
					),
					fill: "grey"
				},
				name: namePrefix + "-linktipstext",
				draggable: true
			});

			appendContentItemStartY += CONTENT_ITEM_HEIGHT;
		}

		KEYSHAPE_HEIGHT = appendContentItemStartY + CONTENT_PADDING_Y - KEYSHAPE_LINEWIDTH
		keyShape.attrs.height = KEYSHAPE_HEIGHT;
		return keyShape;
	},
	getAnchorPoints(cfg) {
		var tmp_anchorPoints = [];
		var anchorPoints = [];
		const KEYSHAPE_WIDTH = 180;
		let KEYSHAPE_HEIGHT = 200;
		const KEYSHAPE_RADIUS = 4;
		const KEYSHAPE_LINEWIDTH = 2;
		const KEYSHAPE_STROKECOLOR = "lightblue";
		const KEYSHAPE_FILLCOLOR = "#00000040";
		const TITLEBAR_HEIGHT = 28;
		const TITLEBAR_PADDING = 4;
		const TITLEBAR_COLOR = "lightpink";
		const TITLEBAR_TITLECOLOR = "grey";
		const TITLEBAR_STATUSCOLOR = "lightblue";
		const CONTENT_PADDING_X = 4;
		const CONTENT_PADDING_Y = 8;
		const CONTENT_ITEM_HEIGHT = 24;
		const CONTENT_ITEM_PADDING_X = 0;
		const CONTENT_ITEM_PADDING_Y = 2;
		const CONTENT_ITEM_ACTUAL_HEIGHT =
			CONTENT_ITEM_HEIGHT - CONTENT_ITEM_PADDING_Y * 2;

		let isEvtx = FUNC_GET_IS_EVTX_NODE(cfg.node_type)
		let isEvrx = FUNC_GET_IS_EVRX_NODE(cfg.node_type)
		let isFunc = FUNC_GET_IS_FUNC_NODE(cfg.node_type)
		let isCtrl = FUNC_GET_IS_CTRL_NODE(cfg.node_type)

		let appendContentItemStartX =
			CONTENT_PADDING_X + KEYSHAPE_LINEWIDTH;
		let appendContentItemStartY =
			TITLEBAR_HEIGHT + CONTENT_PADDING_Y + KEYSHAPE_LINEWIDTH;

		// 输入
		let inList = [];
		if (isFunc || isCtrl || isEvtx) {
			inList.push("pre_edge_id");
		}
		for (let key in cfg.input) {
			inList.push(key);
		}

		for (let i = 0; i < inList.length; i++) {
			const contentItemGroupX = appendContentItemStartX + CONTENT_ITEM_PADDING_X;
			const contentItemGroupY = appendContentItemStartY + CONTENT_ITEM_PADDING_Y;

			let x_center = contentItemGroupX + CONTENT_ITEM_ACTUAL_HEIGHT / 2
			let y_center = contentItemGroupY + CONTENT_ITEM_ACTUAL_HEIGHT / 2

			tmp_anchorPoints.push([x_center, y_center])

			appendContentItemStartY += CONTENT_ITEM_HEIGHT
		}

		// 输出
		appendContentItemStartX = KEYSHAPE_WIDTH + KEYSHAPE_LINEWIDTH - CONTENT_PADDING_X;

		let outList = [];
		if (isFunc || isEvrx) {
			outList.push("nxt_edge_id");
		} else if (isCtrl) {
			cfg.nxt_edge_id.forEach((edge_id, i) => {
				outList.push("nxt_edge_id-" + i + "i");
			})
		}
		for (let key in cfg.output) {
			outList.push(key);
		}

		for (let i = 0; i < outList.length; i++) {
			const contentItemGroupX = appendContentItemStartX - CONTENT_ITEM_PADDING_X - CONTENT_ITEM_ACTUAL_HEIGHT;
			const contentItemGroupY = appendContentItemStartY + CONTENT_ITEM_PADDING_Y;

			let x_center = contentItemGroupX + CONTENT_ITEM_ACTUAL_HEIGHT / 2
			let y_center = contentItemGroupY + CONTENT_ITEM_ACTUAL_HEIGHT / 2

			tmp_anchorPoints.push([x_center, y_center])

			appendContentItemStartY += CONTENT_ITEM_HEIGHT;
		}


		KEYSHAPE_HEIGHT = appendContentItemStartY + CONTENT_PADDING_Y - KEYSHAPE_LINEWIDTH

		tmp_anchorPoints.forEach((value) => {
			// console.log(value)
			anchorPoints.push([value[0] / (KEYSHAPE_WIDTH + KEYSHAPE_LINEWIDTH * 2),
			value[1] / (KEYSHAPE_HEIGHT + KEYSHAPE_LINEWIDTH * 2)])
		})

		// console.log(anchorPoints)

		return anchorPoints;
	}
}, "rect");

G6.registerBehavior('custom-operate', {
	// 设定该自定义行为需要监听的事件及其响应函数
	getEvents() {
		return {
			'node:mousedown': 'onNodeMousedown',
			'mousemove': 'onMousemove',
			'mouseup': 'onMouseup',
			'edge:click': 'onEdgeClick',
			'edge:mouseenter': 'onEdgeMouseenter',
			'edge:mouseleave': 'onEdgeMouseleave',
			'keydown': 'onKeydown',
			'canvas:contextmenu': 'onCanvasContextmenu',
			"nodeselectchange": "onNodeSelectchange",
		};
	},
	onNodeMousedown(e) {
		// console.log(e)
		if (e.originalEvent.button != 0) {
			// 非左键
			return
		}
		const node = e.item;
		const graph = this.graph;
		// 鼠标当前点击的节点的位置
		const point = { x: e.x, y: e.y };
		const model = node.getModel();
		const anchorPointRegExp = /(input|output|pre_edge_id|nxt_edge_id)-*\w*-(linkimage|linkedimage|linkbgimage)/
		const shapeName = e.target.cfg.name
		// console.log(shapeName,anchorPointRegExp.test(shapeName))
		// console.log(model)
		if (anchorPointRegExp.test(shapeName)) {
			let anchorPointClass = shapeName.match(/(input|output|pre_edge_id|nxt_edge_id)/)[0]
			let anchorPointType = anchorPointClass
			if (anchorPointClass === "input") {
				anchorPointType = model.input_type[shapeName.split("-")[1]]
			} else if (anchorPointClass === "output") {
				anchorPointType = model.output_type[shapeName.split("-")[1]]
			}
			// console.log(anchorPointClass, anchorPointType, FUNC_GET_EDGE_ANCHORPOINT_INDEX(model, shapeName))
			let anchorPointIndex = FUNC_GET_EDGE_ANCHORPOINT_INDEX(model, shapeName)
			let addNewEdge = false
			if (anchorPointClass === 'output' || anchorPointClass === 'nxt_edge_id' || anchorPointClass === 'pre_edge_id') {
				// 新增
				addNewEdge = true
			} else {
				// 是否存在边，有则编辑，无则新增
				const findSourceEdge = graph.find('edge', (edge) => {
					let m = edge.getModel()
					return m.source === model.id && m.sourceAnchor === anchorPointIndex
				})
				if (findSourceEdge) {
					// console.log("source", findSourceEdge)
					this.edgeIsUpdate = true
					this.edgeEndpointModel = findSourceEdge.getTarget().getModel()
					this.edgeEndpointIsSource = false
					this.edge = findSourceEdge
					graph.updateItem(findSourceEdge, {
						source: point,
					}, false);
				} else {
					const findTargetEdge = graph.find('edge', (edge) => {
						let m = edge.getModel()
						return m.target === model.id && m.targetAnchor === anchorPointIndex
					})
					if (findTargetEdge) {
						// console.log("target", findTargetEdge)
						this.edgeIsUpdate = true
						this.edgeEndpointModel = findTargetEdge.getSource().getModel()
						this.edgeEndpointIsSource = true
						this.edge = findTargetEdge
						graph.updateItem(findTargetEdge, {
							target: point,
						}, false);
					} else {
						addNewEdge = true
					}
				}
			}
			if (addNewEdge) {
				this.edgeIsUpdate = false
				this.edgeEndpointModel = model;
				// 在图上新增一条边，结束点是鼠标当前点击的节点的位置
				if (anchorPointClass === "input" || anchorPointClass === "pre_edge_id") {
					this.edgeEndpointIsSource = false
					this.edge = graph.addItem('edge', {
						source: point,
						target: model.id,
						targetAnchor: anchorPointIndex
					}, false);
				} else {
					this.edgeEndpointIsSource = true
					this.edge = graph.addItem('edge', {
						source: model.id,
						target: point,
						sourceAnchor: anchorPointIndex
					}, false);
				}
			}
			this.edgeEndpointAnchorPointClass = anchorPointClass
			this.edgeEndpointAnchorPointType = anchorPointType
			this.isAddingEdge = true;
		}
	},
	onMousemove(e) {
		// 鼠标的当前位置
		// console.log(e)
		if (this.isAddingEdge && this.edge) {
			// 更新边的结束点位置为当前鼠标位置
			let isEdgeValid = false
			const currentItem = e.item;
			const point = { x: e.x, y: e.y };
			if (this.edge !== currentItem && currentItem != null) {
				const model = currentItem.getModel();
				const shapeName = e.target.cfg.name
				const anchorPointRegExp = /(input|output|pre_edge_id|nxt_edge_id)-*\w*-(linkimage|linkedimage|linkbgimage)/
				if (anchorPointRegExp.test(shapeName)) {
					let anchorPointClass = shapeName.match(/(input|output|pre_edge_id|nxt_edge_id)/)[0]
					let anchorPointType = anchorPointClass
					if (anchorPointClass === "input") {
						anchorPointType = model.input_type[shapeName.split("-")[1]]
					} else if (anchorPointClass === "output") {
						anchorPointType = model.output_type[shapeName.split("-")[1]]
					}
					// console.log(anchorPointClass, anchorPointType)
					if (this.edgeEndpointModel.id !== model.id) {
						if (this.edgeIsUpdate) {
							// console.log('update', this.edgeEndpointAnchorPointClass, this.edgeEndpointAnchorPointType)
							if ((this.edgeEndpointAnchorPointClass == anchorPointClass || anchorPointType === 'pre_edge_id' || anchorPointType === 'nxt_edge_id') && anchorPointType == this.edgeEndpointAnchorPointType) {
								isEdgeValid = true
							}
						}
						else {
							if ((anchorPointClass === 'pre_edge_id' || anchorPointType === 'pre_edge_id') &&
								(this.edgeEndpointAnchorPointClass === 'nxt_edge_id' ||
									this.edgeEndpointAnchorPointType === 'nxt_edge_id')) {
								isEdgeValid = true
							} else if ((anchorPointClass === 'nxt_edge_id' || anchorPointType === 'nxt_edge_id') &&
								(this.edgeEndpointAnchorPointClass === 'pre_edge_id' ||
									this.edgeEndpointAnchorPointType === 'pre_edge_id')) {
								isEdgeValid = true
							} else if (anchorPointClass === 'input' && this.edgeEndpointAnchorPointClass === 'output' &&
  							(anchorPointType == this.edgeEndpointAnchorPointType ||
  								((this.edgeEndpointAnchorPointType == 'number' || this.edgeEndpointAnchorPointType == 'int' || this.edgeEndpointAnchorPointType == 'float') &&
  									(anchorPointType == 'number' || anchorPointType == 'int' || anchorPointType == 'float')))) {
  							isEdgeValid = true
  						} else if (anchorPointClass === 'output' && this.edgeEndpointAnchorPointClass === 'input' &&
  							(anchorPointType == this.edgeEndpointAnchorPointType ||
  								((this.edgeEndpointAnchorPointType == 'number' || this.edgeEndpointAnchorPointType == 'int' || this.edgeEndpointAnchorPointType == 'float') &&
  									(anchorPointType == 'number' || anchorPointType == 'int' || anchorPointType == 'float')))) {
  							isEdgeValid = true
  						}
						}
					}
				}
			}
			if (this.edgeEndpointIsSource) {
				this.graph.updateItem(this.edge, {
					target: point,
					style: {
						stroke: isEdgeValid ? VALUE_TYPE_COLOR_MAP[this.edgeEndpointAnchorPointType] : 'lightcoral'
					}
				}, false);
			} else {
				this.graph.updateItem(this.edge, {
					source: point,
					style: {
						stroke: isEdgeValid ? VALUE_TYPE_COLOR_MAP[this.edgeEndpointAnchorPointType] : 'lightcoral'
					}
				}, false);
			}
		}
	},
	onMouseup(e) {
		// console.log(e)
		const currentItem = e.item;
		const graph = this.graph;
		// 拖拽过程中，点击会点击到新增的边上
		if (!this.isAddingEdge) {
			return
		} else if (this.edge === currentItem || currentItem == null) {
			graph.removeItem(this.edge, false);
		} else {
			const model = currentItem.getModel();
			const shapeName = e.target.cfg.name
			const anchorPointRegExp = /(input|output|pre_edge_id|nxt_edge_id)-*\w*-(linkimage|linkedimage|linkbgimage)/
			// console.log(shapeName)
			if (anchorPointRegExp.test(shapeName)) {
				let anchorPointClass = shapeName.match(/(input|output|pre_edge_id|nxt_edge_id)/)[0]
				let anchorPointType = anchorPointClass
				if (anchorPointClass === "input") {
					anchorPointType = model.input_type[shapeName.split("-")[1]]
				} else if (anchorPointClass === "output") {
					anchorPointType = model.output_type[shapeName.split("-")[1]]
				}
				// console.log(anchorPointClass,anchorPointType)
				if (this.edgeEndpointModel.id !== model.id) {
					let isEdgeValid = false
					if (this.edgeIsUpdate) {
						// console.log('update', this.edgeEndpointAnchorPointClass, this.edgeEndpointAnchorPointType)
						if ((this.edgeEndpointAnchorPointClass == anchorPointClass || anchorPointType === 'pre_edge_id' || anchorPointType === 'nxt_edge_id') && anchorPointType == this.edgeEndpointAnchorPointType) {
							isEdgeValid = true
						}
					}
					else {
						if ((anchorPointClass === 'pre_edge_id' || anchorPointType === 'pre_edge_id') &&
							(this.edgeEndpointAnchorPointClass === 'nxt_edge_id' ||
								this.edgeEndpointAnchorPointType === 'nxt_edge_id')) {
							isEdgeValid = true
						} else if ((anchorPointClass === 'nxt_edge_id' || anchorPointType === 'nxt_edge_id') &&
							(this.edgeEndpointAnchorPointClass === 'pre_edge_id' ||
								this.edgeEndpointAnchorPointType === 'pre_edge_id')) {
							isEdgeValid = true
						} else if (anchorPointClass === 'input' && this.edgeEndpointAnchorPointClass === 'output' &&
							anchorPointType == this.edgeEndpointAnchorPointType) {
							isEdgeValid = true
						} else if (anchorPointClass === 'output' && this.edgeEndpointAnchorPointClass === 'input' &&
							anchorPointType == this.edgeEndpointAnchorPointType) {
							isEdgeValid = true
						}
					}
					if (isEdgeValid) {
						let anchorPointIndex = FUNC_GET_EDGE_ANCHORPOINT_INDEX(model, shapeName)
						if (this.edgeEndpointIsSource) {
							// 查找并删除重复边、多余边
							let that = this
							const delEdges = graph.findAll('edge', (edge) => {
								let m = edge.getModel()
								if ((that.edgeEndpointAnchorPointType === 'nxt_edge_id')
									&& m.id != that.edge.getModel().id &&
									m.source == that.edge.getModel().source && m.sourceAnchor == that.edge.getModel().sourceAnchor) {
									// 该类型只能有一条边，查找多余边
									return true
								} else if ((anchorPointClass == 'input' && m.target == model.id && m.targetAnchor == anchorPointIndex) &&
									m.id != that.edge.getModel().id) {
									return true
								} else if (m.source == that.edge.getModel().source && m.sourceAnchor == that.edge.getModel().sourceAnchor
									&& m.target == model.id && m.targetAnchor == anchorPointIndex) {
									// 查找重复边
									return true
								}
								return false
							})
							const stackdata = {
								delEdges: [],
								addEdges: []
							}
							// console.log("source", delEdges)
							delEdges.forEach((edge) => {
								stackdata.delEdges.push(edge.getModel())
								graph.removeItem(edge, false)
							})
							// 更新结点
							graph.updateItem(this.edge, {
								target: model.id,
								targetAnchor: anchorPointIndex,
							}, false)
							stackdata.addEdges.push(this.edge.getModel())
							graph.pushStack('updateEdges', stackdata, 'undo')
							// console.log('updateEdges', stackdata, 'undo')
						} else {
							// 查找并删除重复边、多余边
							let that = this
							const delEdges = graph.findAll('edge', (edge) => {
								let m = edge.getModel()
								if ((anchorPointType === 'nxt_edge_id') && m.id != that.edge.getModel().id &&
									m.source == model.id && m.sourceAnchor == anchorPointIndex) {
									// 该类型只能有一条边，查找多余边
									return true
								} else if ((that.edgeEndpointAnchorPointClass == 'input' && m.target == model.id && m.targetAnchor == anchorPointIndex) &&
									m.id != that.edge.getModel().id) {
									return true
								} else if (m.source == model.id && m.sourceAnchor == anchorPointIndex
									&& m.target == that.edge.getModel().target && m.targetAnchor == that.edge.getModel().targetAnchor) {
									// 查找重复边
									return true
								}
								return false
							})
							const stackdata = {
								delEdges: [],
								addEdges: []
							}
							// console.log("target", delEdges)
							delEdges.forEach((edge) => {
								stackdata.delEdges.push(edge.getModel())
								graph.removeItem(edge, false)
							})
							// 更新结点
							graph.updateItem(this.edge, {
								source: model.id,
								sourceAnchor: anchorPointIndex,
							}, false)
							stackdata.addEdges.push(this.edge.getModel())
							graph.pushStack('updateEdges', stackdata, 'undo')
							// console.log('updateEdges', stackdata, 'undo')
						}
					} else {
						graph.removeItem(this.edge, false);
					}
				} else {
					graph.removeItem(this.edge, false);
				}
			} else {
				graph.removeItem(this.edge, false);
			}
		}

		this.edge = null;
		this.edgeIsUpdate = null
		this.edgeEndpointIsSource = null
		this.edgeEndpointModel = null;
		this.edgeEndpointAnchorPointClass = null
		this.edgeEndpointAnchorPointType = null
		this.isAddingEdge = false;
	},
	onEdgeClick(e) {
		const edge = e.item;
		this.graph.setItemState(edge, 'selected', !edge.hasState('selected')); // 切换选中
	},
	onEdgeMouseenter(e) {
		const edge = e.item;
		this.graph.setItemState(edge, 'active', true); // 切换选中
	},
	onEdgeMouseleave(e) {
		const edge = e.item;
		this.graph.setItemState(edge, 'active', false); // 切换选中
	},
	onKeydown(e) {
		// console.log("keydown", e.key, e)
		if (e.key === 'Delete' || e.key === 'Backspace') {
			const nodes = this.graph.findAllByState('node', 'selected')
			const stackdata = {
				delNodes: [],
				delEdges: []
			}
			nodes.forEach((node) => {
				// console.log(node.getModel().id)
				stackdata.delNodes.push(node.getModel())
				this.graph.removeItem(node, false)
			})
			const edges = this.graph.findAllByState('edge', 'selected')
			edges.forEach((edge) => {
				stackdata.delEdges.push(edge.getModel())
				this.graph.removeItem(edge, false)
			})
			graph.pushStack('deleteItems', stackdata, 'undo')
			// console.log('deleteItems', stackdata, 'undo')
		} else if (e.ctrlKey && (e.key === 'z' || e.key === 'Z')) {
			// undo
			undo(this.graph.cfg.id)
		} else if (e.ctrlKey && (e.key === 'y' || e.key === 'Y')) {
			// redo
			redo(this.graph.cfg.id)
		}
	},
	onCanvasContextmenu(e) {
		// console.log("onCanvasContextmenu", e)
		Event.emit("rqAddNode#" + this.graph.cfg.id, { x: e.x, y: e.y })
		// console.log(this.graph)
		// console.log(this.graph.cfg.id)
	},
	onNodeSelectchange({ target, selectedItems, select }) {
		if (target == null) {
			return
		}
		// console.log(target, selectedItems, select)
		let node = target.getModel()
		if (select && selectedItems.nodes.length == 1 && selectedItems.edges.length == 0) {
			node = JSON.parse(JSON.stringify(node))
			Event.emit("rqEditNodeAttr#" + this.graph.cfg.id, node)
		}
	},
});


var graph = {};

const initGraph = (graphElementId, graphWidth, graphHeight, minimapElementId, data) => {
	if (!data) {
		data = {
			nodes: [],
			edges: []
		}
	}
	const id = graphElementId
	const container = document.getElementById(graphElementId);
	// console.log(container)
	const width = graphWidth;
	const height = graphHeight;

	const grid = new G6.Grid()

	let plugins = [grid,]
	if (minimapElementId) {
		plugins.push(new G6.Minimap({
			container: minimapElementId,
			type: 'default'
		}))
	}

	let graph_ = new G6.Graph({
		id: graphElementId,
		minimapId: minimapElementId,
		container: container,
		width,
		height,
		fitCenter: true,
		minZoom: 0.3,
		maxZoom: 3,
		enabledStack: true,
		modes: {
			default: ["drag-canvas", "drag-node", 'custom-operate',
				{
					type: 'zoom-canvas',
					enableOptimize: true,
				}, 'click-select', 'brush-select',
				{
					type: 'activate-relations',//bug:
					inactiveState: 'none'
				},],
		},
		defaultNode: {
			type: "flow-node"
		},
		defaultEdge: {
			type: 'cubic-horizontal-end-distance',
			style: {
				lineWidth: 3,
			}
		},
		plugins: plugins,//, menu
		animate: true, // Boolean，切换布局时是否使用动画过度，默认为 false
		animateCfg: {
			duration: 500, // Number，一次动画的时长
			easing: 'linearEasing', // String，动画函数
		},
	});

	graph_.data(data);
	graph_.render();

	Event.on("addNode#" + graph_.cfg.id, this, (data) => {
		if (data.node_type == 'evrx' || data.node_type == 'evtx') {
			// only one same event node
			const findNode = graph_.find('node', (node) => {
				return node.get('model').node_name === data.node_name
			})
			if (findNode) {
				// stop add node and focus node
				graph_.focusItem(findNode, true, {
					easing: 'easeCubic',
					duration: 400,
				});
				Event.emit("rqShowMessage#" + graph_.cfg.id, {
					message: '已创建该节点，该节点禁止创建多次',
					type: 'error'
				})
				return
			}
		}
		graph_.addItem("node", data, false)
		const stackdata = {
			addNodes: [JSON.parse(JSON.stringify(data))],
		}
		graph_.pushStack('addNodes', stackdata, 'undo')
		// console.log('addNodes', stackdata, 'undo')
	})

	Event.on("editNodeAttr#" + graph_.cfg.id, this, (data) => {
		// console.log(data)
		const stackdata = {
			originNodes: [JSON.parse(JSON.stringify(graph_.findById(data.id).getModel()))],
			updateNodes: [JSON.parse(JSON.stringify(data))],
		}
		graph_.pushStack('updateNodes', stackdata, 'undo')
		// console.log('updateNodes', stackdata, 'undo')
		graph_.updateItem(data.id, data, false)
	})

	graph[id] = graph_
	return graph_
}

const saveConfig = (_graph = null, _dataSource = null, graphElementID = null) => {
	if (!(_graph || _dataSource || graphElementID)) return null
	let dataSource = _graph ? _graph.save() : (_dataSource ? _dataSource : graph[graphElementID].save())
	let data = JSON.parse(JSON.stringify(dataSource))
	let config = {
		graph: {
			node_list: [],
			edge_list: []
		},
		source: {
			graph: JSON.parse(JSON.stringify(dataSource))
		}
	}

	let nodeMap = {}
	for (let i = 0; i < data.nodes.length; i++) {
		let node = data.nodes[i]
		nodeMap[node.id] = node
		config.graph.node_list.push(node)
	}
	for (let i = 0; i < data.edges.length; i++) {
		let edge = data.edges[i]
		let sourceAnchorId = FUNC_GET_EDGE_ANCHORPOINT_INDEX_ID(nodeMap[edge.source], edge.sourceAnchor)
		let targetAnchorId = FUNC_GET_EDGE_ANCHORPOINT_INDEX_ID(nodeMap[edge.target], edge.targetAnchor)
		// console.log(sourceAnchorId, targetAnchorId)
		if (/^[0-9]*$/.test(sourceAnchorId)) {
			// console.log("1")
			nodeMap[edge.source].nxt_edge_id[sourceAnchorId] = edge.id
			config.graph.edge_list.push({
				id: edge.id,
				name: "",
				pre_id: edge.source,
				nxt_id: edge.target
			})
		} else if (sourceAnchorId.search(".output.") != -1 && (targetAnchorId.search(".input.") != -1 || targetAnchorId == "pre_edge_id")) {
			// console.log("2")
			config.graph.edge_list.push({
				id: edge.id,
				name: "",
				pre_id: sourceAnchorId,
				nxt_id: targetAnchorId == "pre_edge_id" ? edge.target : targetAnchorId
			})
		} else {
			// console.log("3")
			config.graph.edge_list.push({
				id: edge.id,
				name: "",
				pre_id: edge.source,
				nxt_id: edge.target
			})
		}
	}

	// console.log(config)
	return config
}

const loadConfig = (graphElementID, config) => {
	config = JSON.parse(JSON.stringify(config))

	if (!UTIL_IS_OBJECT_DIFF(saveConfig(null, config.source.graph).graph, config.graph)) {
		// 配置无改动，加载原图
		let data = config.source.graph
		graph[graphElementID].read(data)
		return data
	}
	// 配置改动，加载配置
	let data = {
		nodes: [],
		edges: [],
	}

	let nodeMap = {}
	for (let i = 0; i < config.graph.node_list.length; i++) {
		let node = config.graph.node_list[i]
		nodeMap[node.id] = node
		data.nodes.push(node)
	}

	for (let i = 0; i < config.graph.edge_list.length; i++) {
		let edge = config.graph.edge_list[i]
		let sourceId = edge.pre_id
		let targetId = edge.nxt_id
		if (sourceId.search(".output.") != -1 && targetId.search(".input.") != -1) {
			let sourceNodeId = sourceId.split(".output.")[0]
			let sourceNodeField = sourceId.split(".output.")[1]
			let sourceNodeAnchor = FUNC_GET_EDGE_ANCHORPOINT_INDEX_FROM_ID(nodeMap[sourceNodeId], sourceId)
			let targetNodeId = targetId.split(".input.")[0]
			let targetNodeAnchor = FUNC_GET_EDGE_ANCHORPOINT_INDEX_FROM_ID(nodeMap[targetNodeId], targetId)
			// console.log(VALUE_TYPE_COLOR_MAP[nodeMap[sourceNodeId].output_type[sourceNodeField]] || VALUE_TYPE_COLOR_MAP.default)
			data.edges.push({
				id: edge.id,
				source: sourceNodeId,
				sourceAnchor: sourceNodeAnchor,
				target: targetNodeId,
				targetAnchor: targetNodeAnchor,
				style: {
					stroke: VALUE_TYPE_COLOR_MAP[nodeMap[sourceNodeId].output_type[sourceNodeField]] || VALUE_TYPE_COLOR_MAP.default
				}
			})
		} else if (sourceId.search(".output.") != -1) {
			let sourceNodeId = sourceId.split(".output.")[0]
			let sourceNodeField = sourceId.split(".output.")[1]
			let sourceNodeAnchor = FUNC_GET_EDGE_ANCHORPOINT_INDEX_FROM_ID(nodeMap[sourceNodeId], sourceId)
			data.edges.push({
				id: edge.id,
				source: sourceNodeId,
				sourceAnchor: sourceNodeAnchor,
				target: targetId,
				targetAnchor: FUNC_GET_EDGE_ANCHORPOINT_INDEX_FROM_ID(nodeMap[targetId], null),
				style: {
					stroke: VALUE_TYPE_COLOR_MAP[nodeMap[sourceNodeId].output_type[sourceNodeField]] || VALUE_TYPE_COLOR_MAP.default
				}
			})
		} else {
			let isBreak = false
			for (let j = 0; j < nodeMap[sourceId].nxt_edge_id.length; j++) {
				if (nodeMap[sourceId].nxt_edge_id[j] == edge.id) {
					let sourceAnchor = FUNC_GET_EDGE_ANCHORPOINT_INDEX_FROM_ID(nodeMap[sourceId], j)
					let targetAnchor = FUNC_GET_EDGE_ANCHORPOINT_INDEX_FROM_ID(nodeMap[targetId], null)
					data.edges.push({
						id: edge.id,
						source: sourceId,
						sourceAnchor: sourceAnchor,
						target: targetId,
						targetAnchor: targetAnchor,
						style: {
							stroke: VALUE_TYPE_COLOR_MAP.nxt_edge_id
						}
					})
					isBreak = true
					break
				}
			}
			if (!isBreak) {
				let sourceAnchor = FUNC_GET_EDGE_ANCHORPOINT_INDEX_FROM_ID(nodeMap[sourceId], 0)
				let targetAnchor = FUNC_GET_EDGE_ANCHORPOINT_INDEX_FROM_ID(nodeMap[targetId], null)
				data.edges.push({
					id: edge.id,
					source: sourceId,
					sourceAnchor: sourceAnchor,
					target: targetId,
					targetAnchor: targetAnchor,
					style: {
						stroke: VALUE_TYPE_COLOR_MAP.nxt_edge_id
					}
				})
			}
		}
	}

	graph[graphElementID].read(data)

	data = JSON.parse(JSON.stringify(data))
	// console.log(data)
	return data
}

const changeLang = (_lang) => {
	if (_lang in Lang) {
		lang = _lang
		for (const id in graph) {
			const data = JSON.parse(JSON.stringify(graph[id].save()))
			graph[id].clear()
			graph[id].data(data)
			graph[id].render()
			const nodes = graph[id].getNodes()
			nodes.forEach((node, index) => {
				Event.emit("rqChangeNodeLang#" + id, node.getModel())
			})
		}
	}
}

const undo = (graphElementID) => {
	const id = graphElementID
	const graph_ = graph[id]
	const undoStack = graph_.getUndoStack();
	// console.log('getStackData', graph_.getStackData());
	if (!undoStack || undoStack.length === 0) {
		return;
	}
	let currentData = undoStack.pop();
	// console.log(currentData);
	let { action, data } = currentData;
	const doAction = (graph_, action, data) => {
		switch (action) {
			case 'addNodes': {
				const { addNodes } = data
				addNodes.forEach((node, index) => {
					graph_.removeItem(node.id, false)
				})
			}
				break
			case 'updateNodes': {
				const { originNodes, updateNodes } = data
				originNodes.forEach((node, index) => {
					graph_.updateItem(node.id, node, false)
				})
			}
				break
			case 'updateEdges': {
				const { addEdges, delEdges } = data
				addEdges.forEach((edge, index) => {
					graph_.removeItem(edge.id, false)
				})
				delEdges.forEach((edge, index) => {
					graph_.addItem('edge', edge, false)
				})
			}
				break
			case 'deleteItems': {
				const { delNodes, delEdges } = data
				delNodes.forEach((node, index) => {
					graph_.addItem('node', node, false)
				})
				delEdges.forEach((edge, index) => {
					graph_.addItem('edge', edge, false)
				})
			}
				break
			case 'update':
				let data_ = data.before
				Object.keys(data_).forEach((key) => {
					const array = data_[key]
					if (!array) return
					array.forEach((model) => {
						const item = graph_.findById(model.id)
						// delete model.id
						graph_.updateItem(item, model, false)
						if (item.getType() === 'combo') graph_.updateCombo(item)
					})
				})
				break
			default:
				return false
		}
		return true
	}
	while (!doAction(graph_, action, data)) {
		currentData = undoStack.pop()
		action = currentData.action
		data = currentData.data
	}
	graph_.pushStack(action, data, 'redo');
}

const redo = (graphElementID) => {
	const id = graphElementID
	const graph_ = graph[id]
	const redoStack = graph_.getRedoStack();
	// console.log('getStackData', graph_.getStackData());
	if (!redoStack || redoStack.length === 0) {
		return;
	}
	const currentData = redoStack.pop();
	// console.log(currentData);
	const { action, data } = currentData;
	graph_.pushStack(action, data, 'undo');
	switch (action) {
		case 'addNodes': {
			const { addNodes } = data
			addNodes.forEach((node, index) => {
				graph_.addItem('node', node, false)
			})
			break
		}
		case 'updateNodes': {
			const { originNodes, updateNodes } = data
			updateNodes.forEach((node, index) => {
				graph_.updateItem(node.id, node, false)
			})
			break
		}
		case 'updateEdges': {
			const { addEdges, delEdges } = data
			delEdges.forEach((edge, index) => {
				graph_.removeItem(edge.id, false)
			})
			addEdges.forEach((edge, index) => {
				graph_.addItem('edge', edge, false)
			})
			break
		}
		case 'deleteItems': {
			const { delNodes, delEdges } = data
			delNodes.forEach((node, index) => {
				graph_.removeItem(node.id, false)
			})
			delEdges.forEach((edge, index) => {
				graph_.removeItem(edge.id, false)
			})
			break
		}
		case 'update':
			let data_ = data.after
			Object.keys(data_).forEach((key) => {
				const array = data_[key]
				if (!array) return
				array.forEach((model) => {
					const item = graph_.findById(model.id)
					//   delete model.id
					graph_.updateItem(item, model, false)
					if (item.getType() === 'combo') graph_.updateCombo(item)
				})
			})
			break
		default:
	}
}

/*
## Features:
- Support multi graph
*/

/*
## Event:

${graphElementID} is replaced with the element id, which needs to be used for multiple graphs

### Graph emit, view listening
- rqAddNode#${graphElementID}: {x,y}
- rqEditNodeAttr#${graphElementID}: {id,input,input_intro,input_type...}  //node
- rqChangeNodeLang#${graphElementID}: {id,input,input_intro,input_type...}  //node
- rqShowMessage#${graphElementID}: {type,message}  //message

### Graph listening, view emit
- addNode#${graphElementID}: {x,y,id,input,input_intro,input_type,name,node_name...}  // node & after editing "rqAddNode"'s params
- editNodeAttr#${graphElementID}:  {id,input,input_intro,input_type...}  //node after editing "rqEditNodeAttr"'s params
*/

/*
## Shortcut
- Delete/Backspace: delete node
- Ctrl+Z: undo
- Ctrl+Y: redo
- Shift+MouseLeftClickSelect: multi-select
*/

export {
	Event,
	initGraph,
	saveConfig,
	loadConfig,
	changeLang,
	undo,
	redo,
}
