import datetime
import os

def write_log():

	now = datetime.datetime.now()

	if not os.path.exists('/logs'):
		print 'Folder not made'
	else: 
		print 'Folder made'
		os.makedirs('logs')	

	hour = now.hour
	minute = now.minute
	second = now.second

	log_name = "%sH.%sM.%sS" %(hour, minute, second)

	file = open('logs/{0}.txt'.format(log_name), 'w') 

	file.write("---------------------------\n")
	file.write("Raw Angle to Target : %s \n" %angle_Tangent) 
	file.write("Raw Distance to Target : %s \n" %actual_Distance) 
	file.write("First Turn to Target : %s \n" %first_Turn) 
	file.write("First Distance to Target : %s \n" %first_Distance) 
	file.write("Second Turn to Target : %s \n"  %second_Turn)
	file.write("Second Distance to Target : %s \n" %second_Distance) 
	file.write("------------------------------")

	file.close()