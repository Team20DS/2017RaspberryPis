from SimpleCV import *
import time
import os
import math
import sys
import cv2
import numpy as np
import io
from PIL import Image as img
import picamera

class VisionTargeting(object):

        def __init__(self, speed = 0.1):

                global display
                global ultraSonic_Dist 
                global text_FontSize
                global img
                global sentence
                self.angle = 0
                self.distance = 0
                
                display = Display()
                

                #CUSTOM COLOR CONSTANTS

                self.ultraSonic_Dist= 0
                self.text_FontSize = 15
                self.speed = speed
                
        
        def Loop(self):
                global text_FontSize
                global img
                global TARGET_WIDTH
                global TARGET_DISTANCE
                global imgorig
                global firstTurn
                global secondTurn
                global sentence

                speed = self.speed
                print 'Loop Started'

                
                #imgorig = cv2image
                TARGET_HEIGHT = 5
                TARGET_DISTANCE = 2.00
                CAMERA_OFFSET = 7.5
                firstTurn = 0
                secondTurn = 0

                while display.isNotDone(): # Breaks loop if SimpleCV gui is exited
                        stream = io.BytesIO()
                        with picamera.PiCamera() as camera:
                                camera.start_preview()
                                time.sleep(.1)
                                camera.brightness = 5
                                #camera.awb_mode = 'off'
                                camera.capture(stream,format='jpeg')
                        stream.seek(0)
                        image = img.open(stream)
                        image = Image(image)
                        
                        angle_Tangent = 0
                        apparentZ = 0
                        real_dist = 0
                        firstDistance = 0
                        first_Turn = 0
                        secondDistance = 0
                        adjacent = 0
                        actual_Distance = 0
                        
                        actual_img = image
                        cv2image = actual_img.getNumpyCv2()
                        actual_img = cv2image
                        cv2.imwrite('test.jpg', actual_img)
                        hsv = cv2.cvtColor(actual_img, cv2.COLOR_BGR2HSV)
                        lower_green = np.array([45,20,15])
                        upper_green = np.array([95,255,60])
                        mask = cv2.inRange(hsv, lower_green, upper_green)
                        res = cv2.bitwise_and(actual_img,actual_img,mask=mask)

                        actual_img = Image(res.transpose(1,0,2)[:,:,::-1])
                        green_target = actual_img
                        green_target = green_target.scale(720,480)
                        img_center = (green_target.width/2, green_target.height/2)

                        try:    # If blobs are not found... program does not crash...prints "No target found" 

                                blobs = green_target.findBlobs()

                                ## BLOB IDENTIFICATION + ASSIGNMENT

                                blobs[-1].drawMinRect(color=Color.RED, width = 1, alpha = 128)
                                blobs[-2].drawMinRect(color=Color.RED, width = 1,  alpha = 128)
                                        


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

                                blobs_height = brc_List[1] - trc_List[1]
                                #print 'height%s' %blobs_height

                                if trc_List[0] < trc_List2[0]:
                                        boundingBox_length = abs(tlc_List[0] - trc_List2[0])
                                        print "blob on left"
                                else:
                                        boundingBox_length = abs(tlc_List2[0] - trc_List[0])

                                blobs_length = boundingBox_length

                                bb_size = (blobs_height ** 2) + (boundingBox_length ** 2) # a^2 + b^2 = c^2
                                bb_size = sqrt(bb_size) #hypotenuse

                                BLOB_HEIGHT = blobs_height
                                FOCAL_LENGTH = (BLOB_HEIGHT * TARGET_DISTANCE) / TARGET_HEIGHT
                                FOCAL_LENGTH = 600.75 #573
                                actual_Distance = (TARGET_HEIGHT * FOCAL_LENGTH) / BLOB_HEIGHT
                                
                                ## DISTANCE FINDER

                                #self.ultraSonic_Dist = 549.295002708 / bb_size # PEGS DISTANCE 549 pixels for 1 foot 
                                #actual_Distance = round(self.ultraSonic_Dist, 2)
                                #actual_Distance = actual_Distance * 12
                                #print actual_Distance

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


                                blob_center = (blobs[-1].minRectX(), blobs[-1].minRectY())                # Identify center of bounding box[-1]
                                blob_center2 = (blobs[-2].minRectX(), blobs[-2].minRectY())       # Identify center of bounding box[-2]

                                center_off = abs(360 - x_center)
                                angle_Tangent = 66 * center_off
                                angle_Tangent_off = angle_Tangent / 720

                                angle_off = 7.5/actual_Distance
                                angle_Tangent = atan(angle_off)
                                angle_Tangent = math.degrees(angle_Tangent)
                                angle_Tangent = abs(angle_Tangent - angle_Tangent_off)
                                angle_Tangent = round(angle_Tangent, 2)

                                real_dist = (.002416 * (actual_Distance ** 2) + (0.926 * actual_Distance) + 0.124) 
                                real_dist = round(real_dist, 2)

                                firstTurn = (angle_Tangent * 2)
                                
                                self.ultraSonic_Dist = math.cos(math.radians(angle_Tangent)) * actual_Distance
                                adjacent = round(self.ultraSonic_Dist, 2)

                                firstDistance = adjacent/(math.cos(math.radians(firstTurn)))
                                firstDistance = round(firstDistance, 2)
                                firstDistance = firstDistance - actual_Distance
                                firstDistance = round(firstDistance, 2)

                                secondTurn = abs(180 - 90 - firstTurn)
                                secondTurn = 90 - secondTurn
                                secondTurn = round(secondTurn, 2)
                                #print 'secondTurn%s : ' %secondTurn

                                if (360) > x_center:
                                        angle_Tangent -= (angle_Tangent * 2)

                                secondDistance = actual_Distance - firstDistance
                                secondDistance = round(secondDistance, 2)

                                # DRAWING LAYERS

                                green_target.dl().selectFont('consolas')
                                green_target.dl().circle((blob_center), 4, color = Color.BLUE)  # Bounding BOX Center Circle - BLUE
                                green_target.dl().circle((blob_center2), 4, color = Color.YELLOW)  # Bounding BOX Center Circle - BLUE
                                green_target.dl().circle((img_center), 2, color = Color.YELLOW) # Image Center Circle - YELLOW
                                #green_target.drawText(text = str(self.ultraSonic_Dist) + " ft", x = tlc_List[0], y = adjusted_y, color = Color.WHITE, fontsize = self.text_FontSize) #Draws distance text for biggest blob
                                #green_target.drawText(text = str(self.ultraSonic_Dist2) + " ft", x = tlc_List2[0], y = adjusted2_y, color = Color.WHITE, fontsize = self.text_FontSize) #Draws distance text for second small blob
                                green_target.dl().circle((target_center), 3, color = Color.RED) #Draws a circle at center of 2 targets, represents peg location
                                green_target.dl().line((target_center), (img_center), color = Color.RED, width = 1) # Draws the hypotenuse
                                #green_target.dl().line((0,250), (500,250), color = Color.WHITE, width = 1) # Draws x axis
                                #green_target.dl().line((250,0), (250, 500), color = Color.WHITE, width = 1) # Draws y axis
                                green_target.dl().line((target_center), (x_center, 240), color = Color.RED, width = 1) # Opposite Side
                                green_target.dl().line((x_center, 240), (360,240), color = Color.RED, width = 1) # Adjacent Side
                                green_target.drawText(text = str(angle_Tangent) + "", x = 255, y = 250, color = Color.WHITE, fontsize = self.text_FontSize)

                        except Exception as e:
                                print e
                                print 'NoneType Error = No Blob found --- Else refer above'
                                pass
                                #return '*008*Angle*%s*Distance*%s*' %(0,0)

                        #green_target.save('Output.png') # Overwrites last save
                        green_target.show()
                        time.sleep(speed) 
                        print 'Loop Ran'
                        self.angle = angle_Tangent
                        self.distance = actual_Distance
                        return '008*FirstAngle*%s*SecondTurn*%s*FirstDistance*%s*SecondDistance*%s*' % (firstTurn, secondTurn, firstDistance, secondDistance)

        def getAngle(self):
                return "%s" %self.angle
        def getDistance(self):
                self.distance = round(self.distance,2)
                return "%s" %self.distance


if __name__ == "__main__":
        VisionTargeting1 = VisionTargeting(0.1)
        VisionTargeting1.Loop()
        print VisionTargeting1.getAngle()
        print VisionTargeting1.getDistance()




1
                

        
