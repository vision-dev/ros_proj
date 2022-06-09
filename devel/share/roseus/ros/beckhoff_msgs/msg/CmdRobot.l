;; Auto-generated. Do not edit!


(when (boundp 'beckhoff_msgs::CmdRobot)
  (if (not (find-package "BECKHOFF_MSGS"))
    (make-package "BECKHOFF_MSGS"))
  (shadow 'CmdRobot (find-package "BECKHOFF_MSGS")))
(unless (find-package "BECKHOFF_MSGS::CMDROBOT")
  (make-package "BECKHOFF_MSGS::CMDROBOT"))

(in-package "ROS")
;;//! \htmlinclude CmdRobot.msg.html


(defclass beckhoff_msgs::CmdRobot
  :super ros::object
  :slots (_Timestamp _dq ))

(defmethod beckhoff_msgs::CmdRobot
  (:init
   (&key
    ((:Timestamp __Timestamp) (instance ros::time :init))
    ((:dq __dq) (instance beckhoff_msgs::Vector_q5 :init))
    )
   (send-super :init)
   (setq _Timestamp __Timestamp)
   (setq _dq __dq)
   self)
  (:Timestamp
   (&optional __Timestamp)
   (if __Timestamp (setq _Timestamp __Timestamp)) _Timestamp)
  (:dq
   (&rest __dq)
   (if (keywordp (car __dq))
       (send* _dq __dq)
     (progn
       (if __dq (setq _dq (car __dq)))
       _dq)))
  (:serialization-length
   ()
   (+
    ;; time _Timestamp
    8
    ;; beckhoff_msgs/Vector_q5 _dq
    (send _dq :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; time _Timestamp
       (write-long (send _Timestamp :sec) s) (write-long (send _Timestamp :nsec) s)
     ;; beckhoff_msgs/Vector_q5 _dq
       (send _dq :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; time _Timestamp
     (send _Timestamp :sec (sys::peek buf ptr- :integer)) (incf ptr- 4)  (send _Timestamp :nsec (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; beckhoff_msgs/Vector_q5 _dq
     (send _dq :deserialize buf ptr-) (incf ptr- (send _dq :serialization-length))
   ;;
   self)
  )

(setf (get beckhoff_msgs::CmdRobot :md5sum-) "272eeeecd8726ab3f273e3bf2ed33455")
(setf (get beckhoff_msgs::CmdRobot :datatype-) "beckhoff_msgs/CmdRobot")
(setf (get beckhoff_msgs::CmdRobot :definition-)
      "time Timestamp
Vector_q5 dq
================================================================================
MSG: beckhoff_msgs/Vector_q5
float32 j0
float32 j1
float32 j2
float32 j3
float32 j4
")



(provide :beckhoff_msgs/CmdRobot "272eeeecd8726ab3f273e3bf2ed33455")


