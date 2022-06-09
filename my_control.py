# Welcome to CARLA ARVY's control.


# ==============================================================================
# -- Find carla module ---------------------------------------------------------
# ==============================================================================

import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


# ==============================================================================
# -- Imports -------------------------------------------------------------------
# ==============================================================================

import carla
from carla import ColorConverter as cc
import random

try:
    import pygame
    from pygame.locals import K_UP # throttle
    from pygame.locals import K_DOWN # reverse 
    from pygame.locals import K_LEFT #left
    from pygame.locals import K_RIGHT # right
    from pygame.locals import K_ESCAPE # -
    from pygame.locals import K_SPACE # brake
    from pygame.locals import K_r # for reseting the game 
    from pygame.locals import K_s # for recording the images
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

try:
    import numpy as np
except ImportError:
    raise RuntimeError('cannot import numpy, make sure numpy package is installed')

import time
from cv2 import cv2
from PIL import Image

# ==============================================================================
# -- constants -----------------------------------------------------------------
# ==============================================================================

IM_WIDTH = 640
IM_HEIGHT = 480
K = 1
# ==============================================================================
# -- World ---------------------------------------------------------------------
# ==============================================================================
'''
DESCRIPTION: 
    this class initiaties a world and spawn a vehicle (by default bmw grandtourer)

'''
class World():
    
    collision_hist = []; #collision history
    def __init__(self, vehicle="grandtourer", record_enabled=False):
        
        self.actor_list = [] 
        self.vehicle = vehicle
        self.surface = pygame.Surface((IM_WIDTH, IM_HEIGHT))
        self.image = None
        self.record = record_enabled
        self.previous_clock = 0

        # initiating world
        self.client = carla.Client("localhost", 2000)
        self.client.set_timeout(10.0)
        self.world = self.client.get_world()
        self.map = self.world.get_map()
        
        # reseting the world
        self.reset(vehicle)
        #time.sleep(3.0)
        
   

    # this method spawns the vehicle (by default grandtourer)
    def spawn_vehicle(self, vehicle):
        # getting all of the blueprints
        self.blueprint_library = self.world.get_blueprint_library()
        
        # making the blueprint of vehicle
        self.vehicle_blueprint = self.blueprint_library.filter(vehicle)[0]


        # getting a random spawn point from the map 
        spawn_point = random.choice(self.world.get_map().get_spawn_points())

        # spawning the vehicle
        self.vehicle = self.world.spawn_actor(self.vehicle_blueprint, spawn_point)
        self.actor_list.append(self.vehicle)


    def spawn_camera_sensor(self):

        # setting up the camera sensor
        camera_blueprint = self.blueprint_library.find("sensor.camera.rgb")
        camera_blueprint.set_attribute("image_size_x", f"{IM_WIDTH}")
        camera_blueprint.set_attribute("image_size_y", f"{IM_HEIGHT}")
        camera_blueprint.set_attribute("fov", "110")

        # getting camera spawn point 
        camera_spawn_point = carla.Transform(carla.Location(x=2.5, z = 0.7))

        # spawning camera sensor
        self.camera_sensor = self.world.spawn_actor(camera_blueprint, camera_spawn_point, attach_to=self.vehicle)
        self.actor_list.append(self.camera_sensor)

    def CollisionSensor(self):

        # spawning collision sensor
        CollisionSensor_blueprint = self.blueprint_library.find('sensor.other.collision')
        self.CollisionSensor =self.world.spawn_actor(CollisionSensor_blueprint, carla.Transform(), attach_to=self.vehicle)
        self.actor_list.append(self.CollisionSensor)

    def reset(self, vehicle):
        # this method spawns the vehicle and all of the sensors
        
        self.actor_list = []

        # spawning the actors 
        self.spawn_vehicle(vehicle)
        self.spawn_camera_sensor()

        # showing and rendering the image
        self.camera_sensor.listen(lambda data: self.process_image(data))

        # using collision sensor's data (event is each collision)
        self.CollisionSensor()
        self.CollisionSensor.listen(lambda event: self.collision_data(event))


    def image_renderer(self, display):
        display.blit(self.surface, (0, 0))
        


    def collision_data(self, event):
        
        #adding each collision to collision history
        self.collision_hist.append(event)

        if len(self.collision_hist) != 0:
            reward =-1*len(self.collision_hist)
            print(reward)
    

    def image_recorder(self, clock):
        self.image.save(f"raw_data\\raw_image_{clock.get_time()}.jpg")

            


    def process_image(self, image):
        image.convert(cc.Raw)
        array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
        array = np.reshape(array, (image.height, image.width, 4))
        array = array[:, :, :3]
        array = array[:, :, ::-1]
        self.image = Image.fromarray(array)
        self.surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))



# ==============================================================================
# -- Keyboard Control ----------------------------------------------------------
# ==============================================================================
'''
DESCRIPTION: 
    defining the key map

'''
class KeyboardControl(object):
    def __init__(self, world):
        self.control = carla.VehicleControl()
        self.steer_cache = 0.0

    def control_keys(self, world, clock):
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    self.control.gear = 1
                    print("up key pressed")
                elif event.key == K_DOWN:
                    self.control.gear = -1
                    print("down key pressed")
                elif event.key == K_LEFT:
                    print("left key pressed")
                elif event.key == K_RIGHT:
                    print("right key pressed")
                elif event.key == K_r:
                    print("r key pressed")
                    world.reset("grandtourer")
                elif event.key == K_ESCAPE:
                    print("esc key pressed")
                elif event.key == K_s:
                    world.record = not world.record
                    print("s key pressed")
                    
                    

        if isinstance(self.control, carla.VehicleControl):
            self.vehicle_control(pygame.key.get_pressed(), clock.get_time())
            self.control.reverse = self.control.gear < 0
        world.vehicle.apply_control(self.control)
        

    def vehicle_control(self, keys, milliseconds):

        # controlling the throttle
        self.control.throttle = 1.0 if keys[K_UP] or keys[K_DOWN] else 0.0

        # controlling the steering
        steer_increment = 5e-4 * milliseconds
        if keys[K_LEFT]:
            self.steer_cache -= steer_increment
        elif keys[K_RIGHT]:
            self.steer_cache += steer_increment
        else:
            self.steer_cache = 0.0
        self.steer_cache = min(0.7, max(-0.7, self.steer_cache))
        self.control.steer = round(self.steer_cache, 1)

        # controllign the brake and hand brake 
        self.control.brake = 1.0 if keys[K_SPACE] else 0.0


# ==============================================================================
# -- Game Loop -----------------------------------------------------------------
# ==============================================================================
'''
DESCRIPTION: 
    this part is for the gameloop and user interface (image rendering)

'''

def game_loop():
    
    # initializing pygame
    pygame.init()
    pygame.font.init()
    world = None
    # image size
    size = IM_WIDTH, IM_HEIGHT

    # color balck rgb
    black = 0, 0, 0

    try: 
        # setting up the display
        display = pygame.display.set_mode(size,
                pygame.HWSURFACE | pygame.DOUBLEBUF)
        display.fill(black)

        # initializing the world
        world = World()
        controller = KeyboardControl(world)
        
        clock = pygame.time.Clock()
        record_time = 0
        while True:

            clock.tick_busy_loop(500)

            if controller.control_keys(world, clock):
                return

            world.image_renderer(display)
            if world.record:
                print(clock.get_time())
                if int(clock.get_time())-int(record_time) > 3000:
                    print("i'm saving")
                    world.image_recorder(clock)
                    record_time = int(clock.get_time())
            pygame.display.flip()

        
    except:
        print("couldn't initialize world")
    
    



# ==============================================================================
# -- Main ----------------------------------------------------------------------
# ==============================================================================

game_loop()
 