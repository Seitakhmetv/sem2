# Paint
import pygame, random

# (x1, y1), (x2, y2)
# A = y2 - y1
# B = x1 - x2
# C = x2 * y1 - x1 * y2
# Ax + By + C = 0
# (x - x1) / (x2 - x1) = (y - y1) / (y2 - y1)

save = pygame.image.load(r'C:\\Users\\User\\main\\surface.png')
def drawLine(screen, start, end, width, color):
    x1 = start[0]
    y1 = start[1]
    x2 = end[0]
    y2 = end[1]

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    A = y2 - y1
    B = x1 - x2
    C = x2 * y1 - x1 * y2

    if dx > dy:
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        for x in range(x1, x2):
            y = (-C - A * x) / B
            pygame.draw.circle(screen, color, (x, y), width)
    else:
        if y1 > y2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        for y in range(y1, y2):
            x = (-C - B * y) / A
            pygame.draw.circle(screen, color, (x, y), width)

def main():
    screen = pygame.display.set_mode((800, 600))
    screen.blit(save, (0, 0))
    mode = 'random'
    draw_on = False
    last_pos = (0, 0)
    color = (255, 128, 0)
    radius = 10

    mousepos = None
    boxes = []

    colors = {
        'red': (255, 0, 0),
        'blue': (0, 0, 255),
        'green': (0, 255, 0),
        'eraser': (0, 0, 0)
    }
    flag = True
    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_r:
                    mode = 'red'
                if event.key == pygame.K_b:
                    mode = 'blue'
                if event.key == pygame.K_g:
                    mode = 'green'
                if event.key == pygame.K_e:
                    mode = 'eraser'
                if event.key == pygame.K_z:
                    screen.fill((0, 0, 0))
                if event.key == pygame.K_s:
                    pygame.image.save( screen, 'surface.png')
                if event.key == pygame.K_UP:
                    radius += 1
                if event.key == pygame.K_DOWN:
                    radius -= 1
                if event.key == pygame.K_1:
                    flag = False
                if event.key == pygame.K_2:
                    flag = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (flag == False):
                    if mode == 'random':
                        color = (random.randrange(256), random.randrange(256), random.randrange(256))
                    else:
                        color = colors[mode]
                    pygame.draw.circle(screen, color, event.pos, radius)
                    draw_on = True
                if (flag):
                    mousepos = [event.pos[0], event.pos[1], 0, 0]
            if event.type == pygame.MOUSEBUTTONUP:
                if (flag == False):
                    draw_on = False
                else:
                    boxes.append(mousepos)
                    mousepos = None
            if event.type == pygame.MOUSEMOTION:
                if (flag == False):
                    if draw_on:
                        drawLine(screen, last_pos, event.pos, radius, color)
                        pygame.draw.circle(screen, color, event.pos, radius)
                    last_pos = event.pos
                if (flag) and mousepos != None:
                    mousepos = [mousepos[0], mousepos[1], event.pos[0] - mousepos[0], event.pos[1] - mousepos[1]]
        if (flag):
            for box in boxes:
                pygame.draw.rect(screen, color, box, 1)

        if mousepos != None:
            pygame.draw.rect(screen, color, mousepos, 1)
        pygame.display.flip()

    pygame.quit()

main()
