#!/usr/bin/env python
import rospy
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
import math
import time

def main():
    # 初始化 ROS 节点
    rospy.init_node("moving_landing_sign_node")
    
    # 等待 Gazebo 的 set_model_state 服务启动
    rospy.wait_for_service('/gazebo/set_model_state')
    set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)

    # 模型参数
    model_name = "landing-sign-moving"   # SDF 中 model name
    start_x = 3.0    #起始位置
    amplitude = 1.0               # 左右移动幅度
    speed = 0.5                   # 最大速度 m/s
    z_height = 0.5                # 平台高度（根据 SDF 设置）

    rate = rospy.Rate(100)        # 100Hz
    t0 = time.time()

    while not rospy.is_shutdown():
        t = time.time() - t0
        # 正弦函数生成周期性位置
        x = start_x + amplitude * math.sin(speed * t * math.pi / amplitude)

        # 构建 ModelState 消息
        state = ModelState()
        state.model_name = model_name
        state.pose.position.x = x
        state.pose.position.y = -3.5
        state.pose.position.z = z_height
        state.pose.orientation.x = 0
        state.pose.orientation.y = 0
        state.pose.orientation.z = 1
        state.pose.orientation.w = 1

        try:
            set_state(state)   # 调用服务更新模型位置
        except rospy.ServiceException as e:
            rospy.logerr("Service call failed: %s" % e)

        rate.sleep()

if __name__ == "__main__":
    main()
