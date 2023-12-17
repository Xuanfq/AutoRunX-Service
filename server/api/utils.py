
import sys
import os
import json


def is_method_GET(request):
    return request.method == 'GET'


def is_method_POST(request):
    return request.method == 'POST'


def is_method_PUT(request):
    return request.method == 'PUT'


def is_method_DELETE(request):
    return request.method == 'DELETE'


def is_method_CONNECT(request):
    return request.method == 'CONNECT'


def is_method_OPTIONS(request):
    return request.method == 'OPTIONS'


def is_method_HEAD(request):
    return request.method == 'HEAD'


def is_method_TRACE(request):
    return request.method == 'TRACE'


def datetime2jsobject(datetime):
    if datetime is None:
        return None
    return int(datetime.timestamp()*1000)


def generate_node_list_for_web(doc_root):
    def get_node_list_by_type_lang(module_root, lang):
        result = []
        for item in os.listdir(module_root):
            config_path = os.path.join(module_root, item, "config.json")
            readme_path = os.path.join(module_root, item, "README.md")
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    config['lang'] = lang
                    config['readme'] = ''
                    with open(readme_path, "r", encoding="utf-8") as rm:
                        config['readme'] = rm.read()
                    result.append(config)
        return result

    def get_node_list_by_lang(doc_root, lang):
        lib_root = os.path.join(doc_root, lang, 'lib')
        dtio = get_node_list_by_type_lang(
            os.path.join(lib_root, "dataio"), lang)
        dtpc = get_node_list_by_type_lang(
            os.path.join(lib_root, "dataprocess"), lang)
        ctrl = get_node_list_by_type_lang(
            os.path.join(lib_root, "flowcontrol"), lang)
        func = get_node_list_by_type_lang(
            os.path.join(lib_root, "flowfunction"), lang)
        evrx = get_node_list_by_type_lang(
            os.path.join(lib_root, "eventreceive"), lang)
        evtx = get_node_list_by_type_lang(
            os.path.join(lib_root, "eventtransmit"), lang)
        node_data = [{
            'type': 'dtio',
            'name': '输入输出节点' if lang == 'zh' else 'Input/Output Node',
            'nodeList': dtio
        }, {
            'type': 'dtpc',
            'name': '数据处理节点' if lang == 'zh' else 'Data Processing Node',
            'nodeList': dtpc
        }, {
            'type': 'ctrl',
            'name': '程序控制节点' if lang == 'zh' else 'Program Control Node',
            'nodeList': ctrl
        }, {
            'type': 'func',
            'name': '程序功能节点' if lang == 'zh' else 'Program Function Node',
            'nodeList': func
        }, {
            'type': 'evrx',
            'name': '事件发生节点' if lang == 'zh' else 'Event Start Node',
            'nodeList': evrx
        }, {
            'type': 'evtx',
            'name': '事件触发节点' if lang == 'zh' else 'Event Emit Node',
            'nodeList': evtx
        }]
        all_node = dtio+dtpc+ctrl+func+evrx+evtx
        return all_node, node_data

    zh = get_node_list_by_lang(doc_root, lang='zh')
    en = get_node_list_by_lang(doc_root, lang='en')
    return zh, en


if __name__ == '__main__':
    result = generate_node_list_for_web(os.path.join(
        sys.path[0], "../media/node/doc"))
    print(result[0])
