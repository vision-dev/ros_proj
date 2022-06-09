// Auto-generated. Do not edit!

// (in-package beckhoff_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let Vector_q5 = require('./Vector_q5.js');

//-----------------------------------------------------------

class CmdRobot {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.Timestamp = null;
      this.dq = null;
    }
    else {
      if (initObj.hasOwnProperty('Timestamp')) {
        this.Timestamp = initObj.Timestamp
      }
      else {
        this.Timestamp = {secs: 0, nsecs: 0};
      }
      if (initObj.hasOwnProperty('dq')) {
        this.dq = initObj.dq
      }
      else {
        this.dq = new Vector_q5();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type CmdRobot
    // Serialize message field [Timestamp]
    bufferOffset = _serializer.time(obj.Timestamp, buffer, bufferOffset);
    // Serialize message field [dq]
    bufferOffset = Vector_q5.serialize(obj.dq, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type CmdRobot
    let len;
    let data = new CmdRobot(null);
    // Deserialize message field [Timestamp]
    data.Timestamp = _deserializer.time(buffer, bufferOffset);
    // Deserialize message field [dq]
    data.dq = Vector_q5.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 28;
  }

  static datatype() {
    // Returns string type for a message object
    return 'beckhoff_msgs/CmdRobot';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '272eeeecd8726ab3f273e3bf2ed33455';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    time Timestamp
    Vector_q5 dq
    ================================================================================
    MSG: beckhoff_msgs/Vector_q5
    float32 j0
    float32 j1
    float32 j2
    float32 j3
    float32 j4
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new CmdRobot(null);
    if (msg.Timestamp !== undefined) {
      resolved.Timestamp = msg.Timestamp;
    }
    else {
      resolved.Timestamp = {secs: 0, nsecs: 0}
    }

    if (msg.dq !== undefined) {
      resolved.dq = Vector_q5.Resolve(msg.dq)
    }
    else {
      resolved.dq = new Vector_q5()
    }

    return resolved;
    }
};

module.exports = CmdRobot;
