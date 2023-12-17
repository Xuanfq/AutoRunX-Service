## Introduce

Log: log, record.

In this frame, it is used for logging.

Can be used for code debugging, etc.



## Method

### init()

**Required parameter**


**Optional parameters**

- COMMON _ LOG _ FILE: common log file. All logs are in this file.
- FUNC _ LOG _ FILE: Logs of modules under lib/flow/function are output to this log file.


**Usage**

Called when the module is initialized

```python
init(COMMON_LOG_FILE="log/common.log",LOG_FILE="log/func.log")
```


### comon_log()

**Required parameter**

- MSG: log information


**Optional parameters**


**Usage**

Developers should not call this method, but should trigger it through func _ log () and other methods. See the source code of func _ log () for details of the triggering process.



### log()

**Required parameter**

- MSG: log information


**Optional parameters**

- Second _ log _ file: In addition to the FUNC _ LOG _ FILE, log messages will also be logged to this file.


**Usage**

```python
log(msg="func test start...")
```



## Example Code


```python
# init
init(COMMON_LOG_FILE="log/common.log",LOG_FILE="log/func.log")
```


```python
# func log
log(msg="func test start...")
```











