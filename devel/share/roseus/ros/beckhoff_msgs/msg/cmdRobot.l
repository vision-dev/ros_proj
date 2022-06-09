;; Auto-generated. Do not edit!


(when (boundp 'beckhoff_msgs::cmdRobot)
  (if (not (find-package "BECKHOFF_MSGS"))
    (make-package "BECKHOFF_MSGS"))
  (shadow 'cmdRobot (find-package "BECKHOFF_MSGS")))
(unless (find-package "BECKHOFF_MSGS::CMDROBOT")
  (make-package "BECKHOFF_MSGS::CMDROBOT"))

(in-package "ROS")
;;//! \htmlinclude cmdRobot.msg.html


(defclass beckhoff_msgs::cmdRobot
  :super ros::object
  :slots (_Timestamp _Vector_q5 ))

(defmethod beckhoff_msgs::cmdRobot
  (:init
   (&key
    ((:Timestamp __Timestamp) 0.0)
    ((:Vector_q5 __Vector_q5) (make-array 5 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _Timestamp (float __Timestamp))
   (setq _Vector_q5 __Vector_q5)
   self)
  (:Timestamp
   (&optional __Timestamp)
   (if __Timestamp (setq _Timestamp __Timestamp)) _Timestamp)
  (:Vector_q5
   (&optional __Vector_q5)
   (if __Vector_q5 (setq _Vector_q5 __Vector_q5)) _Vector_q5)
  (:serialization-length
   ()
   (+
    ;; float32 _Timestamp
    4
    ;; float32[5] _Vector_q5
    (* 4    5)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _Timestamp
       (sys::poke _Timestamp (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32[5] _Vector_q5
     (dotimes (i 5)
       (sys::poke (elt _Vector_q5 i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _Timestamp
     (setq _Timestamp (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32[5] _Vector_q5
   (dotimes (i (length _Vector_q5))
     (setf (elt _Vector_q5 i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     )
   ;;
   self)
  )

(setf (get beckhoff_msgs::cmdRobot :md5sum-) "4c364234fdb48115e683b6d91edb1a06")
(setf (get beckhoff_msgs::cmdRobot :datatype-) "beckhoff_msgs/cmdRobot")
(setf (get beckhoff_msgs::cmdRobot :definition-)
      "float32 Timestamp
float32[5] Vector_q5
")



(provide :beckhoff_msgs/cmdRobot "4c364234fdb48115e683b6d91edb1a06")


