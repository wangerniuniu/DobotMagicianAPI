'''

@author: 王震 西安工程大学

@license: MIT

@contact: 1341046884@qq.com

@file: robot.py

@time: 2018-05-11 21:52

'''
from . import  DobotDllType as dType
# import DobotDllType as dType
from sympy import *


class Magic(object):
    """
    Dobot魔术师机械臂类封装，目前实现功能如下
    1、标定，空间坐标系和机器人末端执行器坐标系
    2、搬运, 把零件从A搬到B
    """
    def __init__(self):
        self.CON_STR = {
            dType.DobotConnect.DobotConnect_NoError: "success",
            dType.DobotConnect.DobotConnect_NotFound: "unconnect",
            dType.DobotConnect.DobotConnect_Occupied: "ccupied"}
        # 二维坐标变换参数
        self.cosa = 1
        self.sina = 0
        self.tx = 0
        self.ty = 0
        #搬运过程中，末端执行器Z轴的高与低位置
        self.hight = 10
        self.low = -26.0113

    def connect(self):
        #加载dll
        self.api = dType.load()
        # Connect Dobot2
        self.state = dType.ConnectDobot(self.api, "", 115200)[0]
        # self.state=self.CON_STR[self.state]
        return self.state
    def calibration(self, A, B,wA,wB):
        """
        标定坐标值，坐标变化，解四元一次方程
        :param 世界坐标系 （0,0）对应的机器人坐标系（x,y）
        :param 世界坐标系 （5,5）对应的机器人坐标系（x,y）:
        :return: 无返回值
        """
        self.cosa = Symbol('cosa')
        self.sina = Symbol('sina')
        self.tx = Symbol('tx')
        self.ty = Symbol('ty')
        self.ans = solve([
                          self.cosa * wA[0] + self.sina * wA[1] + self.tx - A[0],
                          -self.sina * wA[0] + self.cosa * wA[1] + self.ty - A[1],

                          self.cosa * wB[0] + self.sina * wB[1] + self.tx - B[0],
                          -self.sina * wB[0] + self.cosa * wB[1] + self.ty - B[1]],

                         [self.cosa, self.sina, self.tx, self.ty])
        self.cosa = float(self.ans[self.cosa].evalf())
        self.sina = float(self.ans[self.sina].evalf())
        self.tx = float(self.ans[self.tx].evalf())
        self.ty = float(self.ans[self.ty].evalf())

    def transform(self, Word):
        """
        把实际坐标系转化为机体坐标系，此函数应在标定后使用
        :param Word:世界坐标系坐标
        :return:返回机体CPC坐标XY
        """
        p = Word.copy()
        p[0] = self.cosa * Word[0] + self.sina * Word[1] + self.tx
        p[1] = -self.sina * Word[0] + self.cosa * Word[1] + self.ty
        return p
    def mov(self,A):
        if (self.state == dType.DobotConnect.DobotConnect_NoError):
            p = A.copy()
            p[0] = self.cosa * A[0] + self.sina * A[1] + self.tx
            p[1] = -self.sina * A[0] + self.cosa * A[1] + self.ty
            print(p)
            # print(p)
            index=dType.SetCPCmd(self.api, cpMode=1, x=p[0], y=p[1], z=p[2], velocity=0, isQueued=1)
            dType.SetQueuedCmdStartExec(self.api)
            while index> dType.GetQueuedCmdCurrentIndex(self.api):
                dType.dSleep(100)
                # Stop to Execute Command Queued
            dType.SetQueuedCmdStopExec(self.api)
    def carry(self, A, Target, ):
        """
        搬运程序，从A搬到B，配合抓手，
        :param A: 工件位置
        :param Target: 目标位置
        :return: 无返回值
        """
        # print("插入动作")
        if (self.state == dType.DobotConnect.DobotConnect_NoError):
            # Clean Command Queued
            p = A.copy()
            p[0] = self.cosa * A[0] + self.sina * A[1] + self.tx
            p[1] = -self.sina * A[0] + self.cosa * A[1] + self.ty
            # print(p)
            dType.SetCPCmd(self.api, cpMode=1, x=p[0], y=p[1], z=self.hight, velocity=0, isQueued=1)
            dType.SetEndEffectorGripper(self.api, enableCtrl=True, on=False, isQueued=1)
            dType.SetCPCmd(self.api, cpMode=1, x=p[0], y=p[1], z=self.low, velocity=0, isQueued=1)
            dType.SetEndEffectorGripper(self.api, enableCtrl=True, on=True, isQueued=1)
            dType.SetWAITCmd(self.api, 2, isQueued=1)
            dType.SetCPCmd(self.api, cpMode=1, x=p[0], y=p[1], z=self.hight, velocity=0, isQueued=1)

            p = Target.copy()

            p[0] = self.cosa * Target[0] + self.sina * Target[1] + self.tx
            p[1] = -self.sina * Target[0] + self.cosa * Target[1] + self.ty
            dType.SetCPCmd(self.api, cpMode=1, x=p[0], y=p[1], z=self.hight, velocity=0, isQueued=1)
            # index2 = dType.SetEndEffectorGripper(api, enableCtrl=True, on=False, isQueued=1)[0]
            dType.SetCPCmd(self.api, cpMode=1, x=p[0], y=p[1], z=self.low, velocity=0,
                           isQueued=1)
            dType.SetEndEffectorGripper(self.api, enableCtrl=True, on=False, isQueued=1)
            dType.SetCPCmd(self.api, cpMode=1, x=p[0], y=p[1], z=self.hight, velocity=0, isQueued=1)
            dType.SetWAITCmd(self.api, 2, isQueued=1)
            index2 = dType.SetEndEffectorGripper(self.api, enableCtrl=True, on=False, isQueued=1)[0]
            dType.SetQueuedCmdStartExec(self.api)
            #
            while index2 > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
                dType.dSleep(100)
                # Stop to Execute Command Queued
            dType.SetQueuedCmdStopExec(self.api)

    def disconnect(self):
        """
        断开机器人连接
        :return:
        """
        # Disconnect Dobot2
        dType.DisconnectDobot(self.api)

if __name__ == "__main__":
    arm = Magic()
    arm.hight = 30
    arm.low = -33
    arm.connect()
    arm.calibration([133, 59.5], [178.8, 4.84])
    print(arm.transform([10, 10]))
    # arm.carry([0, 0], [10, 10])
