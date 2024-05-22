from designer import *
from dataclasses import dataclass
import random
SPACESHIP_SPEED = 5
ALIEN_SPEED = 3
ALIEN_SPAWN = 200
laser_speed = 5

@dataclass
class World:
    spaceship: DesignerObject
    spaceship_speed: int
    left_key_active: bool
    right_key_active: bool
    aliens: list[DesignerObject]
    alien_rate: int     #when new aliens will spawn
    LIVES: int
    lasers: [DesignerObject]
    explosion: [DesignerObject]
    score: int
    counter: DesignerObject
    
    

def create_world() -> World:
    set_window_color('thistle')
    return World(create_spaceship(), SPACESHIP_SPEED, False, False, [], ALIEN_SPAWN, 5, [], [], 0, create_counter())

def create_spaceship()-> DesignerObject:
    # creates spaceship emoji
    spaceship = emoji("rocket")
    spaceship.y = get_height() * (1 / 3)
    spaceship.flip_x = True
    return spaceship

def create_alien()-> DesignerObject:
    alien = emoji('alien monster')
    alien.y = 0
    alien.x = random.randint(0, get_width())
    return alien

def create_laser(world: World)-> DesignerObject:
    laser = emoji('💥')
    laser.y = world.spaceship.y
    laser.x = world.spaceship.x
    return laser

def create_counter()-> DesignerObject:
    return text("white", "Score: 0   Lives: 5", 20, int(get_width()/2), 8)

def update_counter(world: World)-> DesignerObject:
    new = text('white', 'Score:' + str(world.score) + '  Lives:' + str(world.LIVES),20, get_width()/2, 8)
    destroy(world.counter)
    world.counter = new
    
def move_spaceship(world: World):
    # moves spaceship horizontally
    if world.left_key_active:
        world.spaceship.x -= world.spaceship_speed
    if world.right_key_active:
        world.spaceship.x += world.spaceship_speed
    # wraps spaceship around screen 
    if world.spaceship.x < 0:
        world.spaceship.x = get_width()
    elif world.spaceship.x > get_width():
        world.spaceship.x = 0
        
def move_aliens(world: World):   
    for alien in world.aliens:
        alien.y += ALIEN_SPEED
        if alien.y > get_height():
            alien.y = 0     # wraps alien around top
           
        if alien.x < 0:
            alien.x = get_width()
        elif alien.x > get_width():
            alien.x = 0
def move_laser(world: World):
    # makes laser move forward
    for laser in world.lasers:
        laser.y -= laser_speed
        
def spawn_aliens(world: World):
    # makes aliens appear
    world.alien_rate -= 5
    if world.alien_rate <= 0:
        world.aliens.append(create_alien())
        world.alien_rate = ALIEN_SPAWN
        
def press_key(world: World, key: str):
    # when key is pressed, move left or right
    if key == 'left':
        world.left_key_active = True
    if key == 'right':
        world.right_key_active = True
    if key == 'space': #when space is pressed, laser moves forward
        world.lasers.append(create_laser(world))
    
        
def release_key(world: World, key: str):
    # when key is released, spaceship stops moving
    if key == 'left':
        world.left_key_active = False
    if key == 'right':
        world.right_key_active = False
        
def create_explosion(world: World)-> DesignerObject:
    # when an explosion is created
    explosion = emoji('fire')
    explosion.y = world.spaceship.y
    explosion.x = world.spaceship.x
    return explosion

def explode_alien(world: World, alien: DesignerObject)->DesignerObject:
    #when an alien is exploded from collision 
    explosion = emoji('fire')
    explosion.y = alien.y
    explosion.x = alien.x
    return explosion

def collision (world: World):
    # when aliens and spaceship collide, explosion occurs
    alien_Numb = 0
    for alien in world.aliens:
        if colliding(world.spaceship, alien):
            world.LIVES -= 1
            world.explosion.append(create_explosion(world))
            world.aliens.pop(alien_Numb)
            destroy(alien)           
        alien_Numb += 1
        
def shrink_explosion(world: World):
    #makes explosion shrink and then disappear when colliding alien and spaceship
    explosion_numb = 0
    for explosion in world.explosion:
        explosion.scale_x -= .01
        explosion.scale_y -= .01
        if explosion.scale_x < 0: #if fire shrinks to 0, removed from list of explosions
            destroy(explosion)
            world.explosion.pop(explosion_numb)
        explosion_numb += 1
        
def hit_alien(world: World):
    #checks through each index value to see if the laser and alien collide, if they do collide, they're removed from the list using .pop()
    laser_Numb = 0
    for laser in world.lasers:
        alien_Numb = 0        
        for alien in world.aliens:      
            if colliding(laser, alien):
                world.explosion.append(explode_alien(world, alien))
                world.aliens.pop(alien_Numb)
                world.lasers.pop(laser_Numb)
                destroy(alien)
                destroy(laser)
                world.score+=1
            alien_Numb += 1    
        laser_Numb += 1
        
def game_over(world: World):
    if world.LIVES == 0:
        text('black', 'Game Over', 20, int(get_width()/2), int(get_height()/2))
        

when('starting', create_world)
when('done typing', release_key)
when('typing', press_key)
when('updating', move_spaceship)
when('updating', move_aliens)
when('updating', move_laser)
when('updating', spawn_aliens)
when('updating', collision)
when('updating', hit_alien)
when('updating', shrink_explosion)
when('updating', update_counter)
when('updating', game_over)

start()