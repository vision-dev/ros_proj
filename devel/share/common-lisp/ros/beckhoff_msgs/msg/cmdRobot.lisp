; Auto-generated. Do not edit!


(cl:in-package beckhoff_msgs-msg)


;//! \htmlinclude cmdRobot.msg.html

(cl:defclass <cmdRobot> (roslisp-msg-protocol:ros-message)
  ((Timestamp
    :reader Timestamp
    :initarg :Timestamp
    :type cl:float
    :initform 0.0)
   (Vector_q5
    :reader Vector_q5
    :initarg :Vector_q5
    :type (cl:vector cl:float)
   :initform (cl:make-array 5 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass cmdRobot (<cmdRobot>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <cmdRobot>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'cmdRobot)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name beckhoff_msgs-msg:<cmdRobot> is deprecated: use beckhoff_msgs-msg:cmdRobot instead.")))

(cl:ensure-generic-function 'Timestamp-val :lambda-list '(m))
(cl:defmethod Timestamp-val ((m <cmdRobot>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader beckhoff_msgs-msg:Timestamp-val is deprecated.  Use beckhoff_msgs-msg:Timestamp instead.")
  (Timestamp m))

(cl:ensure-generic-function 'Vector_q5-val :lambda-list '(m))
(cl:defmethod Vector_q5-val ((m <cmdRobot>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader beckhoff_msgs-msg:Vector_q5-val is deprecated.  Use beckhoff_msgs-msg:Vector_q5 instead.")
  (Vector_q5 m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <cmdRobot>) ostream)
  "Serializes a message object of type '<cmdRobot>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'Timestamp))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'Vector_q5))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <cmdRobot>) istream)
  "Deserializes a message object of type '<cmdRobot>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'Timestamp) (roslisp-utils:decode-single-float-bits bits)))
  (cl:setf (cl:slot-value msg 'Vector_q5) (cl:make-array 5))
  (cl:let ((vals (cl:slot-value msg 'Vector_q5)))
    (cl:dotimes (i 5)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<cmdRobot>)))
  "Returns string type for a message object of type '<cmdRobot>"
  "beckhoff_msgs/cmdRobot")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'cmdRobot)))
  "Returns string type for a message object of type 'cmdRobot"
  "beckhoff_msgs/cmdRobot")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<cmdRobot>)))
  "Returns md5sum for a message object of type '<cmdRobot>"
  "4c364234fdb48115e683b6d91edb1a06")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'cmdRobot)))
  "Returns md5sum for a message object of type 'cmdRobot"
  "4c364234fdb48115e683b6d91edb1a06")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<cmdRobot>)))
  "Returns full string definition for message of type '<cmdRobot>"
  (cl:format cl:nil "float32 Timestamp~%float32[5] Vector_q5~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'cmdRobot)))
  "Returns full string definition for message of type 'cmdRobot"
  (cl:format cl:nil "float32 Timestamp~%float32[5] Vector_q5~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <cmdRobot>))
  (cl:+ 0
     4
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'Vector_q5) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <cmdRobot>))
  "Converts a ROS message object to a list"
  (cl:list 'cmdRobot
    (cl:cons ':Timestamp (Timestamp msg))
    (cl:cons ':Vector_q5 (Vector_q5 msg))
))
