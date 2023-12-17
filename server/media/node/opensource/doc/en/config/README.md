## Introduce

This document focuses on the configuration file for framework startup.



### common

Configuration of globally common module parameters.


#### aop

Refer to the configuration file for the AOP module.


#### log

Refer to the log module's configuration file.



### graph

The process of program execution is mainly represented by program flow chart, which consists of nodes and directed edges.


#### node

**Configuration description**

-  `id` : String. The node ID should be guaranteed to be globally unique and preserve the key distinguishing attributes of the node type.
-  `name` : String. The name, or more precisely, the label, is easy for the user to remember, and it should be distinguished from the node _ name.
-  `node_name` : String. Node name, which is actually the module name in the code and the file name without suffix.
-  `node_type` : String. Node types. According to the lib code base and the framework engine, there are six main node types: `start/ end/ ctrl/ func/ dtio/ dtpc`. Where `dtio` and `dtpc` are data nodes (data flows) and the others are process nodes (program flow control flows). In the data node, the complete input parameters can be output, and the data flow is automatically managed and calculated by the framework engine. The program flow control flow is closely related to the function node execution logic and execution process configured by the user.
-  `pre_edge_id` : Array. The ID of the previous edge, that is, the ID of the edge pointing to this node in the directed edge.
-  `nxt_edge_id` : Array. The ID of the back edge, that is, the ID of the edge in the directed edge where this node points to another node.
-  `nxt_edge_id_intro` : Array. A brief introduction to each element `nxt_edge_id` in.
-  `input` : Dictionary, object. Parameters and values that need to be passed in during the execution of this node. Each parameter is a data node. If the ID of "this node" mentioned above is 1, the node ID of parameter 1 is: `"{}.input.{}".format(1,"parameter_1")`. If the provided parameter value is static, it can be configured in the configuration of the corresponding node. If it is dynamic, it can be linked to the parameter value source through the "directed edge" (the edge points to the parameter node, and the edge between general data nodes points to `xxx.output.yyy --> aaa.input.bbb`).
-  `input_type` : Dictionary, object. The type corresponding to the field `input` in the.
-  `input_intro` : Dictionary, object. The introduction corresponding to the field `input` in.
-  `output` : Dictionary, object. The parameter and value returned after the node is executed. Each parameter is a data node. If the ID of "this node" mentioned above is 1, the node ID of parameter 1 is: `"{}.output.{}".format(1,"parameter_1")`. The parameter value can be passed to the input parameters of other nodes through the "directed edge" (the edge points to the parameter node of other nodes, and the edge between general data nodes points to `xxx.output.yyy --> aaa.input.bbb`).
-  `input_type` : Dictionary, object. The type corresponding to the field `output` in the.
-  `input_intro` : Dictionary, object. The introduction corresponding to the field `output` in.




#### edge

**Configuration description**

-  `id` : String. The directed edge ID should be guaranteed to be globally unique and preserve the key distinguishing property of the node type.
-  `name` : String. The name, or more precisely, the label, is easy for the user to remember.
-  `pre_id` : The ID of the starting node of the directed edge.
-  `nxt_id` : The ID of the node where the directed edge terminates.




## Example Code


```json
{
    "common": {
        "aop": {
            "AOP_MODULE_NAME": "aop",
            "AOP_LOG_FILE": "log/aop.log"
        },
        "log": {
            "LOG_MODULE_NAME": "log",
            "COMMON_LOG_FILE": "log/common.log",
            "LOG_FILE": "log/func.log"
        }
    },
    "graph": {
        "node_list": [
            {
                "id": "flow-01",
                "name": "",
                "node_name": "ctrl-start",
                "node_type": "start",
                "pre_edge_id": [],
                "nxt_edge_id": [
                    "flow-01 --> flow-02"
                ],
                "input": {},
                "output": {}
            },
            {
                "id": "flow-02",
                "name": "",
                "node_name": "ctrl-for",
                "node_type": "ctrl",
                "pre_edge_id": [
                    "flow-01 --> flow-02"
                ],
                "nxt_edge_id": [
                    "flow-02 --> flow-03"
                ],
                "input": {
                    "start_index": 0,
                    "end_index": 5,
                    "step": 1
                },
                "output": {}
            },
            {
                "id": "flow-03",
                "name": "",
                "node_name": "ctrl-end",
                "node_type": "end",
                "pre_edge_id": [
                    "flow-02 --> flow-03"
                ],
                "nxt_edge_id": [],
                "input": {},
                "output": {}
            },
            {
                "id": "flow-formain",
                "name": "",
                "node_name": "func-test-1692798936169238-bc2b8ee241bc11ee8331dcf505272cb8-0_0_1",
                "node_type": "func",
                "pre_edge_id": [],
                "nxt_edge_id": [],
                "input": {
                    "test": "formain"
                },
                "output": {}
            }
        ],
        "edge_list": [
            {
                "id": "flow-01 --> flow-02",
                "name": "",
                "pre_id": "flow-01",
                "nxt_id": "flow-02"
            },
            {
                "id": "flow-02 --> flow-03",
                "name": "",
                "pre_id": "flow-02",
                "nxt_id": "flow-03"
            },
            {
                "id": "flow-02 --> flow-formain",
                "name": "",
                "pre_id": "flow-02.input.loop_edge_id",
                "nxt_id": "flow-formain"
            },
            {
                "id": "flow-02.output.index --> flow-formain",
                "name": "",
                "pre_id": "flow-02.output.index",
                "nxt_id": "flow-formain.input.index"
            }
        ]
    }
}
```













































