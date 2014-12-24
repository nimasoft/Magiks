'''   Header
@file:          trajectory.py
@brief:    	    This module provides a class containing a trajectory in the taskspace.
                The trajectory is generated by a number of key points containing poses, twists and corresponding phase phi
                
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
@version:	    1
Last Revision:  04 June 2014

'''

import matplotlib.pyplot as plt
import numpy as np
import copy, math

# from packages.nima.mathematics import vectors_and_matrices as vm
from packages.nima.mathematics import polynomials as pl
from packages.nima.mathematics import general as gen


class Trajectory(object):
    
    def __init__(self):
        self.n = 1  # Number of keypoints. By default the trajectory is a constant pose (not changing)
        self.current_phi = 0
        self.current_position = np.zeros(3)
        self.current_velocity = np.zeros(3)
        self.current_acceleration = np.zeros(3)
        self.current_orientation = np.eye(3)
        self.current_angular_velocity = np.zeros(3)
        self.current_angular_acceleration = np.zeros(3)

    def interpolate(self, phi = [0.0], positions = [np.zeros(3)], orientations = None, velocities = None, angular_velocities = None, accelerations = None, angular_accelerations = None):
        '''
        specifies the coefficients of the trajectory which passes through a number of poses
        At the moment, orientations, angular velocities and angular accelerations are not supported.
        At least one position and one phi is required.
        phi[0] must be zero.
        '''
        n = len(positions)
        assert n > 0
        assert n == len(positions)
        assert phi[0] == 0.0

        for i in range(n):
            if positions[i] == None:
                positions[i] = np.array([None, None, None])

        if velocities == None:
            velocities = [np.array([None, None, None]) for i in range(n)]
        else:
            assert n == len(velocities)
            for i in range(n):
                if velocities[i] == None:
                    velocities[i] = np.array([None, None, None])

        if accelerations == None:
            accelerations = [np.array([None, None, None]) for i in range(n)]
        else:
            assert n == len(accelerations)
            for i in range(n):
                if accelerations[i] == None:
                    accelerations[i] = np.array([None, None, None])

        pnt_x = []
        pnt_y = []
        pnt_z = []

        for i in range(n):
            pnt_x.append(pl.Point(t = phi[i], x = positions[i][0], v = velocities[i][0], a = accelerations[i][0]))
            pnt_y.append(pl.Point(t = phi[i], x = positions[i][1], v = velocities[i][1], a = accelerations[i][1]))
            pnt_z.append(pl.Point(t = phi[i], x = positions[i][2], v = velocities[i][2], a = accelerations[i][2]))

        self.traj_x = pl.Polynomial()
        self.traj_y = pl.Polynomial()
        self.traj_z = pl.Polynomial()

        self.traj_x.interpolate_smart(pnt_x)
        self.traj_y.interpolate_smart(pnt_y)
        self.traj_z.interpolate_smart(pnt_z)

    def set_phi(self, phi):
        self.current_phi = phi
        self.current_position[0] = self.traj_x.position( t = phi )
        self.current_position[1] = self.traj_y.position( t = phi )
        self.current_position[2] = self.traj_z.position( t = phi )

        self.current_velocity[0] = self.traj_x.velocity( t = phi )
        self.current_velocity[1] = self.traj_y.velocity( t = phi )
        self.current_velocity[2] = self.traj_z.velocity( t = phi )

        self.current_acceleration[0] = self.traj_x.acceleration( t = phi )
        self.current_acceleration[1] = self.traj_y.acceleration( t = phi )
        self.current_acceleration[2] = self.traj_z.acceleration( t = phi )

# Special Trajectories


    
class Colin_Graf_Trajectory(object):
    '''
    A one dimensional trajectory based on paper written by Colin Graf et.al. 2009
    "A Robust Closed-Loop Gait for the Standard Platform League Humanoid" 
    Proceedings of the 4th Workshop on Humanoid Soccer Robots
    '''
    def __init__(self, xl = 0.22, yl=0.55, xm=0.22, ym=0.55, h=30.0, dx=0.0, dy=120.0, Ol=np.array([-55,25,-385]), Or=np.array([55,25,-385]), Cs=np.zeros(3), Ss=np.array([20.0,0.0,0.0])):
        self.xl  = xl
        self.yl  = yl
        self.xm  = xm
        self.ym  = ym
        self.h   = h
        self.dx  = dx
        self.dy  = dy
        self.Ol  = Ol
        self.Or  = Or
        self.Cs  = Cs
        self.Ss  = Ss
        
    def tl_lift(self, phi):
        if (2*phi > self.xl) and (2*phi < self.xl + self.yl):
            return 0.5*(1.0- math.cos(2*math.pi*(2*phi-self.xl)/self.yl))
        else:
            return 0.0

    def tr_lift(self, phi):
        return self.tl_lift(phi-1)

    def tl_move(self, phi):
        if (2*phi > self.xm) and (2*phi < self.xm + self.ym):
            return 0.5*(1.0- math.cos(math.pi*(2*phi-self.xm)/self.ym))
        elif (2*phi >= self.xm + self.ym) and (2*phi <= 1.0):
            return 1.0
        else:
            return 0.0

    def tr_move(self, phi):
        return self.tl_move(phi-1)
            
    def tl(self, phi):
        if phi < 0.5:
            return 0.5*(1.0 - math.cos(2.0*math.pi*phi))
        else:
            return 0.0

    def tr(self, phi):
        if phi >= 0.5:
            return 0.5*(1.0 - math.cos(2.0*math.pi*(phi-0.5)))
        else:
            return 0.0

    def t_com(self, phi):    
        def ss(t):
            return math.sin(2*math.pi*t)
        def rr(t):
            s = ss(t)
            return math.sqrt(abs(s))*gen.sign(s)
        def ll(t):
            if (t < 0.25):
                return 4*t
            elif (t >= 0.25) and (t < 0.75):
                return 2 - 4*t
            else:
                return 4*(t - 1)
        xc = 20.0
        yc = 50.0
        zc = 2.0
        return (xc*ss(phi) + yc*rr(phi) + zc*ll(phi))/(xc + yc + zc)

    def t_lin(self, phi):
        if (phi < 0.5):
            return 2*phi
        else:
            return 2*phi - 1.0

    def pl_rel(self, phi):
        sl_lift = np.array([0.0, 0.0, self.h])
        sl      = np.array([self.dx, self.dy, 0.0])
        sr      = sl
        if (phi < 0.5):
            return self.Ol + sl_lift*self.tl_lift(phi) + sl*self.tl_move(phi) + sr*(1.0 - self.tl_move(phi))*self.tl(phi)
        else:
            return self.Ol + sl_lift*self.tl_lift(phi) + sl*(1.0 - self.tr(phi))
             
    def pr_rel(self, phi):
        sr_lift = np.array([0.0, 0.0, self.h])
        sl      = np.array([self.dx, self.dy, 0.0])
        sr      = sl 
        if (phi >= 0.5):
            return self.Or + sr_lift*self.tr_lift(phi) + sr*self.tr_move(phi) + sl*(1.0 - self.tr_move(phi))*self.tr(phi)
        else:
            return self.Or + sr_lift*self.tr_lift(phi) + sr*(1.0 - self.tl(phi))

    def pl_com(self, phi):
        sl      = np.array([self.dx, self.dy, 0.0])
        sr      = sl
        if (phi < 0.5):
            return - self.Cs + self.Ss*self.t_com(phi) + self.Ol - 0.5*(sl*self.t_lin(phi) - sr*(1.0 - self.t_lin(phi)))
        else:
            return self.pr_com(phi) - self.pr_rel(phi) + self.pl_rel(phi)

    def pr_com(self, phi):
        sl      = np.array([self.dx, self.dy, 0.0])
        sr      = sl
        if (phi >= 0.5):
            return - self.Cs + self.Ss*self.t_com(phi) + self.Or - 0.5*(sr*self.t_lin(phi) - sl*(1.0 - self.t_lin(phi)))
        else:
            return self.pl_com(phi) - self.pl_rel(phi) + self.pr_rel(phi)
    
    def plot(self, wtp = 'pl_com_x', n = 100):
        '''
        wtp (what to plot) is a string indicating which trajectory to be plotted
        n specifies how many points need to be created in the trajectory function domain
        '''
        x = np.arange(0.0, 1.0, 1.0/n)
        y = copy.copy(x)
        for i in range(n):
            if wtp == 'pl_com_x':
                y[i] = self.pl_com(x[i])[0]
            elif wtp == 'pl_com_y':
                y[i] = self.pl_com(x[i])[1]
            elif wtp == 'pl_com_z':
                y[i] = self.pl_com(x[i])[2]
            elif wtp == 'pr_com_x':
                y[i] = self.pr_com(x[i])[0]
            elif wtp == 'pr_com_y':
                y[i] = self.pr_com(x[i])[1]
            elif wtp == 'pr_com_z':
                y[i] = self.pr_com(x[i])[2]
            elif wtp == 'pl_rel_x':
                y[i] = self.pl_rel(x[i])[0]
            elif wtp == 'pl_rel_y':
                y[i] = self.pl_rel(x[i])[1]
            elif wtp == 'pl_rel_z':
                y[i] = self.pl_rel(x[i])[2]
            elif wtp == 'pr_rel_x':
                y[i] = self.pr_rel(x[i])[0]
            elif wtp == 'pr_rel_y':
                y[i] = self.pr_rel(x[i])[1]
            elif wtp == 'pr_rel_z':
                y[i] = self.pr_rel(x[i])[2]
            elif wtp == 'tl_lift':
                y[i] = self.tl_lift(x[i])
            elif wtp == 'tr_lift':
                y[i] = self.tr_lift(x[i])
            elif wtp == 't_com':
                y[i] = self.t_com(x[i])
            elif wtp == 'tl_move':
                y[i] = self.tl_move(x[i])
            elif wtp == 'tr_move':
                y[i] = self.tr_move(x[i])
            elif wtp == 'tr':
                y[i] = self.tr(x[i])
            elif wtp == 'tl':
                y[i] = self.tl(x[i])

        plt.plot(x, y) 
        plt.ylabel(wtp)
        plt.xlabel('phi')
        plt.show()

                
