#!/usr/bin/env python
import rospy
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
import math
import time

def triangle_wave(t, start_x, amplitude, v_max):
    # 周期
    T = 4.0 * amplitude / v_max
    # 归一化时间
    phase = (t % T) / T
    # 三角波 [-1, 1]
    tri = 4 * abs(phase - 0.5) - 1
    return start_x + amplitude * tri

def main():
    rospy.init_node("moving_landing_sign_node")
    rospy.wait_for_service('/gazebo/set_model_state')
    set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)

    model_name = "landing-sign-moving"
    start_x = 3.0        # 中心位置
    amplitude = 1.0      # 往返振幅 (m)
    v_max = 0.5          # 匀速速度 (m/s)
    z_height = 0.0       # 平台高度

    rate = rospy.Rate(50)  # 50Hz
    t0 = time.time()

    while not rospy.is_shutdown():
        t = time.time() - t0
        x = triangle_wave(t, start_x, amplitude, v_max)

        state = ModelState()
        state.model_name = model_name
        state.pose.position.x = x
        state.pose.position.y = -3.5
        state.pose.position.z = z_height
        state.pose.orientation.x = 0
        state.pose.orientation.y = 0
        state.pose.orientation.z = 0
        state.pose.orientation.w = 1

        try:
            set_state(state)
        except rospy.ServiceException as e:
            rospy.logerr("Service call failed: %s" % e)

        rate.sleep()

if __name__ == "__main__":
    main()
