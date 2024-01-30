# generate a 6x6 grid
cell_width = 60
D = 6
thickness = 3
width, height = 800, 600

grid_length = (cell_width + thickness)*D
locx, locy = (width - grid_length)//2, (height-grid_length)//2


# print([(locx + cell_width*x, locy + cell_width*(x%6)) for x in range(6*6)])
print([((x%6), (x//6)) for x in range(6*6)])

