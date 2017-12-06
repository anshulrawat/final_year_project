from Startup import*
surface= (0,100,100)

class Car:
    def __init__(self,pos_x=width/2,pos_y=height/2):
        self.body = pygame.image.load("Images//Body//Grey.png")
        self.wheels = pygame.image.load("Images//Wheels//Black.png")
        self.rect = self.body.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.ww=self.rect.w/2
        self.hh=self.rect.h/2
        self.rect.center = self.rect.x, self.rect.y

        # movement
        self.forward = False
        self.backward = False
        self.left = False
        self.right = False
        self.angle = 0
        self.turn_angle=0
        self.turn_speed = 5
        self.top_speed = 4
        self.acceleration = 0.2
        self.deceleration = 0.2
        self.current_speed = 0.0
        self.move_x = 0
        self.move_y = 0
        self.p1=(0,0)
        self.p2=(0,0)
        #self.p3=(0,0)
        #self.p4=(0,0)
    def is_collision(self):
        if(self.p1[0]+self.move_x <= 0 or self.p1[0]+self.move_x >= 1000 or self.p1[1]+self.move_y <= 0 or self.p1[1]+self.move_y >= 600):
            return False
        if(self.p2[0]+self.move_x <= 0 or self.p2[0]+self.move_x >= 1000 or self.p2[1]+self.move_y <= 0 or self.p2[1]+self.move_y >= 600):
            return False
        else:
            return True


    def reset_data(self):
        self.left = False
        self.right = False
        self.forward = False
        self.backward = False

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
            if (self.is_collision()):
                self.rect.x += self.move_x
                self.rect.y += self.move_y
                self.angle+=self.turn_angle
        else:
            angle_rad = deg_to_rad(self.angle)
            self.move_x = -(float(self.current_speed * math.sin(angle_rad)))
            self.move_y = -(float(self.current_speed * math.cos(angle_rad)))
            if (self.is_collision()):
                self.rect.x += self.move_x
                self.rect.y += self.move_y
    def display(self, main_surface):
        temp_image = pygame.transform.rotate(self.body, self.angle)
        temp_rect = temp_image.get_rect()
        main_surface.blit(temp_image, (self.rect.x-temp_rect.w/2, self.rect.y-temp_rect.h/2))
        temp_image = pygame.transform.rotate(self.wheels, self.angle)
        main_surface.blit(temp_image, (self.rect.x-temp_rect.w/2, self.rect.y-temp_rect.h/2))

        temp_rect.x=self.rect.x-temp_rect.w/2
        temp_rect.y=self.rect.y-temp_rect.h/2
        angle_rad = deg_to_rad(self.angle+90+30)
        point_x=int(temp_rect.center[0] +float(26 * math.cos(angle_rad)))
        point_y = int(temp_rect.center[1] - float(26 * math.sin(angle_rad)))
        self.p1=(point_x,point_y)
        pygame.draw.circle(main_surface, (255, 0, 0), self.p1, 3, 2)
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
        point_y = int(temp_rect.center[1] - float(26 * math.sin(angle_rad)))
        self.p2=(point_x,point_y)
        pygame.draw.circle(main_surface, (255, 0, 0), self.p2, 3, 2)

        pygame.draw.rect(main_surface,(0,255,0),temp_rect,3)
    def update(self):
        self.move_x = 0
        self.move_y = 0
        self.turn_angle=0
        #self.rotate()
        self.move()
        self.reset_data()
