# ros_cellphonerobot

## Step 1: Install ROS
* Follow the [link](http://wiki.ros.org/ROS/Tutorials/InstallingandConfiguringROSEnvironment) and configure the ROS environment. For instance you can build the catkin works space in `~/catkin_ws`.
* Type the following line in your terminal. Make sure 
```
$ cd ~/catkin_ws/src
$ git clone https://github.com/wang3303/ros_cellphonerobot.git
$ cd ~/catkin_ws
$ catkin_make
```
* Note: ROS_PACKAGE_PATH environment variable includes the directory you're in. You should see something similar as below in your terminal.
```
$ echo $ROS_PACKAGE_PATH
/home/youruser/catkin_ws/src:/opt/ros/kinetic/share
```
## Step 2:Run the robot system using the following line:

```
$ roslaunch ros_cellphonerobot robot.launch
```

This will bring all the nodes online.

## Change profiles in rosparam for your robot

You can modify the profile for your robot in `/ros_cellphonerobot/rosparam/profile.yaml`. The explanation for this file could be found [here]()

## Action publishing

You can run the following line to publish keys to `/action` topic for debugging. For instance, `w` could stand for moving forward. `a` could stand for moving backward.
```
$ rosrun ros_cellphonerobot key_publisher.py
```

## Image classification
* Install [Tensorflow](https://github.com/samjabrahams/tensorflow-on-raspberry-pi)
* Uncomment the node `` in `ros_cellphonerobot/`.
You can publish images to topic `` 
