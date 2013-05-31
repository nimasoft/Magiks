'''   Header
@file:          PR2_kinematics.py
@brief:    	    Contains specific functions that define all geometric and kinematic parameters for PR2 robot
                A transparent version of pr2_kinematics.py

@author:        Nima Ramezani Taghiabadi
                PhD Researcher
                Faculty of Engineering and Information Technology
                University of Technology Sydney (UTS)
                Broadway, Ultimo, NSW 2007, Australia
                Room No.: CB10.03.512
                Phone:    02 9514 4621
                Mobile:   04 5027 4611
                Email(1): Nima.RamezaniTaghiabadi@student.uts.edu.au 
                Email(2): nima.ramezani@gmail.com
                Email(3): nima_ramezani@yahoo.com
                Email(4): ramezanitn@alum.sharif.edu
@version:	    1.4
Last Revision:  1 June 2013

Changes from ver 1.3:
                function permission_set_analytic uses arithmetic of intervals to find the intervals faster. The results have been compared to the previous method in the transparent version

'''

import packages.nima.mathematics.general as gen
from sympy import Symbol, simplify
from interval import interval, inf, imath
from sets import Set

'''
The most convenient way to install "pyinterval" library is by means of easy_install:
sudo easy_install pyinterval
Alternatively, it is possible to download the sources from PyPI and invoking
python setup.py install
from sets import Set
Please refer to:
http://pyinterval.googlecode.com/svn-history/r25/trunk/html/index.html
'''
import numpy, math
import packages.nima.robotics.kinematics.kinematicpy.general as genkin
import packages.nima.robotics.kinematics.joint_space.configuration as configlib
import packages.nima.mathematics.general as gen
import packages.nima.mathematics.trigonometry as trig
import packages.nima.mathematics.vectors_and_matrices as vecmat

drc     = math.pi/180.00


class PR2_ARM_Configuration():

    def joint_in_range(self,i, qi):
        '''
        returns True if the given joint angle qi is in feasible range for the i-th joint (within the specified joint limits for that joint)
        '''
        qi = trig.angle_standard_range(qi) 
        if abs(qi - self.ql[i]) < gen.epsilon:
            qi = self.ql[i]
        if abs(qi - self.qh[i]) < gen.epsilon:
            qi = self.qh[i]

        return ((qi <= self.qh[i]) and (qi >= self.ql[i]))
    
    def all_joints_in_range(self, qd):
        '''
        Then, if The given joints "qd" are out of the range specified by properties: ql and qh, returns False, otherwise returns True  
        '''
        flag = True
        for i in range(0, 7):
            flag = flag and self.joint_in_range(i, qd[i])
        return flag

    def set_config(self, qd):
        '''
        sets the configuration to "qd"
        This function should not be called by the end user. Use function "set_config" in class PR2_ARM  
        '''    

        if not len(qd) == 7:
            print "set_config error: Number of input elements must be 7"
            return False

        if self.all_joints_in_range(qd):
         
            self.q = trig.angles_standard_range(qd)

            self.c = [math.cos(self.q[i]) for i in range(0,7)]
            self.s = [math.sin(self.q[i]) for i in range(0,7)]

            [s0, s1, s2, s3, s4, s5, s6] = self.s
            [c0, c1, c2, c3, c4, c5, c6] = self.c

            self.s1_mult1 = [s1*s0]
            [s10]         = self.s1_mult1

            self.s2_mult1 = s2*numpy.array([s0, s1, s2, s10])
            [s20,s21, s22, s210]  = self.s2_mult1

            self.s3_mult1 = s3*numpy.array([s0, s1, s2, s10, s20, s21, s22, s3,s210])
            [s30, s31, s32, s310, s320, s321, s322, s33,s3210] = self.s3_mult1

            self.c0_mult = c0*numpy.array([s0,s1,s2,s10,s20,s21,s30,s31,s32,s321])
            [c0s0,c0s1,c0s2,c0s10,c0s20,c0s21,c0s30,c0s31,c0s32,c0s321] = self.c0_mult

            self.c1_mult = c1*numpy.array([c0, s0, s1, s2, s3, s10, s20,s30,s32, s320])
            [c10, c1s0, c1s1, c1s2, c1s3, c1s10, c1s20,c1s30,c1s32,c1s320] = self.c1_mult

            self.c2_mult = c2*numpy.array([c0,c1,c2,c10,s0,s1,s2,s3,s10,s20,s30,s31,s310, c1s30,c0s31])
            [c20,c21,c22,c210,c2s0,c2s1,c2s2,c2s3,c2s10,c2s20,c2s30,c2s31,c2s310,c21s30,c20s31] = self.c2_mult

            self.c3_mult = c3*numpy.array([c0,c1,c2,c3, s0,s1,s2,s3,s10,s20,s21,s30,c10,c20,c21,c210,c2s0,c2s10])
            [c30,c31,c32,c33,c3s0,c3s1,c3s2,c3s3,c3s10,c3s20,c3s21,c3s30,c310,c320,c321,c3210,c32s0,c32s10] = self.c3_mult

            self.s0_mult = s0*numpy.array([c21,c31,c321])
            [c21s0,c31s0,c321s0]  = self.s0_mult

            self.s1_mult2 = s1*numpy.array([c10,c20,c30, c32,c320])
            [c10s1,c20s1,c30s1, c32s1,c320s1] = self.s1_mult2

            self.s2_mult2 = s2*numpy.array([c10,c20,c30, c32,c310])
            [c10s2,c20s2,c30s2, c32s2,c310s2]  = self.s2_mult2

            self.s3_mult2 = s3*numpy.array([c10, c20, c30, c21, c210,s32])
            [c10s3, c20s3, c30s3, c21s3, c210s3,s332]  = self.s3_mult2

            self.cs_mult = [c10*s32, c31*s20, s5*s4]
            [c10s32, c31s20, s54] = self.cs_mult

            self.c5_mult = c5*numpy.array([c4, s4, s5])
            [c54, c5s4, c5s5] = self.c5_mult

            self.s6_mult = s6*numpy.array([s4, s5, c4, c5, c54, s54])
            [s64, s65, c4s6, c5s6, c54s6, s654] = self.s6_mult

            self.c6_mult = c6*numpy.array([c4, c5, s4, s5, c54, s54])
            [c64, c65, c6s4, c6s5, c654, C6s54] = self.c6_mult
            return True
        else:
            print "set_config error: Input joint configuration is not in the defined feasible range"
            return False
        

    def __init__(self, ql = drc*numpy.array([-130, -30, -180, 0, -180, 0, -180]), qh = drc*numpy.array([40, 80, 44, 130, 180, 130, 180])):
        '''
        ql and qh define the lower and higher bounds of the joints
        
        '''    

        assert (len(ql) == 7) and (len(qh) == 7)

        self.ql = ql
        self.qh = qh
        self.qm = (qh + ql)/2

        # sets all angles as zero by default
        self.set_config(numpy.zeros(7))
        self.W = numpy.zeros(7)
        for i in range(0,7):
            self.W[i] = 1/(qh[i] - ql[i])

class PR2_ARM():

    def set_config(self, qd):
        if self.config.set_config(qd):
            self.wrist_position_updated = False
            self.wrist_orientation_updated = False
            self.jacobian_updated = False
            self.in_target_updated = False
            self.joint_jacobian_updated = False
            return True
        else:
            print "Given joints out of feasible range"
            return False

    def set_target(self, target_position, target_orientation):
        '''
        sets the endeffector target to the given position and orientation
        variables self.xd and self.Rd should not be manipulated by the user. Always use this function
        '''    
        self.xd = target_position
        self.Rd = target_orientation

        [Q, Q2, d42, d44, a00, d22_plus_d44, foura00d44, alpha] = self.additional_dims

        sai = math.atan2(self.xd[0], self.xd[1])
        r2  = self.xd[0]**2 + self.xd[1]**2
        ro2 = r2 + self.xd[2]**2
        R2  = ro2 - d22_plus_d44 + a00
        '''
        alpha, betta and gamma are selected so that w^2 * (1 - v^2) = alpha*v^2 + betta*v + gamma
        '''
        
        T2    = R2**2 - 4*a00*r2
        betta = - 2*R2*Q/foura00d44
        gamma = - T2/foura00d44

        self.in_target_updated = False
        self.joint_jacobian_updated = False

        self.target_parameters = [r2, ro2, R2, T2, alpha, betta, gamma, sai]
            
    def wrist_position(self):        
        '''
        Returns the cartesian coordiantes of the origin of the wrist. The origin of the wrist is the wrist joint center 
        '''    
        if not self.wrist_position_updated:
            [s0, s1, s2, s3, s4, s5, s6] = self.config.s
            [c0, c1, c2, c3, c4, c5, c6] = self.config.c
            [s10]         = self.config.s1_mult1
            [s30, s31, s32, s310, s320, s321, s322, s33,s3210] = self.config.s3_mult1
            [c0s0,c0s1,c0s2,c0s10,c0s20,c0s21,c0s30,c0s31,c0s32,c0s321] = self.config.c0_mult
            [c20,c21,c22,c210,c2s0,c2s1,c2s2,c2s3,c2s10,c2s20,c2s30,c2s31,c2s310,c21s30,c20s31] = self.config.c2_mult
            [c30,c31,c32,c33,c3s0,c3s1,c3s2,c3s3,c3s10,c3s20,c3s21,c3s30,c310,c320,c321,c3210,c32s0,c32s10] = self.config.c3_mult
            [c10s1,c20s1,c30s1, c32s1,c320s1] = self.config.s1_mult2
            [c10s3, c20s3, c30s3, c21s3,c210s3,s332]  = self.config.s3_mult2

            X =  c0*self.a0 + c0s1*self.d2 + (c30s1 + c210s3 - s320)*self.d4

            Y =  s0*self.a0 + s10*self.d2 + (c3s10 + c0s32 + c21s30)*self.d4

            Z =  c1*self.d2 + (c31 - c2s31)*self.d4
        
            self.wrist_position_vector = numpy.array([X, Y, Z])
            self.wrist_position_updated = True

        return self.wrist_position_vector

    def wrist_orientation(self):        

        if not self.wrist_orientation_updated:
            [s0, s1, s2, s3, s4, s5, s6] = self.config.s
            [c0, c1, c2, c3, c4, c5, c6] = self.config.c
            [s10]         = self.config.s1_mult1
            [s20,s21, s22, s210]  = self.config.s2_mult1
            [c0s0,c0s1,c0s2,c0s10,c0s20,c0s21,c0s30,c0s31,c0s32,c0s321] = self.config.c0_mult
            [c10, c1s0, c1s1, c1s2, c1s3, c1s10, c1s20,c1s30,c1s32,c1s320] = self.config.c1_mult
            [c20,c21,c22,c210,c2s0,c2s1,c2s2,c2s3,c2s10,c2s20,c2s30,c2s31,c2s310,c21s30,c20s31] = self.config.c2_mult
            [c21s0,c31s0,c321s0]  = self.config.s0_mult
            [c10s2,c20s2,c30s2, c32s2,c310s2]  = self.config.s2_mult2
            [c10s32, c31s20, s54] = self.config.cs_mult
            [s64, s65, c4s6, c5s6, c54s6, s654] = self.config.s6_mult
            [c64, c65, c6s4, c6s5, c654, C6s54] = self.config.c6_mult

            R03 = numpy.array([[-s20 + c210, -c0s1, -c2s0 - c10s2],
                               [c0s2 + c21s0, -s10, c20 - c1s20],                
                               [-c2s1, -c1, s21]]) 

            R47 = numpy.array([[-s64 + c654, -c6s4 - c54s6, c4*s5],
                               [c4s6 + c65*s4, c64 - c5*s64, s54],                
                               [-c6s5, s65, c5]]) 

            R34 =  numpy.array([[  c3,     0,     s3 ],
                                [  s3,     0,    -c3 ],
                                [  0,      1,     0  ]])


            self.wrist_orientation_matrix = numpy.dot(numpy.dot(R03, R34), R47)
            self.wrist_orientation_updated = True

        return self.wrist_orientation_matrix

    def joint_jacobian(self):  
        '''
        make sure that the IK is already run or:
        Current joints must lead to x_d and R_d  
        '''

        if not self.joint_jacobian_updated:

            [[nx, sx, ax],
            [ny, sy, ay],
            [nz, sz, az]] = self.Rd


            [s0, s1, s2, s3, s4, s5, s6] = self.config.s
            [c0, c1, c2, c3, c4, c5, c6] = self.config.c

            [s10]         = self.config.s1_mult1
            [s20,s21, s22, s210]  = self.config.s2_mult1
            [s30, s31, s32, s310, s320, s321, s322, s33,s3210] = self.config.s3_mult1
            [c0s0,c0s1,c0s2,c0s10,c0s20,c0s21,c0s30,c0s31,c0s32,c0s321] = self.config.c0_mult
            [c10, c1s0, c1s1, c1s2, c1s3, c1s10, c1s20,c1s30,c1s32,c1s320] = self.config.c1_mult
            [c20,c21,c22,c210,c2s0,c2s1,c2s2,c2s3,c2s10,c2s20,c2s30,c2s31,c2s310,c21s30,c20s31] = self.config.c2_mult
            [c30,c31,c32,c33,c3s0,c3s1,c3s2,c3s3,c3s10,c3s20,c3s21,c3s30,c310,c320,c321,c3210,c32s0,c32s10] = self.config.c3_mult
            [c21s0,c31s0,c321s0]  = self.config.s0_mult
            [c10s1,c20s1,c30s1, c32s1,c320s1] = self.config.s1_mult2
            [c10s2,c20s2,c30s2, c32s2,c310s2]  = self.config.s2_mult2
            [c10s3, c20s3, c30s3, c21s3, c210s3,s332]  = self.config.s3_mult2
            [c10s32, c31s20, s54] = self.config.cs_mult
            [c54, c5s4, c5s5] = self.config.c5_mult
            [s64, s65, c4s6, c5s6, c54s6, s654] = self.config.s6_mult
            [c64, c65, c6s4, c6s5, c654, C6s54] = self.config.c6_mult

            [Q, Q2, d42, d44, a00, d22_plus_d44, foura00d44, alpha] = self.additional_dims

            [r2, ro2, R2, T2, alpha, betta, gamma, sai] = self.target_parameters

            # Assert the following equalities:

            F = numpy.zeros((7,7))

            F[1,0] =   2*self.a0*(s0*self.xd[0] - c0*self.xd[1])
            F[1,3] = - Q*s3

            F[2,2] = - 2*c2*s332
            F[2,3] = - 2*alpha*c3s3 - betta*s3 - 2*c3*s322
            
            F[3,1] = - self.d2*s1 - (c3*s1 + c2*c1*s3)*self.d4
            F[3,2] =   s321*self.d4
            F[3,3] =   - (c1s3 + c32s1)*self.d4
            
            F[4,0] = ax*(- c0s32 - c21s30 - c3s10) + ay*(- s320  + c210s3 + c30s1)  
            F[4,1] = ax*(- c20*s31 + c310) + ay*(- c2s310 + c31s0) - az*(c3s1 + c21*s3)
            F[4,2] = - ax*(c2s30 + c10s32) + ay*(c20s3 - c1s320) + az*s321

            F[4,3] = ax*(- c3s20 + c3210 - c0s31) + ay*(c30s2 + c321s0 - s310) + az*(- c1s3 - c32s1)
            F[4,5] = s5

            F[5,0] = ax*(-c20 + c1s20) - ay*(c2s0 + c10s2)
            F[5,1] = ax*c0s21 - ay*s210 + az*c1s2
            F[5,2] = ax*(s20 - c210) - ay*(c0s2 + c21s0) + az*c2s1
            F[5,4] = - c4*s5
            F[5,5] = - c5*s4

            F[6,0] = - nx*(c0s32 + c21s30 + c3s10) + ny*(- s320 + c210s3 + c30s1)
            F[6,1] =   nx*(- c20s31 + c310) + ny*(- c2s310 + c31s0) - nz*(c3s1 + c21s3)
            F[6,2] = - nx*(c2s30 + c10s32) + ny*(c20s3 - c1s320) + nz*s321
            F[6,3] =   nx*(- c3s20 + c3210 - c0s31) + ny*(c30s2 + c321s0 - s310) - nz*(c1s3 + c32s1)
            F[6,5] =   c65
            F[6,6] = - s65

            self.JJ = numpy.zeros(7)

            self.JJ[0] =   1.0
            self.JJ[3] = - F[1,0]/F[1,3]
            self.JJ[2] = - F[2,3]*self.JJ[3]/F[2,2]
            self.JJ[1] = - (F[3,2]*self.JJ[2] + F[3,3]*self.JJ[3])/F[3,1]

            self.JJ[5] = - numpy.dot(F[4,0:4],self.JJ[0:4])/F[4,5]
            #J[5] = - (F[4,0] + F[4,1]*J[1] + F[4,2]*J[2] + F[4,3]*J[3])/F[4,5]
            self.JJ[4] = - (F[5,0] + F[5,1]*self.JJ[1] + F[5,2]*self.JJ[2] + F[5,5]*self.JJ[5])/F[5,4] 
            self.JJ[6] = - numpy.dot(F[6,0:6],self.JJ[0:6])/F[6,6]
            #F60*J0 + F61*J1 + F62*J2 + F63*J3 + F64*J4 + F65*J5 + F66*J6 = 0  ==> J6 = - (F60 + F61*J1 + F62*J2 + F63*J3 + F64*J4 + F65*J5)/ J66
            self.joint_jacobian_updated = True

        return self.JJ

    def position_permission_workspace(self,fixed):
        '''
        returns the permission range of x, y and z of the endeffector.
        fixed is an array of size 4, specifying if the corresponding joint is fixed or free
        The size is 4 because only the first four joints influence the position of the EE
        '''
        int_c = []
        int_s = []

        for i in range(0,4):
            if fixed[i]:
                int_c.append(imath.cos(interval(self.config.q[i])))
                int_s.append(imath.sin(interval(self.config.q[i])))
            else:
                int_c.append(imath.cos(interval([self.config.ql[i], self.config.qh[i]])))
                int_s.append(imath.sin(interval([self.config.ql[i], self.config.qh[i]])))

        int_s10    = int_s[1]*int_s[0]
        int_s32    = int_s[3]*int_s[2]        
        int_s31    = int_s[3]*int_s[1]        
        int_s320   = int_s32*int_s[0]

        int_c21    = int_c[2]*int_c[1]
        int_c31    = int_c[3]*int_c[1]
        int_c0s1   = int_c[0]*int_s[1]
        int_c30s1  = int_c[3]*int_c0s1
        int_c0s32  = int_s32*int_c[0]
        int_c21s3  = int_c21*int_s[3]
        int_c21s30 = int_c21s3*int_s[0]
        int_c210s3 = int_c21s3*int_c[0]
        int_c2s31  = int_s31*int_c[2]
        int_c3s10  = int_s10*int_c[3]

        int_X =  int_c[0]*interval(self.a0) + int_c0s1*interval(self.d2) + (int_c30s1 + int_c210s3 - int_s320)*interval(self.d4)

        int_Y =  int_s[0]*interval(self.a0) + int_s10*interval(self.d2) + (int_c3s10 + int_c0s32 + int_c21s30)*interval(self.d4)

        int_Z =  int_c[1]*interval(self.d2) + (int_c31 - int_c2s31)*interval(self.d4)

        return [int_X, int_Y, int_Z]
        
    def inverse_update(self):    
        '''
        Finds the inverse kinematic which is closest to the midrange of joints 
        The new joint angles will be set if all the kinematic equations are satisfied. 
        All kinematic parameters will be updated.
        '''
        # Finding a feasible phi (theta0)

        # first try the current theta0:
        phi     = self.config.q[0]
        phi_l   = self.config.ql[0]
        phi_h   = self.config.qh[0]
        q_d     = self.IK_config(phi)

        # If solution not found search within the range:
        
        n = 3
        while (len(q_d) == 0) and (n < 10):
            i = 0
            while (len(q_d) == 0) and (i < n):
                phi = phi_l + (2*i + 1)*(phi_h - phi_l)/(2*n)
                q_d = self.IK_config(phi)
                i = i + 1
            n = n + 1

        if len(q_d) == 0:
            print "Given pose out of workspace. No solution found"
            return False
        
        new_error       = numpy.linalg.norm(trig.angles_standard_range(q_d - self.config.qm))
        old_error       = 10000

        P = numpy.zeros(7)
        e = numpy.zeros(7)
        while (new_error < old_error - gen.epsilon) and (len(q_d) != 0) and (new_error > gen.epsilon):
            old_error = new_error
            assert self.set_config(q_d)                        
            J = self.joint_jacobian()
            for i in range(0,7):
                P[i] = self.config.W[i]*J[i]
                e[i] = self.config.W[i]*(q_d[i] - self.config.qm[i])        

            Delta_phi  = - numpy.dot(P.T, e) / numpy.dot(P.T, P)
            old_error  = numpy.linalg.norm(e)

            q_d        = self.IK_config(phi + Delta_phi)

            if len(q_d) == 0:
                new_error = 0
            else:
                #new_error = numpy.linalg.norm(trig.angles_standard_range(q_d - self.config.qm))
                for i in range(0,7):
                    e[i] = self.config.W[i]*(q_d[i] - self.config.qm[i])        

                new_error  = numpy.linalg.norm(e)
          
        assert vecmat.equal(self.wrist_position(), self.xd)
        assert vecmat.equal(self.wrist_orientation(), self.Rd)
        return True
        
    def IK_config(self, tt0):    
        '''
        Finds the solution of the Inverse Kinematic problem for given theta0 = tt0

        In case of redundant solutions, the one closest to current joint angles will be selected 
        ''' 
        if not self.config.joint_in_range(0, tt0):
            print "IK_config error: Given theta0 out of feasible range"
            return []

        solution_set = []

        c0 = math.cos(tt0)
        s0 = math.sin(tt0)

        [Q, Q2, d42, d44, a00, d22_plus_d44, foura00d44, alpha] = self.additional_dims
        [r2, ro2, R2, T2, alpha, betta, gamma, sai] = self.target_parameters

        u  = c0*self.xd[0] + s0*self.xd[1]
        v  = (2*self.a0*u - R2)/Q

        v2 = v**2
        A  = self.d2 + v*self.d4

        if gen.equal(v, 1.0):
            #"Singular Point"
            return []
            '''
            In this case, a singularity happens
            '''
        elif (v > 1.0) or (v < -1.0): 
            #"Given pose out of workspace"
            return []
        else:
            i  = 0
            tt3 = trig.arccos(v)

            while (i < 2):
                theta3 = (2*i - 1)*tt3  # theta3 is certainly in standard range
                if self.config.joint_in_range(3,theta3):
                    s3     = math.sin(theta3)
                    c3     = v
                    c30    = c3*c0
                    B      = self.d4*s3
                    T34 = genkin.transfer_DH_standard( 0.0 , math.pi/2, 0.0, 0.0, theta3)
                    R34 = T34[0:3,0:3]

                    w  = math.sqrt((alpha*v2 + betta*v + gamma)/(1 - v2))
                    if (w < 1.0):
                        m = 0
                        while (m < 2):
                            s2  = (2*m - 1)*w
                            s20 = s2*s0 
                            c0s2= c0*s2  
                            
                            tt2 = trig.arcsin(s2)
                            j = 0
                            while (j < 2):
                                theta2 = trig.angle_standard_range(math.pi*(1 - j) + (2*j - 1)*tt2)
                                if self.config.joint_in_range(2, theta2):
                                    c2     = math.cos(theta2)
                                    c20    = c2*c0
                                    c2s0   = c2*s0
                                    E      = B*s2
                                    F      = B*c2
                                    R1     = math.sqrt(A**2 + F**2)
                                    sai1   = math.atan2(F,A)
                                    R1_nul = gen.equal(R1, 0)
                                    if not R1_nul:
                                        z_R1 = self.xd[2]/R1    
                                        flg  = (z_R1 < 1.0) and (z_R1 > - 1.0)
                                    else:
                                        flg = False

                                    if flg:
                                        tt1 = trig.arccos(self.xd[2]/R1)
                                        k = 0                
                                        while (k < 2):
                                            theta1 = (2*k - 1)*tt1 - sai1 
                                            if self.config.joint_in_range(1, theta1):
                                                s1   = math.sin(theta1)
                                                c1   = math.cos(theta1)
                                                
                                                As1Fc1 = self.a0 + A*s1 + F*c1
                                                X      = c0*As1Fc1 - E*s0
                                                Y      = s0*As1Fc1 + E*c0
                                                Z      = A*c1 - F*s1 

                                                u2 = s2*s3*self.d4
                                                u3 = c2*s3*self.d4
                                                u4 = self.d2+ c3*self.d4
                                                u1 = self.a0 + u3*c1 + u4*s1
                                                AA = numpy.array([[alpha*d44, d44*betta - 2*d42 , - self.d2**2 + d44*(gamma -1)],
                                                                   [0.0 , 2*self.xd[2]*self.d4 , 2*self.xd[2]*self.d2],   
                                                                   [- d44*(1+alpha) , -betta*d44 , - self.xd[2]**2 + d44*(1-gamma) ]])
                                                lnda = numpy.array([c1*c1, c1, 1.0])
                                                vvct = numpy.array([v*v, v, 1.0])

                                                if vecmat.equal(self.xd, [X,Y,Z]):
                                                    R03 = numpy.array([[c20*c1 - s20, -c0*s1, -c2s0 - c1*c0*s2],
                                                                       [c0s2 + c1*c2*s0, -s1*s0, c20 - c1*s20],   
                                                                       [-c2*s1, -c1, s2*s1 ]])

                                                    R04 = numpy.dot(R03, R34)
                                                    R47 = numpy.dot(R04.T, self.Rd)
                                                    tt5 = trig.arccos(R47[2,2])
                                                    l = 0
                                                    while (l < 2):
                                                        theta5 = (2*l - 1)*tt5 # theta5 is certainly in standard range
                                                        if self.config.joint_in_range(5, theta5):
                                                            s5     = math.sin(theta5)
                                                            c5     = math.cos(theta5)
                                                            if gen.equal(s5,0):
                                                                assert gen.equal(R47[2,0], 0)
                                                                # "Singular Point"
                                                                return []
                                                                '''
                                                                In this case, only sum of theta4 + theta6 is known 
                                                                '''
                                                            else:
                                                                c6     = - R47[2,0]/s5
                                                                s6     =   R47[2,1]/s5
                                                                c4     =   R47[0,2]/s5
                                                                s4     =   R47[1,2]/s5

                                                                theta6 =   gen.sign(s6)*trig.arccos(c6)
                                                                assert gen.equal(s6, math.sin(theta6))

                                                                theta4 =   gen.sign(s4)*trig.arccos(c4)
                                                                assert gen.equal(s4, math.sin(theta4))

                                                                assert gen.equal(R47[1,0] ,  c4*s6 + c5*c6*s4)
                                                                assert gen.equal(R47[1,1] ,  c4*c6 - c5*s4*s6)
                                                                assert gen.equal(R47[0,0] ,  -s4*s6 + c4*c5*c6)
                                                                assert gen.equal(R47[0,1] ,  -c6*s4 - c4*c5*s6)

                                                                assert self.config.joint_in_range(4, theta4)    
                                                                assert self.config.joint_in_range(6, theta6)    

                                                                solution_set.append(numpy.array([tt0, theta1, theta2, theta3, theta4, theta5, theta6]))
                                                        l = l + 1
                                            k = k + 1
                                j = j + 1
                            m = m + 1
                i = i + 1 

        if len(solution_set) == 0:
            #"No solution within the feasible joint ranges"
            return []

        delta_min = 1000
        for i in range(0, len(solution_set)):
            solution = solution_set[i]
            delta    = numpy.linalg.norm(trig.angles_standard_range(solution - self.config.q))
            if delta < delta_min:
                delta_min = delta
                i_min = i
            
        return solution_set[i_min]

        self.set_config()

        pos = self.wrist_position()

        return True

    def __init__(self, a0 = 0.1, d2 = 0.4, d4 = 0.321):

        self.config = PR2_ARM_Configuration()        
    
        self.a0 = a0
        self.d2 = d2
        self.d4 = d4

        d42 = d4*d2
        Q   = -2*d42
        Q2  = Q**2
        d44 = d4**2
        a00 = a0**2

        d22_plus_d44 = d2*d2 + d44
        foura00d44   = 4*a00*d44 
        alpha        = - Q2/foura00d44

        self.additional_dims = [Q, Q2, d42, d44, a00, d22_plus_d44, foura00d44, alpha]


        self.l_se = [0.0, - d2, 0.0]
        self.l_ew = [0.0, 0.0, d4]

        self.wrist_position_updated         = False
        self.wrist_orientation_updated      = False
        self.jacobian_updated               = False
        self.joint_jacobian_updated         = False


    '''
    def confidence_set_analytic(self):
        """
        This function finds and returns the confidence set for q0 so that joint angles q0 , q2 and q3 in the analytic solution to the inverse kinematic problem
        will be in their feasible range.
        For q0 being in the confidence set is a necessary and sufficient condition for three joints q0, q2 and q3 to be in their feasible range.
        "Confidence set" is a subset of "Permission set"
        The confidence set depends on the defined joint limits, the desired endeffector pose and current position of the joints (the quarter in which q2 and q3 are located).
        """
        s2_l  = math.sin(self.config.ql[2])
        s2_l2 = s2_l**2
        s2_h  = math.sin(self.config.qh[2])
        s2_h2 = s2_h**2

        # Finding wl, wh:

        qnl = trig.quarter_number(self.config.ql[2])
        qnh = trig.quarter_number(self.config.qh[2])
        qn  = trig.quarter_number(self.config.q[2])

        if qn == qnl:   # lower bound is in the same quarter as q2
            if (qn == qnh): # upper bound is in the same quarter as q2
                wl = min(s2_l2,s2_h2)
                wh = max(s2_l2,s2_h2)
            elif qn in [1,3]:
                (wl,wh) = (s2_l2, 1.0)
            else:
                (wl,wh) = (0.0, s2_l2)
        else:
            if (qn != qnh): # upper bound is not in the same quarter as q2
                (wl,wh) = (0.0, 1.0)
            elif qn in [1,3]:
                (wl,wh) = (0.0, s2_h2)
            else:
                (wl,wh) = (s2_h2, 1.0)

        # From here, copied from permission set
        #Finding Sl
        '''

    def permission_set_position(self):
        """
        This function finds and returns the set from which q0 is allowed to be chosen so that joint angles q0 , q2 and q3 in the analytic solution 
        to the inverse kinematic problem are in their range. 
        Consider that being q0 in the permission set, does not guarantee that all q0, q2 and q3 are in their ranges, but
        it means that if q0 is out of permission set, one of the joints q0, q2 or q3 will definitely be out of their feasible range.
        In other words, q0 being in perm. set, is a necessary but not enough condition for three joints q0, q2 and q3 to be in their range.
        Permission set is broader than "confidence set" which ensures all q0, q2 and q3 to be in range.
        The output depends on the defined joint limits and the desired endeffector pose but does not depend on the current position of the joints.
        """

        [r2, ro2, R2, T2, alpha, betta, gamma, sai] = self.target_parameters
        [Q, Q2, d42, d44, a00, d22_plus_d44, foura00d44, alpha] = self.additional_dims

        # feasibility set for v imposed by theta1

        int_theta1 = interval([self.config.ql[1],self.config.qh[1]])
        int_lnda   = imath.cos(int_theta1)
        int_lnda2   = int_lnda**2

        AA = numpy.array([[alpha*d44, d44*betta - 2*d42 , - self.d2**2 + d44*(gamma -1)],
                          [0.0 , 2*self.xd[2]*self.d4 , 2*self.xd[2]*self.d2],   
                          [- d44*(1+alpha) , -betta*d44 , - self.xd[2]**2 + d44*(1-gamma) ]])

        int_alpha = interval(AA[0,0])*int_lnda2 + interval(AA[1,0])*int_lnda + interval(AA[2,0])
        int_betap = interval(AA[0,1])*int_lnda2 + interval(AA[1,1])*int_lnda + interval(AA[2,1])
        int_gamma = interval(AA[0,2])*int_lnda2 + interval(AA[1,2])*int_lnda + interval(AA[2,2])
    
        (alpha_l, alpha_h) = int_alpha[0]
        (betap_l, betap_h) = int_betap[0]
        (gamma_l, gamma_h) = int_gamma[0]

        Vp_1l = gen.solve_quadratic_inequality(- alpha_l, - betap_l, -gamma_l)
        Vp_1h = gen.solve_quadratic_inequality(  alpha_h,   betap_h,  gamma_h)
        Vn_1l = gen.solve_quadratic_inequality(- alpha_l, - betap_h, -gamma_l)
        Vn_1h = gen.solve_quadratic_inequality(  alpha_h,   betap_l,  gamma_h)

        V1 = (Vp_1l & Vp_1h & interval([0.0,1.0])) | (Vn_1l &  Vn_1h & interval([-1.0,0.0]))

        # Finding wh,wl:

        int_theta2 = interval([self.config.ql[2],self.config.qh[2]])
        int_w   = imath.sin(int_theta2)**2
        (wl, wh) = int_w[0]

        #Finding V2l, V2h

        V2l = gen.solve_quadratic_inequality(alpha + wl, betta, gamma - wl) & interval([-1.0, 1.0])
        V2h = gen.solve_quadratic_inequality(- alpha - wh, - betta, wh - gamma) & interval([-1.0, 1.0])

        #Finding V2

        V2 = V2l & V2h

        #Finding V3

        int_theta3 = interval([self.config.ql[3],self.config.qh[3]])
        V3         = imath.cos(int_theta3)

        #Finding V

        V = V3 & V2 & V1

        #Finding Ui

        denum = 2*self.a0*math.sqrt(r2)
        a     = R2/denum
        b     = 2*self.d2*self.d4/denum

        Phi1_3 = interval()
        nv = len(V)
        for i in range(0, nv):
            Ui = interval(a) - interval(b)*interval(V[i])
            (uli, uhi) = Ui[0]            

            zl = math.asin(uli)
            zh = math.asin(uhi)

            B1 = trig.standard_interval(zl - sai, zh - sai)
            B2 = trig.standard_interval(math.pi- zh - sai, math.pi- zl - sai)

            Phi1_3 = Phi1_3 | B1 | B2    

        #Finding P_phi

        Phi0 = interval([self.config.ql[0], self.config.qh[0]])

        Phi = gen.connect_interval(Phi0 & Phi1_3)

        return Phi



