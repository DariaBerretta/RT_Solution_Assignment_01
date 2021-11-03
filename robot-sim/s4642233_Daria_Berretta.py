from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: minimum distance necessary for grabbing a silver token"""

R = Robot()
""" instance of the class Robot"""

fov_gold = 45
""" angle of fov of the robot with golden token"""

fov_silver = 45
""" angle of fov of the robot with silver token"""

offset = 10
"""offset for the fov of the robot when it have to look to right and left"""

min_d=0.7
"""minimum possible distance between the robot and a golden token"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
def find_token_silver():
	
	#Funcion to locate silver tokens
	#In this funcion the robot's field of view is limited
	#to a cone of 90 degrees of amplitude -45 degrees,45 degrees
	#It returns the distance and the angle from the closer token 
	    
    dist=100
    for token in R.see():
		min_dist = 2
		
		if token.info.marker_type == 'silver-token' and token.rot_y > -fov_silver and token.rot_y < fov_silver and token.dist < min_dist:
			dist=token.dist
			rot_y=token.rot_y
            
	#if no tokens are present
    if dist==100:
		return -1, -1
    else:
		return dist, rot_y
   	
def find_token_gold():
	
	#Funcion to locate golden tokens
	#In this funcion the robot's field of view is unlimited
	#It returns the distance and the angle from the closer token 
   
    dist=100
    for token in R.see():
        if token.info.marker_type == 'gold-token' and token.dist < dist:
            dist=token.dist
            rot_y=token.rot_y
	    
	#in no tokens are present
    if dist==100:
		return -1, -1
    else:
		return dist, rot_y
   	
def find_token_gold_FOV():
	
	#Funcion to locate the farther golden token
	#In this funcion the robot's field of view is limited
	#to a cone of 20 degrees of amplitude to the right and left
	#It returns the distance from the closer token to the right and 
	#the closer token to the left 
   
    dist_r=100
    dist_l=100
    
    #look right
    for token in R.see():
        if token.info.marker_type == 'gold-token' and token.rot_y >= (90-offset) and token.rot_y <= (90+offset) and token.dist < dist_r:
            dist_r=token.dist
    
    #look left       
    for token in R.see():
        if token.info.marker_type == 'gold-token' and token.rot_y >=-(90+offset) and token.rot_y <=-(90-offset) and token.dist < dist_l:
            dist_l=token.dist
	    
	#inf no tokens are present
    if dist_r==100 or dist_l==100:
		return -1, -1
    else:
   		return dist_r, dist_l
   		
   	
def drive_silver():
	#The function compute the distance and the angle from the closer
	#silver token. Then if the robot is not aligned provides to do that.
	#With a control on the distance the function decide if the robot
	#can grab the token or if it have to get close to it

	distance, angle = find_token_silver()
	
	flag = 1
	while(flag):
		#call to the function to align the robot to the token 
		flag=checker(angle)
		distance, angle = find_token_silver()
		
	if distance < d_th:
		#if the distance is small enough
		#the robot grab the token
		grabbing()
		print('grabbing token')
	else:
		#otherwise it moves forward
		drive(80,0.05)
		#print('go on')
		
def grabbing():
	#belong to the silver's routine
	#The robot grabs the token and realese it behind him
	R.grab()
	turn(60,1)
	drive(20,1)
	R.release()
	drive(-20,1)
	turn(-60,1)

def avoid_gold():
	#robot routine to avoid touching the golden tokens
	
	distance, angle = find_token_gold()
	
	if distance < min_d:
		
		if angle >= -fov_gold and angle <= fov_gold :
			#took decision for marking the curve
			print("took decision for the curve")
			dist_r, dist_l = find_token_gold_FOV()
			print(dist_r,dist_l)
			choose_corner(dist_r,dist_l)
			
		elif angle >=-90 and angle<-fov_gold:
			# turn clockwise until angle -90
			allign_to_border(0)
			
			
		elif angle>fov_gold and angle <=90:
			# turn anti-clockwise until angle 90
			allign_to_border(1)
			
			#else:
			# angle [90,180] or [-180,-90]
			# do nothing

def allign_to_border(orientation):
	# The function realign the robot to avoid
	# the golden token
	
	# orientation = 0-> the robot must turn clockwise
	# orientation = 1-> the robot must turn anti-clockwise
	
	if orientation == 0:
		#realignment to right
		print("realignment to right")
		flag = 1
		while(flag):
			turn(20,0.05)
			distance,angle = find_token_gold()
			if angle < -90:
				flag=0
	else:
		#realignment to left
		print("realignment to left")
		flag = 1
		while(flag):
			turn(-20,0.05)
			distance,angle = find_token_gold()
			if angle > 90:
				flag=0
				
def choose_corner(dist_r,dist_l):
	#head for the farthest distance
		if dist_r > dist_l:
			# turn cloclwise
			print("choose right")
			turn(30,1)
		else:
			# turn anti-clockwise
			print("choose left")
			turn(-30,1)

def check_silver_token():
	#robot routine to move the silver tokens it encounters
	distance, angle = find_token_silver()
	
	if distance != -1 or angle != -1:
		#get silver token
		print("see silver token")
		drive_silver()
	#else nothing
	
def checker(angle):
	#belong to the silver's routine
	#The function checks that the robot is aligned,
	#otherwise it takes care of aligning it 
	if angle > -a_th and angle < a_th:
		print('Robot aligned')
		return 0
		
	elif angle > 0:
		print('clockwise turn')
		turn(20,0.05)
		return 1
		
	else:
		print('anti-clockwise turn')
		turn(-20,0.05)
		return 1
			

#main code
def main():

	while(1):
		avoid_gold()
		drive(60,0.1)
		check_silver_token()

#call to main funcion	
main()
