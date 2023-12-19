from pygame.math import Vector2
import pygame
import math

#What do i have to do?
# Make a class for a wall
# Each wall should have 4 points
# Cast a ray to each of the points
# Measure the distance
#   (Should I be silly and do some linear algebra in that)
#   
class Manager:
  _instance = None
  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance

class Structure:

  def __init__(self, positionX=None, positionY=None, width=None, height=None, name=None):
    self.x = positionX
    self.y = positionY    
    self.x = width
    self.y = height
    self.name = name



class Map:

  def __init__(self, sizex, sizey):
    self.x = sizex
    self.y = sizey
    #self.grid = [[0] * sizex] * sizey
    self.objects = []

  

  def addWall(self, start, end):
    limitx = self.x
    limity = self.y
    start = Vector2(pygame.math.clamp(start.x, 0, limitx),pygame.math.clamp(start.y, 0, limity))
    end = Vector2(pygame.math.clamp(end.x, 0, limitx),pygame.math.clamp(end.y, 0, limity))

    self.objects.append(Wall(start, end))
    


class Wall:
  def __init__(self, start : Vector2, end : Vector2):
    self.start = start
    self.end = end
    self.length = math.dist(start, end) 

  def length(self):
    return self.length

  def setStart(self, start):
    self.start = start
    self.length = math.dist(start, end)   

  def setEnd(self, start):
    self.end = end
    self.length = math.dist(start, end) 
