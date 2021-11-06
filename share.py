from funcs.helpers import formatCommand
from funcs.functions import getNodes,getNodePods,evalPod
from config.config import *
from config.cmd import *

## Get node names
getNodes(nodesFile,cmd1,nodes)
 
## Get Node Pods
for node in nodes:
    trail = "spec.nodeName="
    getNodePods(podstmpFile,node,trail,cmd2,podstmpFile,nodePods)

## Evaluate Pods
for pod in nodePods:
    cmd3.pop()
    cmd = formatCommand(cmd3, pod)
    evalPod(podDescFile,cmd,currentPod)
    







