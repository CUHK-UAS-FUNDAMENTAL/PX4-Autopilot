import rospy
from gazebo_msgs.srv import SetLinkState
from gazebo_msgs.msg import LinkState
import time
from gazebo_msgs.msg import ModelStates


def model_state_callback(msg):
    model_name = "landing-sign-moving"
    if model_name in msg.name:
        idx = msg.name.index(model_name)
        position = msg.pose[idx].position
        velocity = msg.twist[idx].linear
        rospy.loginfo("Position: x=%.2f, y=%.2f, z=%.2f | Velocity: x=%.2f, y=%.2f, z=%.2f",
                      position.x, position.y, position.z,
                      velocity.x, velocity.y, velocity.z)

def main():
    rospy.init_node("moving_landing_sign_velocity_node")
    rospy.wait_for_service('/gazebo/set_link_state')
    set_link_state = rospy.ServiceProxy('/gazebo/set_link_state', SetLinkState)


    rospy.Subscriber("/gazebo/model_states", ModelStates, model_state_callback)

    link_name = "landing-sign-moving::link"  # 根据实际模型修改
    x = 3.0
    x_0 = x
    length = 1.0 # 单边移动行程
    vx = 0.5
    y = -3.5
    z = 0.0

    rate = rospy.Rate(100)
    dt = 0.01  # 与rate一致

    while not rospy.is_shutdown():
        # 更新位置
        x += vx * dt
        # 边界判断
        if x >= x_0 + length:
            x = x_0 + length
            vx = -abs(vx)
        elif x <= x_0 - length:
            x = x_0 - length
            vx = abs(vx)

        link_state = LinkState()
        link_state.link_name = link_name
        link_state.pose.position.x = x
        link_state.pose.position.y = y
        link_state.pose.position.z = z
        link_state.twist.linear.x = vx
        link_state.twist.linear.y = 0
        link_state.twist.linear.z = 0

        try:
            set_link_state(link_state)
        except rospy.ServiceException as e:
            rospy.logerr("Service call failed: %s" % e)

        rate.sleep()

if __name__ == "__main__":
    main()
