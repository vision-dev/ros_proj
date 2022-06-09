; Auto-generated. Do not edit!


(cl:in-package beckhoff_msgs-msg)


;//! \htmlinclude CmdRobot.msg.html

(cl:defclass <CmdRobot> (roslisp-msg-protocol:ros-message)
  ((Timestamp
    :reader Timestamp
    :initarg :Timestamp
    :type cl:real
    :initform 0)
   (dq
    :reader dq
    :initarg :dq
    :type beckhoff_msgs-msg:Vector_q5
    :initform (cl:make-instance 'beckhoff_msgs-msg:Vector_q5)))
)

(cl:defclass CmdRobot (<CmdRobot>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <CmdRobot>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'CmdRobot)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name beckhoff_msgs-msg:<CmdRobot> is deprecated: use beckhoff_msgs-msg:CmdRobot instead.")))

(cl:ensure-generic-function 'Timestamp-val :lambda-list '(m))
(cl:defmethod Timestamp-val ((m <CmdRobot>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader beckhoff_msgs-msg:Timestamp-val is deprecated.  Use beckhoff_msgs-msg:Timestamp instead.")
  (Timestamp m))

(cl:ensure-generic-function 'dq-val :lambda-list '(m))
(cl:defmethod dq-val ((m <CmdRobot>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader beckhoff_msgs-msg:dq-val is deprecated.  Use beckhoff_msgs-msg:dq instead.")
  (dq m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <CmdRobot>) ostream)
  "Serializes a message object of type '<CmdRobot>"
  (cl:let ((__sec (cl:floor (cl:slot-value msg 'Timestamp)))
        (__nsec (cl:round (cl:* 1e9 (cl:- (cl:slot-value msg 'Timestamp) (cl:floor (cl:slot-value msg 'Timestamp)))))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __sec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 0) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __nsec) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __nsec) ostream))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'dq) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <CmdRobot>) istream)
  "Deserializes a message object of type '<CmdRobot>"
    (cl:let ((__sec 0) (__nsec 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __sec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 0) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __nsec) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __nsec) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'Timestamp) (cl:+ (cl:coerce __sec 'cl:double-float) (cl:/ __nsec 1e9))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'dq) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<CmdRobot>)))
  "Returns string type for a message object of type '<CmdRobot>"
  "beckhoff_msgs/CmdRobot")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'CmdRobot)))
  "Returns string type for a message object of type 'CmdRobot"
  "beckhoff_msgs/CmdRobot")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<CmdRobot>)))
  "Returns md5sum for a message object of type '<CmdRobot>"
  "272eeeecd8726ab3f273e3bf2ed33455")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'CmdRobot)))
  "Returns md5sum for a message object of type 'CmdRobot"
  "272eeeecd8726ab3f273e3bf2ed33455")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<CmdRobot>)))
  "Returns full string definition for message of type '<CmdRobot>"
  (cl:format cl:nil "time Timestamp~%Vector_q5 dq~%================================================================================~%MSG: beckhoff_msgs/Vector_q5~%float32 j0~%float32 j1~%float32 j2~%float32 j3~%float32 j4~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'CmdRobot)))
  "Returns full string definition for message of type 'CmdRobot"
  (cl:format cl:nil "time Timestamp~%Vector_q5 dq~%================================================================================~%MSG: beckhoff_msgs/Vector_q5~%float32 j0~%float32 j1~%float32 j2~%float32 j3~%float32 j4~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <CmdRobot>))
  (cl:+ 0
     8
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'dq))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <CmdRobot>))
  "Converts a ROS message object to a list"
  (cl:list 'CmdRobot
    (cl:cons ':Timestamp (Timestamp msg))
    (cl:cons ':dq (dq msg))
))
