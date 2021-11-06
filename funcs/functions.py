from .helpers import setLog,getLog,dateDiff

import time
import json
import subprocess


# Get Nodes
def getNodes(nodesFile,cmd,nodesLst):
    setLog(nodesFile,cmd)
    getLog(nodesFile,nodesLst)


# Get Pods
def getNodePods(podsFile,node,trail,cmd,podstmpFile,nodePods):
    # Print all pods for every node
    trail = trail + node
    setLog(podsFile,cmd,trail)

    ## Get current node pods
    with open(podstmpFile) as podFiles:
        pods = podFiles.readlines()
        for pod in pods:
            if not pod.isspace():
                nodePods.append(pod.strip())

# Evaluate Pod Description
def evalPod(file,cmd,currentPod):
    with open(file, 'w') as out:
        stdout = subprocess.call(cmd, stdout=out)

    outputFile = open(file, 'r')
    Lines = outputFile.readlines()

    # Reset
    currentPod = {}
    currentPod ['pod'] = 'none'
    currentPod ['rule_evaluation'] = [{}]
    others = [{},{},{}]  
    
    # Team Label
    others[1] = ({'name':'team_label_present','valid':False})
    
    # Iterate
    for line in Lines:

        # Get Pod Name
        #if 'Name:' in line.strip():
        if line.strip().startswith('Name:'):
            currentPod['pod'] = line.split('Name:')[1].strip()
           
        # Get Pod Image
        if 'Image:' in line.strip():
            imageName = line.split('Image:')[1].strip()
            others[0] = vaidateImagePrefix(imageName)

        # Check Pod Team Label

        #if 'team=' in line.strip():
        if  line.strip().find('team=') != -1:
            others[1] = ({'name':'team_label_present','valid':True})
        
        # Validate Pod Start Date
        validStartDate = False
        if'Start Time:' in line.strip():
            startDate = line.split('Start Time:')[1].strip()
            others[2] = vaidatePodDates(startDate,7) 
       

        currentPod['rule_evaluation'] = others
    # Sleep
    time.sleep(.3)

    #Json Response 
    json_object = json.dumps(currentPod, indent = 4) 
    print(json_object)

    out.close()
 
# Validate Prefix
def vaidateImagePrefix(imageName):
    valid = False
    if imageName.find('bitnami/') != -1:
        valid = True
      
    return {'name' : imageName,'valid':valid}
 
#  Validate pod Date
def vaidatePodDates(startDate,deltaDays):
    validStartDate = False
    if(dateDiff(startDate,deltaDays)):
        validStartDate = True 
    return {'name':'recent_start_time','valid':validStartDate}
