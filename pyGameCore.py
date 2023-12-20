import raycast

# Example file showing a basic pygame "game loop"
import pygame
import random
import structures
import math
from pygame import Vector2

  

def RunGame():
  # pygame setup
  pygame.init()
  Bounds = (1280, 720)
  screen = pygame.display.set_mode(Bounds)
  pygame.display.set_caption("Ray Casting by Binh Nguyen")
  clock = pygame.time.Clock()
  running = True

  #camfldkjakY = 300
  rot = Vector2(0,0)
  Cam = raycast.Camera(Bounds[0]/2, Bounds[1]/2, Bounds[0])
  Cam.Set_Fov(45)

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
    s = pygame.Surface((Bounds[0],Bounds[1]))
    s.set_alpha(50)
    
    for i in listLines:
      pygame.draw.line(s, (255,255,255), pos, i, 1)
      #pygame.draw.circle(screen, 0x00ff0000, i, 6) #This lets us see the endpoints
    
    screen.blit(s,(0,0))
  def DrawLight(listLines):
    s = pygame.Surface((Bounds[0],Bounds[1]))
    s.set_alpha(50)
    pygame.draw.polygon(s, (255,255,255), listLines)
    screen.blit(s,(0,0))
      
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
#Main Loop
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
        PosOffset.x += move.x * 50
        PosOffset.y += move.y * 50
        #Cam.move(move, 100)
        #print(Cam.position)
    
      # fill the screen with a color to wipe away anything from last frame
      screen.fill(0x00000000)
      #Rotation of the character
      #This is for a orbit effect, only for demo of raycasting
      rot = Cam.RotationMatrix(rot.x, rot.y, .01)
      Cam.position.x = rot.x + PosOffset.x
      Cam.position.y = rot.y + PosOffset.y

      #Gets points the cam in the direction of the mouse
      #Cam.direction = Vector2(pygame.mouse.get_pos()[0] - Cam.position.x ,pygame.mouse.get_pos()[1] - Cam.position.y).normalize() 
      #Rotates the character based on the movement of the x direction of the mouse
      Cam.Rotate(pygame.mouse.get_rel()[0]/100)

      # RENDER YOUR GAME HERE
      #Draws the walls
      #DrawLines(MapManager.objects)
      pygame.draw.rect(screen, 0x0000ff00, pygame.Rect(0,Bounds[1]/2, Bounds[0],Bounds[1]/2))


      endpoints = Cam.RaycastSphere(MapManager.objects)
      Cam.Render(screen, MapManager.objects, endpoints)
      endpoints.append(Cam.position) #This is for the polygon stuff
      #Draw the raycast lines
      DrawLight(endpoints)
      #DrawRayCastLines(Cam.position,endpoints)
      #Draw circle pf players
      #pygame.draw.circle(screen, 0x00ffffff, Cam.position, 20)
      #Cam.Rotate(0.01)
      # flip() the display to put your work on screen

      pygame.display.flip()

      clock.tick(144)  # limits FPS to 60

  pygame.quit()