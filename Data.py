import pygame

Heros_Dic={"Big_Hero" :
               {"DAMAGE_RATE":90 ,
                "SPEED_RATE":10,
                "HEALTH":100,
                "BULLET":None ,
                'IMAGE':pygame.image.load('Images/Big_Hero.gif')},
           "knight" :{
               "DAMAGE_RATE":90 ,
               "SPEED_RATE":10,
               "HEALTH":100,
               "BULLET":"Sword",
                'IMAGE':pygame.image.load('Images/Knight.gif')}
           }

Bullets_Dic={"Sword" : {"DAMAGE" : 30 , "SPEED" : 40 , "RANGE" : 3 }}

image = {'Big_Hero':pygame.image.load('Images/Big_Hero.gif'), }