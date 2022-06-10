**** 08.06.22 *****

Zagon programa za premikanje robota po točkah.

1) Zaženemo "roscore"
2) Zaženemo "rosrun beckhoff_comm plc_pc_comm" s tem se vzpostavi komunikacija med beckhoff krmilnikom in ros pc-jem
3) Zaženemo "rosrun delta_robot c_moveL_control.py". Odpre se nam okno, ki kaže nastavljeno pozicijo robota. Pozicijo spreminjamo s številkami 1,2,3... Robot se premakne na shranjeno pozicijo.
4) Zaženemo "rosrun delta_robot control_r2omegas.py". V tej kodi teče PD regulator za robota.
