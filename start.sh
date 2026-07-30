killall -9 px4 gzserver gzclient

source devel/setup.bash

cd src/PX4-Autopilot
source Tools/simulation/gazebo-classic/setup_gazebo.bash $(pwd) $(pwd)/build/px4_sitl_default
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)/Tools/simulation/gazebo-classic/sitl_gazebo-classic
export GAZEBO_PLUGIN_PATH=$GAZEBO_PLUGIN_PATH:$(pwd)/build/px4_sitl_default/build_gazebo-classic

cd ../..

roslaunch px4 mavros_posix_sitl_imav_indoor.launch
