[Wiki gazebo tutorial](http://wiki.ros.org/simulator_gazebo/Tutorials/StartingGazebo)

[gazebo page](http://gazebosim.org/tutorials?tut=ros_roslaunch)
#### 위에 내용을 확인 해보면 알겠지만 indigo 이상 부터는 gazebo empty_world를 실행할 때 다음과 같이 해야한다.


### [Catkin system](http://wiki.ros.org/catkin)
- catkin_make와 catkin build, catkin_make_isolated의 차이는 무엇인가
```
If you have a previously compiled workspace and you add a new package inside it, you can tell catkin to add this new package to the already-compiled binaries by adding this parameter:

$ catkin_make --force-cmake

Feel free to read more details about the inner workings of catkin_make or continue on to the next tutorial: Overlaying catkin
http://wiki.ros.org/ko/catkin/Tutorials/using_a_workspace
```



1. [catkin/CMakeLists.txt](http://wiki.ros.org/catkin/CMakeLists.txt)
- 어떻게 build되는지 CMake build system 에 넣어주는 것
##### 구조
    1) Required CMake Version 
        - cmake_minimum_required(VERSION 2.8.3)
    2) Package Name 
        - project(robot_description)
    3) Find other CMake/Catkin packages needed for build 
        - find_package(catkin REQUIRED)
        - ex) find_package(catkin REQUIRED COMPONENTS nodelet) 
              ----------------------------------------- 아래 같은 의미 ----------
              find_package(catkin REQUIRED)
              find_package(nodelet REQUIRED)
    4) Enable Python module support 
        - catkin_python_setup()
    5) Message/Service/Action Generators (add_message_files(), add_service_files(), add_action_files())
    6) Invoke message/service/action generation (generate_messages())
    7) Specify package build info export (catkin_package())
    8) Libraries/Executables to build (add_library()/add_executable()/target_link_libraries())
    9) Tests to build (catkin_add_gtest())
    10) Install rules (install())


2. [package.xml](http://wiki.ros.org/catkin/package.xml#Metapackages)
        
        - <depend>
        - <build_depend>
        - <build_export_depend>
        - <exec_depend> : 실행하는 데 필요한 패키지 종속성  (especially when these packages are declared as (CATKIN_)DEPENDS in catkin_package() in CMake).
        - <test_depend>
        - <buildtool_depend>
        - <doc_depend>


-------------------------------------------------------------

##### [rosdep](http://wiki.ros.org/rosdep)
- rosdep update :  sudo 와 함께 쓰면 안됨 permission errors 발생! 나중에
- rosdep install --from-paths src --ignore-src -r -y : 필요한데 없는 패키지 모두 설치 하는 거 


-------------------------------------------------------------

##### URDF 파일 만들기

- catkin 의존성에 gazebo 만 있으면 되는 건가



##### Gazebo plugin 

1. 처음 실행할 경우

```shell
$ sudo apt-get install ros-indigo-simulators
$ source /opt/ros/%YOUR_ROS_DISTRO%/setup.bash
$ roslaunch gazebo_ros empty_world.launch


------------ 나중에 실행하고 싶다면 ----------------
$ roslaunch gazebo_ros empty_world.launch
```

2. launch 파일에 gazebo_worlds를 연결하고 싶다면

```xml
<launch>
  <!-- start gazebo with an empty plane -->
  <param name="/use_sim_time" value="true" />
  <node name="gazebo" pkg="gazebo" type="gazebo" args="$(find gazebo_worlds)/worlds/empty.world" respawn="false" output="screen"/>
</launch>

<!-- respawn 계속 실행할 것인가?-->
```
- Gazebo roslaunch Arguments
```
- paused : start gazebo in a paused state (default false)
- use_sim_time : tells ROS nodes asking for time to get the Gazebo-pulished simulation time, published over the ROS topic/clock(default true)
- gui : Launch the user interface window of Gazebo (default true)
- headless (deprecated) recording (previously called headless) : Enable gazebo state log recording
- debug : Start gzserver (Gazebo Server) in debug mode using gdb (default false)
- verbose : Run gzserver and gzclient with --verbose, printing errors and warnings to the terminal (default false)
- server_required : Terminate launch script when gzserver (Gazebo Server) exits (default false)
- gui_required : Terminate launch script when gzclient (user interface window) exits (default false)
```



##### URDF파일을  > GAZEBO simulation 사용 시 해주어야할 일

1. URDF 파일에 넣어 줄 부분
```
- <link></link> 에 <inertial></inertial> 관련 정보 꼭 추가 : 동역학 정보
- 조인트를 움직이고 싶다면 <transmission></transmission> 관련 정보 꼭 추가 (추후 ros_control과 연동)
        [urdf/transmission](http://wiki.ros.org/urdf/XML/Transmission)
- 용도별 Gazebo 플러그인 추가 <gazebo></gazebo>
        [gazebo plugin](http://gazebosim.org/tutorials?tut=ros_gzplugins)
- (옵션) <joint></joint>에 <dynamics></dynamics> 및 기타 구문 추가
```

2. spawn_model 사용
        1) $ rosrun gazebo_ros spawn_model -file `rospack find MYROBOT_description`/urdf/MYROBOT.urdf -urdf -x 0 -y 0 -z 1 -model MYROBOT

        2) launch 파일

```xml
<lanch>
 <node name="spawn_urdf" pkg="gazebo_ros" type="spawn_model" args="-param robot_description -urdf -model MYROBOT”/>
<launch/>
<!-- -->

```
```
필요한 의존

  <node name="spawn_gazebo_model" pkg="gazebo_ros" type="spawn_model" args="-urdf -param robot_description -model robot -z 0.1" respawn=성"false" output="screen" />

  <buildtool_depend>catkin</buildtool_depend>
  <test_depend>roslaunch</test_depend>
  <exec_depend>controller_manager</exec_depend>
  <exec_depend>effort_controllers</exec_depend>
  <exec_depend>gazebo_ros</exec_depend>
  <exec_depend>gazebo_ros_control</exec_depend>
  <exec_depend>joint_state_controller</exec_depend>
  <exec_depend>joint_trajectory_controller</exec_depend>
  <exec_depend>position_controllers</exec_depend>
  <exec_depend>robot_state_publisher</exec_depend>
  <exec_depend>rostopic</exec_depend>
  <exec_depend>ur_description</exec_depend>

```


#### robot_state_publisher란?[출처](http://wiki.ros.org/robot_state_publisher)

1. param server의 robot_description을 읽어들여, tf로 변환해주는 역할
    - link --> link joint --> fixed joint or revolute, continuous 

1) Subscribed topics
        - joint_states (sensor_msgs/JointState)
          : joint position information
2) Parameters
        - robot_description (urdf map)
          : The urdf xml robot description. This is accessed via `urdf_model::initParam`
        - tf_prefix (string)
          : Set the tf prefix for namespace-aware publishing of transforms. See tf_prefix for more details.
        - publish_frequency (double)
          : Publish frequency of state publisher, default: 50Hz.
        - ignore_timestamp (bool)
          : If true, ignore the publish_frequency and the timestamp of joint_states and publish a tf for each of the received joint_states. Default is "false".
        - use_tf_static (bool)
          : Set whether to use the /tf_static latched static transform broadcaster. Default: true.

> fixed 조인트는 고정된 값이라 연관 관계 파악 가능 / 움직이는 조인트는 현재 값을 알 수 없음 >> joint_state_publisher 혹은 joing_state_publisher_gui 필요



#### ros_control
- 하드웨어를 ROS로 좀 더 쉽게 제어할 수 있도록 하기위한 툴?

- 제공되는 컨트롤러 
```
effort_controllers - Command a desired force/torque to joints.
	joint_effort_controller
	joint_position_controller
	joint_velocity_controller

joint_state_controller - Read all joint positions.
	joint_state_controller

position_controllers - Set one or multiple joint positions at once.
	joint_position_controller
	joint_group_position_controller

velocity_controllers - Set one or multiple joint velocities at once.
	joint_velocity_controller
	joint_group_velocity_controller
 
joint_trajectory_controllers - Extra functionality for splining an entire trajectory.
	position_controller
	velocity_controller
	effort_controller
	position_velocity_controller
	position_velocity_acceleration_controller

```

- 대응되는 하드웨어 인터페이스
```
Joint Command Interfaces
	Effort Joint Interface
	Velocity Joint Interface
	Position Joint Interface

Joint State Interfaces

Actuator State Interfaces
Actuator Command Interfaces
	Effort Actuator Interface
	Velocity Actuator Interface
	Position Actuator Interface

Force-torque sensor Interface
IMU sensor Interface
```







