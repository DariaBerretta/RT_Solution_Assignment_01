# Research Track 1: assignment n. 01
## Description of the assigment
In this assigment the robot have to move inside a map in anti-clockwise direction. 
As it moves it must avoid touching golden boxes, and when the robot encounters a silver token it should grab it, and move it behind itself.

## How to install and run the code
In order to run the code the simulator requires a Python 2.7 installation, the  [pygame](http://pygame.org/)  library,  [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and  [PyYAML](https://pypi.python.org/pypi/PyYAML/).

To run the script in the simulator, use `run.py`, passing it the file names, like this:

    python2 run.py s4642233_Daria_Berretta.py
    
## Peseudocode
In this pseudocode is described how the program should work, what are the decision and the action that the robot takes, and how it gets to take them.
```  
define an istance of the class Robot
define a constant to identify the visual cone for which the robot is aligned with a silver token
define a constant to identify the minimun distance necessary for grabbing a silver token
define a constant to identify the minimum possible distance between the robot and a golden token
define a constant to identify the angle of fov of the robot with golden token
define a constant to identify the angle of fov of the robot with silver token
define a constant to identify the offset for the fov of the robot when it have to look to right and left


def drive(speed,seconds):
	give to the two motors the same speed
	attend for the seconds indicates
	turn off the motors

def turn(speed,seconds)
	give to the two motors same speed but opposite
	attend for the seconds indicates
	turn off the motors
	
def find_token_silver():
	define distance as 100
	
	for each token in the map:
		define min. distance as 2
		
		if token is silver and it is inside of the fov of the robots [-45°,45°] and the distance of the token form the robot < min. distance:
			define distance as the distance of the token from the robot
			define an angle as the angle of disalignment of the robot from the token
		
	if no token are detected, so distnace is still 100:
		return -1, -1
	else:
		return the distance and the angle
		
def find_token_gold():
	define distance as 100
	
	for each token in the map:
		if token is gold and the distance of the token from the robot is < of distance:
			define distance as the distance of the token from the robot
			define an angle as the angle of disalignment of the robot from the token
	
	if no token are detected, so distnace is still 100:
		return -1, -1
	else:
		return the distance and the angle
		
def find_token_gold_FOV():
	define a distance for the right side as 100
	define a distance for the left side as 100
	
	the robot look at right so
	for each token in the map:
		if the token is gold and the token is inside the right fov of the robot [-90+offset°,-90-offset°] and the distance of the token from the robot is < of distance for the right:
		define the distance for the right side as the distance of the token from the robot
		
	the robot look at left so
	for each token in the map:
		if the token is gold and the token is inside the left fov of the robot [-90+offset°,-90-offset°] and the distance of the token from the robot is < of distance for the left:
		define the distance for the left side as the distance of the token from the robot
		
	
	if no token are detected, so the two distnace are still 100:
		return -1, -1
	else:
		return the distance for the right side and the distance for the left side
		
def grabbing():
	call the funcion grab
	turn the robot about 180°
	move the robot forward
	call the realise function
	move the robot backward
	turn the robot about 180° again
	
def align_to_border(orientation):
	if the parameter orientation is 0
		the robot has to turn to right
		so set a flag to 1
		
		while flag is 1:
			turn the robot to right
			compute his new angle with the function find_token_gold()
			if the angle is < -90°:
				put the flag to 0
	else:
		the robot has to turn to left
		so set a flag to 1
		
		while flag is 1:
			turn the robot to left
			compute his new angle with the function find_token_gold()
			if the angle is > 90°:
				put the flag to 0
				
def choose_corner(dist_r,dist_l)
	if the dist_r > dist_l:
		the robot turn to the right
	else:
		the robot turn to the left
		
def checker(angle):
	if angle is included within a visual cone of [-2°,2°]
		the robot is alligned to the target so return 0
		
	else if angle > 0:
		the robot has to turn clockwise
		and the function return 1
		
	else:
		the robot has to turn anti-clockwise
		and the function return 1
		
def drive_silver():
	compute the distance and the angle of the robot from a silver token with the function find_silver_token()
	
	define a flag as 1
	while flag is 1, whitch that means that the robot isn't align with the silver token:
		define flag as the return of the function checker wich take as parameter the angle
		recompute the distance and the angle
		
	if the distance is < of the minimum distance necessary for grabbing a silver token:
		call the function to grab a silver token
	else:
		drives the robot forward
		
def avoid_gold():
		compute the distance and the angle of the robot from the closer golden token with the function find_token_gold()
		
		if the distance is < of the minimum possible distance between the robot and a golden token:
			if the angle is within the robot's fov specific to golden tokens [-45°.45°]:
				the robot makes a decision between turning left or right
				compute the distance between the robot and his most closer golden token to the left and right with the function find_token_gold_FOV.
				Depending on the return of the two distance the robot take a decision with the function choose_corner, whitch takes in input the two distance.
			
			else if the angle is within [-90°,-45°]:
				the robot turns clockwise until it reaches -90 degrees using the allign_to_border function
			else if the angle is within [45°,90°]:
				the robot turns anti-clockwise until it reaches 90 degrees using the allign_to_border function

def check_silver_token():
	compute the distance and the angle of the robot from a silver token with the function find_silver_token()
	if the distance or the angle as a value different from -1:
		call the function drive_silver() to reach the silver token
	 	

def main():
	while(1):
		avoid golden token
		drive forward
		serch for silver token on the way
		
call to the main function 
```
## Code details
In order to allow the robot to move as smoothly as possible, precise functions have been developed in the code.
Clearly the main task of the robot is to avoid the 'walls of the map', i.e. the golden tokens. 
Precisely for this purpose it was necessary to develop two functions that allow the robot to make a choice in the event that it has to make a curve, which means that
the robot is in front of a corner.
```Python
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
```
Other important aspects for a fluid movement were:
- the distance to be kept from the walls
- when to start looking for silver tokens
- how to grab and release silver tokens

All these aspects required the definition of specific constants and dedicated parts of code within the functions.
## Authors
Daria Berretta
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTQyMDMyODcyOCw3Nzc5NjY3MjMsNzU1NT
AwNTI1LDEwMzIxNzA0NTksNzU1NTAwNTI1LDEyMzE2NzAxODMs
LTEzMjE0NzczMSwyMDczMjA0NDk1XX0=
-->
