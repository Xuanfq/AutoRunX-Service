

## Introduce

本文档主要介绍框架启动的配置文件。



### common

全局通用的模块参数的配置。


#### aop

请参考aop模块的配置文件。


#### log

请参考log模块的配置文件。



### graph

程序执行过程主要通过程序流程图表现，“图”由节点和有向边。


#### node

**配置说明**

- `id`: 字符串。节点id，应保证全局唯一并保留节点类型的关键区别属性。
- `name`: 字符串。名字，更确切来讲应该是标签，方便用户记忆，注意和node_name区分开来。
- `node_name`: 字符串。节点名称，实际为代码中的模块名、不带后缀的文件名。
- `node_type`: 字符串。节点类型，根据lib代码库以及框架引擎，主要节点类型有6种：`start / end / ctrl / func / dtio / dtpc`。其中`dtio`和`dtpc`是数据节点（数据流），其他为流程节点（程序流程控制流）。数据节点中，输入参数完整即可输出，数据流完全由框架引擎自动管理和计算。程序流程控制流与用户配置的功能节点执行逻辑、执行过程密切相关。
- `pre_edge_id`: 数组。前边的id，即有向边中指向本节点的边的id。
- `nxt_edge_id`: 数组。后边的id，即有向边中本节点指向其他节点的边的id。
- `nxt_edge_id_intro`: 数组。`nxt_edge_id`中各元素对应的简介。
- `input`: 字典、对象。本节点执行时需要传入的参数和值。其中，每一个参数都是一个数据节点，若上述提的“本节点”的id是1，则参数1节点id为：`"{}.input.{}".format(1,"参数1")`。若提供的参数值是静态的，可在对应节点的配置中进行配置，若是动态的，可通过“有向边”链接到参数值来源（边指向该参数节点，一般数据节点间边指向为`xxx.output.yyy --> aaa.input.bbb`）。
- `input_type`: 字典、对象。`input`中字段对应的类型。
- `input_intro`: 字典、对象。`input`中字段对应的简介。
- `output`: 字典、对象。本节点执行时完成后返回的参数和值。其中，每一个参数都是一个数据节点，若上述提的“本节点”的id是1，则参数1节点id为：`"{}.output.{}".format(1,"参数1")`。可通过“有向边”把参数值传到其他节点的输入参数中（边指向其他节点的参数节点上，一般数据节点间边指向为`xxx.output.yyy --> aaa.input.bbb`）。
- `input_type`: 字典、对象。`output`中字段对应的类型。
- `input_intro`: 字典、对象。`output`中字段对应的简介。




#### edge

**配置说明**

- `id`: 字符串。有向边id，应保证全局唯一并保留节点类型的关键区别属性。
- `name`: 字符串。名字，更确切来讲应该是标签，方便用户记忆。
- `pre_id`: 有向边起始节点的id。
- `nxt_id`: 有向边终止节点的id。




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













































