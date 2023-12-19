import raycast

# Example file showing a basic pygame "game loop"
import pygame
import random
import structures
import math
from pygame import Vector2

# pygame setup
pygame.init()
Bounds = (1600, 900)
screen = pygame.display.set_mode(Bounds)
pygame.display.set_caption("Ray Casting by Binh Nguyen")
clock = pygame.time.Clock()
running = True

#camfldkjakY = 300
rot = Vector2(0,0)
Cam = raycast.Camera(500, 500, 270)
Cam.Set_Fov(90)

PosOffset = Vector2(500, 500)
#Maps
MapManager = structures.Map(Bounds[0],Bounds[1])
# Borders
  #Top Left -> Top Right 
MapManager.addWall(Vector2(0, 0), Vector2(Bounds[0],0))
  #Top Left -> Bottom Left
MapManager.addWall(Vector2(0, 0), Vector2(0,Bounds[1]-1))
  #Top Right -> Bottom Right
MapManager.addWall(Vector2(0, Bounds[1]), Vector2(Bounds[0],Bounds[1]))
  #Bottom Left -> Bottom Right
MapManager.addWall(Vector2(Bounds[0], 0), Vector2(Bounds[0],Bounds[1]))

#Structure
MapManager.addWall(Vector2(300, 100), Vector2(400,000))
MapManager.addWall(Vector2(700, 700), Vector2(800,500))
MapManager.addWall(Vector2(200, 100), Vector2(100, 200))
MapManager.addWall(Vector2(700, 100), Vector2(1000, 600))

Cam.direction = Vector2(1,-3)
def DrawLines(listLines):
  for i in listLines:
    pygame.draw.line(screen, 0x00ffffff, i.start, i.end, 5)
def DrawRayCastLines(pos, listLines):
  for i in listLines:
    pygame.draw.aaline(screen, 0x00ffffff, pos, i, 1)
    pygame.draw.circle(screen, 0x00ff0000, i, 6) #This lets us see the endpoints
def DrawLight(listLines):
  pygame.draw.polygon(screen, 0x00444444, listLines)
    
def DrawRay():
  closestmag = math.inf
  closestVec = Vector2(0,0) #This is a holder for the closest vector
  #Check every line
  for i in MapManager.objects:
    #Calculate the point of intersection
    endpoint = Cam.intersection(Cam.position, Cam.direction, i)
    #Check if there was a hit or not
    if endpoint != None:
      #Get the distance
      dist =  pygame.math.Vector2.distance_to(Cam.position, endpoint)
      #Check if it is the closest one to the line
      if dist < closestmag:
        #Swap the things
        closestVec = endpoint 
        closestmag = dist
  #Check if there was no hit at all
  if closestmag != math.inf:
    pygame.draw.line(screen, 0x00ffffff, Cam.position, closestVec, 5)  

def GetMovement():
  movement = Vector2(0.0,0.0)
  if event.type == pygame.KEYDOWN:
    if event.key  == pygame.K_w:
      print("Key W has been pressed")
      movement.y = -1.0
    if event.key  == pygame.K_s:
      print("Key S has been pressed")
      movement.y = 1.0
    if event.key  == pygame.K_a:
      print("Key A has been pressed")
      movement.x = -1.0
    if event.key  == pygame.K_d:
      print("Key D has been pressed")
      movement.x = 1.0
  #print(movement)
  return movement
    
while running:
    move = Vector2(0,0)
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False
      t = GetMovement()
      if t != Vector2(0,0):
        move = t
        print(move)

    if move != Vector2(0,0):
      PosOffset.x += move.x * 100
      PosOffset.y += move.y * 100
      #Cam.move(move, 100)
      #print(Cam.position)
  
    # fill the screen with a color to wipe away anything from last frame
    screen.fill(0x00000000)
    rot = Cam.RotationMatrix(rot.x, rot.y, .01)
    Cam.position.x = rot.x + PosOffset.x
    Cam.position.y = rot.y + PosOffset.y
    #print(Cam.position)

    # RENDER YOUR GAME HERE
    #Draws the walls
    DrawLines(MapManager.objects)
    Cam.direction = Vector2(-pygame.mouse.get_pos()[0] + Cam.position.x ,-pygame.mouse.get_pos()[1] + Cam.position.y).normalize() 
    endpoints = Cam.RaycastSphere(MapManager.objects)
    endpoints.append(Cam.position)
    #Draw the raycast lines
    DrawLight(endpoints)
    #DrawRayCastLines(Cam.position,endpoints)
    #Draw circle pf players
    pygame.draw.circle(screen, 0x00ffffff, Cam.position, 20)
    #Cam.Rotate(0.01)
    # flip() the display to put your work on screen

    pygame.display.flip()

    clock.tick(144)  # limits FPS to 60

pygame.quit()