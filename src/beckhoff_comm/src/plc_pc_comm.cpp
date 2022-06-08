// Ros libraries
#include "ros/ros.h"
#include "std_msgs/Float32MultiArray.h"
#include "std_msgs/Float32.h"

#include "beckhoff_msgs/dataArray.h"

//#include "std_msgs/MultiArrayDimension.h"
// Ads libraries
#include "../AdsLib/AdsLib.h"
#include "../AdsLib/AdsVariable.h"
#include "../AdsLib/AdsNotificationOOI.h"

#include <array>
#include <iostream>
#include <iomanip>


// Create route to the PLC
static const AmsNetId remoteNetId { 5, 59, 143, 52, 1, 1 };
static const char remoteIpV4[] = "192.168.65.220";
// uncomment and adjust if automatic AmsNetId deduction is not working as expected
//bhf::ads::SetLocalAddress({192, 168, 65, 146, 1, 1});
AdsDevice route {remoteIpV4, remoteNetId, AMSPORT_R0_PLC_TC3};

// Define data to send to delta robot
AdsVariable<std::array<double, 20>> delta_to_plc {route, "MAIN.RobotDataExchange.PC_to_PLC.dataArray"};
// Define data to send to delta robot
//AdsVariable<std::array<double, 20>> cat_to_plc {route, "Odometry.CaterpillarDataExchange.PC_to_PLC.dataArray"};


// Define publisher
ros::Publisher delta_pub; 
//ros::Publisher caterpillar_pub;

//create odometry to publish
/*nav_msgs::Odometry createOdom(const double robot_odom[]){

	static uint32_t  seq = 0;
	nav_msgs::Odometry odom;

	//header
	std_msgs::Header header;
	header.seq = seq;
	int64_t s = std::chrono::duration_cast<std::chrono::seconds>(std::chrono::system_clock::now().time_since_epoch()).count();
	int64_t ns = std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::system_clock::now().time_since_epoch()).count() - s * 1000000000;
	header.stamp.sec = s;
	header.stamp.nsec = ns;
	header.frame_id = "odom";
	odom.header = header;


	//frame_id
	odom.child_frame_id = "base_link";


	//pose
	geometry_msgs::PoseWithCovariance poseWC;
	geometry_msgs::Pose pose;

	geometry_msgs::Point position;
	position.x = robot_odom[0];
	position.y = robot_odom[1];
	position.z = 0;
	pose.position = position;

	geometry_msgs::Quaternion orientation;
	orientation.x = 0;
	orientation.y = 0;
	orientation.z = -1 * sin(robot_odom[2] / 2);
	orientation.w = cos(robot_odom[2] / 2);
	pose.orientation = orientation;
	poseWC.pose = pose;

	poseWC.covariance = { 0.003, 0, 0, 0, 0, 0,
		0, 0.003, 0, 0, 0, 0,
		0, 0, 0.003, 0, 0, 0,
		0, 0, 0, 0.003, 0, 0,
		0, 0, 0, 0, 0.003, 0,
		0, 0, 0, 0, 0, 0.003 };

	odom.pose = poseWC;


	//twist
	geometry_msgs::TwistWithCovariance twistWC;
	geometry_msgs::Twist twist;

	geometry_msgs::Vector3 linear;
	linear.x = robot_odom[3];
	linear.y = robot_odom[4];
	linear.z = 0;
	twist.linear = linear;

	geometry_msgs::Vector3 angular;
	angular.x = 0;
	angular.y = 0;
	angular.z = robot_odom[5];
	twist.angular = angular;

	twistWC.twist = twist;

	twistWC.covariance = { 0.01, 0, 0, 0, 0, 0,
		0, 0.01, 0, 0, 0, 0,
		0, 0, 0.01, 0, 0, 0,
		0, 0, 0, 0.01, 0, 0,
		0, 0, 0, 0, 0.01, 0,
		0, 0, 0, 0, 0, 0.01 };

	odom.twist = twistWC;
	if ((seq++)>4294967294){ seq = 0; }

	return odom;
}*/


//notification callback function - odometry create and publish on topic
/*void odometryCallback(const AmsAddr* pAddr, const AdsNotificationHeader* pNotification, uint32_t hUser){

	const double* data = reinterpret_cast<const double*>(pNotification + 1);
	nav_msgs::Odometry odom = createOdom(data);
	pub_odom.publish(odom);
}*/


// Notification callback function - read alphas from PLC and publish on topic
void callback_delta_from_plc(const AmsAddr* pAddr, const AdsNotificationHeader* pNotification, uint32_t hUser){

	const double* data = reinterpret_cast<const double*>(pNotification + 1);
    
    beckhoff_msgs::dataArray delta_receive;
	// Read 5 position from motor encoders
    delta_receive.data = {data[0],data[1],data[2],data[3],data[4]};

	//std::cout <<" ADS read " << data[0] << '\n';

	delta_pub.publish(delta_receive);
}

// Send omegas to PLC
void callback_delta_to_plc(const beckhoff_msgs::dataArray& data){
	
	// Send omegas[0..4], timestamp to PLC
	delta_to_plc = { data.data[0], data.data[1], data.data[2], data.data[3], data.data[4], data.data[5],0,0,0,0,0,0,0,0,0,0,0,0,0,0 };

	std::cout <<" ADS write " << data.data[0] << '\n';

    
}

// Notification callback function - read odometry data
void callback_cat_from_plc(const AmsAddr* pAddr, const AdsNotificationHeader* pNotification, uint32_t hUser){

	const double* data = reinterpret_cast<const double*>(pNotification + 1);
    
    beckhoff_msgs::dataArray cat_receive;
	// Read velocity of each caterpillar
    cat_receive.data[0] = data[0];
	cat_receive.data[1] = data[1];
	// Read linear and angular velocity
	cat_receive.data[2] = data[2];
	cat_receive.data[3] = data[3];
	// Read positions -> x, y ,theta, thetaPi
	cat_receive.data[4] = data[4];
	cat_receive.data[5] = data[5];
	cat_receive.data[6] = data[6];
	cat_receive.data[7] = data[7];

	//caterpillar_pub.publish(cat_receive);
}

// Send data to caterpillars
void callback_cat_to_plc(const beckhoff_msgs::dataArray& data){
	
	// Send linear and angular velocities, timestamp to PLC
	//cat_to_plc = { data.data[0], data.data[1], data.data[2]};
    
}


int main(int argc, char **argv)
{

    //std::cout <<" ADS read " << alpha_Delta_0 << '\n';

    ros::init(argc, argv, "ads_communication");
    ros::NodeHandle nh;

    //subscriber
	ros::Subscriber delta_sub = nh.subscribe("/delta_to_plc", 1000, callback_delta_to_plc);
	//ros::Subscriber cat_sub = nh.subscribe("/cat_to_plc", 1000, callback_cat_to_plc);
	//ros::Subscriber sub_ESPG = nh.subscribe("/ESPG", 1000, callback_receive_ESPG);

    // Publish alphas (angles in degrees) from delta robot joints
    delta_pub = nh.advertise<beckhoff_msgs::dataArray >("/delta_from_plc", 1000);
	// Publish odometry data from caterpillar
	//caterpillar_pub = nh.advertise<beckhoff_msgs::dataArray >("/cat_from_plc", 1000);
    
    //notifications -> delta robot
	const AdsNotificationAttrib attrib = { sizeof(double)* 20, ADSTRANS_SERVERCYCLE, 0, { 10000 } };
	AdsNotification notification{ route, "MAIN.RobotDataExchange.PLC_to_PC.dataArray", attrib, &callback_delta_from_plc, 0xBEEFDEAD };
    
	//notifications -> odometry (caterpillars)
	//const AdsNotificationAttrib attrib1 = { sizeof(double)* 20, ADSTRANS_SERVERCYCLE, 0, { 10000 } };
	//AdsNotification notification1{ route, "Odometry.CaterpillarDataExchange.PLC_to_PC.dataArray", attrib1, &callback_cat_from_plc, 0xBEEFDEAD };
    

	ros::spin();
	return 0;
}