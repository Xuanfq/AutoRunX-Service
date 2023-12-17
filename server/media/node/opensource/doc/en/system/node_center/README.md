## Introduce

Node _ center: node center.

In this framework, the module used to store and generate nodes mainly stores the input and output data of nodes in the form of map. Where key is `node_id` or `node_name`, `node_name` that is, the module name. `node_id` When key is used, the node will not be destroyed, but the module may have multiple instances; When it `node_name` is a key, the execution order determines the number of module instances. Since there is no relevant requirement at present and the requirement has not been developed, this usage is retained at present.

Nodes are generally generated once and destroyed after running, and are not retained, except for global modules such as AOP and log. The node can continue to keep alive after execution by adding keep _ alive = True in the return parameter.



## Method




## Example Code


```python

```