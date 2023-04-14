import asyncio
import pygame, random
pygame.init()



FPS = random.randint(5,8) # Frames per second
fps_clock = pygame.time.Clock()
TILE_LEN = 25
TILES = random.randint(20,30)
BACKGROUND_COLOR = (0,0,0)
HUD_COLOR = (255,255,255)
PLAYER_COLOR = (255,255,255)
SHADOW_COLOR = (127,127,127)
BOMB_COLOR_PICKUP = (0,255,0)
BOMB_COLOR_PLACED = (255,0,0)
BOMB_IMAGE_COLOR = (0,0,0)
EXPLOSION_FADE_TIME = 5
EXPLOSION_KILL_TIME = 2
EXPLOSION_COLOR = (255,255,0)
LEFT, RIGHT, UP, DOWN = False, False, False, False
ticks = 1
START_SHADOW_SPAWN_TIME = FPS*random.randint(2,5)
BIG_SHADOW_AREA = 2
BIG_SHADOW_CHANCE_TO_NOT_MOVE = 0.2
BIG_SHADOW_POINTS = 500
SHADOW_POINTS = 200
HEATMAP_INCREASE = 32

SHADOW_FALL_ACC = 2

SCREEN_WIDTH = TILE_LEN*TILES
SCREEN_HEIGHT = SCREEN_WIDTH + TILE_LEN*2
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

default_font = pygame.font.Font(None, 20)
TEXT_COLOR = (0,0,0)

class Free_Class:
    pass

class Player:
    def __init__(self):
        self.x = random.randint(0,TILES-1)*TILE_LEN
        self.y = random.randint(0,TILES-1)*TILE_LEN
        self.x_dir = 1
        self.y_dir = 0
        
        self.places = [(self.x,self.y)]

        self.bombs = [] # {bomb_type:XXX,draw_func:XXX} objects in array
        self.alive = True
    def logic(self):
        self.move()
        self.check_boundaries()
    def move(self):
        self.x += self.x_dir*TILE_LEN
        self.y += self.y_dir*TILE_LEN
        self.places.append((self.x,self.y))
    def check_boundaries(self):
        if self.x >= TILES*TILE_LEN or self.y >= TILES*TILE_LEN or self.x<0 or self.y < 0:
            self.die()
    def change_dir(self,dir):
        self.x_dir = dir[0]
        self.y_dir = dir[1]
    def die(self):
        #global reset_everything
        #reset_everything = True
        self.alive = False
        dead_shadows.append(Dead_Shadow((self.x,self.y),1,PLAYER_COLOR,True))

    def draw(self):
        if self.alive:
            pygame.draw.rect(screen, PLAYER_COLOR, (self.x,self.y,TILE_LEN,TILE_LEN))

def draw_bomb0(self, bomb_color):
    pygame.draw.rect(screen, bomb_color, (self.x,self.y,TILE_LEN,TILE_LEN))
    pygame.draw.circle(screen, BOMB_IMAGE_COLOR, (self.x+int(TILE_LEN/2),self.y+int(TILE_LEN/2)),int(TILE_LEN*0.4))
def draw_bomb1(self, bomb_color):
    pygame.draw.rect(screen, bomb_color, (self.x,self.y,TILE_LEN,TILE_LEN))
    pygame.draw.rect(screen, BOMB_IMAGE_COLOR, (self.x,self.y+int(TILE_LEN*0.45),TILE_LEN,int(TILE_LEN*0.2)))
    pygame.draw.rect(screen, BOMB_IMAGE_COLOR, (self.x+int(TILE_LEN*0.45),self.y,int(TILE_LEN*0.2),TILE_LEN))
def draw_bomb2(self, bomb_color):
    pygame.draw.rect(screen, bomb_color, (self.x,self.y,TILE_LEN,TILE_LEN))
    pygame.draw.line(screen, BOMB_IMAGE_COLOR, (self.x,self.y),(self.x+TILE_LEN,self.y+TILE_LEN),int(TILE_LEN*0.1))
    pygame.draw.line(screen, BOMB_IMAGE_COLOR, (self.x+TILE_LEN,self.y),(self.x,self.y+TILE_LEN),int(TILE_LEN*0.1))

class Pickup_Bomb:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.bomb_type = 0
        self.draw_func = draw_bomb0
        self.reset()
    def reset(self):
        self.x = random.randint(0,TILES-1)*TILE_LEN
        self.y = random.randint(0,TILES-1)*TILE_LEN
        self.bomb_type = random.randint(0,2)
        if self.bomb_type == 0:
            self.draw_func = draw_bomb0
        if self.bomb_type == 1:
            self.draw_func = draw_bomb1
        if self.bomb_type == 2:
            self.draw_func = draw_bomb2
    def logic(self):
        if player.x == self.x and player.y == self.y:
            print("picked up bomb with type:", self.bomb_type)# get picked up
            obj = Free_Class()
            obj.bomb_type = self.bomb_type
            obj.draw_func = self.draw_func
            player.bombs.append(obj)
            # move
            self.reset()
    
    def draw(self):
        self.draw_func(self, BOMB_COLOR_PICKUP)
class Placed_Bomb:
    def __init__(self):
        self.exploded = True
        self.bomb_type = 0
        self.x = 0
        self.y = 0
        self.draw_func = draw_bomb0
    def trigger(self):
        if self.exploded:
            # place
            if len(player.bombs) > 0:
                self.get_placed((player.x,player.y), player.bombs[0])
                # delete bomb from player inventory
                player.bombs.pop(0)
        else:
            # explode
            self.exploded = True
            explosions.append(Explosion((self.x,self.y),self.bomb_type))
    def get_placed(self, pos, bomb):
        self.x = pos[0]
        self.y = pos[1]
        self.bomb_type = bomb.bomb_type
        self.exploded = False
        self.draw_func = bomb.draw_func
    def draw(self):
        if not self.exploded:
            self.draw_func(self, BOMB_COLOR_PLACED)
class Explosion:
    def __init__(self, pos, bomb_type):
        self.x = pos[0]
        self.y = pos[1]
        self.bomb_type = bomb_type
        self.age = 0
        self.positions = []

        if bomb_type == 0: # square
            self.positions = [(0,0),(1,0),(2,0),(2,1),(2,2),(1,2),(1,1),(0,1),(0,2),
                              (-1,2),(-2,2),(-2,1),(-1,1),(-1,0),(-2,0),(-2,-1),(-1,-1),(-1,-2),(-2,-2),
                              (0,-1),(0,-2),(1,-2),(1,-1),(2,-1),(2,-2)]
        elif bomb_type == 1: # cross
            self.positions = [(0,0),
                              (1,0),(2,0),(3,0),(4,0),(5,0),(6,0),
                              (0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
                              (-1,0),(-2,0),(-3,0),(-4,0),(-5,0),(-6,0),
                              (0,-1),(0,-2),(0,-3),(0,-4),(0,-5),(0,-6)]
        elif bomb_type == 2: # diagonal cross
            self.positions = [(0,0),
                              (1,1),(2,2),(3,3),(4,4),(5,5),(6,6),
                              (-1,1),(-2,2),(-3,3),(-4,4),(-5,5),(-6,6),
                              (-1,-1),(-2,-2),(-3,-3),(-4,-4),(-5,-5),(-6,-6),
                              (1,-1),(2,-2),(3,-3),(4,-4),(5,-5),(6,-6)]
    def draw(self):
        alpha = min(255,int(255*(1 - self.age/(EXPLOSION_FADE_TIME*2))))
        #alpha = random.randint(0,255)
        
        for pos in self.positions:
            #pygame.draw.rect(screen, EXPLOSION_COLOR, )
            s = pygame.Surface((TILE_LEN,TILE_LEN))
            s.set_alpha(alpha)
            s.fill(EXPLOSION_COLOR)
            screen.blit(s,(self.x+pos[0]*TILE_LEN,self.y+pos[1]*TILE_LEN))

    def logic(self):
        if self.age < EXPLOSION_KILL_TIME:
            # kill shadow and player and big shadow
            for pos in self.positions: # player
                if player.x == self.x+pos[0]*TILE_LEN and player.y == self.y+pos[1]*TILE_LEN:
                    # player hit by explosion
                    player.die()
                    print("Player hit by explosion")
                for i in range(len(shadows)-1,-1,-1):
                    if shadows[i].x == self.x+pos[0]*TILE_LEN and shadows[i].y == self.y+pos[1]*TILE_LEN:
                        # shadow hit by explosion
                        print("shadow of age", shadows[i].age, "exploded")
                        shadows[i].exploded()
                for i in range(len(big_shadows)-1,-1,-1):
                    if self.x+pos[0]*TILE_LEN >= big_shadows[i].x and self.x+pos[0]*TILE_LEN <= big_shadows[i].x+BIG_SHADOW_AREA*TILE_LEN and self.y+pos[1]*TILE_LEN >= big_shadows[i].y and self.y+pos[1]*TILE_LEN <= big_shadows[i].y+BIG_SHADOW_AREA*TILE_LEN:
                        print("big shadow died")
                        big_shadows[i].exploded()
                        
        elif self.age == EXPLOSION_FADE_TIME:
            explosions.remove(self) # remove
        self.age += 1

class Shadow:
    def __init__(self):
        self.age = 0
        self.x = 0
        self.y = 0
    def logic(self):
        self.kill_player()
        self.move()
    def move(self):
        self.x = player.places[self.age][0]
        self.y = player.places[self.age][1]
        self.age += 1
    def kill_player(self):
        if self.x == player.x and self.y == player.y:
            player.die()
    def exploded(self):
        global points
        points += SHADOW_POINTS
        dead_shadows.append(Dead_Shadow((self.x,self.y),1))
        shadows.remove(self)
    def draw(self):
        pygame.draw.rect(screen, SHADOW_COLOR, (self.x,self.y,TILE_LEN,TILE_LEN))
class Big_Shadow:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
    def logic(self):
        self.kill_player()
        self.move()
        
    def move(self):
        if random.uniform(0,1) > BIG_SHADOW_CHANCE_TO_NOT_MOVE:
            x_dif = abs(player.x-self.x)
            y_dif = abs(player.y-self.y)
            if random.randint(0,x_dif) > random.randint(0,y_dif):
                self.x += TILE_LEN if player.x > self.x else -TILE_LEN
            else:
                self.y += TILE_LEN if player.y > self.y else -TILE_LEN
    def kill_player(self): # if inside big shadow, player dies
        if player.x >= self.x and player.x <= self.x+BIG_SHADOW_AREA*TILE_LEN and player.y >= self.y and player.y <= self.y+BIG_SHADOW_AREA*TILE_LEN:
            player.die()
    def exploded(self):
        global points
        points += BIG_SHADOW_POINTS
        dead_shadows.append(Dead_Shadow((self.x,self.y),2))
        big_shadows.remove(self)
    def draw(self):
        pygame.draw.rect(screen, SHADOW_COLOR, (self.x,self.y,TILE_LEN*BIG_SHADOW_AREA,TILE_LEN*BIG_SHADOW_AREA))
class Dead_Shadow:
    def __init__(self,pos, size, color=SHADOW_COLOR,restart_game=False):
        self.x = pos[0]
        self.y = pos[1]
        self.x_vel = random.uniform(-2,2)
        self.y_vel = 6
        self.size = size
        self.color = color
        self.restart_game = restart_game
    def logic(self):
        self.move()
        self.die()
    def move(self):
        self.y_vel += SHADOW_FALL_ACC
        self.x += self.x_vel
        self.y += self.y_vel
    def die(self):
        global reset_everything
        if self.y > SCREEN_HEIGHT: # if fallen off
            if self.restart_game:
                reset_everything = True
            dead_shadows.remove(self)
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x,self.y,TILE_LEN*self.size,TILE_LEN*self.size))
def shadow_logic():
    global points
    if ticks % shadow_spawn_time == 0: # spawn shadows every so often
        shadows.append(Shadow())
        points += shadow_spawn_time
    for i in range(0,len(shadows)-1): # spawn big shadow if two shadows coalesce/merge
        for j in range(i+1,len(shadows)):
            if shadows[i].x == shadows[j].x and shadows[i].y == shadows[j].y:
                big_shadows.append(Big_Shadow((shadows[i].x,shadows[i].y)))
                shadows.pop(j)
                shadows.pop(i)

                return

def draw_hud():
    hud_y = TILE_LEN*TILES
    pygame.draw.rect(screen,HUD_COLOR, (0,hud_y,SCREEN_WIDTH,SCREEN_HEIGHT-TILES*TILE_LEN))
    for i in range(len(player.bombs)):
        obj = Free_Class()
        obj.x = i*TILE_LEN
        obj.y = hud_y
        player.bombs[i].draw_func(obj, BOMB_COLOR_PICKUP)
    text = "Points:" + str(points) + " Highscore:" + str(high_score)
    text_surface = default_font.render(text, True, TEXT_COLOR)
    screen.blit(text_surface,(0,hud_y+TILE_LEN))
    if ticks < FPS*2:
        text = "Move with arrow keys | Use bombs with space"
        text_surface = default_font.render(text, True, (255,255,255))
        screen.blit(text_surface,(0,0))
def draw_heatmap():
    if player.alive:
        if (player.x,player.y) in heatmap:
            heatmap[(player.x,player.y)] += HEATMAP_INCREASE
        else:
            heatmap[(player.x,player.y)] = HEATMAP_INCREASE
    for place in heatmap:
        value = min(255,heatmap[place])
        pygame.draw.rect(screen, (value,0,0), (place[0],place[1],TILE_LEN,TILE_LEN))
heatmap = {}
explosions = []
player = Player()
pickup_bomb = Pickup_Bomb()
placed_bomb = Placed_Bomb()
shadows = []
big_shadows = []
dead_shadows = []
points = 0
high_score = 0
reset_everything = False
shadow_spawn_time = START_SHADOW_SPAWN_TIME

running = True
async def main():
    global heatmap, explosions, player, pickup_bomb, placed_bomb, shadows, big_shadows, dead_shadows, points, high_score, reset_everything, shadow_spawn_time, ticks, running
    while running:

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.change_dir((-1,0))
                if event.key == pygame.K_RIGHT:
                    player.change_dir((1,0))
                if event.key == pygame.K_UP:
                    player.change_dir((0,-1))
                if event.key == pygame.K_DOWN:
                    player.change_dir((0,1))
                if event.key == pygame.K_SPACE:
                    placed_bomb.trigger()
        # LOGIC
        if player.alive:
            shadow_logic()
        
            for shadow in shadows: shadow.logic()
            for big_shadow in big_shadows: big_shadow.logic()
            pickup_bomb.logic()
            player.logic()
            for i in range(len(explosions)-1,-1,-1): explosions[i].logic()
        for i in range(len(dead_shadows)-1,-1,-1): dead_shadows[i].logic()

        # DRAW THINGS
        screen.fill(BACKGROUND_COLOR)
        draw_heatmap()
        
        for explosion in explosions: explosion.draw()
        for shadow in shadows: shadow.draw()
        for big_shadow in big_shadows: big_shadow.draw()
        placed_bomb.draw()
        pickup_bomb.draw()
        player.draw()
        draw_hud()
        for dead_shadow in dead_shadows: dead_shadow.draw()

        pygame.display.flip()
        fps_clock.tick(FPS)
        ticks += 1
        await asyncio.sleep(0) # very important

        if reset_everything: # when you die
            heatmap = {}
            shadows = []
            big_shadows = []
            dead_shadows = []
            shadow_spawn_time = START_SHADOW_SPAWN_TIME
            explosions = []
            player = Player()
            pickup_bomb = Pickup_Bomb()
            placed_bomb = Placed_Bomb()
            reset_everything = False
            if points > high_score:
                high_score = points
            points = 0
            ticks = 1
            

asyncio.run(main())
pygame.quit()
