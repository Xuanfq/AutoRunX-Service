## Introduce

Engine: engine.

The framework is an execution framework of a program flow chart. The framework defines a set of program flow charts, which are composed of a main node and an edge. Edges are mainly used to link nodes, no actual code needs to be executed, and all code is in nodes.

In lib, except for the system directory, all directories are node directories, including two types of nodes: data and flow. Data includes dataio (data input and output, data definition) and dataprocess (data processing). A flow includes a flowcontrol and a flowfunction. Of course, events, including eventreceive and eventtransmit, also belong to the flow class.

The data node is data-dependent, requiring no involvement in process control, and is scanned and processed by the algorithm.

The flow node is related to the process, and the execution process of the control program follows the program flow chart, so process control is required. The flowcontrol is the key to controlling the direction of the process, and there is generally no need to add or modify the code base.

In addition, it should be noted that the event node is unique. After the program is started, all passive event (event receive, nodes that cannot be directly called or triggered by the user) will run, and all flow nodes will run directly or indirectly through event (event receive). Therefore, do not write code in an event that blocks other events from starting. The active class event (event transmit, an event node that can be directly called and triggered by the user) is triggered when the user performs process control, such as calling or triggering through flowcontrol, flowfunction, or event receive. Event receive and event transmit can communicate with each other through globals, engine, etc.

The common code base that developers need to modify is flowfunction.





## Method




## Example Code


```python

```