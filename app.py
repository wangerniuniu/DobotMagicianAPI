'''

@author: 王震 西安工程大学

@license: MIT

@contact: 1341046884@qq.com

@file: app.py

@time: 2018-05-16 18:11

'''

from Dobot.Robot import Magic

arm = Magic()#实例化机械臂
arm.connect()  # 连接机器人
arm.calibration([139.6, 119.2], [214.1, 35.8],  # 标定，实现机器人末端执行器坐标与实际物理坐标的转化
                [1, 1], [9, 8])
arm.mov([1, 1, 0])  # 移动到（x，y，z）
arm.carry([10, 9], [0, 0])  # 把实际坐标系（10,9）搬运到（0,0）
