import pygame
class grid:
    size=(640,480)
    database=None
    columns=[]
    surface = None
    margin=(20,20)
    border=1
    column_list=[]
    dictionary={}
    def __init__(self,surface,Table,size):
        self.surface =surface
        self.Table = Table
        self.size = size
       # self.column_list = Table.columns
        #self.columns = Table.col_name
    def update(self):
        pygame.draw.rect(self.surface,(240,240,240),[self.margin,self.size],self.border)