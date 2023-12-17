from django.shortcuts import render

from django.http import JsonResponse
from . import models
import json
from . import utils
import os


# node/delete
def delete(request):
    """
    post: {data:[]} | {data:{}}
    """
    if not utils.is_method_POST(request):
        return JsonResponse({"flag": False, "data": "Error Request Method"})
    # print("delete node")
    _data = json.loads(request.body)["data"]
    data = _data if isinstance(_data, list) else [_data]
    result = []
    for nodedata in data:
        if 'node_name' in nodedata:
            node_name = nodedata['node_name']
            query_result = models.Node.objects.filter(node_name=node_name)
            for node in query_result:
                result.append({'node_name': node.node_name})
                node.delete()
    return JsonResponse({"flag": True, "data": result})


# node/add
def add(request):
    """
    post: {data:[]} | {data:{}}
    """
    if not utils.is_method_POST(request):
        return JsonResponse({"flag": False, "data": "Error Request Method"})
    lang = request.GET.get('lang', None)
    if lang is None:
        return JsonResponse({"flag": False, "data": "Error Request Params"})
    _data = json.loads(request.body)["data"]
    data = _data if isinstance(_data, list) else [_data]
    for nodedata in data:
        # print("nodedata", nodedata, 'input_intro' in nodedata)
        node = models.Node(node_name=nodedata['node_name'],
                           name=nodedata['name'],
                           node_type=nodedata['node_type'],
                           pre_edge_id=json.dumps(
                               nodedata['pre_edge_id'], ensure_ascii=False),
                           nxt_edge_id=json.dumps(
                               nodedata['nxt_edge_id'], ensure_ascii=False),
                           nxt_edge_id_intro=json.dumps(
                               nodedata['nxt_edge_id_intro'], ensure_ascii=False) if 'nxt_edge_id_intro' in nodedata else "[]",
                           input=json.dumps(
                               nodedata['input'], ensure_ascii=False),
                           input_type=json.dumps(
                               nodedata['input_type'], ensure_ascii=False),
                           input_intro=json.dumps(
                               nodedata['input_intro'], ensure_ascii=False),
                           output=json.dumps(
                               nodedata['output'], ensure_ascii=False),
                           output_type=json.dumps(
                               nodedata['output_type'], ensure_ascii=False),
                           output_intro=json.dumps(
                               nodedata['output_intro'], ensure_ascii=False),
                           readme=nodedata['readme'] if 'readme' in nodedata else '',
                           lang=lang
                           )
        node.save()
        # print("node",node)
    return JsonResponse({"flag": True, "data": None})


# node/sync
def sync(request):
    """
    post:
    """
    if not utils.is_method_POST(request):
        return JsonResponse({"flag": False, "data": "Error Request Method"})

    def sync_sublib(sublib):
        zh, en = utils.generate_node_list_for_web(
            os.path.join(os.getcwd(), 'media', 'node', sublib, 'doc'))
        data = zh[0]+en[0]
        for nodedata in data:
            node = models.Node(node_name=nodedata['node_name'],
                               name=nodedata['name'],
                               node_type=nodedata['node_type'],
                               pre_edge_id=json.dumps(
                nodedata['pre_edge_id'], ensure_ascii=False),
                nxt_edge_id=json.dumps(
                nodedata['nxt_edge_id'], ensure_ascii=False),
                nxt_edge_id_intro=json.dumps(
                nodedata['nxt_edge_id_intro'], ensure_ascii=False) if 'nxt_edge_id_intro' in nodedata else "[]",
                input=json.dumps(
                nodedata['input'], ensure_ascii=False),
                input_type=json.dumps(
                nodedata['input_type'], ensure_ascii=False),
                input_intro=json.dumps(
                nodedata['input_intro'], ensure_ascii=False),
                output=json.dumps(
                nodedata['output'], ensure_ascii=False),
                output_type=json.dumps(
                nodedata['output_type'], ensure_ascii=False),
                output_intro=json.dumps(
                nodedata['output_intro'], ensure_ascii=False),
                readme=nodedata['readme'] if 'readme' in nodedata else '',
                lang=nodedata['lang'],
                lib_id=sublib
            )
            node.save()
    models.Node.objects.all().delete()
    sync_sublib('opensource')
    return JsonResponse({"flag": True, "data": None})


# node/get_config
def get_config(request):
    """
    get: null | uri?node_name=xxx
    """
    if not utils.is_method_GET(request):
        return JsonResponse({"flag": False, "data": "Error Request Method"})
    # print("get node")
    lang = request.GET.get('lang', None)
    if lang is None:
        return JsonResponse({"flag": False, "data": "Error Request Params"})
    node_name = request.GET.get('node_name', None)
    if node_name is None:
        query_result = models.Node.objects.filter(lang=lang, delete_time=None)
    else:
        query_result = models.Node.objects.filter(node_name=node_name,
                                                  lang=lang, delete_time=None)
    result = []
    for node in query_result:
        result.append({
            "id": "",
            "node_name": node.node_name,
            "name": node.name,
            "node_type": node.node_type,
            "pre_edge_id": json.loads(node.pre_edge_id),
            "nxt_edge_id": json.loads(node.nxt_edge_id),
            "nxt_edge_id_intro": json.loads(node.nxt_edge_id_intro),
            "input": json.loads(node.input),
            "input_type": json.loads(node.input_type),
            "input_intro": json.loads(node.input_intro),
            "output": json.loads(node.output),
            "output_type": json.loads(node.output_type),
            "output_intro": json.loads(node.output_intro),
        })
    # print(data)
    return JsonResponse({"flag": True, "data": result})


# node/get_readme
def get_readme(request):
    """
    get: null | uri?node_name=xxx
    """
    if not utils.is_method_GET(request):
        return JsonResponse({"flag": False, "data": "Error Request Method"})
    # print("get node")
    lang = request.GET.get('lang', None)
    if lang is None:
        return JsonResponse({"flag": False, "data": "Error Request Params"})
    node_name = request.GET.get('node_name', None)
    if node_name is None:
        query_result = models.Node.objects.filter(lang=lang, delete_time=None)
    else:
        query_result = models.Node.objects.filter(node_name=node_name,
                                                  lang=lang, delete_time=None)
    result = []
    for node in query_result:
        result.append({
            "node_name": node.node_name,
            "readme": node.readme,
        })
    # print(data)
    return JsonResponse({"flag": True, "data": result})
