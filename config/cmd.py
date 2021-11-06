from .config import nameSpace

# List all nodes
cmd1 = ["kubectl","get","nodes","-o=jsonpath={range.items[*]}{.metadata.name}"]

# List all pods in a apecific node
cmd2 = ["kubectl","get","pods","-n",nameSpace,"-o","wide","-o=jsonpath={range.items[*]}{.metadata.name}\n","--field-selector"]
 
# Describe a specific pod in a node
cmd3 = ['kubectl','describe','pod','POD_NAME_HERE']