

## Introduce

node_center：节点中心。

本框架中，用于储存、生成node模块，主要以map的方式储存节点输入和输出的数据。其中key为`node_id`或`node_name`，`node_name`也即模块名，`node_id`为key时，节点不销毁，但模块可能会有多个实例；而`node_name`为key时，执行顺序决定模块实例个数，由于目前还没有相关的需求，且需求并未开发，所以目前保留该用法。

节点一般一次生成一次运行后销毁，不作保留，当然aop、log等全局模块除外。节点可在执行后继续keep alive，只需在返回参数中加入keep_alive=True即可。



## Method




## Example Code

```python
```
