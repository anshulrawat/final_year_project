from Car import*
from random import *
vehicle =[]
#vehicle.append(Car(100,200))
#vehicle.append(Car(300,500))
vehicle.append(Car(300,700))
blue = (0,0,255)
black = (0,0,0)
def check_all(check_list):
    for element in check_list:
        element.check()
def display_all(main_surface, display_list):
    main_surface.fill((255, 255, 255))
    #pygame.draw.rect(main_surface, blue, (200, 150, 100, 50))
    #pygame.draw.rect(main_surface, blue, (600, 350, 100, 50))
    pygame.draw.line(main_surface,black ,(1000,0),(1000,700), 2)
    for i in range(0,4):
        pygame.draw.rect(main_surface, green, (50,50+i*170,80,80))
    for i in range(0,4):
        pygame.draw.rect(main_surface, blue, (900,50+i*170,80,80))

    for element in display_list:
        element.display(main_surface)
    #for element_val in range(0, len(text_list)):
     #   main_surface.blit(font.render(str(text_list[element_val]), True, (0, 255, 0)), (10, 10 + (10 * element_val)))


def update_all(update_list):
    for element in update_list:
       """" key = randint(0, 3)
        if key == 0:
            element.left = True
        if key == 1:
            element.right = True
        if key == 2:
            element.forward = True
        if key == 3:
            element.backward = True
        element.update()

"""

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        element.left = True
    if key[pygame.K_RIGHT]:
        element.right = True
    if key[pygame.K_UP]:
        element.forward = True
    if key[pygame.K_DOWN]:
        element.backward = True
    if key[pygame.K_r]:
        element.rect.x = 500
        element.rect.y = 300
        element.angle = 0
    element.update()

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            None

    update_all(vehicle)
    check_all(vehicle)
    display_all(main_s, vehicle)
    pygame.display.flip()

