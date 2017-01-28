from SimpleCV import *
import time
import os
import math
import sys
import cv2
#from imageInMem import im
import numpy as np

class VisionTargeting(object):

	def __init__(self, speed = 0.1):

		global display
		global ultraSonic_Dist 
		global text_FontSize
		global img

		img = cv2.imread('straight7.jpg')

		#CUSTOM COLOR CONSTANTS

		self.ultraSonic_Dist= 0 
		self.ultraSonic_Dist2 = 0
		self.text_FontSize = 15
		self.speed = speed

	
	def Loop(self):
		global text_FontSize
		global img
		global TARGET_WIDTH
		global TARGET_DISTANCE
		global imgorig
		global state

		state = True

		speed = self.speed
		print 'Loop Started'
		
		imgorig = img
		TARGET_WIDTH = 10.25
		TARGET_DISTANCE = 2.00

		while state: # Breaks loop if SimpleCV gui is exited

			img = imgorig
			hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
			lower_green = np.array([75,150,15])
			upper_green = np.array([95,255,60])
			mask = cv2.inRange(hsv, lower_green, upper_green)
			res = cv2.bitwise_and(img,img,mask=mask)
			cv2.imwrite('show.jpg', res)

			img = Image('show.jpg')
			green_target = img
			green_target = green_target.scale(720,480)
			#green_target = green_target.flipHorizontal()
			img_center = (green_target.width/2, green_target.height/2)

			try:	# If blobs are not found... program does not crash...prints "No target found" 

				blobs = green_target.findBlobs()

				## BLOB IDENTIFICATION + ASSIGNMENT
					
				BLOB_AREA = blobs[-1].area()

				top_LeftCorner = blobs[-1].topLeftCorner()
				top_RightCorner = blobs[-1].topRightCorner()
				bottom_LeftCorner = blobs[-1].bottomLeftCorner()
				bottom_RightCorner = blobs[-1].bottomRightCorner()

				top_LeftCorner2 = blobs[-2].topLeftCorner()
				top_RightCorner2 = blobs[-2].topRightCorner()
				bottom_LeftCorner2 = blobs[-2].bottomLeftCorner()
				bottom_RightCorner2 = blobs[-2].bottomRightCorner()


				tlc_List = list(top_LeftCorner)
				trc_List = list(top_RightCorner)
				blc_List = list(bottom_LeftCorner)
				brc_List = list(bottom_RightCorner)

				tlc_List2 = list(top_LeftCorner2)
				trc_List2 = list(top_RightCorner2)
				blc_List2 = list(bottom_LeftCorner2)
				brc_List2 = list(bottom_RightCorner2)

				if trc_List[0] < trc_List2[0]:
					boundingBox_length = abs(tlc_List[0] - trc_List2[0])
					boundingBox_width = abs(brc_List[1] - trc_List[1])
					print "blob on left"
				else:
					boundingBox_length = abs(tlc_List2[0] - trc_List[0])
					boundingBox_width = abs(brc_List2[1] - trc_List2[1])

				bb_size = (boundingBox_length ** 2) + (boundingBox_width ** 2) # a^2 + b^2 = c^2
				bb_size = sqrt(bb_size) #hypotenuse

				FOCAL_LENGTH = (BLOB_AREA * TARGET_DISTANCE) / TARGET_WIDTH
				print FOCAL_LENGTH
				actual_Distance = (TARGET_WIDTH * 753.658536585) / BLOB_AREA

				## DISTANCE FINDER

				self.ultraSonic_Dist = 549.295002708 / bb_size # PEGS DISTANCE 549 pixels for 1 foot 
				self.ultraSonic_Dist = round(self.ultraSonic_Dist, 2)

				adjusted_y = tlc_List[1] - 17
				adjusted2_y = tlc_List2[1] - 17        # Adjusted Y axis for text to show in a better location

				x_center = (brc_List2[0] - blc_List[0]) / 2
				x_center += blc_List[0]
				y_center = (blc_List[1] - tlc_List[1]) / 2
				y_center += tlc_List[1]
				target_center = (x_center, y_center)


				if tlc_List[0] < trc_List2[0]:
					x_center = (brc_List[0] - blc_List2[0]) / 2
					x_center += blc_List2[0]
					y_center = (blc_List2[1] - tlc_List2[1]) / 2
					y_center += tlc_List2[1]
					target_center = (x_center, y_center)


				blob_center = (blobs[-1].minRectX(), blobs[-1].minRectY())		  # Identify center of bounding box[-1]
				blob_center2 = (blobs[-2].minRectX(), blobs[-2].minRectY())       # Identify center of bounding box[-2]

				angle_OppSide = abs(240 - y_center)
				angle_AdjSide = abs(360 - x_center)
				angle_Tangent = float(angle_OppSide)/float(angle_AdjSide)
				angle_Tangent = math.atan(angle_Tangent)
				angle_Tangent = math.degrees(angle_Tangent)
				angle_Tangent = round(angle_Tangent, 2)

				if (250) > x_center:
					angle_Tangent -= (angle_Tangent * 2)

				real_dist = (.002416 * (self.ultraSonic_Dist ** 2) + (0.926 * self.ultraSonic_Dist) + 0.124) 
				real_dist = round(real_dist, 2)

			except Exception as e:
				print e
				print 'NoneType Error = No Blob found --- Else refer above'
				return '*008*Angle*%s*Distance*%s*' %(0,0)

			green_target.save('Output.png') # Overwrites last save
			time.sleep(speed) 
			print 'Loop Ran'
			print "Raw camera feed = %s" % self.ultraSonic_Dist
			os.remove('show.jpg')
			return '008*Angle*%s*Distance*%s*' % (angle_Tangent, real_dist) 


if __name__ == "__main__":
	VisionTargeting1 = VisionTargeting(0.1)
	print VisionTargeting1.Loop()





		

	
