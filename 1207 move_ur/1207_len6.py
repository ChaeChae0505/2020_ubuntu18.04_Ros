import rospy
from std_msgs.msg import String
from control_msgs.msg import *
from trajectory_msgs.msg import *
from sensor_msgs.msg import JointState
import tf
import roslib
import numpy as np
import math
from math import pi
import joint_state_publisher
import actionlib


class VelListener():
    def __init__(self):
        self.jointstate = None
        self.isReceived = False
        self.final_velocity = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        rospy.init_node('kwon_moveJ', anonymous=True)
        rospy.Subscriber("joint_states",JointState, self.callback) #,"jointstate"
        # rospy.Subscriber("command",JointState,callback,"command")

    def callback(self, data): #,who
        self.jointstate = data.position        
        #print("name: ", who, "value: ", data.position)
        #print(data.position)
        
        self.isReceived = True
    
    #def listen():
        #rospy.init_node('sibal',anonymous=True)
        #ospy.Subscriber("joint_states",JointState,callback) #,"jointstate"
        # rospy.Subscriber("command",JointState,callback,"command")
    def moveJ(self, q_goal,q_init,T):

        A = np.array([[1.0, 0.0, 0.0, 0.0],[1.0, T, T*T, T*T*T],[0.0, 1.0, 0.0, 0.0],[0.0, 1.0, 2*T, 3*T*T]])
        A = np.asmatrix(A)
        a = np.asmatrix([[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0]])
        for i in range(0,6):
          b = np.array([[q_init[i]],[q_goal[i]],[0],[0]])
          b = np.asmatrix(b)
          invA= np.linalg.inv(A)
          a[i,:] =np.transpose(invA*b)
        return a

    def velcitycommand(self,position):
        pub = rospy.Publisher('command', JointState, queue_size=10)
        
        Joint = JointState()
        Joint.header.stamp = rospy.Time.now()
        #rospy.loginfo("Current time %i", Joint.header.stamp.secs)
        Joint.name = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint',
                   'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
        Joint.position = position
        Joint.velocity = []

        rate= rospy.Rate(125)
        pub.publish(Joint)
        rate.sleep()


    def run(self):
        #try:
        #listen()
        r=125
        T=3
        rate= rospy.Rate(r)
        final_velocity = np.array(self.final_velocity)
        while not rospy.is_shutdown():        
            if self.isReceived:
                q = np.array(self.jointstate)
#                q_goal = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                                   
                q_goal = list(raw_input('joint:').split())
                q_goal = map(float, q_goal)
                while True:
                    if len(q_goal)==6:
                        break
                    else:
                        q_goal = list(raw_input('joint again:').split())
                        q_goal = map(float, q_goal)
               
                    
                print q_goal                         
                joint = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                a=self.moveJ(q_goal,q,T)

                for i in range(0,r*T):
                    t = float(i)/125
                    print "1"
                    for j in range(0,5):
                        joint[j] = a[j,:]*[[1.0],[t],[t*t],[t*t*t]]
#                    print(joint)
                    self.velcitycommand(joint)
                self.isReceived = False
                break
#        self.velcitycommand(final_velocity)
            # rate.sleep()
        #except rospy.ROSInterruptException:
            # pass






if __name__=='__main__':
    while True :
 #       try:
        vL = VelListener()
        vL.run()
        
#        except SyntaxError:
           
#        except rospy.ROSInterruptException:
#           print "shut"

