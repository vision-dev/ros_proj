// Ros libraries
#include "ros/ros.h"

// Include msg to communicate with caterpillars
#include "geometry_msgs/TwistStamped.h"

// Include msg to communicate with robot
#include "beckhoff_msgs/CmdRobot.h"
#include "beckhoff_msgs/JointStateRobot.h"

#include "std_msgs/Float32.h"
#include "rospy_tutorials/Floats.h"

// Raw message for sending to PLC
#include "beckhoff_msgs/dataArray.h"

//#include "std_msgs/MultiArrayDimension.h"
// Ads libraries
#include "../AdsLib/AdsLib.h"
#include "../AdsLib/AdsVariable.h"
#include "../AdsLib/AdsNotificationOOI.h"

#include <array>
#include <iostream>
#include <iomanip>
#include <math.h>
#include <chrono>


// Create route to the PLC
static const AmsNetId remoteNetId { 5, 59, 143, 52, 1, 1 };
static const char remoteIpV4[] = "192.168.65.220";
// uncomment and adjust if automatic AmsNetId deduction is not working as expected
//bhf::ads::SetLocalAddress({192, 168, 65, 146, 1, 1});
AdsDevice route {remoteIpV4, remoteNetId, AMSPORT_R0_PLC_TC3};

// Define data to send to delta robot
AdsVariable<std::array<float, 20>> delta_to_plc {route, "MAIN.RobotDataExchange.PC_to_PLC.dataArray"};

// Define publisher
ros::Publisher alphas_pub; 

int16_t counter;
auto start = std::chrono::steady_clock::now();
auto end = std::chrono::steady_clock::now();


// Notification callback function - read alphas from PLC and publish on topic
void callback_delta_from_plc(const AmsAddr* pAddr, const AdsNotificationHeader* pNotification, uint32_t hUser){
	//counter = counter + 1;

	if (counter==0)
	{
		start = std::chrono::steady_clock::now();	
		counter = 1;
	}
	
	


	//if (counter==1){
	//	start = std::chrono::steady_clock::now();
	//}
	//else{
	//	end = std::chrono::steady_clock::now();

	//	std::cout << "Elapsed time in milliseconds: "
    //    << std::chrono::duration_cast<std::chrono::microseconds>(end - start).count()
    //    << " µs" << std::endl;

	//	counter = 0;
	//}
	
	const float* data = reinterpret_cast<const float*>(pNotification + 1);
    
	// Read raw data from PLC
    beckhoff_msgs::dataArray delta_receive;
	// Timestamp, 5 position from motor encoders
    delta_receive.data = { data[0], data[1], data[2], data[3], data[4],
						data[5], data[6], data[7], data[8], data[9],
						data[10], data[11], data[12], data[13], data[14],
						data[15], data[16], data[17], data[18], data[19] };

	// Read timestamp
	beckhoff_msgs::JointStateRobot RobotJointState;
	// Read actual positions

	//int32_t now_sec = int(floor(delta_receive.data[0]*0.001));
	//int32_t now_nsec = int(delta_receive.data[0]*0.001*1e9)% int(1e9) ;
	//RobotJointState.Timestamp.sec = now_sec;
	//RobotJointState.Timestamp.nsec = now_nsec;
	RobotJointState.Timestamp.sec  = int(delta_receive.data[0]);
	RobotJointState.Timestamp.nsec = int((delta_receive.data[0] - int(delta_receive.data[0]))*1e9);

	RobotJointState.qq.j0 = delta_receive.data[1];
	RobotJointState.qq.j1 = delta_receive.data[2];
	RobotJointState.qq.j2 = delta_receive.data[3];
	RobotJointState.qq.j3 = delta_receive.data[4];
	RobotJointState.qq.j4 = delta_receive.data[5];
	// Read actual velocities
	RobotJointState.dq.j0 = delta_receive.data[6];
	RobotJointState.dq.j1 = delta_receive.data[7];
	RobotJointState.dq.j2 = delta_receive.data[8];
	RobotJointState.dq.j3 = delta_receive.data[9];
	RobotJointState.dq.j4 = delta_receive.data[10];

	alphas_pub.publish(RobotJointState);

}

// Send omegas to PLC
void callback_delta_to_plc(const beckhoff_msgs::CmdRobot& data){

	
	
	// Timestamp, omegas to PLC
	float now_time = float(data.Timestamp.sec) + float(data.Timestamp.nsec) / 10e-9;
	delta_to_plc = {now_time, data.dq.j0, data.dq.j1, data.dq.j2, data.dq.j3, data.dq.j4,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	//delta_to_plc = { 0, 0.0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 };

	//std::cout <<" ADS write " << now_time << '\n';
	
	if (counter==1)
	{
		end = std::chrono::steady_clock::now();

		std::cout << "Elapsed time in microseconds: "
		<< std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count()
		<< " ms" << std::endl;

		counter = 0;
	}
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
	ros::Subscriber omegas_sub = nh.subscribe("/robot/cmd", 1, callback_delta_to_plc);
	
    // Publish alphas (angles in degrees) from delta robot joints
    alphas_pub = nh.advertise<beckhoff_msgs::JointStateRobot >("/robot/joint_state", 1);
    
    //notifications -> delta robot
	const AdsNotificationAttrib attrib = { sizeof(float)* 20, ADSTRANS_SERVERCYCLE, 0, { 10000 } };
	AdsNotification notification{ route, "MAIN.RobotDataExchange.PLC_to_PC.dataArray", attrib, &callback_delta_from_plc, 0xBEEFDEAD };
    
	//notifications -> odometry (caterpillars)
	//const AdsNotificationAttrib attrib1 = { sizeof(double)* 20, ADSTRANS_SERVERCYCLE, 0, { 10000 } };
	//AdsNotification notification1{ route, "Odometry.CaterpillarDataExchange.PLC_to_PC.dataArray", attrib1, &callback_cat_from_plc, 0xBEEFDEAD };
    

	ros::spin();
	return 0;
}