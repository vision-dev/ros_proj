; Auto-generated. Do not edit!


(cl:in-package beckhoff_msgs-msg)


;//! \htmlinclude dataArray.msg.html

(cl:defclass <dataArray> (roslisp-msg-protocol:ros-message)
  ((data
    :reader data
    :initarg :data
    :type (cl:vector cl:float)
   :initform (cl:make-array 20 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass dataArray (<dataArray>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <dataArray>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'dataArray)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name beckhoff_msgs-msg:<dataArray> is deprecated: use beckhoff_msgs-msg:dataArray instead.")))

(cl:ensure-generic-function 'data-val :lambda-list '(m))
(cl:defmethod data-val ((m <dataArray>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader beckhoff_msgs-msg:data-val is deprecated.  Use beckhoff_msgs-msg:data instead.")
  (data m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <dataArray>) ostream)
  "Serializes a message object of type '<dataArray>"
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'data))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <dataArray>) istream)
  "Deserializes a message object of type '<dataArray>"
  (cl:setf (cl:slot-value msg 'data) (cl:make-array 20))
  (cl:let ((vals (cl:slot-value msg 'data)))
    (cl:dotimes (i 20)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-double-float-bits bits)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<dataArray>)))
  "Returns string type for a message object of type '<dataArray>"
  "beckhoff_msgs/dataArray")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'dataArray)))
  "Returns string type for a message object of type 'dataArray"
  "beckhoff_msgs/dataArray")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<dataArray>)))
  "Returns md5sum for a message object of type '<dataArray>"
  "c56fc869e3a3f36debd8a653b1ddb834")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'dataArray)))
  "Returns md5sum for a message object of type 'dataArray"
  "c56fc869e3a3f36debd8a653b1ddb834")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<dataArray>)))
  "Returns full string definition for message of type '<dataArray>"
  (cl:format cl:nil "float64[20] data~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'dataArray)))
  "Returns full string definition for message of type 'dataArray"
  (cl:format cl:nil "float64[20] data~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <dataArray>))
  (cl:+ 0
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'data) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <dataArray>))
  "Converts a ROS message object to a list"
  (cl:list 'dataArray
    (cl:cons ':data (data msg))
))
