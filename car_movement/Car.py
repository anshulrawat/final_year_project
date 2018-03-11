from Startup import*

from random import *
black = (0,0,0)
surface= (255,255,255)
grey= (86,86,86)
red = (255,0,0)
yellow = (204,204,0)
car = (68,68,68)
green=(0,255,0)
blue = (0,0,255)
sensor_limit =400

def sum_readings(readings):
    """Sum the number of non-zero readings."""
    tot = 0
    for i in readings:
        tot += i
    return tot


def distfromline(a,b,c,x1,y1):
    return abs(a*x1+b*y1+c)/math.sqrt(a*a + b*b)
def equation_cal(x1,y1,x2,y2):
    a=y1-y2
    b=x2-x1
    c=(y2-y1)*x1+(x1-x2)*y1
    return a,b,c

def drawlabels():
    myfont = pygame.font.SysFont("monospace", 10)
    label = myfont.render("Obstacle Angle dist", 1, red)
    label1 = myfont.render("0", 1, red)
    label2 = myfont.render("45", 1, red)
    label3 = myfont.render("90", 1, red)
    label4 = myfont.render("135", 1, red)
    label5 = myfont.render("180", 1, red)
    label6 = myfont.render("Speed", 1, red)
    main_s.blit(label, (1230, 20))
    main_s.blit(label1, (1220, 220))
    main_s.blit(label2, (1245, 220))
    main_s.blit(label3, (1270, 220))
    main_s.blit(label4, (1295, 220))
    main_s.blit(label5, (1320, 220))
    main_s.blit(label6, (1060, 20))

class Car:
    def __init__(self,pos_x=width/2,pos_y=height/2):
        self.body = pygame.image.load("Images//Body//car.png")
        self.wheels = pygame.image.load("Images//Wheels//Black.png")
        self.rect = self.body.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.ww=self.rect.w/2
        self.hh=self.rect.h/2
        self.rect.center = self.rect.x, self.rect.y
        #journey
        self.source = -1
        self.destination=-1
        self.ob_color=None
        # movement
        self.forward = False
        self.backward = False
        self.left = False
        self.right = False
        self.angle = 0
        self.turn_angle=0
        self.turn_speed = 5
        self.top_speed = 3
        self.acceleration = 0.2
        self.deceleration = 0.2
        self.current_speed = 0.0
        self.move_x = 0
        self.move_y = 0
        self.p1=(0,0)
        self.p2=(0,0)
        self.d1,self.d2,self.d3,self.d4,self.d5=(10,10,10,10,10)
        self.collide = False
        #self.p3=(0,0)
        #self.p4=(0,0)
    def is_collision(self,main_surface):
        if(self.d2<30 or self.d3<=30 or self.d4<=30):
            return False
        else:
            return True
    def find_dis(self,main_surface,x1,y1,alpha):
        c_x=1000
        if((alpha>=315 and alpha<=360) or (alpha>=0 and alpha<=45)):
            t1=1.0
            t2=math.tan(deg_to_rad(alpha))
        elif((alpha>=45 and alpha<135)):
            t2=1.0
            t1=-math.tan(deg_to_rad(alpha-90))
        elif((alpha >= 135 and alpha <= 225)):
            t1=-1.0
            t2=-math.tan(deg_to_rad(alpha-180))
        else:
            t2=-1.0
            t1 = math.tan(deg_to_rad(alpha - 270))
        for t in range(int(self.rect.w/math.sqrt(2)+1), int(c_x)):
            x=x1+t*t1
            y=y1-t*t2
            factor_x = int(2*t1)
            factor_y = int(2*t2)
            if (x > 2 and x < 998 and y >2 and y < 692):
                if (main_surface.get_at((int(x)+factor_x, int(y)+factor_y)) == black or main_surface.get_at((int(x)+factor_x, int(y)+factor_y)) == grey ):
                    return math.sqrt((x - x1) * (x - x1) + (y - y1) * (y - y1))
            else:
                return math.sqrt((x - x1) * (x - x1) + (y - y1) * (y - y1))
            pygame.draw.circle(main_surface, (255, 0, 0), (int(x), int(y)), 1, 1)



        return 10000
    def angle_cal(self,theta):
        return (360+theta)%360

    def reset_data(self):
        self.left = False
        self.right = False
        self.forward = False
        self.backward = False
        self.collide= False

    def rotate(self):
        if self.angle > 360:
            self.angle = 0
        else:
            if self.angle < 0:
                self.angle = 360
        if self.left:
            self.angle += self.turn_speed * self.current_speed
        if self.right:
            self.angle -= self.turn_speed * self.current_speed

    def move(self):
        if self.forward:
            if self.current_speed < self.top_speed:
                self.current_speed += self.acceleration
        else:
            if self.current_speed > 1:
                self.current_speed -= self.deceleration/2
            else:
                self.current_speed = 0
        if self.backward:
            if self.current_speed > 1:
                self.current_speed -=self.deceleration
            else:
                self.current_speed = 0
        if self.left:
            self.turn_angle = self.turn_speed
        if self.right:
            self.turn_angle = -self.turn_speed

        if self.turn_angle:
            if self.turn_angle>0:
                offset=270
            else:
                offset=90
            offset+=self.angle

            angle_rad = deg_to_rad(offset)
            init_x = (float(self.ww*(self.current_speed+1)* math.sin(angle_rad)))
            init_y = (float(self.ww *(self.current_speed+1)* math.cos(angle_rad)))
            offset+=self.turn_angle
            angle_rad = deg_to_rad(offset)
            final_x = (float(self.ww *(self.current_speed+1)* math.sin(angle_rad)))
            final_y = (float(self.ww *(self.current_speed+1)* math.cos(angle_rad)))
            self.move_x = init_x-final_x
            self.move_y = init_y-final_y
            if (self.is_collision(main_s)):
                self.rect.x += self.move_x
                self.rect.y += self.move_y
                self.angle+=self.turn_angle
            else:
                self.collide=True
                self.angle += self.turn_angle+75

        else:
            angle_rad = deg_to_rad(self.angle)
            self.move_x = -(float(self.current_speed * math.sin(angle_rad)))
            self.move_y = -(float(self.current_speed * math.cos(angle_rad)))
            if (self.is_collision(main_s)):
                self.rect.x += self.move_x
                self.rect.y += self.move_y
            else:
                self.collide=True
                self.angle +=  75

    def display(self, main_surface):
        main_surface.fill((255, 255, 255))
        # pygame.draw.rect(main_surface, blue, (200, 150, 100, 50))
        # pygame.draw.rect(main_surface, blue, (600, 350, 100, 50))
        pygame.draw.line(main_surface, black, (1000, 0), (1000, 700), 2)
        """for i in range(0, 4):
            pygame.draw.rect(main_surface, green, (50, 50 + i * 170, 80, 80))
        for i in range(0, 4):
            pygame.draw.rect(main_surface, blue, (900, 50 + i * 170, 80, 80))
        """

        for i in range(0, 10):
            pygame.draw.circle(main_surface, black, (obsx[i],obsy[i]), 20, 0)
        if (self.source != -1):
            pygame.draw.rect(main_s, red, (900, 50 + self.source * 170, 80, 80))
        if (self.destination != -1):
            pygame.draw.rect(main_s, object_colors[self.destination], (50, 50 + self.destination * 170, 80, 80))
            x1 = 900
            y1 = 90 + self.source * 170
            x2 = 130
            y2 = 90 + self.destination * 170
            a, b, c = equation_cal(x1, y1, x2, y2)
            d = distfromline(a, b, c, self.rect.x, self.rect.y)
            pygame.draw.rect(main_surface, green, (1160, 220 - int(d / 5), 20, int(d / 5)))
            pygame.draw.line(main_surface, green, (x1, y1), (x2, y2), 2)
        temp_image = pygame.transform.rotate(self.body, self.angle)
        temp_rect = temp_image.get_rect()
        main_surface.blit(temp_image, (self.rect.x-temp_rect.w/2, self.rect.y-temp_rect.h/2))
        temp_image = pygame.transform.rotate(self.wheels, self.angle)
        #main_surface.blit(temp_image, (self.rect.x-temp_rect.w/2, self.rect.y-temp_rect.h/2))

        temp_rect.x=self.rect.x-temp_rect.w/2
        temp_rect.y=self.rect.y-temp_rect.h/2
        angle_rad = deg_to_rad(self.angle+90+30)
        point_x=int(temp_rect.center[0] +float(26 * math.cos(angle_rad)))
        point_y = int(temp_rect.center[1] - float(20 * math.sin(angle_rad)))
        self.p1=(point_x,point_y)
        #pygame.draw.circle(main_surface, (255, 0, 0 ), self.p1, 3, 2)
        angle_rad = deg_to_rad(self.angle+90)
        init_x = (int(self.ww * math.sin(angle_rad)))
        init_y = (int(self.ww * math.cos(angle_rad)))
        pygame.draw.circle(main_surface, (255, 0, 0), (self.rect.x+init_x, self.rect.y+init_y), 3, 2)
        angle_rad = deg_to_rad(self.angle+270)
        init_x = (int(self.ww * math.sin(angle_rad)))
        init_y = (int(self.ww * math.cos(angle_rad)))
        pygame.draw.circle(main_surface, (255, 0, 0), (self.rect.x+init_x, self.rect.y+init_y), 3, 2)
        angle_rad = deg_to_rad(self.angle+90-30)
        point_x=int(temp_rect.center[0] +float(26 * math.cos(angle_rad)))
        point_y = int(temp_rect.center[1] - float(20 * math.sin(angle_rad)))
        self.p2=(point_x,point_y)
        #pygame.draw.circle(main_surface, (255, 0, 0), self.p2, 3, 2)


       # pygame.draw.rect(main_surface,(0,255,0),temp_rect,3)
        #print("#",self.angle)


        x1 = self.find_dis(main_surface, self.rect.x, self.rect.y, self.angle_cal(self.angle+30))
        self.d1 =x1
        #print("0 degree dis: ",x1)
        x2 = self.find_dis(main_surface, self.rect.x, self.rect.y, self.angle_cal(self.angle + 60))
        self.d2 = x2
        #print("45 degree dis: ", x2)
        x3 = self.find_dis(main_surface, self.rect.x, self.rect.y, self.angle_cal(self.angle + 90))
        self.d3 = x3
        #print("90 degree dis: ",x3 )
        x4 = self.find_dis(main_surface, self.rect.x, self.rect.y, self.angle_cal(self.angle + 120))
        self.d4 = x4
        #print("135 degree dis: ",x4 )
        x5 = self.find_dis(main_surface, self.rect.x, self.rect.y, self.angle_cal(self.angle + 150))
        self.d5 = x5
        #print("180 degree dis: ", x5)
        pygame.draw.rect(main_surface, (255,100,50), (1060, 220 - int(self.current_speed * 50), 30, int(self.current_speed * 50)))
        pygame.draw.rect(main_surface, yellow, (1160+60, 220-int(x1/5), 20, int(x1/5)))
        pygame.draw.rect(main_surface, yellow, (1185+60, 220 - int(x2 / 5), 20, int(x2 / 5)))
        pygame.draw.rect(main_surface, yellow, (1210+60, 220 - int(x3 / 5), 20, int(x3 / 5)))
        pygame.draw.rect(main_surface, yellow, (1235+60, 220 - int(x4 / 5), 20, int(x4 / 5)))
        pygame.draw.rect(main_surface, yellow, (1260+60, 220 - int(x5 / 5), 20, int(x5 / 5)))
        drawlabels()

        if (self.destination != -1):
            pygame.draw.circle(main_s, object_colors[self.destination], (self.rect.x, self.rect.y),8)


    def check(self):
        if(self.source==-1):
            self.source=generate_source()
        if(math.sqrt((940-self.rect.x)*(940-self.rect.x)+(90+self.source * 170-self.rect.y)*(90+self.source * 170-self.rect.y))<30 and self.destination==-1):
            self.destination=generate_destination()
            source_ticket[self.source]=-1
        if(math.sqrt((90-self.rect.x)*(90-self.rect.x)+(90+self.destination * 170-self.rect.y)*(90+self.destination * 170-self.rect.y))<30 and self.destination!=-1):
            destination_ticket[self.destination] = -1
            self.source=-1
            self.destination=-1

    def learningval(self):
        readings = [self.d1,self.d2,self.d3,self.d4,self.d5]
        for i in range(5):
            if readings[i] > 400:
                readings[i] = 40
            else:
                readings[i]=int(readings[i]/10)
        normalized_readings = [(x - 20.0) / 20.0 for x in readings]
        state = np.array([normalized_readings])
        reward =0
        # Set the reward.
        # Car crashed when any reading == 1
        if self.collide:
            reward = -500
        else:
            reward = -5 + int(sum_readings(readings) / 10)


        return reward, state

    def update(self,action=2):
        self.move_x = 0
        self.move_y = 0
        self.turn_angle=0
        #self.rotate()
        if action == 0:
            self.left = True
        if action == 1:
            self.right = True
        if action == 2:
            self.forward = True
        if action == 3:
            self.forward = True
        self.move()

        self.display(main_s)
        reward,state = self.learningval()
        self.reset_data()
        return reward,state


