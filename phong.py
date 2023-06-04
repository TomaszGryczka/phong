import pygame
from pygame.locals import *
from sphererenderer import SphereRenderer
import configparser

# Initialize Pygame
pygame.init()

# Define the screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load properties from the INI file
def load_properties_from_ini():
    config = configparser.ConfigParser()
    config.read('config.ini')

    light_color = tuple(map(int, config.get('Light', 'color').split(',')))
    ambient_intensity = config.getfloat('Light', 'k_a')
    diffuse_intensity = config.getfloat('Light', 'k_d')
    specular_intensity = config.getfloat('Light', 'k_s')
    specular_power = config.getint('Light', 'n')

    return light_color, ambient_intensity, diffuse_intensity, specular_intensity, specular_power

light_color, ambient_intensity, diffuse_intensity, specular_intensity, specular_power = load_properties_from_ini()

# Define light properties
light_position = pygame.Vector3(width // 2 - 400, height // 2 - 300, -500)  # Updated light position as a Vector3

# Create an instance of the SphereRenderer class
sphere = SphereRenderer((width // 2, height // 2, 0), 200, light_color, ambient_intensity, diffuse_intensity,
                        specular_intensity, specular_power)

# Main game loop
running = True
reload_file = False
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                light_position.y -= 30
            elif event.key == K_DOWN:
                light_position.y += 30
            elif event.key == K_LEFT:
                light_position.x -= 30
            elif event.key == K_RIGHT:
                light_position.x += 30
            elif event.key == K_l:
                reload_file = True
            elif event.key == K_1:
                sphere.silver_texture()
            elif event.key == K_2:
                sphere.wood_texture()
            elif event.key == K_3:
                sphere.brass_texture()
            elif event.key == K_4:
                sphere.plastic_texture()

    if reload_file:
        light_color, ambient_intensity, diffuse_intensity, specular_intensity, specular_power = load_properties_from_ini()
        sphere.update_light_properties(light_color, ambient_intensity, diffuse_intensity, specular_intensity, specular_power)
        reload_file = False

    # Clear the screen
    screen.fill(BLACK)

    # Set the updated light position in the SphereRenderer instance
    sphere.set_light_position(light_position)

    # Draw the sphere
    sphere.draw(screen)

    # Update the screen
    pygame.display.flip()
    clock.tick(30)

# Quit the program
pygame.quit()
