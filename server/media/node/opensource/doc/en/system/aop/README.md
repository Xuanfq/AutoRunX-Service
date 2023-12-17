## Introduce

AOP: The full name of Aspect Oriented Programming, meaning aspect-oriented programming.

In this framework, it is used to record the code execution process of the non-system layer (libraries under the lib/directory except system), that is, it is mainly used to record the execution process of the configuration file.

Can be used for code debugging, etc.


## Method

### init()

**Required parameter**


**Optional parameters**

- AOP _ LOG _ FILE: AOP log output films
- AOP _ MODULE _ NAME: AOP module name


**Usage**

Called when the module is initialized

```python
init(AOP_LOG_FILE="log/aop.log")
```



### aop()

**Required parameter**

- ID: node ID
- Name: Node name


**Optional parameters**


**Usage**

This method should not be called by the developer, but by the framework system, such as engine.

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
# node.run() is the way to be cut
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











