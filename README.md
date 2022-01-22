# Image Based Visual Servoing

This repo has different folders contaning different ways of doing visual servoing with different robots. The end goal is perform IBVS on aerial manipulator. (The approaches are not restricted to Gazebo sim)

 # 1. ROS - Visual Servoing IBVS with Blobs Detection
 
**For IBVS_PointBased**

**Table-of-contents**

* [Dependencies](#dependencies)
* [Process](#process)
* [Execution](#execution)

More description is given in the subsections.

## Dependencies

The following project is being tested with **Ubuntu 18.04 LTS**

Following libraries are needed:

* ROS Melodic - `sudo apt-get install ros-melodic-desktop-full`
* Gazebo Simulation - `sudo apt-get install ros-melodic-gazebo-ros-pkgs ros-melodic-gazebo-ros-control`
* Turtlebot for Gazebo in Melodic - `sudo apt-get install ros-melodic-turtlebot3` (useful link https://answers.ros.org/question/305162/has-the-turtlebot-simulator-been-released-for-melodic-version/) 

The development part has been performed using CPP and ViSP:

* ROS Melodic ViSP - `sudo apt-get install ros-melodic-visp-*`
* ViSP - `sudo apt-get install libvisp-dev libvisp-doc visp-images-data`

## Getting your marker in the Gazebo world:
Paste the 'marker0' folder in 'gazeboResources' into your gazebo resources directory.

Usually, this is a hidden folder in your 'home' directory, named '.gazebo'. Paste the 'marker0' folder inside '.gazebo/models/'. In your Gazebo, you'll now be able to 'insert' marker0, check the insert pane!

The 'qr.world' file available in 'world' folder contains a Gazebo world with a pattern containing 5 dots. Copy this world file in your turtlebot3 folder.


## Process

The following code performs multiple operations to compute **visual servoing task** using **ROS Melodic** and a **Turlebot**.

* Extraction of image from the Kinect ( and dependant topic) .
* Manual initialization of blobs to be tracked 
* Tracking of blobs in successive image frames
* Compute velocities to minimize error between current positions of blobs and their desired positions
* Stop the velocity publishing and computation when error has dropped below a threshold.


## Execution

### Preliminary commands
You'll first need to do a minimal launch and a 3dsensor launch on your turtlebot (tip: use ssh!)
Running the minimal launch and the 3Dsensor launch from ros.

* minimal - `roslaunch turtlebot-bringup minimal.launch`
* 3dsensor - `roslaunch turtlebot-bringup 3dsensor.launch`

### Running PointsBased IBVS

* Simulation : 
1 : `roslaunch turtlebot_gazebo turtlebot_world.launch world_file:='/world/NameofWorld.world' `
2: `rosrun IBVS_PointsBased IBVS_PointsBased_gazebo` or `rosrun project_vs IBVS_PointsBased_gazebo`

# 2. Simple use of visp with ros-gazebo

* Install ros-melodic-visp package from Synaptic.
* Installation of pioneer model https://github.com/SD-Robot-Vision/PioneerModel or https://github.com/mario-serna/pioneer_p3dx_model 
(Link for p2od files https://github.com/allenh1/p2os) 

