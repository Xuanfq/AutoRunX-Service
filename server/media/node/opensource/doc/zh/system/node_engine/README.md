

## Introduce

engine：引擎。

本框架是一个程序流程图的执行框架，本框架定义了一套程序流程图，主由节点(node)和边(edge)组成。边主要用于链接节点，无实际代码需执行，一切代码都在节点中。

在lib中，除system目录外皆为节点目录，包含data和flow两大类节点，data包括dataio(数据输入输出，数据定义)以及dataprocess(数据处理)，flow包括flowcontrol(流程控制)以及flowfunction(流程功能)。当然，事件event包括eventreceive和eventtransmit也属于flow类。

data类节点是数据相关，无需介入流程控制，由算法进行扫描并执行数据处理。

flow类节点是流程相关，控制程序执行流程按照程序流程图走，需进行流程控制。flowcontrol是流程走向控制的关键，一般不需要添加或修改该代码库。

另外需要注意event事件的结点是唯一的，程序启动后会运行所有被动类event(eventreceive，不能被用户直接调用或触发的结点)，所有的flow结点通过event(eventreceive)直接或间接运行。因此，请勿在event中书写阻塞其他event启动的代码。主动类event(eventtransmit，用户能直接调用、触发的event结点)由用户进行流程控制时触发，如通过flowcontrol、flowfunction或eventreceive调用或触发。eventreceive和eventtransmit间能通过globals、engine等相互通讯。

开发者一般需要修改的代码库是flowfunction。





## Method




## Example Code

```python
```
