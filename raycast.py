from pygame.math import Vector2
import pygame
import math
class Ray:
  def __init__(self, x, y, direction, _len = None):
    self.x = x
    self.y = y
    self.position = Vector2(x, y)
    #This has to be a tuple
    self.direction = direction.normalize()
    if _len != None:
      self.length = 100.0
    else:
      self.length = _len
    self.endpoint = self.position + (self.length * self.direction)
  def set_length(self, _len):
    self.length = _len
    self.endpoint = self.position + direction.scale_to_length(_len)
  

class Camera:
  def __init__ (self, posx, posy, resolution):

    self.position = Vector2(posx, posy)
    self.resolution = resolution  #How many rays we will be drawing within the fov


    self.direction = Vector2(1,0)
    self.fov = 360
    
  def move(self, direction, speed):
    self.position = Vector2(self.position.x + direction.x * speed,self.position.y + direction.y * speed)
    #print(direction)
    #self.position.y = self.position.y + direction.y * speed
  def Set_Fov(self, fov):
    self.fov = fov

  def intersection(self, pos, direc, wall):
    #https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_wall
    #Ray 
    x3 = pos.x
    y3 = pos.y

    x4 = direc.x + x3
    y4 = direc.y + y3

    #Line Segment
    x1 = wall.start.x
    y1 = wall.start.y
    #End
    x2 = wall.end.x
    y2 = wall.end.y

    den = (( x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4))
    if den == 0:
      return None
    tnumo = ((x1-x3) * (y3-y4)) - ((y1 - y3) * (x3 - x4))
    t = tnumo / den
    unumo = ((x1-x3) * (y1-y2)) - ((y1 - y3) * (x1 - x2))
    u = unumo/ den
    # -> intersection point (x, y) 

    if t > 0 and t < 1 and u > 0:
      #this means that there is an intersection
      return Vector2(x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    return None
  def Rotate(self, turnAmount):
    #x = self.dirx
    #y = self.diry
    self.direction = Vector2((self.direction.x * math.cos(turnAmount)) - (self.direction.y * math.sin(turnAmount)), (self.direction.x * math.sin(turnAmount) )+ (self.direction.y * math.cos(turnAmount)))

    self.dirx = self.direction.x
    self.diry = self.direction.y

  def RotationMatrix(self, x, y, turnAmount):
    return Vector2((x * math.cos(turnAmount)) - (y * math.sin(turnAmount)), (x * math.sin(turnAmount) )+ (y * math.cos(turnAmount)))

  def FindGrid(self, direction: Vector2):
    
    
    pass

  def GetEndPoints(self, ray, _map):
    closestmag = math.inf
    closestVec = Vector2(0,0) #This is a holder for the closest vector
    #Check every line
    for i in _map:
      #Calculate the point of intersection
      endpoint = self.intersection(self.position, ray, i)
      #Check if there was a hit or not
      if endpoint != None:
        #Get the distance
        dist =  pygame.math.Vector2.distance_to(self.position, endpoint)
        #Check if it is the closest one to the line
        if dist < closestmag:
          #Swap the things
          closestVec = endpoint 
          closestmag = dist
    #Check if there was no hit at all
    if closestmag != math.inf:
      return closestVec


  def RaycastSphere(self, _map):
    #How much we are moving per degree
    fovRad =  math.radians(self.fov)
    anglestep = -fovRad / self.resolution

    start = self.RotationMatrix(self.direction.x, self.direction.y, fovRad/2)
    i = 0
    ray = start

    EndPoints = []
    while i < self.resolution:
      endpoint = self.GetEndPoints(ray, _map)
      if endpoint != None:
        EndPoints.append(endpoint)

      i += 1
      ray = self.RotationMatrix(ray.x, ray.y, anglestep)

    return EndPoints
  def Render(self, screen, _map, endpoints) -> list:
    j = screen.get_width()
    for i in endpoints:
      dist = self.position.distance_to(i)
      
      #print(f" Distance: {dist}")
      maxBright = pygame.Color("white")
      
      #The 1000 for the distance limit is arbitrary
      brightness = maxBright.lerp(0, pygame.math.clamp(dist,0.0, 1000.0)/ 1000.0)

      start = Vector2(j, math.sqrt(dist) *5) 
      print(f"Start: {start}")
      end = Vector2(j, screen.get_height() - math.sqrt(dist)*5)
      print(f"End: {end}")

      #print(f" Brightness: {brightness}")
      pygame.draw.line(screen, brightness, start, end)
      j -= 1
               

c = Camera(10, 10, 90)