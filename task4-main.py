'''
*Team Id:            132
*Author List:        T.Lokesh, A.R.Phani Kumar, K.Deva Kishore, P.H.Bharadwaj
*
*Filename:           task4-main.py
*Theme:              PLANTER BOT - eYRC specific
*Functions:          main, blink_led, straight, left, right, sharp_left, sharp_right, outside, blend, read_csv
*Global Variables:   flag, zi, flag2, fr_cnt, a, RED,GREEN,BLUE, mtr_right, mtr_left

'''

import numpy as np 
import os
import csv
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import RPi.GPIO as GPIO
from time import sleep
import subprocess
frm_cnt=0
GPIO.setwarnings(False)  
GPIO.setmode(GPIO.BOARD)  
Motor1A = 33
Motor1B = 35
Motor1E = 37
Motor2A = 36
Motor2B = 38
Motor2E = 40
RED = 21
GREEN = 15
BLUE = 19
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)
GPIO.setup(RED,GPIO.OUT)
GPIO.setup(GREEN,GPIO.OUT)
GPIO.setup(BLUE,GPIO.OUT)
GPIO.output(Motor2A,GPIO.LOW) 
GPIO.output(Motor2A,GPIO.LOW) 
GPIO.output(Motor2A,GPIO.LOW)
mtr_right = GPIO.PWM(Motor1E, 10)
mtr_left = GPIO.PWM(Motor2E, 10)
flag=0
flag2=0
fr_cnt=0
zi=1
'''
*Function Name:     main
*Input:             None
*Output:            None
*Logic:             The entire processing of the theme takes place in this function .
*                   Settting up picamera, analysis the input image and calling the corressponding function as per the result of the image processing of the input  *                   frame, Checking for the color markers and shape of th same and then calling the appopriate function for reading csv file and blending * 
*                   accordingly.  The logic used to follow line is to find the centroid of the largest contour and then check the region of the centroid in the
*                   frame so that the robot moves depending on the region of the centroid w.r.t frame.
*Example:           main()


'''
def main():
  a=5
  led=[0]*5
  #plant_img = cv2.imread('Plantation.png')
  #cv2.imshow('plantation_image',plant_img)
  global flag,zi,flag2,fr_cnt,imgSrc
  are=0
  stop_flag = 0
  cam = PiCamera()
  cam.resolution = (200,200)
  #cam.framerate =5
  raw_cap = PiRGBArray(cam,(200,200))
  #frm_cnt= 0 
  #sleep(2)
  imgSrc = cv2.imread('Plantation.png')
  cv2.imshow('plantation_image',imgSrc)
  pts1 = np.float32([[72,41],[259,27],[30,206],[300,199]]) # [[48,29],[560,32],[12,359],[580,360]]
  pts2 = np.float32([[0,0],[640,0],[0,480],[640,480]])
  for frame in cam.capture_continuous(raw_cap,format="bgr",use_video_port=True,splitter_port=2,resize=(200,200)):  
     ar=0
     global imgSrc
     count=0  
     frame = frame.array
     crop_img = frame[:,:]
     lower = (0,0,80)  
     upper = (180,255,255)
     if flag==1:
         fr_cnt+=1
     imgHSV= cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
     imgHSV2= imgHSV.copy()
     blur = cv2.blur(crop_img,(5,5))
     blur = cv2.GaussianBlur(blur,(5,5),0)
     thresh = cv2.inRange(imgHSV,lower,upper)
     #cv2.imshow('thresh',thresh)
     kernel = np.ones((5,5),np.uint8) 
     thresh1= cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
     thresh2= cv2.morphologyEx(thresh1, cv2.MORPH_CLOSE, kernel)
     _,contours,hierachy = cv2.findContours(cv2.bitwise_not(thresh2),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
     if len(contours) > 0 :
         ct = cv2.countNonZero(thresh)
         ratio = ct/float(200*200)
         #print ratio
         #print ' ratio: '+str(r)
         '''
         if ratio <0.35 and zi >6:
              _,contours,hierachy = cv2.findContours(thresh2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
              #stop_flag = 1
         '''
         c = max(contours, key=cv2.contourArea)
         M = cv2.moments(c)         
         area=cv2.contourArea(c)
         #print 'area= ',area
         try:

            cx = int(M['m10']/M['m00'])
 
            cy = int(M['m01']/M['m00'])
         except:
            pass
         #print zi
         '''if flag ==1 and flag2 == 0 and fr_cnt == 3 and ratio > 0.6 and stop_flag ==1:
               stop()
               last_blink(led)
               print 'completed task'
               #return
         '''
         if flag ==1 and flag2 == 0 and fr_cnt == 1  and ratio > 0.6 and stop_flag == 0 and zi>2 :
           flag2=1
           stop()
           sleep(0.5)
           if zi == 3:
               blink_led('RED',2)
               read_csv('RED','Circle',2,(zi-2))
           if zi == 4:
               blink_led('BLUE',2)
               read_csv('BLUE','Circle',2,(zi-2))
           if zi == 5:
               blink_led('RED',4)
               read_csv('RED','Triangle',4,(zi-2))
           if zi == 6:
               blink_led('GREEN',4)
               read_csv('GREEN','Triangle',4,(zi-2))
           '''if zi == 7:
               last_blink(['BLUE','RED','RED','GREEN','NONE'])
           '''
           sleep(2)
         else:
           pass
         #print area
         #print zi
         if zi>90:
             stop()
             last_blink(['RED','BLUE','RED','GREEN','NONE'])
             cv2.imshow('blended_output',imgSrc)
             #command = "/usr/bin/sudo /sbin/shutdown -h now"
             #process = subprocess.Popen(command.split(),stdout = subprocess.PIPE)
             sleep(100)
         if zi>6:
            zi+=1
         #print area
         if area>8000 and area< 15000 and flag is 0:
           #stop()
           #print 'Got ZI'
           flag=1
           fr_cnt = 0
           zi+=1
           raw_cap.truncate(0)
           continue
         if area < 5000 and fr_cnt >= 13:
            flag = 0
            flag2=0
     
         cv2.line(crop_img,(cx,0),(cx,200),(255,0,0),1)
 
         cv2.line(crop_img,(0,cy),(200,cy),(255,0,0),1)
         cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)  
         if cy<160 or zi == 1 :
          if cx <=40:
               left()
          if (cx >40 and cx < 160) :
               straight()
          if cx >= 160:
               right()
         if cy>160 and zi>1:
             if cx>=100:
                sharp_right()
             if cx<100:
                 sharp_left()    
                          
   
     else:
               outside(a)
     #cv2.imshow('frame',crop_img)
     raw_cap.truncate(0)
     if cv2.waitKey(1) & 0xFF == ord('q'):
         GPIO.cleanup()
         break
  cv2.destroyAllWindows()


'''
*Function Name:      blink_led
*Input:              led_colour  ->  The led_colour is the parameter which inputs the colour of led to blink 
*                    n          ->  gives number of times to blink depenidng
*                    on the number and colour of the color_markers at the Zone Indicator(ZI).
*Output:             None
*Logic:              This function is dedicated for RGB_LED blinking at the Zone Indicators if any colour markers are detected and is performed by simple GPIO
*                    operations of the Raspberry Pi.
*Example Call:       blink_led('RED',3)  
'''   
def blink_led(led_colour,n):
    global RED,GREEN,BLUE
    if n > 4:
       n = 4 
    if led_colour is 'RED':
     for l in range(0,n):
       GPIO.output(RED,GPIO.HIGH)
       sleep(1)
       GPIO.output(RED,GPIO.LOW)
       sleep(1)
     
    elif led_colour is 'GREEN':
     for l in range(0,n):
       GPIO.output(GREEN,GPIO.HIGH)
       sleep(1)
       GPIO.output(GREEN,GPIO.LOW)
       sleep(1)
    elif led_colour is 'BLUE':
     for l in range(0,n):
       GPIO.output(BLUE,GPIO.HIGH)
       sleep(1)
       GPIO.output(BLUE,GPIO.LOW)
       sleep(1)
     
'''
*Function Name:     straight
*Input:             None
*Output:            None
*Logic:             The function moves the robot in a straight path. There being a mismatch in the speeds of both motors, So we have used PWM to make the robot 
*                   move in a straight line, and the PWM values are found out by trail and error method. This function is called by the main() function whenever 
*                   the centroid of the black line is in the centre or near to the mid region of the input frame. 
*Example Call:      staight()
'''
        
def straight():
     a=0
     global mtr_right  #########   left 20 and right 60 at high charging and  left 35 and right 70  at low charging of  Li- ion battetry 
     global mtr_left
     mtr_left.start(0)
     mtr_right.start(0)
     GPIO.output(Motor1A,GPIO.HIGH)
     GPIO.output(Motor1B,GPIO.LOW)
     mtr_left.ChangeDutyCycle(20)  
     GPIO.output(Motor2A,GPIO.HIGH) 
     GPIO.output(Motor2B,GPIO.LOW)
     mtr_right.ChangeDutyCycle(40)
     return

'''
*Function Name:      right 
*Input:              None
*Output:             None
*Logic:              The function turns the Planter_Bot right side. This function is called by the main() function whenever the centroid of the black line is at 
*                    the rightmost end of the input frame. The bot can be turned towards right by stopping the right motor and running the left motor forward or an*                    even larger radius turn can be made by slowing down the  right motor and moving the left motor forward. The same is implemented by simple GPIO*                    operations of the Raspberry Pi. The PWM values are found out by Trail and error method to overcome the mismatch in speeds of both the motors. *                    This function is used to traverse  on a curved path. 
*Example Call:       right()
'''
        
def right():
     a=1
     #print "Turn Right"
     global mtr_right
     global mtr_left
     GPIO.output(Motor1E,GPIO.LOW)
     GPIO.output(Motor2E,GPIO.LOW)
     #time=calc(x,y)
     mtr_left.start(0)
     mtr_right.start(0)
     GPIO.output(Motor1A,GPIO.LOW)
     GPIO.output(Motor1B,GPIO.LOW)
     mtr_left.ChangeDutyCycle(20)  
     GPIO.output(Motor2A,GPIO.HIGH) 
     GPIO.output(Motor2B,GPIO.LOW)
     mtr_right.ChangeDutyCycle(25)
     return 
     
'''
*Function Name:      left 
*Input:              None
*Output:             None
*Logic:              The function turns the Planter_Bot left side. This function is called by the main() function whenever the centroid of the black line is at 
*                    the leftmost end of the input frame. The bot can be turned towards right by stopping the left motor and running the right motor forward or an *                    even larger radius turn can be made by slowing down the  left motor and moving the right motor forward. The same is implemented by simple GPIO*                    operations of the Raspberry Pi. The PWM values are found out by Trail and error method to overcome the mismatch in speeds of both the motors. *                    This function is used to traverse  on a curved path. 
*Example Call:       left()
'''
         
def left():
     a=-1
     global mtr_right
     global mtr_left
     GPIO.output(Motor1E,GPIO.LOW)
     GPIO.output(Motor2E,GPIO.LOW)
     #time=calc(x,y)
     #print "Turn Left"
     mtr_left.start(0)
     mtr_right.start(0)
     GPIO.output(Motor1A,GPIO.HIGH)
     GPIO.output(Motor1B,GPIO.LOW)
     mtr_left.ChangeDutyCycle(5)  
     GPIO.output(Motor2A,GPIO.LOW) 
     GPIO.output(Motor2B,GPIO.LOW)
     mtr_right.ChangeDutyCycle(50)
     return
     
'''
*Function Name:      sharp_right 
*Input:              None
*Output:             None
*Logic:              The function turns the Planter_Bot right side sharply. This function is called by the main() function whenever the centroid of the black line *                    is at the rightmost and bottom  end of the input frame. The bot can be turned right sharply by moving the right motor back and running the    *                    left motor forward. The same is implemented by simple GPIO  operations of the Raspberry Pi. The sharp turns are required to be made whenever   *                    the robot has to turn a 90 degree turn.
*Example Call:       sharp_right()
'''
        
def sharp_right():
     a=1
     global mtr_right
     global mtr_left
     mtr_left.start(0)
     mtr_right.start(0)
     GPIO.output(Motor1A,GPIO.LOW)
     GPIO.output(Motor1B,GPIO.HIGH)
     mtr_left.ChangeDutyCycle(30)  
     GPIO.output(Motor2A,GPIO.HIGH) 
     GPIO.output(Motor2B,GPIO.LOW)
     mtr_right.ChangeDutyCycle(60)
     return     
     
'''
*Function Name:      sharp_left 
*Input:              None
*Output:             None
*Logic:              The function turns the Planter_Bot left  side sharply. This function is called by the main() function whenever the centroid of the black line *                    is at the leftmost and bottom  end of the input frame. The bot can be turned left sharply by moving the left  motor back and running the      *                    right  motor forward. The same is implemented by simple GPIO  operations of the Raspberry Pi. The sharp turns are required to be made whenever*                    the robot has to turn a 90 degree turn.
*Example Call:       sharp_left()
'''
def sharp_left():
     a=-1
     global mtr_right
     global mtr_left
     mtr_left.start(0)
     mtr_right.start(0)
     GPIO.output(Motor1A,GPIO.HIGH)
     GPIO.output(Motor1B,GPIO.LOW)
     mtr_left.ChangeDutyCycle(35)  
     GPIO.output(Motor2A,GPIO.LOW) 
     GPIO.output(Motor2B,GPIO.HIGH)
     mtr_right.ChangeDutyCycle(50)
     return 
     
'''
*Function Name:      stop 
*Input:              None
*Output:             None
*Logic:              This function stops both the motors.
*Example Call:       stop()
'''

def stop():
     global mtr_right
     global mtr_left
     mtr_left.start(0)
     mtr_right.start(0)
     GPIO.output(Motor1A,GPIO.LOW)
     GPIO.output(Motor1B,GPIO.LOW)
     mtr_left.ChangeDutyCycle(0)  
     GPIO.output(Motor2A,GPIO.LOW) 
     GPIO.output(Motor2B,GPIO.LOW)
     mtr_right.ChangeDutyCycle(0) 
     GPIO.output(Motor1E,GPIO.LOW)
     GPIO.output(Motor2E,GPIO.LOW) 
##############################################################################

'''
*Function Name:      outside 
*Input:              a -> It describes the direction the robot is moving before it goes out of the track 
*Output:             None
*Logic:              The input parameter is set by the left,right(both sharp and normal) whenever they are called so that the robot will have a track of the       *                    directions it has been moving before getting out of track. So if a robot out of the track and its previously set flag- a was by right then the*                    robot has to move towards LEFT and Rigth if previously it was moving towards Left before getting out of the track. So by moving the robot in  *                    opposite direction as mentioned above it can get into track whenever it is out of the track.
*Example Call:       outside(1)
'''

def outside(a):
    #print "I don't see the lines"
    #b=time_constant
    if a==1:
        left()
    elif a==-1:
        right()
        

'''
*Function Name:      blend 
*Input:              img     -> It is the name of the seedling image that is obtained by csv table 
*                    number  -> It is the umber of seedlings to be blended on the plantation image.
*                    zone    -> It is the name of the zone on which the seedlings should be blended.
*                    It takes the plantation imagee as an input not as parameter but reads it from the disk.
*Output:             Outputs the blended image with seedlings on different plantation zones ont he plantation image.
*Logic:              The coordinates of different plantation zones are initialised and the blending operation is performed by removing the entire background of the*                    seedling image and then replacing the part of plantation image with the seeding image. NOTE: The belndinig result of two flowers namely -     *                    lily-double.png and hydrangeablue.png will be found to be distorted which is due to the defect i  the input image which is also brought to    *                    eyantra notice through piazza platform.
*Example Call:       blend('carnation.png',3,2)
'''

   
def blend(img,number,zone):
        global imgSrc
        img_prev = imgSrc
        template1 = cv2.imread(img)
        template1=cv2.resize(template1,(658,334), interpolation = cv2.INTER_CUBIC)

        flag = zone

        if flag == 'A':
          box = [304,239,296,52]
        elif flag == 'B':
          box = [70,206,115,50]
        elif flag == 'C':    
          box = [238,168,160,39]
        elif flag == 'D':
          box= [474,163,176,56]
        height,width=template1.shape[:2]

        mask=np.zeros(template1.shape[:2],np.uint8)

        bgdmodel=np.zeros((1,65),np.float64)
        fgdmodel=np.zeros((1,65),np.float64)
        #rows,cols,channels = template1.shape
        rect=(0,0,640,330)
        cv2.grabCut(template1,mask,rect,bgdmodel,fgdmodel,5,cv2.GC_INIT_WITH_RECT)
        mask=np.where((mask==2)|(mask==0),0,1).astype('uint8')
        img1=template1*mask[:,:,np.newaxis]

        background = template1-img1
        background[np.where((background>[200,0,0]).all(axis=2))]=[0,0,0]

        template2=background + img1



        x,y,w,h = box
        #imgSrc = cv2.rectangle(imgSrc,(x,y),(x+w,y+h),(0,0,255),2)

        n = number 

        res_width = int(w/(n+1))
        res_height = h
        template2 = cv2.resize(template2,(res_width,res_height), interpolation = cv2.INTER_CUBIC)

        t_height,t_width,_ = template2.shape
        i_height,i_width,_ = img_prev.shape

        x_top = x
        y_top = y

        for k in range (0,n):
            for i in range(t_height):
                for j in range(t_width):
                    if all(template2[i,j]) != 0:
                        img_prev[y_top+i,x_top+j] = template2[i,j]
            x_top = x_top+res_width+4
            imgSrc = img_prev
        cv2.imwrite('p_final.png',imgSrc)
        #print 'done blending '
        if zone == 'D':
             pass
             cv2.imshow('blended_output',imgSrc)
        
        
'''
*Function Name:      read_csv 
*Input:              col    ->  It is the colour of the color marker detected.
*                    shape  ->  it is the shape of the color_marker deteced.
*                    number ->  It si the number of colour markers detected at the ZI.
*                    zone   ->  It is the name of the Plantation zone where the blending has to be performed.
*Output:             no return value but calls the blend() function with the seedling name that is read from th csv file.
*Logic:              The function inputs the colour an shape of the and then searches the csv file with colour and shape as keywords. csv file is converted  to    *                    dictionary with the fir row of  each column as keyword of the dictionary.
*Example Call:       blend('carnation.png',3,2)
'''
def read_csv(col,shape,number,zone):
    if zone == 1:
      PZ = 'A'
    if zone == 2:
      PZ = 'B'
    if zone == 3:
      PZ = 'C'
    if zone == 4:
      PZ = 'D'
    if col == 'RED':
      col='Red'
    if col == 'GREEN':
      col='Green'
    if col == 'BLUE':
      col='Blue'
    with open('Input Table.csv','r') as csv_file:
      csv_reader = csv.DictReader(csv_file)
      for line in csv_reader:
        if line['Color'] == col and line['Shape'] == shape:
             image_name  = line['Seedling Image']
             print line['Seedling Image']
             blend(image_name,number,PZ)

'''
*Function Name:      last_blink
*Input:              led_list ->  It is an ordered list of the colours detected at each zone indicator.
*Output:             no return value led binking serves as an output.
*Logic:              simple GPIO operations
*Example Call:       last_blink(['BLUE','RED','GREEN','RED',''])
'''
def last_blink(led_list):
    for b in range(0,len(led_list)):
       blink_led(led_list[b],1)
         
                    
try:
  main()
except KeyboardInterrupt:
   print"Exception accepted"
   GPIO.output(Motor1E,GPIO.LOW)
   GPIO.output(Motor2E,GPIO.LOW)
   GPIO.output(RED,GPIO.LOW)
   GPIO.output(GREEN,GPIO.LOW)
   GPIO.output(BLUE,GPIO.LOW)   
   GPIO.cleanup()
