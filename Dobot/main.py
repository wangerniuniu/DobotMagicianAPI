'''

@author: 王震 西安工程大学

@license: MIT

@contact: 1341046884@qq.com

@file: robot.py

@time: 2018-05-11 21:52

'''
import threading
import DobotDllType as dType
def RobotInit():
    """
    机器人初始化，测试是否有机器人
    :return:
    """
    CON_STR = {
        dType.DobotConnect.DobotConnect_NoError:  "success",
        dType.DobotConnect.DobotConnect_NotFound: "unconnect",
        dType.DobotConnect.DobotConnect_Occupied: "ccupied"}

    #Load Dll
    api = dType.load()

    #Connect Dobot2
    state = dType.ConnectDobot(api, "", 115200)[0]
    print("Connect status:",CON_STR[state])
    return CON_STR[state]
CON_STR = {
        dType.DobotConnect.DobotConnect_NoError: "success",
        dType.DobotConnect.DobotConnect_NotFound: "unconnect",
        dType.DobotConnect.DobotConnect_Occupied: "ccupied"}

    # Load Dll
api = dType.load()

    # Connect Dobot2
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:", CON_STR[state])


p=[15,15]

def Mov(PosB,PosA):
    if (state == dType.DobotConnect.DobotConnect_NoError):

        # Clean Command Queued
        dType.SetQueuedCmdClear(api)
        print("Now_index", dType.GetQueuedCmdCurrentIndex(api))
        # #Async Motion Params Setting
        # dType.SetHOMEParams(api, 250, 0, 50, 0, isQueued = 1)
        # # dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
        # # dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
        #
        # #Async Home
        # dType.SetHOMECmd(api, temp = 0, isQueued = 1)

        # print (dType.GetPose(api))
        # dType.SetEndEffectorGripper(api,enableCtrl=True,on=True)
        print("start")
        p = PosB
        index = dType.SetCPCmd(api, cpMode=1, x=133.7 + 10 * p[0], y=59.5 - 10 * p[1], z=30, velocity=0, isQueued=1)
        dType.SetEndEffectorGripper(api, enableCtrl=True, on=False, isQueued=1)
        index = dType.SetCPCmd(api, cpMode=1, x=133.7 + 10 * p[0], y=59.5 - 10 * p[1], z=-31, velocity=0, isQueued=1)

        # dType.SetWAITCmd(api, 2, isQueued=1)
        dType.SetEndEffectorGripper(api, enableCtrl=True, on=True, isQueued=1)
        dType.SetWAITCmd(api, 2, isQueued=1)
        index = dType.SetCPCmd(api, cpMode=1, x=133.7 + 10 * p[0], y=59.5 - 10 * p[1], z=23, velocity=0, isQueued=1)
        p = PosA
        index = dType.SetCPCmd(api, cpMode=1, x=133.7 + 10 * p[0], y=59.5 - 10 * p[1], z=30, velocity=0, isQueued=1)
        # index2 = dType.SetEndEffectorGripper(api, enableCtrl=True, on=False, isQueued=1)[0]
        index = dType.SetCPCmd(api, cpMode=1, x=133.7 + 10 * p[0], y=59.5 - 10 * p[1], z=-31, velocity=0, isQueued=1)
        index2 = dType.SetEndEffectorGripper(api, enableCtrl=True, on=False, isQueued=1)[0]
        index = dType.SetCPCmd(api, cpMode=1, x=133.7 + 10 * p[0], y=59.5 - 10 * p[1], z=30, velocity=0, isQueued=1)
        print(index2)
        dType.SetWAITCmd(api, 2, isQueued=1)
        index2 = dType.SetEndEffectorGripper(api, enableCtrl=False, on=False, isQueued=1)[0]
        # dType.SetEndEffectorGripper(api, enableCtrl=True, on=True)
        # Async PTP Motion
        # for i in range(0, 5):
        #     if i % 2 == 0:
        #         offset = 50
        #     else:
        #         offset = -50
        #     lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 200 + offset, offset, offset, offset, isQueued = 1)[0]
        #
        #
        #
        # #Start to Execute Command Queued
        dType.SetQueuedCmdStartExec(api)
        #
        while index2 > dType.GetQueuedCmdCurrentIndex(api)[0]:
            dType.dSleep(100)
            # Stop to Execute Command Queued
        dType.SetQueuedCmdStopExec(api)

        # Stop to Execute Command Queued
while True:
    Mov([10,10],[0,0])
    Mov([0,0],[10,10])
# if (state == dType.DobotConnect.DobotConnect_NoError):
#
#     #Clean Command Queued
#     dType.SetQueuedCmdClear(api)
#     print("Now_index", dType.GetQueuedCmdCurrentIndex(api))
#     # #Async Motion Params Setting
#     # dType.SetHOMEParams(api, 250, 0, 50, 0, isQueued = 1)
#     # # dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
#     # # dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
#     #
#     # #Async Home
#     # dType.SetHOMECmd(api, temp = 0, isQueued = 1)
#
#     # print (dType.GetPose(api))
#     # dType.SetEndEffectorGripper(api,enableCtrl=True,on=True)
#     print("start")
#     p = [10, 10]
#     index = dType.SetCPCmd(api, cpMode=1, x=132 + 10 * p[0], y=57.5 - 10 * p[1], z=30, velocity=0, isQueued=1)
#     dType.SetEndEffectorGripper(api, enableCtrl=True, on=False, isQueued=1)
#     index=dType.SetCPCmd(api,cpMode=1,x=132+10*p[0],y=57.5-10*p[1],z=-31,velocity=0,isQueued=1)
#
#     dType.SetWAITCmd(api,2,isQueued=1)
#     dType.SetEndEffectorGripper(api, enableCtrl=True, on=True,isQueued=1)
#     dType.SetWAITCmd(api, 2, isQueued=1)
#     index = dType.SetCPCmd(api, cpMode=1, x=133.7 + 10 * p[0], y=59.5 - 10 * p[1], z=23, velocity=0, isQueued=1)
#     p = [1, 1]
#     index = dType.SetCPCmd(api, cpMode=1, x=133.7 + 10 * p[0], y=59.5 - 10 * p[1], z=30, velocity=0, isQueued=1)
#     # index2 = dType.SetEndEffectorGripper(api, enableCtrl=True, on=False, isQueued=1)[0]
#     index=dType.SetCPCmd(api,cpMode=1,x=133.7+10*p[0],y=59.5-10*p[1],z=-31,velocity=0,isQueued=1)
#     index2=dType.SetEndEffectorGripper(api, enableCtrl=True, on=False,isQueued=1)[0]
#     index = dType.SetCPCmd(api, cpMode=1, x=133.7 + 10 * p[0], y=59.5 - 10 * p[1], z=30, velocity=0, isQueued=1)
#     print(index2)
#     # dType.SetWAITCmd(api, 2, isQueued=1)
#     index2 = dType.SetEndEffectorGripper(api, enableCtrl=False, on=False, isQueued=1)[0]
#     # dType.SetEndEffectorGripper(api, enableCtrl=True, on=True)
#     #Async PTP Motion
#     # for i in range(0, 5):
#     #     if i % 2 == 0:
#     #         offset = 50
#     #     else:
#     #         offset = -50
#     #     lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 200 + offset, offset, offset, offset, isQueued = 1)[0]
#     #
#     #
#     #
#     # #Start to Execute Command Queued
#     dType.SetQueuedCmdStartExec(api)
#     #
#     while index2 > dType.GetQueuedCmdCurrentIndex(api)[0]:
#         dType.dSleep(100)
#         # Stop to Execute Command Queued
#     dType.SetQueuedCmdStopExec(api)
#
#     #Stop to Execute Command Queued
# # dType.SetQueuedCmdStopExec(api)
print(dType.GetPose(api))
#Disconnect Dobot2
dType.DisconnectDobot(api)
