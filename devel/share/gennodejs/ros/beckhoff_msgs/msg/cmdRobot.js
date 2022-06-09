// Auto-generated. Do not edit!

// (in-package beckhoff_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class cmdRobot {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.Timestamp = null;
      this.Vector_q5 = null;
    }
    else {
      if (initObj.hasOwnProperty('Timestamp')) {
        this.Timestamp = initObj.Timestamp
      }
      else {
        this.Timestamp = 0.0;
      }
      if (initObj.hasOwnProperty('Vector_q5')) {
        this.Vector_q5 = initObj.Vector_q5
      }
      else {
        this.Vector_q5 = new Array(5).fill(0);
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type cmdRobot
    // Serialize message field [Timestamp]
    bufferOffset = _serializer.float32(obj.Timestamp, buffer, bufferOffset);
    // Check that the constant length array field [Vector_q5] has the right length
    if (obj.Vector_q5.length !== 5) {
      throw new Error('Unable to serialize array field Vector_q5 - length must be 5')
    }
    // Serialize message field [Vector_q5]
    bufferOffset = _arraySerializer.float32(obj.Vector_q5, buffer, bufferOffset, 5);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type cmdRobot
    let len;
    let data = new cmdRobot(null);
    // Deserialize message field [Timestamp]
    data.Timestamp = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [Vector_q5]
    data.Vector_q5 = _arrayDeserializer.float32(buffer, bufferOffset, 5)
    return data;
  }

  static getMessageSize(object) {
    return 24;
  }

  static datatype() {
    // Returns string type for a message object
    return 'beckhoff_msgs/cmdRobot';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '4c364234fdb48115e683b6d91edb1a06';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 Timestamp
    float32[5] Vector_q5
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new cmdRobot(null);
    if (msg.Timestamp !== undefined) {
      resolved.Timestamp = msg.Timestamp;
    }
    else {
      resolved.Timestamp = 0.0
    }

    if (msg.Vector_q5 !== undefined) {
      resolved.Vector_q5 = msg.Vector_q5;
    }
    else {
      resolved.Vector_q5 = new Array(5).fill(0)
    }

    return resolved;
    }
};

module.exports = cmdRobot;
