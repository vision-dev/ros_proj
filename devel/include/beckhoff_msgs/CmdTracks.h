// Generated by gencpp from file beckhoff_msgs/CmdTracks.msg
// DO NOT EDIT!


#ifndef BECKHOFF_MSGS_MESSAGE_CMDTRACKS_H
#define BECKHOFF_MSGS_MESSAGE_CMDTRACKS_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace beckhoff_msgs
{
template <class ContainerAllocator>
struct CmdTracks_
{
  typedef CmdTracks_<ContainerAllocator> Type;

  CmdTracks_()
    : stop_tracks(false)
    , start_tracks(false)
    , linear_vel(0.0)
    , rot_vel(0.0)  {
    }
  CmdTracks_(const ContainerAllocator& _alloc)
    : stop_tracks(false)
    , start_tracks(false)
    , linear_vel(0.0)
    , rot_vel(0.0)  {
  (void)_alloc;
    }



   typedef uint8_t _stop_tracks_type;
  _stop_tracks_type stop_tracks;

   typedef uint8_t _start_tracks_type;
  _start_tracks_type start_tracks;

   typedef double _linear_vel_type;
  _linear_vel_type linear_vel;

   typedef double _rot_vel_type;
  _rot_vel_type rot_vel;





  typedef boost::shared_ptr< ::beckhoff_msgs::CmdTracks_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::beckhoff_msgs::CmdTracks_<ContainerAllocator> const> ConstPtr;

}; // struct CmdTracks_

typedef ::beckhoff_msgs::CmdTracks_<std::allocator<void> > CmdTracks;

typedef boost::shared_ptr< ::beckhoff_msgs::CmdTracks > CmdTracksPtr;
typedef boost::shared_ptr< ::beckhoff_msgs::CmdTracks const> CmdTracksConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::beckhoff_msgs::CmdTracks_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::beckhoff_msgs::CmdTracks_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::beckhoff_msgs::CmdTracks_<ContainerAllocator1> & lhs, const ::beckhoff_msgs::CmdTracks_<ContainerAllocator2> & rhs)
{
  return lhs.stop_tracks == rhs.stop_tracks &&
    lhs.start_tracks == rhs.start_tracks &&
    lhs.linear_vel == rhs.linear_vel &&
    lhs.rot_vel == rhs.rot_vel;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::beckhoff_msgs::CmdTracks_<ContainerAllocator1> & lhs, const ::beckhoff_msgs::CmdTracks_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace beckhoff_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::beckhoff_msgs::CmdTracks_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::beckhoff_msgs::CmdTracks_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::beckhoff_msgs::CmdTracks_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::beckhoff_msgs::CmdTracks_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::beckhoff_msgs::CmdTracks_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::beckhoff_msgs::CmdTracks_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::beckhoff_msgs::CmdTracks_<ContainerAllocator> >
{
  static const char* value()
  {
    return "9944d5598f5dddfb3ecdf391f9c85ed5";
  }

  static const char* value(const ::beckhoff_msgs::CmdTracks_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x9944d5598f5dddfbULL;
  static const uint64_t static_value2 = 0x3ecdf391f9c85ed5ULL;
};

template<class ContainerAllocator>
struct DataType< ::beckhoff_msgs::CmdTracks_<ContainerAllocator> >
{
  static const char* value()
  {
    return "beckhoff_msgs/CmdTracks";
  }

  static const char* value(const ::beckhoff_msgs::CmdTracks_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::beckhoff_msgs::CmdTracks_<ContainerAllocator> >
{
  static const char* value()
  {
    return "bool stop_tracks\n"
"bool start_tracks\n"
"float64 linear_vel\n"
"float64 rot_vel\n"
;
  }

  static const char* value(const ::beckhoff_msgs::CmdTracks_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::beckhoff_msgs::CmdTracks_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.stop_tracks);
      stream.next(m.start_tracks);
      stream.next(m.linear_vel);
      stream.next(m.rot_vel);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct CmdTracks_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::beckhoff_msgs::CmdTracks_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::beckhoff_msgs::CmdTracks_<ContainerAllocator>& v)
  {
    s << indent << "stop_tracks: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.stop_tracks);
    s << indent << "start_tracks: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.start_tracks);
    s << indent << "linear_vel: ";
    Printer<double>::stream(s, indent + "  ", v.linear_vel);
    s << indent << "rot_vel: ";
    Printer<double>::stream(s, indent + "  ", v.rot_vel);
  }
};

} // namespace message_operations
} // namespace ros

#endif // BECKHOFF_MSGS_MESSAGE_CMDTRACKS_H
