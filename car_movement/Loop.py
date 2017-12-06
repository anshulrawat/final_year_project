from Car import*
from random import *
vehicle =[]
vehicle.append(Car(100,200))
vehicle.append(Car(300,500))
vehicle.append(Car(600,300))
blue = (0,0,255)


def display_all(main_surface, display_list):
    main_surface.fill((0, 100, 100))
    pygame.draw.rect(main_s, blue, (200, 150, 100, 50))
    for element in display_list:
        element.display(main_surface)
    #for element_val in range(0, len(text_list)):
     #   main_surface.blit(font.render(str(text_list[element_val]), True, (0, 255, 0)), (10, 10 + (10 * element_val)))


def update_all(update_list):
    for element in update_list:
        key = randint(0, 3)
        if key == 0:
            element.left = True
        if key == 1:
            element.right = True
        if key == 2:
            element.forward = True
        if key == 3:
            element.backward = True
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
    display_all(main_s, vehicle)
    pygame.display.flip()

