# Tetris.py
# Jonatan Sundqvist
# January 11 2017


import pygame
import random

from math import pi as π


class Vector(object):
  
  def __init__(self, x, y):
    self.x = x
    self.y = y
  
  def tuple(self):
    return (self.x, self.y)

  def list(self):
    return [self.x, self.y]

  def __add__(self, other):
    return Vector(self.x + other.x, self.y + other.y)

  def __sub__(self, other):
    return Vector(self.x - other.x, self.y - other.y)

  def hadamard(self, other):
    return Vector(self.x * other.x, self.y * other.y)

  @staticmethod
  def dotwise(f, a, b):
    return Vector(f(a.x, b.x), f(a.y, b.y))


class Piece(object):
  
  # All possible shape
  # TODO: Rename
  possible = [[[True], [True], [True], [True]],

              [[True, True],
               [True, True]],

              [[True, False],
               [True, False],
               [True, False],
               [True, True]],

              [[True, True],
               [True, False],
               [True, False],
               [True, False]],

              [[True,  False],
               [True,  True],
               [False, True]],

              [[False, True],
               [True,  True],
               [False, True]]]


  def __init__(self, pos, colour, shape):
    self.pos    = pos    # Position of the top left corner of the piece's bounding box
    self.colour = colour #
    self.shape  = shape  #
  
  def copy(self):
    return Piece(self.pos, self.colour, self.shape)

  def render(self, surface, resolution):
    size   = Vector.dotwise(lambda a, b: a*b, self.size(), resolution) #
    origin = self.pos.hadamard(resolution)
    for (x, column) in enumerate(self.shape):
      for y, slot in enumerate(column):
        if slot:
          pygame.draw.rect(surface, self.colour, pygame.Rect((origin + Vector(x,y).hadamard(resolution)).tuple(), resolution.tuple()))
    return surface

  def size(self):
    return Vector(len(self.shape), len(self.shape[0]))

  def rotate(self, quarters):
    ''' Rotate the piece by some number of clockwise quarter-turns'''
    # TODO: Check collisions on rotation
    for _ in range(quarters % 4):
      self.shape = list([list(reversed(col)) for col in list(zip(*self.shape))])

  def move(self, delta):
    self.pos = self.pos + delta
    return self

  def collide(self, other):
    xspanA, yspanA = zip(self.pos.tuple(),  (self.pos  + self.size()).tuple())
    xspanB, yspanB = zip(other.pos.tuple(), (other.pos + other.size()).tuple())
    print(*intersect(xspanA, yspanA))
    print(*intersect(xspanB, yspanB))
    return any(self.shape[x-self.pos.x][y-self.pos.y] and other.shape[x-other.pos.x][y-other.pos.y] for x in range(*intersect(xspanA, xspanB)) for y in range(*intersect(yspanA, yspanB)))

  @staticmethod
  def random(width):
    shape  = random.choice(Piece.possible)
    pos    = Vector(random.randint(0, width - 1), -len(shape[0]))
    colour = tuple(random.randint(0, 255) for _ in range(3))
    return Piece(pos, colour, shape)


class Tetris(object):


  def __init__(self):
    # Parameters
    self.size       = Vector(14, 22) #
    self.resolution = Vector(20, 20) # Pixels per square (X, Y)
    self.canvasSize = Vector.dotwise(lambda a, b: a*b, self.size, self.resolution) #
     
    self.shouldQuit = False

    # Game Logic
    self.board = [[False for _ in range(self.size.y)] for _ in range(self.size.x)]
    self.piece = None
    self.history = [] # TODO: Use deque

    # Pygame
    pygame.init()
    self.screen = pygame.display.set_mode(self.canvasSize.tuple())
    self.clock  = pygame.time.Clock()
    pygame.display.set_caption('Shameless Arcade Clone')

  def play(self):
    #
    while not self.shouldQuit:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.shouldQuit = True

        if event.type == pygame.KEYDOWN:

          if self.piece is not None:
            if event.key == pygame.K_LEFT:
              if self.piece.pos.x > 0:
                self.piece.move(Vector(-1, 0))
            elif event.key == pygame.K_RIGHT:
              if (self.piece.pos.x + self.piece.size().x) < self.size.x:
                self.piece.move(Vector( 1, 0))
            elif event.key == pygame.K_UP:
              self.piece.rotate(3)
              # self.piece.move(Vector(0, -1))
            elif event.key == pygame.K_DOWN:
              self.piece.rotate(1)
              # self.piece.move(Vector(0,  1))
            elif event.key == pygame.K_SPACE:
              print('Space')

      self.tick()

      self.screen.fill((255,255,255))

      # font = pygame.font.SysFont('Calibri', 25, True, False)
      # text = font.render('WIP', True, (255, 80, 200))
      # self.screen.blit(text, [0,0])

      if self.piece is not None:
        self.piece.render(self.screen, self.resolution)

      for piece in self.history:
        piece.render(self.screen, self.resolution)

      pygame.display.flip()
      self.clock.tick(12) # TODO: De-couple input FPS from tick and graphics FPS
    pygame.quit()

  def tick(self):
    if self.piece is None:
      # Spawn new random piece
      # TODO: Randomise
      self.piece = Piece.random(self.size.x)
    else:
      # Let it fall
      # TODO: Collision checks
      collided = any(self.piece.copy().move(Vector(0,1)).collide(other) for other in self.history)
      if ((self.piece.pos.y + self.piece.size().y) < self.size.y) and (not collided):
        self.piece.move(Vector(0, 1))
        pass
      else:
        # Piece has landed
        # TODO: Check complete rows
        # TODO: 'Stamp' piece onto board (?)
        self.history.insert(0, self.piece)
        self.piece = None
  def render(self):
    pass


def intersect(a, b):
  ordered = sorted(a + b)
  return ordered[1:3] if min(a, b) != tuple(ordered[0:2]) else (0,0)


def main():
  game = Tetris()
  game.play()


if __name__ == '__main__':
  main()