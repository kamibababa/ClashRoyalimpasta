import Util

mapMat = Util.buildGrid('map.txt')

class Grid:
  def __init__(self):
    self.height = len(mapMat)
    self.width = len(mapMat[0])
    self.mat = [[0 for j in range(self.width)] for i in range(self.height)]
    for i in range(self.height):
      for j in range(self.width):
        if (mapMat[i][j] in ['d', 'l']):
          self.mat[i][j] = 1
  def get(self, r, c):
    return self.mat[r][c]

g = Grid()