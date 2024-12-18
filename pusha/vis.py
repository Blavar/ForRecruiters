'''

I also scraped together a quick visualization for the tree from some preexisting code
It ain't pretty, but it more or less shows what the algorithm did with the data

'''

import pygame

import pandas as pd

from builder import Node, NumericNode, CategoricalNode, TerminalNode
from builder import builder

pygame.init()

'''
let's do a faster version:
for now i'd just like to visualize the given tree
so do a copy of what i need n thats it
'''

class Elem():
    def __init__(self, node, parent=None):
        self.val    = None
        self.parent = parent

        self.children = {}
        
        node_type = type(node)
        if node_type == NumericNode or node_type == CategoricalNode:
            self.val = node.attr
            for key, child in node.children.items():
                self.children[key] = Elem( child, self )
        elif node_type == TerminalNode:
            self.val = node.klass


        self.rect = pygame.Rect(0,0,0,0)

    def update(self, x, y, w, h):
        self.rect.update( x, y, w, h )

    def resize(self):
        if self.children:
            x, y, w, h = self.rect

            kw = w // len( self.children )
            for i, child in enumerate( self.children.values() ):
                child.rect.update( x + kw*i, y + h, kw, h )
                child.resize()


class Walnuts:
    def __init__(self, WIN_SZ, CELL_H):
        self.surface = pygame.Surface( WIN_SZ )
        self.font = pygame.font.Font( 'Helvetica.ttf', CELL_H//2 )
        self.CELL_H = CELL_H
    
    def draw( self, node ):
        
        text = self.font.render( str(node.val), False,  '#ffffff' )
        text_rect = text.get_rect( center = node.rect.center )
        pygame.draw.rect( self.surface, '#666666', text_rect, 1 )
        self.surface.blit( text, text_rect )

        for key, child in node.children.items():
            p = text_rect.midbottom
            q = child.rect.center

            mid = ( (p[0] + q[0])//2, (p[1] + q[1])//2 )

            key_text = self.font.render( key, False, '#aa0000' )
            key_text_rect = text.get_rect( center = mid )

            pygame.draw.line( self.surface, '#666666', p, q )
            self.surface.blit( key_text, key_text_rect )

            self.draw( child )




WIN_SZ = ( 1500, 750 )
CELL_H = 50


df = pd.read_csv( 'drug.csv')
DT_root = builder( df, df.columns.drop('Drug'), 'Drug' )
vis_root = Elem( DT_root )

vis_root.update( 0, 0, WIN_SZ[0], CELL_H )
vis_root.resize()


display = pygame.display.set_mode( WIN_SZ )
Paulie = Walnuts( WIN_SZ, CELL_H )

run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.QUIT()

    Paulie.draw( vis_root )
    display.blit( Paulie.surface, (0,0) )

    pygame.display.update()