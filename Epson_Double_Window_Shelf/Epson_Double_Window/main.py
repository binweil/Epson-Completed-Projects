# This example illustrates how to use the path/motion
# planning functionality from a remote API client.
#
# Load the demo scene 'motionPlanningServerDemo.ttt' in V-REP 
# then run this program. 
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

import vrep
import numpy as np
import math

data = np.genfromtxt("Start_and_Goal_Config.txt")
data = np.around(data, decimals=4)
data = data.tolist()
data_sample = [0,-0.88073,-0.16937,0,1.09779,0]
data_go = [0,-1.35204,-0.02597,0,1.26186,0]

def listToStringWithoutBrackets(list1):
    return str(list1).replace('[','').replace(']','')

print ('Program started')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19997,True,True,-500000,5) # Connect to V-REP, set a very large time-out for blocking commands
if clientID!=-1:
    print ('Connected to remote API server')
    emptyBuff = bytearray()
    #Start the simulation:
    vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot_wait)
    # Load a robot instance: res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_childscript,'loadRobot',[],[0,0,0,0],['d:/v_rep/qrelease/release/test.ttm'],emptyBuff,vrep.simx_opmode_oneshot_wait)
    #    robotHandle=retInts[0]
    # Retrieve some handles:
    res,robotHandle=vrep.simxGetObjectHandle(clientID,'Epson#',vrep.simx_opmode_oneshot_wait)  
    # res,target1=vrep.simxGetObjectHandle(clientID,'testPose1#',vrep.simx_opmode_oneshot_wait)
    tryConfig = [0.5,0.5,-0.5,0.5,0.5,0.5]

    # Retrieve the poses (i.e. transformation matrices, 12 values, last row is implicit) of some dummies in the scene
    # res,retInts,target1Pose,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_childscript,'getObjectPose',[target1],[],[],emptyBuff,vrep.simx_opmode_oneshot_wait)

    res, retInts, robotInitialState, retStrings, retBuffer = vrep.simxCallScriptFunction(clientID, 'remoteApiCommandServer', vrep.sim_scripttype_childscript,'getRobotState',[robotHandle],[],[],emptyBuff,vrep.simx_opmode_oneshot_wait)
    
     # Some parameters:
    approachVector = [0, 0, 0]  #often a linear approach is required. This should also be part of the calculations when selecting an appropriate state for a given pose
    maxConfigsForDesiredPose = 100  # we will try to find 10 different states corresponding to the goal pose and order them according to distance from initial state
    maxTrialsForConfigSearch=300 # a parameter needed for finding appropriate goal states
    searchCount=4 # how many times OMPL will run for a given task
    minConfigsForPathPlanningPath=400 # interpolation states for the OMPL path
    minConfigsForIkPath=100 # interpolation states for the linear approach path
    collisionChecking=1 # whether collision checking is on or off

    inInts=[robotHandle,collisionChecking,minConfigsForPathPlanningPath,searchCount]
    
    res, retInts, robotCurrentConfig, retStrings ,retBuffer = vrep.simxCallScriptFunction(clientID, 'remoteApiCommandServer', vrep.sim_scripttype_childscript, 'getRobotState',[robotHandle],[],[],emptyBuff,vrep.simx_opmode_oneshot_wait)
    for i in range(0, int(len(data) / 2), 1):
        #inFloats = data[2*i]+data[2*i+1]
        inFloats = data_sample + data_go
        print(inFloats)

        res,retInts,path,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_childscript,'findPath_goalIsState',inInts,inFloats,[],emptyBuff,vrep.simx_opmode_oneshot_wait)
        print(path)
        n = 1
        f = open('path.txt','w')
        for m in range(0,len(path),1):
            if n >= 7:
                n = 1
                f.write('\n')
                output = listToStringWithoutBrackets(path[m]*180/3.14159)
                f.write(output+',')
            else:
                output = listToStringWithoutBrackets(path[m]*180/3.14159)
                f.write(output+',')
            n = n + 1
        f.close()

        if (res==0) and len(path)>0:
            # Visualize the path:
            res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_childscript,'visualizePath',[robotHandle,255,0,255],path,[],emptyBuff,vrep.simx_opmode_oneshot_wait)
            lineHandle=retInts[0]


            # Make the robot follow the path:
            res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_childscript,'runThroughPath',[robotHandle],path,[],emptyBuff,vrep.simx_opmode_oneshot_wait)

            # Wait until the end of the movement:
            runningPath=True
            while runningPath:
                res,retInts,retFloats,retStrings,retBuffer = vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_childscript,'isRunningThroughPath',[robotHandle],[],[],emptyBuff,vrep.simx_opmode_oneshot_wait)
                runningPath=retInts[0]==1

            # Clear the path visualization:
            res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'remoteApiCommandServer',vrep.sim_scripttype_childscript,'removeLine',[lineHandle],[],[],emptyBuff,vrep.simx_opmode_oneshot_wait)

    # Stop simulation:
    vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot_wait)

    # Now close the connection to V-REP:
    vrep.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')