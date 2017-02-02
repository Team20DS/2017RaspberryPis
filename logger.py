import datetime

def write_log():

	now = datetime.datetime.now()

	hour = now.hour
	minute = now.minute
	second = now.second

	log_name = "%sH.%sM.%sS" %(hour, minute, second)

	file = open('logs/{0}.txt'.format(log_name), 'w') 

	file.write("---------------------------")
	file.write("Raw Angle to Target : %s") %angle_Tangent
	file write("Raw Distance to Target : %s\n") %actual_Distance
	file.write("First Turn to Target : %s") %first_Turn
	file.write("First Distance to Target : %s") %first_Distance
	file.write("Second Turn to Target : %s") %second_Turn
	file.write("Second Distance to Target : %s") %second_Turn
	file.write("------------------------------")

	file.close()

