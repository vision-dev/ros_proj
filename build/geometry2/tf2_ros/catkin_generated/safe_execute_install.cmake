execute_process(COMMAND "/home/student/Asparagus_project/ros_proj/build/geometry2/tf2_ros/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/student/Asparagus_project/ros_proj/build/geometry2/tf2_ros/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
