**** 08.06.22 *****

Zagon programa za premikanje robota po točkah.

1) Zaženemo "roscore"
2) Zaženemo "rosrun beckhoff_comm plc_pc_comm" s tem se vzpostavi komunikacija med beckhoff krmilnikom in ros pc-jem
3) Zaženemo "rosrun delta_robot c_moveL_control.py". Odpre se nam okno, ki kaže nastavljeno pozicijo robota. Pozicijo spreminjamo s številkami 1,2,3... Robot se premakne na shranjeno pozicijo.
4) Zaženemo "rosrun delta_robot control_r2omegas.py". V tej kodi teče PD regulator za robota.




**** 30.06.22 *****

Zagon programa za pemikanje robota z joystickom

1) Zaženemo "roscore"
2) Zaženemo "rosrun beckhoff_comm plc_pc_comm" s tem se vzpostavi komunikacija med beckhoff krmilnikom in ros pc-jem
3) Zaženemo "rosrun joy joy_node" s tem se vzpostavi povezava z joystickom
4) Zaženemo "rosrun delta_robot joy_control.py" s tem beremo ukaz iz joysticka
5) Zaženemo "rosrun delta_robot control_r2omegas.py". V tej kodi teče PD regulator za robota.
6) Zaženemo "rosrun delta_robot control_r2omegas.py". V tej kodi teče PD regulator za robota.


**** 1.07.22 *****

Povezava na računalnik brez monitorja.
https://kb.nomachine.com/AR03P00973

**** 13.07.22 *****

Zagon laserskega skenerja Sick LMS111 in programov za generiranje 3D slike in pretvorbo v world koordinatni sistem

1) Zaženemo "roslaunch sick_scan sick_lms_1xx.launch hostname:=192.168.1.100" s tem se vzpostavi komunikacija za laserskim skenerjem
2) Zaženemo "rosrun transformations sensor_to_robot.py laser 0.7 0.05 0.5 0 2.36 0" da dobimo statično transformacijo med koordinatnim sistemom laserja in robota
3) Zaženemo "rosrun beckhoff_comm plc_pc_comm" s tem se vzpostavi komunikacija med beckhoff krmilnikom in ros pc-jem
4) Zaženemo "rosrun joy joy_node" s tem se vzpostavi povezava z joystickom
5) Zaženemo "rosrun tracks joy_control.py" s tem se vzpostavi povezava z joystickom za premikanje gosenic
6) Zaženemo "rosrun transformations robot_to_global.py" da dobimo dinamično transformacijo med koordinatnim sistemom robota in globalnim sistemom
7) Zaženemo "rosrun delta_robot sick_scanner.py" program pretvarja koordinate v robot cs
8) Zaženemo "rosrun delta_robot get_img_from_scanner2.py" program sestavlja sliko skenerja v globalnem koordinatnem sistemu


**** 21.07.22 *****

Lokacija ros knjižnjic: /opt/ros/noetic/lib/python3/dist-packages
Zagon vizualizacije za intel realsense kamere: "realsense-viewer"
Lokacijo launch datoteke poiščemo z ukazom "roscd ime_datoteke.launch"
Zagon intel realsense v ros: "roslaunch realsense2_camera rs_camera.launch"
Pretvorba iz koordinatnega sistema realsense kamere v ks robota: "rosrun transformations sensor_to_robot.py camera_depth_optical_frame 0.75 0.1 0.4 2.37 0 -1.57"
Shranjevanje podatkov z rosbag: "rosbag record -O L515_global_points.bag --duration=10 /intel_l515_global_cloud"



