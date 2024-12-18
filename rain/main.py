'''
Here's a problem: leetcode.com/problems/trapping-rain-water
"Given n non-negative integers representing an elevation map where the width of each bar is 1, 
compute how much water it can trap after raining."

I wanted to do a little visualization to check if my algorithm is correct.
Didn't bother to upload it yet, though.

'''
import pygame

WIN_SZ = (1000, 850)
CELL_SZ = 5

MAX_H = WIN_SZ[1] // CELL_SZ
MAX_L = WIN_SZ[0] // CELL_SZ


#generate test case
def gen():
    from random import randint as rand
    L = MAX_L
    
    res = []
    for i in range( L ):
        res.append( rand(0, MAX_H - 1) )

    return res


class Cell:
    def __init__(self, x, y, w, h, col='#000000'):
        self.rect = pygame.Rect( x, y, w, h )
        self.col = col

    def update(self, col):
        self.col = col

#generate a grid of rectangles representing the test case
def build_grid(heights):
    grid = [ [None for j in range( len(heights) )] for i in range( MAX_H ) ]

    for i in range( MAX_H ):
        for j in range( len(heights) ):
            
            cell = Cell( j*CELL_SZ, i*CELL_SZ, CELL_SZ, CELL_SZ )
            if MAX_H - i <= heights[j]:
                cell.update( '#666666' )

            grid[i][j] = cell

    return grid

# # # # # # # # # # # # # # # # # # # # # # # # # # #

'''
The main algorithm
It basically sequentially fills the terrain with water

Given the list of heights, sort it in decreasing order
Start from the heighest point. Fill the terain between it and the next second highest
Maitain what 'interval' of the terrain was already 'flooded'
Given next height, check if it's already flooded. If yes, go to the next one
If one, flood the terrain from this height to the closest end of the flooded interval
Calculate how many cells were filled with water

'''
def rain_qk( heights ):

    L = len( heights )
    sums = [ heights[0] ]
    for i in range( 1, L ):
        sums.append( sums[i-1] + heights[i] )

    pairs = [ (i, heights[i]) for i in range(L) ]
    pairs = sorted( pairs, key=lambda x:x[1], reverse=True )
    

    filled_left = pairs[0][0]
    filled_right = filled_left

    filled_num = 0

    for idx, h in pairs:

        beg = None
        end = None
        if idx < filled_left:
            beg = idx
            end = filled_left
        elif idx > filled_right:
            beg = filled_right
            end = idx
        else:
            continue

        filled_num += (end-beg-1) * (h) - (sums[end] - sums[beg] - heights[end])

        filled_left  = min( filled_left, beg )
        filled_right = max( filled_right, end )

    return filled_num

def draw_grid( display, grid ):
    for row in grid:
        for cell in row:
            pygame.draw.rect( display, cell.col, cell.rect )


#BruteForce visualization, it works like the main alg, but manually checks each cell for being filled with rain
def rain_vis( display, grid, heights ):
    L = len(heights)
    pairs = [ (i, heights[i]) for i in range( L ) ]
    pairs = sorted( pairs, key=lambda x:x[1], reverse=True )

    filled_num = 0

    filled_left = pairs[0][0]
    filled_right = filled_left

    clock = pygame.time.Clock()
    draw_grid( display, grid ) 
    pygame.display.update()

    for idx, h in pairs:

        if idx < filled_left:
            beg = idx
            end = filled_left
        elif idx > filled_right:
            beg = filled_right
            end = idx
        else:
            continue

        for j in range( beg+1, end ):
            for i in range( h ):
                cell = grid[ MAX_H-1-i ][j]
                if heights[j] <= i and i <= h:
                    cell.update( '#0000AA' )
                    filled_num += 1     

        clock.tick(2)
        draw_grid( display, grid )
        pygame.display.update()

        filled_left = min( filled_left, beg )
        filled_right = max( filled_right, end)       

    return filled_num

# # # # # # # # # # # # # # # # # # # # # # # # # # #
 
heights = gen()
L = len( heights )
grid = build_grid(heights)



display = pygame.display.set_mode(WIN_SZ)
qk_res = rain_qk( heights )
vis_res = rain_vis( display, grid, heights )

print( f'RESULTS EQUAL: {qk_res == vis_res}' )

for e in pygame.event.get():
    if e.type == pygame.QUIT:
        pygame.QUIT()

