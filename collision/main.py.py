'''
A little axis-aligned rectangle collsion and resolution simulation I put together around Halloween.
I'm putting it in here mainly because the code is so gruesome that it's actually funny.
It was another case of 'I wanna get some results fast so I'll do the most horrific implementation
known to man, despite the fact that were I to take some time to do it neatly, the overall
implementation time would be shorter AND the thing would work better'

Funny thing: the squares used to go through one another quite frequently (i think). I didn't really
know what the issue could be so I asked Google Gemini. It suggested lowering the time interval for the
simulation ticks. Lo-and-behold it actually worked. Beaten by a machine.

The algorithm is really better explained (and visually too) here:
https://www.youtube.com/watch?v=8JJ-4JgR7Dg

I was actually pretty close to getting it myself, still, the explanation in the video
proved to be invaluable. It'd probably take me a loooong time without it.


SIDENOTE: informative sources on axis-aligned rectangular (or square rather) collision resolution
were surprisingly sparse. Google either flooded me with the algorithm for the static case,
or provided me with posts from some arcane forums talking about matrices of differential equations.
Google was VASTLY overestimating me with the second class.

'''

import pygame.freetype
from vector import Vector

class Line:
    def __init__(self, p, q):
        self.p = p
        self.q = q

class Rect:
    def __init__(self, x=0, y=0, w=0, h=0, v=Vector(0,0)):
        self.set( x, y, w, h )
        self.v = v

    def set(self, x, y, w, h):
        self.pos = Vector(x, y)
        self.size = Vector(w, h)

    def to_tuple(self):
        return (self.pos.x, self.pos.y, self.size.x, self.size.y)
    
    def __str__(self):
        return f'x:{self.pos.x} y:{self.pos.y}\nw:{self.size.x} h:{self.size.y}\nv: {self.v}'

    def center(self):
        return Vector( self.pos.x + self.size.x//2, self.pos.y + self.size.y//2 )

##########################

class Collision:
    def __init__(self, norm, t):
        self.norm = norm
        self.t    = t

##########################


def DrawV(rect: Rect):
    DrawLine( display, '#0000FF', rect.center(), rect.center() + rect.v*4 )

#######################################



def DrawLine(display, color, p: Vector, q: Vector):
    pygame.draw.line( display, color, p.to_pair(), q.to_pair() )

#in a class DrawRect(rect, col="smth")
def DrawRect(display, color, rect:Rect):
    pygame.draw.rect( display, color, rect.to_tuple(), 2 )

##########################

##########################
    # MARGIN = 0.1
    # if v.x != 0:
    #     near.x = (rect.pos.x - p.x) / v.x
    #     far.x  = (rect.pos.x + rect.size.x - p.x) / v.x
    # else:
    #     if p.x >= rect.pos.x and p.x <= (rect.pos.x + rect.size.x):
    #         near.x = p.x
    #         far.x  = p.x
    #     else:
    #         return False
    
    # if v.y != 0:
    #     near.y = (rect.pos.y - p.y) / v.y
    #     far.y  = (rect.pos.y + rect.size.y - p.y) / v.y
    # else:
    #     if p.y >= rect.pos.y and p.y <= (rect.pos.y + rect.size.y):
    #         near.y = p.y
    #         far.y  = p.y
    #     else:
    #         return False

# v.x!= 0
# near, far
# else
#
#
#
#
#
import pygame
pygame.init()

win_sz = Vector(1000, 500)
display = pygame.display.set_mode( win_sz.to_pair() )




def ray_rect(p, v, rect: Rect):
    
    if v.x == 0 and v.y == 0:
        return None



    near = Vector()
    far  = Vector()
    if v.x != 0:
        near.x = (rect.pos.x - p.x) / v.x
        far.x  = (rect.pos.x + rect.size.x - p.x) / v.x

    if v.y != 0:
        near.y = (rect.pos.y - p.y) / v.y
        far.y  = (rect.pos.y + rect.size.y - p.y) / v.y

    if near.x > far.x:
        near.x, far.x = far.x, near.x
    if near.y > far.y:
        near.y, far.y = far.y, near.y


    norm = None
    t = None

    if v.x == 0:

        if p.x > rect.pos.x and p.x < rect.pos.x + rect.size.x:
            if p.y < rect.pos.y:
                norm = Vector( 0,-1 )
            else:
                norm = Vector( 0,+1)
            t = min( near.y, far.y )
            if 0 <= t and t <= 1:
                return Collision( norm, t )
            else:
                return None
        else:
            return None
    if v.y == 0:
 
        if p.y > rect.pos.y and p.y < rect.pos.y + rect.size.y:
            if p.x < rect.pos.x:
                norm = Vector( -1,0)
            else:
                norm = Vector( +1,0)
            t = min( near.x, far.x )
            if 0 <= t and t <= 1:
                return Collision( norm, t )
            else:
                return None
        else:
            return None




    if not( near.x <= far.y and near.y <= far.x):
        return None
    #print( f'p: {p.x}, {p.y}\nv: {v.x}, {v.y}\nnear: {near.x}, {near.y}\nfar: {far.x}, {far.y}' )

    if near.x >= near.y:
        t = near.x
        if p.x <= rect.pos.x:
            norm = Vector(-1,0)
        elif p.x >= rect.pos.x + rect.size.x:
            norm = Vector(+1,0)
    elif near.x <= near.y:
        t = near.y
        if p.y <= rect.pos.y:
            norm = Vector( 0,-1)
        elif p.y >= rect.pos.y + rect.size.y:
            norm = Vector( 0,+1)


    if 0 <= t and t <= 1:
        return Collision( norm, t )
    else:
        return None



#make it a function of two moving objects?
def rect_rect(A: Rect, B: Rect):


    #draw_v(A)
    #draw_v(B)


    rect_dummy = Rect( B.pos.x - A.size.x/2, B.pos.y - A.size.y/2, B.size.x + A.size.x, B.size.y + A.size.y)

    DrawRect(display, '#222222', rect_dummy)
    DrawLine(display, "#00FF00", A.pos, A.pos+A.v*10)

    return ray_rect( A.center(), A.v-B.v, rect_dummy )

    



#automatize according to a 
class Color:
    def __init__(self):
        Color.red = '#FF0000'
        Color.blue = '#0000FF'
        Color.white = '#FFFFFF'
        Color.gray = '#666666'

###########################



font = pygame.font.Font("Helvetica.ttf", 20)

clock = pygame.time.Clock()
# 
# UL = Vector(0,0)
# BR = Vector( win_sz.x, win_sz.y )
# mouse_tail = BR
# mouse_pos = Vector(0, 0)
# rect = Rect(100,100,100,100)
# 
black = "#000000"
white = "#FFFFFF"
red   = "#FF0000"
gray  = "#666666"

###########################



def gen_rect():
    from random import randint as rand

    margin_x = 100
    margin_y = 100

    dim = 50

    x = rand(0, win_sz.x - margin_x)
    y = rand(0, win_sz.y - margin_y)

    v = Vector( rand(0,2), rand(0,2) )

    return Rect( x, y, dim, dim, v )



walls = [Rect(0, 0, win_sz.x, 0), Rect(0,0,win_sz.y,0), Rect(win_sz.x,0,0,win_sz.y), Rect(0,win_sz.y,win_sz.x,0)]

Jigs = [gen_rect() for i in range(30)]

#Jigs = [Rect(0,0,100,100, Vector( 0,5 )), Rect(0,500,100,100, Vector(0,-5))]

##########################



###########################

run = True
pause = False
while run:


    dt = clock.tick(120)
    dt /= 120
    #dt /= 240

    colors = [white for i in range(len(Jigs))]

    keys = pygame.key.get_pressed()

    #events
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_p:
                pause = not pause
    

    

        # elif e.type == pygame.MOUSEMOTION:
        #     x, y = pygame.mouse.get_pos()
        #     A.pos.x = x
        #     A.pos.y = y


    #drawing

    #ENGINE
    if not pause:

        display.fill(black)

        for i in range( len(Jigs) ):
            jig = Jigs[i]

            dtdt = dt

            for j in range( i+1, len(Jigs)):

                jig2 = Jigs[j]

                collision = rect_rect( jig, jig2 )
                if collision:

                    colors[i] = red
                    colors[j] = red

                    jig.pos += jig.v * collision.t * (dt*0.99)
                    jig2.pos += jig2.v * collision.t * (dt*0.99)
                    #print(f"COLLISION i:{i} j:{j}")
                    #print(collision.norm)
                    
                    norm = collision.norm

                    if norm.x != 0:
                        jig.v.x, jig2.v.x = jig2.v.x, jig.v.x
                    elif norm.y != 0:
                        jig.v.y, jig2.v.y = jig2.v.y, jig.v.y
                    # if norm.x != 0:
                    #     if jig.v.x * norm.x < 0:
                    #         jig.v.x *= -1
                    #     if jig2.v.x * norm.x > 0:
                    #         jig2.v.x *= -1
                    # elif norm.y != 0:
                    #     if jig.v.y * norm.y < 0:
                    #         jig.v.y *= -1
                    #     if jig2.v.y * norm.y > 0:
                    #         jig2.v.y *= -1



                    jig.pos += -jig.v*(1-collision.t)
                    jig2.pos += -jig2.v*(1-collision.t)

            #bounds
            if jig.pos.x < 0:
                jig.v.x *= -1
                jig.pos.x = 0 
            elif jig.pos.x + jig.size.x > win_sz.x:
                jig.v.x *= -1
                jig.pos.x = win_sz.x - jig.size.x
            elif jig.pos.y < 0:
                jig.v.y *= -1
                jig.pos.y = 0
            elif jig.pos.y + jig.size.y > win_sz.y:
                jig.v.y *= -1
                jig.pos.y = win_sz.y - jig.size.y

            jig.pos += jig.v
            
        #draw the velocity vector for A


        for i, jig in enumerate(Jigs):

            DrawRect( display, colors[i], jig )
            text = font.render(f'{i}', True, black, white)
            display.blit( text, jig.pos.to_pair() )


        ##############################


        # rect_col = gray
        # collision = ray_rect( mouse_tail, mouse_pos, rect )
        # if collision:
        #     rect_col = red
        #     print( collision.norm )

        # #draw a line
        # DrawLine(display, white, mouse_tail, mouse_pos)
        # DrawRect(display, rect_col, rect)
        pygame.display.update()

