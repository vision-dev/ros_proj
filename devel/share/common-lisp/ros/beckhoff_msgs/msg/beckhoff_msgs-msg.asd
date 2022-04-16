
(cl:in-package :asdf)

(defsystem "beckhoff_msgs-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "array5" :depends-on ("_package_array5"))
    (:file "_package_array5" :depends-on ("_package"))
  ))