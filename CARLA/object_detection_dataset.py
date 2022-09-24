print(" control keys: ")
print(" up arrow key = throttle \n down arrow key = reverse \n right arrow key = steer right \n left arrow key = steer left \n space bar = brake")
print(" 'd' key = object detection \n 'a' key = autopilot \n 's' key = save dataset \n ")

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
    from pygame.locals import K_UP
    from pygame.locals import K_DOWN
    from pygame.locals import K_LEFT
    from pygame.locals import K_RIGHT
    from pygame.locals import K_a
    from pygame.locals import K_s
    from pygame.locals import K_d
    from pygame.locals import K_ESCAPE
    from pygame.locals import K_SPACE
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

try:
    import numpy as np
except ImportError:
    raise RuntimeError('cannot import numpy, make sure numpy package is installed')

import time
from cv2 import cv2
from PIL import Image
from io import StringIO

import torch 
from matplotlib import pyplot as plt 

# ==============================================================================
# -- constants -----------------------------------------------------------------
# ==============================================================================

IM_WIDTH = 640
IM_HEIGHT = 480

# ==============================================================================
# -- World ---------------------------------------------------------------------
# ==============================================================================

'''
DESCRIPTION: 
    this class initiaties a world and spawn a vehicle (by default bmw grandtourer)
'''

class World():

    def __init__(self, vehicle="grandtourer"):
        

        # initializing a list of all of the actors in the world - assigning attributes to self  
        self.vehicle = vehicle
        self.surface = pygame.Surface((IM_WIDTH, IM_HEIGHT))

        # initiating world
        self.client = carla.Client("localhost", 2000)
        self.client.set_timeout(10.0)
        self.world = self.client.get_world()
        self.map = self.world.get_map()
        
        # reseting the world
        self.reset(vehicle)

    def spawn_vehicle(self, vehicle):
        # this method spawns the vehicle (by default grandtourer)

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


    def reset(self, vehicle):
        # destorying everything in the world
        self.actor_list = []

        # re-spawning the actors 
        self.spawn_vehicle(vehicle)
        self.spawn_camera_sensor()

        # showing and rendering the image
        self.camera_sensor.listen(lambda data: self.process_image(data))

    def image_renderer(self, display):
        # renders the image onto the screen
        display.blit(self.surface, (0, 0))

    def process_image(self, image):
        # getting the image on display and converting it to surface 
        image.convert(cc.Raw)
        array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
        array = np.reshape(array, (image.height, image.width, 4))
        array = array[:, :, :3]
        array = array[:, :, ::-1]
        self.image = array
        self.surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))

    def exit(self):
        for actor in self.actor_list: 
            destroyed_sucessfully = actor.destroy()
            print(actor)
            print(destroyed_sucessfully)

# ==============================================================================
# -- Keyboard Control ----------------------------------------------------------
# ==============================================================================

'''
DESCRIPTION: 
    defining the key map
'''

class KeyboardControl(object):
    def __init__(self, model):

        self.model = model
        self.control = carla.VehicleControl()
        self.steer_cache = 0.0
        self.toggle_autopilot = False
        self.toggle_datasave = False 
    def control_keys(self, world, clock):
        
        for event in pygame.event.get():
            # what to do with each key pressed 
            if event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    self.control.gear = 1
                    print("Throttle")
                elif event.key == K_DOWN:
                    self.control.gear = -1
                    print("Reverse")
                elif event.key == K_LEFT:
                    print("Turn left")
                elif event.key == K_RIGHT:
                    print("Turn right")
                elif event.key == K_ESCAPE:
                    self.exit_game(world)
                    print("Exit")
                elif event.key == K_SPACE:
                    print("Brake")
                elif event.key == K_a:
                    self.autopilot(world)
                    print("Autopilot toggled: ", self.toggle_autopilot)
                elif event.key == K_s:
                    self.toggle_datasave = not self.toggle_datasave
                    print("Dataset toggled: ", self.toggle_datasave)
                elif event.key == K_d:
                    print("detection initialized")
                    image = np.squeeze(self.model(world.image).render())
                    image = Image.fromarray(image)
                    image.save("detected_picture.jpg")
                    print("image saved")
        
        # using the control function of vehicle 
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

    def exit_game(self, world):
        world.exit()
        pygame.quite()
    
    def autopilot(self, world): 
        # turns autopilot on/off 
        self.toggle_autopilot = not self.toggle_autopilot
        if self.toggle_autopilot: 
            world.vehicle.set_autopilot(1)
        else: 
            world.vehicle.set_autopilot(0) 
        
    def get_dataset(self, world, temp_time):
        if self.toggle_datasave:
            pygame.image.save(world.surface, str(temp_time) + '.png')
        else: 
            pass

# ==============================================================================
# -- Game Loop -----------------------------------------------------------------
# ==============================================================================

'''
DESCRIPTION: 
    this part is for the gameloop and user interface (image rendering)
'''

def game_loop():

    # initilizing the model
    try:
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    except:
        print('something is wrong here ')

    # initializing pygame
    pygame.init()
    pygame.font.init()
    world = None
    # image size
    size = IM_WIDTH, IM_HEIGHT

    # color balck rgb
    black = 0, 0, 0

    temp_time_initial = 0
    temp_time_final = 0
    try: 
        # setting up the display
        display = pygame.display.set_mode(size,
                pygame.HWSURFACE | pygame.DOUBLEBUF)
        display.fill(black)
        
        # initializing the world
        world = World()
        controller = KeyboardControl(model)
        clock = pygame.time.Clock()

        while True:
            clock.tick_busy_loop(60)
            temp_time_final += clock.get_time()

            # using the contorller 
            if controller.control_keys(world, clock):
                return
            
            if temp_time_final - temp_time_initial > 3000:
                temp_time_initial = temp_time_final
                controller.get_dataset(world, temp_time_final)
            
            if temp_time_final > 5000000:
                controller.exit_game()
            

            # rendering the image 
            world.image_renderer(display)
            pygame.display.flip()
            


    except:
        print("couldn't initialize world")
    

# ==============================================================================
# -- Main ----------------------------------------------------------------------
# ==============================================================================

game_loop()
