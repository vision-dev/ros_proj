# Install script for directory: /home/student/Asparagus_project/ros_proj/src/geometry2/tf2_msgs

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/student/Asparagus_project/ros_proj/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tf2_msgs/msg" TYPE FILE FILES
    "/home/student/Asparagus_project/ros_proj/src/geometry2/tf2_msgs/msg/TF2Error.msg"
    "/home/student/Asparagus_project/ros_proj/src/geometry2/tf2_msgs/msg/TFMessage.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tf2_msgs/srv" TYPE FILE FILES "/home/student/Asparagus_project/ros_proj/src/geometry2/tf2_msgs/srv/FrameGraph.srv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tf2_msgs/action" TYPE FILE FILES "/home/student/Asparagus_project/ros_proj/src/geometry2/tf2_msgs/action/LookupTransform.action")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tf2_msgs/msg" TYPE FILE FILES
    "/home/student/Asparagus_project/ros_proj/devel/share/tf2_msgs/msg/LookupTransformAction.msg"
    "/home/student/Asparagus_project/ros_proj/devel/share/tf2_msgs/msg/LookupTransformActionGoal.msg"
    "/home/student/Asparagus_project/ros_proj/devel/share/tf2_msgs/msg/LookupTransformActionResult.msg"
    "/home/student/Asparagus_project/ros_proj/devel/share/tf2_msgs/msg/LookupTransformActionFeedback.msg"
    "/home/student/Asparagus_project/ros_proj/devel/share/tf2_msgs/msg/LookupTransformGoal.msg"
    "/home/student/Asparagus_project/ros_proj/devel/share/tf2_msgs/msg/LookupTransformResult.msg"
    "/home/student/Asparagus_project/ros_proj/devel/share/tf2_msgs/msg/LookupTransformFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tf2_msgs/cmake" TYPE FILE FILES "/home/student/Asparagus_project/ros_proj/build/geometry2/tf2_msgs/catkin_generated/installspace/tf2_msgs-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/student/Asparagus_project/ros_proj/devel/include/tf2_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/student/Asparagus_project/ros_proj/devel/share/roseus/ros/tf2_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/student/Asparagus_project/ros_proj/devel/share/common-lisp/ros/tf2_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/student/Asparagus_project/ros_proj/devel/share/gennodejs/ros/tf2_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/home/student/anaconda3/bin/python3" -m compileall "/home/student/Asparagus_project/ros_proj/devel/lib/python3/dist-packages/tf2_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/student/Asparagus_project/ros_proj/devel/lib/python3/dist-packages/tf2_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/student/Asparagus_project/ros_proj/build/geometry2/tf2_msgs/catkin_generated/installspace/tf2_msgs.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tf2_msgs/cmake" TYPE FILE FILES "/home/student/Asparagus_project/ros_proj/build/geometry2/tf2_msgs/catkin_generated/installspace/tf2_msgs-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tf2_msgs/cmake" TYPE FILE FILES
    "/home/student/Asparagus_project/ros_proj/build/geometry2/tf2_msgs/catkin_generated/installspace/tf2_msgsConfig.cmake"
    "/home/student/Asparagus_project/ros_proj/build/geometry2/tf2_msgs/catkin_generated/installspace/tf2_msgsConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tf2_msgs" TYPE FILE FILES "/home/student/Asparagus_project/ros_proj/src/geometry2/tf2_msgs/package.xml")
endif()

