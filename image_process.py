import imutils
import serial
import random
import time
import cv2
import numpy as np
import math
cap = cv2.VideoCapture(1)
green=[ 100,158,94]
sky=[133,164,166]
blue = [225,185,120]
red = [66,50,250]
yellow = [44,127,157]
pink = [176,90,172]
th=10
w=400
h=200
source = 0
depart =0
arduino = serial.Serial('COM5',115200, timeout=.1)
def stop_car():
    txt = 's'
    arduino.write(txt.encode('utf-8'))

def find_dis( main_surface, x1, y1, alpha,rw,rh):
    c_x = 1000
    if ((alpha >= 315 and alpha <= 360) or (alpha >= 0 and alpha <= 45)):
        t1 = 1.0
        t2 = math.tan(deg_to_rad(alpha))
    elif ((alpha >= 45 and alpha < 135)):
        t2 = 1.0
        t1 = -math.tan(deg_to_rad(alpha - 90))
    elif ((alpha >= 135 and alpha <= 225)):
        t1 = -1.0
        t2 = -math.tan(deg_to_rad(alpha - 180))
    else:
        t2 = -1.0
        t1 = math.tan(deg_to_rad(alpha - 270))
    for t in range(int(math.sqrt((rw*rw/4)+(rh*rh))), int(c_x)):
        x = x1 + t * t1
        y = y1 - t * t2
        factor_x = int(2 * t1)
        factor_y = int(2 * t2)
        if (x > 2 and x < 600 and y > 2 and y < 450):
            print(main_surface[int(x) + factor_x, int(y) + factor_y])
            if (main_surface[int(x) + factor_x, int(y) + factor_y][0] == 0 and main_surface[int(x) + factor_x, int(y) + factor_y][1] == 0 and main_surface[int(x) + factor_x, int(y) + factor_y][2] == 0 ):
                return math.sqrt((x - x1) * (x - x1) + (y - y1) * (y - y1))
        else:
            return math.sqrt((x - x1) * (x - x1) + (y - y1) * (y - y1))

        cv2.circle(main_surface,(int(x),int(y)), 1,(0, 0, 255), -1)

def tar_dist(x1,y1,x2,y2):
    return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
def deg_to_rad(degrees):
    return degrees / 180.0 * math.pi
def rad_to_deg(radians):
    return radians *180.0/ math.pi
def car_angle(x1,y1,x2,y2):
    if x1==x2 and y1<y2 :
        return 90
    if x1 == x2 and y1 > y2:
        return 270
    if x2 < x1 and y2 >= y1:
        return rad_to_deg(math.atan((y2 - y1) / (x1 - x2)))
    if x2 > x1 and y2 >= y1:
        return 180 + rad_to_deg(math.atan((y2 - y1) / (x1 - x2)))
    if x2 > x1 and y2 < y1:
        return 180 + rad_to_deg(math.atan((y2 - y1) / (x1 - x2)))
    if x2 < x1 and y2 < y1:
        return 360 + rad_to_deg(math.atan((y2 - y1) / (x1 - x2)))


def angle_limit(theta):
    theta = (360+theta)%360
    if theta >180:
        theta = theta -360
    return theta
def anglefromline(x1,y1,x2,y2,ang):
    if x1==x2:
        if y1>y2:
            return ang-90
        else:
            return ang-270
    if x2>x1 and y2 <=y1:
        return ang+rad_to_deg(math.atan((y2-y1)/(x2-x1)))
        #first
    elif x2<x1 and y2 <y1:
        return ang-180+rad_to_deg(math.atan((y2-y1)/(x2-x1)))
        #second
    elif x2 <x1 and y2>=y1:
        return ang - 180+rad_to_deg(math.atan((y2 - y1) / (x2 - x1)))
        #third
    elif x2>x1 and y2>y1:
        return ang - 360+rad_to_deg(math.atan( (y2 - y1) / (x2 - x1)))
def find_mask(hsv,hsv_color):
    lower = np.array([hsv_color[0][0][0] - 10, 100, 100])
    upper = np.array([hsv_color[0][0][0] + 10, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    return mask
def findhsv_color(color):
    h_color = np.uint8([[color]])
    hsv_color = cv2.cvtColor(h_color, cv2.COLOR_BGR2HSV)
    return hsv_color
def distance(x,y,i,j):
    return math.sqrt((x[i][0]-y[j][0])*(x[i][0]-y[j][0])+((x[i][1]-y[j][1])*(x[i][1]-y[j][1])))
while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    kernel = np.ones((5, 5), np.uint8)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    img_erosion = cv2.erode(hsv, kernel, iterations=1)
    img_dilation = cv2.dilate(hsv, kernel, iterations=1)
    # define range of blue color in HSV
    #print(hsv_color)
    print(frame[1,1])
    # Threshold the HSV image to get only blue colors
    mask1 = find_mask(hsv,findhsv_color(red))
    mask2 = find_mask(hsv, findhsv_color(green))
    mask3 = find_mask(hsv, findhsv_color(blue))
    mask4 = find_mask(hsv, findhsv_color(pink))
    mask5 = find_mask(hsv, findhsv_color(yellow))
    im25, contours5, hierarchy5 = cv2.findContours(mask5, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    im24, contours4, hierarchy4 = cv2.findContours(mask4, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    im23, contours3, hierarchy3 = cv2.findContours(mask3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    im22, contours2, hierarchy2 = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours3, -1, (0, 0, 0), 3)
    cv2.drawContours(frame, contours2, -1, (0, 0, 0), 3)
    cv2.drawContours(frame, contours4, -1, (0, 0, 100), 3)
    cv2.drawContours(frame, contours5, -1, (0, 100, 0), 3)
    #cnts = im22[0] if imutils.is_cv2() else im22[1]


    ceterg = []
    ceterb = []
    dim = []
    d = [[1000 for x in range(4)] for y in range(4)]
    bindex = [-1 for x in range(4)]
    beta = [360 for x in range(4)]
    target_center = []
    dest_center = []
    for cnt2 in contours4:
        rect2 = cv2.minAreaRect(cnt2)
        if rect2[1][0]>th and rect2[1][1]>th:
            target_center.append((rect2[0][0],rect2[0][1]))
    for cnt2 in contours5:
        rect2 = cv2.minAreaRect(cnt2)
        if rect2[1][0]>th and rect2[1][1]>th:
            dest_center.append((rect2[0][0],rect2[0][1]))

    if len(target_center)>0 :
        if source==0:
            i = random.randint(0, len(target_center)-1)
            w=int(target_center[i][0])
            h=int(target_center[i][1])
            source=1
    if len(dest_center)>0:
        if source==2 and depart==0:
            i = random.randint(0, len(dest_center) - 1)
            w = int(dest_center[i][0])
            h = int(dest_center[i][1])
            depart=1

    for cnt2 in contours2:
        rect2 = cv2.minAreaRect(cnt2)
        box = cv2.boxPoints(rect2)
        box = np.int0(box)
        if rect2[1][0]>th and rect2[1][1]>th:
            cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
            ceterg.append((rect2[0][0],rect2[0][1]))
            dim.append((rect2[1][0],rect2[1][1]))
    for c in ceterg:
        cv2.circle(frame, (int(c[0]), int(c[1])), 5, (0, 0, 255), -1)

    for cnt2 in contours3:
        rect2 = cv2.minAreaRect(cnt2)
        box = cv2.boxPoints(rect2)
        box = np.int0(box)

        if rect2[1][0] > th and rect2[1][1] > th:
            cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)


            ceterb.append((rect2[0][0], rect2[0][1]))
    for c in ceterb:
        cv2.circle(frame, (int(c[0]), int(c[1])), 5, (0, 0, 255), -1)
    if len(ceterb)>0 and len(ceterg)>0 :
        for i in range(0,len(ceterg)):
            for j in range(0,len(ceterb)):
                if i<4 and j<4:
                    d[i][j] = distance(ceterg,ceterb,i,j)

        for i in range(0, len(d)):
            min=1000

            for j in range(0, 4):
                if(d[i][j]<min):
                    min=d[i][j]
                    bindex[i] = j
            if bindex[i]>=0 and bindex[i]<len(ceterb) and i>=0 and i<len(ceterg):
                cv2.line(frame, (int(ceterg[i][0]), int(ceterg[i][1])), (int(ceterb[bindex[i]][0]),int(ceterb[bindex[i]][1])), (0, 0,255), 3)
                cv2.circle(frame, (int((ceterg[i][0]+ceterb[bindex[i]][0])/2), int((ceterg[i][1]+ceterb[bindex[i]][1])/2)), 5, (0, 255, 255), -1)
                cv2.line(frame, (int((ceterg[i][0]+ceterb[bindex[i]][0])/2), int((ceterg[i][1]+ceterb[bindex[i]][1])/2)),(w,h), (0, 0, 255), 3)
                car_ang = car_angle(int(ceterg[i][0]), int(ceterg[i][1]),int(ceterb[bindex[i]][0]),int(ceterb[bindex[i]][1]))
                target_dist= tar_dist((int(ceterg[i][0]+ceterb[bindex[i]][0])/2), int((ceterg[i][1]+ceterb[bindex[i]][1])/2),w,h)
                beta[i] = angle_limit(anglefromline(int((ceterg[i][0]+ceterb[bindex[i]][0])/2), int((ceterg[i][1]+ceterb[bindex[i]][1])/2),w,h,car_ang))
                print(target_dist)
                if (target_dist<20):
                    print('s')
                    txt = 's'
                    if source==1:
                        source=2
                        depart=0
                    elif depart==1:
                        source=0
                        depart=2

                    arduino.write(txt.encode('utf-8'))
                elif(beta[i]>25):
                    print('d')
                    txt='d'
                    arduino.write(txt.encode('utf-8'))

                elif(beta[i]<-25):
                    txt='a'
                    arduino.write(txt.encode('utf-8'))
                    print('a')
                else:
                    txt = 'w'
                    arduino.write(txt.encode('utf-8'))
                    print('w')



                #find_dis(frame,(ceterg[i][0]+ceterb[bindex[i]][0])/2,(ceterg[i][1]+ceterb[bindex[i]][1])/2,(car_ang+45)%360,dim[i][0],dim[i][1])
        #print(beta)
            #hull = cv2.convexHull(cnt)
    # Bitwise-AND mask and original image
    #res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imshow('frame',frame)
    #cv2.imshow('Erosion', img_erosion)
    #cv2.imshow('Dilation', img_dilation)
    #cv2.imshow('mask1',mask1)
    #cv2.imshow('mask2',mask2)
    #cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        i=0
        while(i<100):
            stop_car()
            i+=1
        break

cv2.destroyAllWindows()