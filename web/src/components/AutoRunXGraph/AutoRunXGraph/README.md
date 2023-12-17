
# AutoRunXGraph


## Event:

`${graphElementID}` is replaced with the element id, which needs to be used for multiple graphs


### Graph emit, view listening
- rqAddNode#${graphElementID}: 
  - {x,y}
- rqEditNodeAttr#${graphElementID}: 
  - {id,input,input_intro,input_type...}  //node
- rqChangeNodeLang#${graphElementID}: 
  - {id,input,input_intro,input_type...}  //node
- rqShowMessage#${graphElementID}: 
  - {type,message}  //message


### Graph listening, view emit
- addNode#${graphElementID}: 
  - {x,y,id,input,input_intro,input_type,name,node_name...}  // node & after editing "rqAddNode"'s params
- editNodeAttr#${graphElementID}:  
  - {id,input,input_intro,input_type...}  //node after editing "rqEditNodeAttr"'s params



## Shortcut
- Delete/Backspace: delete node
- Ctrl+Z: undo
- Ctrl+Y: redo
- Shift+MouseLeftClickSelect: multi-select
