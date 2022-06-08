
(cl:in-package :asdf)

(defsystem "beckhoff_msgs-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "array5" :depends-on ("_package_array5"))
    (:file "_package_array5" :depends-on ("_package"))
    (:file "array6" :depends-on ("_package_array6"))
    (:file "_package_array6" :depends-on ("_package"))
    (:file "catReceive" :depends-on ("_package_catReceive"))
    (:file "_package_catReceive" :depends-on ("_package"))
    (:file "catSend" :depends-on ("_package_catSend"))
    (:file "_package_catSend" :depends-on ("_package"))
    (:file "dataArray" :depends-on ("_package_dataArray"))
    (:file "_package_dataArray" :depends-on ("_package"))
  ))