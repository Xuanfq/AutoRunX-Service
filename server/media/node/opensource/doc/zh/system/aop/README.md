

## Introduce

AOP：全称Aspect Oriented Programming，意为面向切面编程。

本框架中，用于记录非系统层（lib/目录下除system的库）的代码执行过程，即主要记录配置文件执行过程。

可用于代码调试等。


## Method

### init()

**必须参数**


**可选参数**

- AOP_LOG_FILE: aop 日志输出文件
- AOP_MODULE_NAME: aop 模块名


**用法**

模块初始化时调用
```python
init(AOP_LOG_FILE="log/aop.log")
```



### aop()

**必须参数**

- id: 节点id
- name: 节点名称


**可选参数**


**用法**

开发者不应调用该方法，应由框架系统调用，如engine。
```python
@globals.aop(id=id,name=node_config["node_name"])
def node_run(*args,**kwargs):
    global running_node_id,runnint_node_config
    running_node_id=id
    runnint_node_config=copy.deepcopy(nodes_config[id])
    results = node.run(*args,**kwargs)
    running_node_id=""
    runnint_node_config=None
    return results
results=node_run(**node_config["input"])
```



## Example Code
```python
# init
init(AOP_LOG_FILE="log/aop.log")
```

```python
# aop
# node.run()是被切面的方法
@globals.aop(id=id,name=node_config["node_name"])
def node_run(*args,**kwargs):
    global running_node_id,runnint_node_config
    running_node_id=id
    runnint_node_config=copy.deepcopy(nodes_config[id])
    results = node.run(*args,**kwargs)
    running_node_id=""
    runnint_node_config=None
    return results
results=node_run(**node_config["input"])
```











