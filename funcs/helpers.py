from datetime import datetime
import subprocess

# Log To a file
def setLog(file,cmd,trail = None):
    with open(file, 'w') as out:
        if(trail != None):
            cmd = formatCommand(cmd, trail)
        stdout = subprocess.call(cmd, stdout=out)


# Get Log
def getLog(file,lstOf):
    with open(file,'r') as outputFile:
        Lines = outputFile.readlines()
        for line in Lines:
            lstOf.append(line.strip())


# Get Date Diff
def dateDiff(givenDate,compare):
    #Date Cleansing
    splittedDate= givenDate.split(' ')
    cleanedDateTime = ' '.join(splittedDate[1:5])

    formatteDateTime = datetime.strptime(cleanedDateTime,'%d %b %Y %H:%M:%S')
    
    currentDateTime = datetime.now()

    delta = currentDateTime - formatteDateTime
    deltaDays = delta.days;

    if(deltaDays < compare):
        return True
    
    return False

# Format CMD Command
def formatCommand(cmd,trail):
    cmd.append(trail)
    return cmd

