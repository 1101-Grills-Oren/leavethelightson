#!/usr/bin/env python
""" pygame.examples.aliens

Shows a mini game where you have to defend against aliens.

What does it show you about pygame?

* pg.sprite, the difference between Sprite and Group.
* dirty rectangle optimization for processing for speed.
* music with pg.mixer.music, including fadeout
* sound effects with pg.Sound
* event processing, keyboard handling, QUIT handling.
* a main loop frame limited with a game clock from pg.time.Clock
* fullscreen switching.


Controls
--------

* Left and right arrows to move.
* Space bar to shoot
* f key to toggle between fullscreen.

"""

import os
import random
from typing import List

# import basic pygame modules
import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from numpy import array
# see if we can load more than standard BMP
if not pg.image.get_extended():
    raise SystemExit("Sorry, extended image module required")


# game constants
MAX_SHOTS = 2  # most player bullets onscreen
ALIEN_ODDS = 22  # chances a new alien appears
BOMB_ODDS = 60  # chances a new bomb will drop
ALIEN_RELOAD = 12  # frames between new aliens
SCREENRECT = pg.Rect(0, 0, 940, 480)
SCORE = 0


FRAMERATE=120


main_dir = os.path.split(os.path.abspath(__file__))[0]
CAMERA_POS=[0,0]
CAMERA_SCALE=2
CAMERA_BOUNDARIES=(0,0,0,0)
rooms={}

global OPENGL_CAMERA_SHIFT
OPENGL_CAMERA_SHIFT=[0,0]

def toBinary(value:int,length=0):
    return ''.join([str(int(value/(2**x))%2) for x in range(length)])

def fromBinary(value):
    retval=0
    for i in value:
        retval*=2
        retval+=int(i)
    return retval

def load_image(file):
    """loads an image, prepares it for play"""
    file = os.path.join(main_dir, "data", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert()


def load_sound(file):
    """because pygame can be compiled without mixer."""
    if not pg.mixer:
        return None
    file = os.path.join(main_dir, "data", file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print(f"Warning, unable to load, {file}")
    return None
global winfo
winfo=0

def surface_array(surfaceobj):
    x=[]
    w=surfaceobj.get_width()
    h=surfaceobj.get_height()
    for j in range(h):
        for i in range(w):
            b=surfaceobj.get_at((i,j))
            for c in range(3):
                x.append(b[c])
            x.append([255 if b!=(0,0,0,255) else 0][0])
    #for i in range(w):
    #    for j in range(h):
    #        x.append(1)
    return {'data':x,'size':[w,h]}


def loadTexture(texture2):

    textData = array(texture2['data'])
    textID = glGenTextures(1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glBindTexture(GL_TEXTURE_2D, textID)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_FUNC,GL_NOTEQUAL)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_MODE,GL_COMPARE_REF_TO_TEXTURE)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture2['size'][0], texture2['size'][1], 0, GL_RGBA, GL_UNSIGNED_BYTE, textData)
    return textID

def drawQuad(centerX, centerY,width,height, textureID, shouldCenter=0):
    global OPENGL_CAMERA_SHIFT
    width=width/20
    height=height/20
    #print(textureID,centerX,centerY,width,height)
    centerX=centerX/20-15+width+OPENGL_CAMERA_SHIFT[0]
    centerY=-centerY/20+8-height+OPENGL_CAMERA_SHIFT[1]
    if shouldCenter:
        OPENGL_CAMERA_SHIFT=[OPENGL_CAMERA_SHIFT[0]-centerX,OPENGL_CAMERA_SHIFT[1]-centerY]
    #print(centerX,centerY)
    verts = ((width, height), (width,-height), (-width,-height), (-width,height))
    texts = ((1, 0), (1, 1), (0, 1), (0, 0))
    surf = (0, 1, 2, 3)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textureID)
    glBegin(GL_QUADS)
    for i in surf:
        glTexCoord2f(texts[i][0], texts[i][1])
        glVertex2f(centerX + verts[i][0], centerY + verts[i][1])
    glEnd()
    
    glDisable(GL_TEXTURE_2D)
import math
def drawQuadRoated(centerX, centerY,width,height, textureID,rotation=0, shouldCenter=0):
    global OPENGL_CAMERA_SHIFT
    width=width/20
    height=height/20
    #print(textureID,centerX,centerY,width,height)
    centerX=centerX/20-15+width+OPENGL_CAMERA_SHIFT[0]
    centerY=-centerY/20+8-height+OPENGL_CAMERA_SHIFT[1]
    if shouldCenter:
        OPENGL_CAMERA_SHIFT=[OPENGL_CAMERA_SHIFT[0]-centerX,OPENGL_CAMERA_SHIFT[1]-centerY]
    #print(centerX,centerY)
    x=(width*math.cos(rotation)+height*math.sin(rotation), width*math.sin(rotation)-height*math.cos(rotation))
    verts = ((x[0],x[1]),
             (x[1],-x[0]),
             (-x[0],-x[1]),
             (-x[1],x[0])
            )
    texts = ((1, 0), (1, 1), (0, 1), (0, 0))
    surf = (0, 1, 2, 3)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textureID)
    glBegin(GL_QUADS)
    for i in surf:
        glTexCoord2f(texts[i][0], texts[i][1])
        glVertex2f(centerX + verts[i][0], centerY + verts[i][1])
    glEnd()
    
    glDisable(GL_TEXTURE_2D)

def drawQuadStatic(centerX, centerY,width,height, textureID):
    width=width
    height=height
    #print(textureID,centerX,centerY,width,height)
    centerX=centerX
    centerY=-centerY
    verts = ((width, height), (width,-height), (-width,-height), (-width,height))
    texts = ((1, 0), (1, 1), (0, 1), (0, 0))
    surf = (0, 1, 2, 3)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textureID)
    glBegin(GL_QUADS)
    for i in surf:
        glTexCoord2f(texts[i][0], texts[i][1])
        glVertex2f(centerX + verts[i][0], centerY + verts[i][1])
    glEnd()
    
    glDisable(GL_TEXTURE_2D)

#16 render width
def setup():
    gluPerspective(45, (940 / 480), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -40)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
def drawAll(all):
    glClear(GL_DEPTH_BUFFER_BIT| GL_COLOR_BUFFER_BIT)
    for i in all:
        if((type(i)!=Player)):
            if 'imgid' in i.__dict__:
                if i.imgid!=None:
                    if(i.rect.left>-400):
                        if(i.rect.top>-200):
                            if(i.rect.left+i.rect.size[0])<900+200:
                                if(i.rect.top+i.rect.size[1])<459.574468+200:
                                    if 'rotation' in i.__dict__:
                                        drawQuadRoated(i.rect.left, i.rect.top,i.rect.size[0],i.rect.size[1], i.imgid,i.rotation)
                                    else:
                                        drawQuad(i.rect.left, i.rect.top,i.rect.size[0],i.rect.size[1], i.imgid)
    for i in all:
        if((type(i)==Player)):
            if 'imgid' in i.__dict__:
                if i.imgid!=None:
                    drawQuad(i.rect.left, i.rect.top,i.rect.size[0],i.rect.size[1], i.imgid,1)
def drawGUI(elements):
    for i in elements:
        if 'imgid' in i.__dict__:
            if i.imgid!=None:    
                drawQuadStatic(i.rect.left/20-8*4, i.rect.top/20-4.08510638*4,i.rect.size[0]/20,i.rect.size[1]/20, i.imgid)





# Each type of game object gets an init and an update function.
# The update function is called once per frame, and it is when each object should
# change its current position and state.
#
# The Player object actually gets a "move" function instead of update,
# since it is passed extra information about the keyboard.
def isColliding(a,b):
    return (a[0]<b[2])&(a[2]>b[0])&(a[1]<b[3])&(a[3]>b[1])
global newParticles
class Player(pg.sprite.Sprite):
    speed = 10
    images: List[pg.Surface] = []
    textureIds: List[int] = []
    mass=2
    width=20
    height=35
    gravity=[0,1]
    def __init__(self, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        for i in range(self.images.__len__()):
            self.images[i]=pg.transform.scale(self.images[i],(20*CAMERA_SCALE,35*CAMERA_SCALE))
        self.image = pg.transform.scale(self.images[0],(20*CAMERA_SCALE/2,35*CAMERA_SCALE/2))
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.facing = -1
        self.velocity=[0,0]
        self.pos=[200,100]
        self.onGround=0
        self.attributes={'barrels':2,'health':10,'maxhealth':10,'stepsize':10}
        self.animationFrame=0
        self.savePos=self.pos
        self.anticorruptroomandpos=(0,[0,-50])
        self.immunityFrames=0
        self.friction=0.1
        self.imgid=self.textureIds[0]
        self.imgidy=None
        self.firecooldown=0
        self.shotsleft=0
        self.wasOnGround=0
        self.target=None
    def move(self, direction):
        if direction:
            self.facing = direction
        #self.rect.move_ip(direction * self.speed, 0)
        if direction < 0:
            self.image = self.images[0]
        elif direction > 0:
            self.image = self.images[1]
        self.rect = self.image.get_rect()
        #self.rect.top = self.origtop# - (self.rect.left // self.bounce % 2)
    def accelerateHoriz(self,amount):
        self.animationFrame+=0.1
        if(self.animationFrame>=4):
            self.animationFrame=0
        self.velocity[0]+=(self.friction*2)*amount/self.mass
        if self.onGround:
            if amount < 0:
                self.image = self.images[int(self.animationFrame)]
                self.imgid = self.textureIds[int(self.animationFrame)]
            elif amount > 0:
                self.image = self.images[5+int(self.animationFrame)]
                self.imgid = self.textureIds[5+int(self.animationFrame)]
        else:
            if amount < 0:
                self.image = self.images[4+int(self.animationFrame/4)]
                self.imgid = self.textureIds[4+int(self.animationFrame/4)]
            elif amount > 0:
                self.image = self.images[9+int(self.animationFrame/4)]
                self.imgid = self.textureIds[9+int(self.animationFrame/4)]
        #self.rect = self.image.get_rect()
    def applyFriction(self,amount):
        self.velocity[0]-=self.velocity[0]*amount/self.mass*60/FRAMERATE
        self.velocity[1]-=self.velocity[1]*amount/self.mass*60/FRAMERATE
        if(self.velocity[0]**2<0.01):
            self.velocity[0]=0
        if(self.velocity[1]**2<0.01):
            self.velocity[1]=0
    def applyGravity(self):
        self.velocity[0]+=self.gravity[0]*(60/FRAMERATE)**0.5
        self.velocity[1]+=self.gravity[1]*(60/FRAMERATE)**0.5
    def applyVelocity(self):
        self.pos[0]+=self.velocity[0]
        self.pos[1]+=self.velocity[1]
    def jump(self):
        if(self.onGround):
            self.velocity[1]=-13
    def collideAndMove(self,objs,platformobjs=[]):
        objs2=[]
        self.rect.left-=self.rect.size[0]*2
        self.rect.top-=self.rect.size[1]*2
        size1=self.rect.size
        self.rect.size=(self.rect.size[0]*5,self.rect.size[1]*5)
        for i in pg.sprite.spritecollide(self,objs,0):
            objs2.append(i)
        objs=objs2
        self.rect.size=size1
        resetVelocity=[0,0]
        hazardCollision=0
        sendBack=0
        self.pos[0]+=self.velocity[0]*1.5*60/FRAMERATE
        playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
        if(self.velocity[1]<0):
            playerpos=(self.pos[0],self.pos[1]+self.attributes['stepsize'],self.pos[0]+self.width,self.pos[1]+self.height)
        if(self.onGround):
            playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height-self.attributes['stepsize'])
        
        
        farthestDownRoofPosition=-10000000000000000000000000000000000
        for obj in objs:    
            objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
            if(isColliding(objpos,playerpos)):
        
                objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)        
                if(self.velocity[0]<0):
                    self.pos[0]=max(objpos[2],self.pos[0])
                    resetVelocity[0]=1
                elif(self.velocity[0]>0):
                    self.pos[0]=min(self.pos[0],objpos[0]-self.width)
                    resetVelocity[0]=1
                if(type(obj)==Hazard):
                    hazardCollision=obj.damage
                    sendBack=obj.sendBack
        if(resetVelocity[0]):
            self.velocity[0]=0
        canStandOnObjs=[]
        playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
        for obj in platformobjs:
            objpos=(obj.pos[0],obj.pos[1]-self.height+1,obj.pos[0]+obj.width,obj.pos[1]+obj.height-self.height+1)
            if(isColliding(objpos,playerpos)):
                canStandOnObjs.append(obj)
        
        wasOnGround=self.onGround
        self.onGround=0
        leftStairsPos=-100
        self.pos[1]+=self.velocity[1]*1.5*60/FRAMERATE
        playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
        for obj in objs:
            
            objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
            objposb=(obj.pos[0],obj.pos[1]-self.attributes['stepsize'],obj.pos[0]+obj.width,obj.pos[1]+obj.height-self.attributes['stepsize'])
            if(isColliding(objpos,playerpos)):
                objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)        
                if(self.velocity[1]<0)|(farthestDownRoofPosition!=-10000000000000000000000000000000000):
                    farthestDownRoofPosition=max(objpos[3],farthestDownRoofPosition)
                    self.pos[1]=farthestDownRoofPosition+1
                    resetVelocity[1]=1
                elif(self.velocity[1]>0)|((self.velocity[1]==0)&(self.onGround)):
                    self.onGround=1
                    self.pos[1]=min(self.pos[1],objpos[1]-self.height)
                    resetVelocity[1]=1
                if(type(obj)==Hazard):
                    hazardCollision=obj.damage
                    sendBack=obj.sendBack
            if(wasOnGround):
                if not self.onGround:
                    if obj.width==2:
                        if(isColliding(objposb,playerpos)):
                            if self.velocity[0]>0:
                                self.onGround=1
                                self.pos[1]=(self.pos[1],objpos[1]-self.height)[1]
                                self.velocity[1]=0
                            elif self.velocity[0]<0:
                                self.onGround=1
                                self.pos[1]=(self.pos[1],objpos[1]-self.height)[1]
                                self.velocity[1]=0
        if(resetVelocity[1]):
            self.velocity[1]=0
        for obj in canStandOnObjs:
            
            objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
            if(isColliding(objpos,playerpos)):
                
                if(self.velocity[1]<0):
                    self.pos[1]=objpos[3]
                    resetVelocity[1]=1
                else:
                    self.onGround=1
                    self.pos[1]=objpos[1]-self.height
                    resetVelocity[1]=1
                if(type(obj)==Hazard):
                    hazardCollision=obj.damage
                    sendBack=obj.sendBack
        if self.immunityFrames==-1:
            if(hazardCollision!=0):
                self.immunityFrames=90
                self.attributes['health']-=hazardCollision
                for i in range(42):
                    newParticles.append([[self.pos[0]+self.width/2-5,self.pos[1]+self.height/2-5],[random.random()*8-4,random.random()*4-8-self.velocity[1]*4],[0,0.5],0,[5+random.random()*5]*2,120+240*random.random(),2*random.random()-1,2])
                if(sendBack):
                    self.velocity=[0,0]
                    self.pos=self.savePos
                
        if(resetVelocity[1]):
            self.velocity[1]=0
        #    if pg.mixer and boom_sound is not None:
        #        boom_sound.play()
        #    Explosion(alien, all)
        #    Explosion(player, all)
        #    SCORE = SCORE + 1
        #    player.kill()
    def updateRooms(self,groups):
        allobjs=groups[5]
        roomslist=groups[3]
        allrooms=groups[4]
        pos=(self.pos[0],self.pos[1],self.pos[0]+self.height,self.pos[1]+self.height)
        for obj in roomslist:
            if obj.disabled==0:
                pos2=(obj.pos[0]-winfo.current_w*0.75,obj.pos[1]-winfo.current_h*0.75,obj.pos[0]+obj.width+winfo.current_w*0.75,obj.pos[1]+obj.height+winfo.current_h*0.75)
                if(isColliding(pos,pos2)):
                    obj.triggerBuildRoom(groups[0],groups[1],groups[2],groups[3],groups[4],groups[5])
        for obj in allrooms:
            pos2=(obj.pos[0]-winfo.current_w*0.75,obj.pos[1]-winfo.current_h*0.75,obj.pos[0]+obj.width+winfo.current_w*0.75,obj.pos[1]+obj.height+winfo.current_h*0.75)
            if not (isColliding(pos,pos2)):
                obj.unbuildRoom(groups[5],roomslist)
                #obj.unbuildRoom(allobjs,roomslist)
    def updateFrame(self):
        b=pg.display.get_window_size()
        CAMERA_POS[0]=(CAMERA_POS[0]*1+(self.pos[0]+self.width/2-b[0]/2)*9)/10+b[0]*(1-1/CAMERA_SCALE)/2
        CAMERA_POS[1]=(CAMERA_POS[1]*1+(self.pos[1]+self.height/2-b[1]/2)*9)/10+b[1]*(1-1/CAMERA_SCALE)/2
        self.rect.left=(self.pos[0]-CAMERA_POS[0])*CAMERA_SCALE
        self.rect.top=(self.pos[1]-CAMERA_POS[1])*CAMERA_SCALE
    #def gunpos(self):
    #    pos = self.facing * self.gun_offset + self.rect.centerx
    #    return pos, self.rect.top
    def fixNoRooms(self,objs):
        if objs[4].__len__()==0:
            self.attributes['health']-=5
            self.velocity=[0,0]
            self.pos=self.savePos
            rooms[self.anticorruptroomandpos[0]].buildRoom(self.anticorruptroomandpos[1],*objs)
    def immunityFramesVisuals(self):
        if(self.immunityFrames>-1):
            if(self.immunityFrames%30>=15):
                if(self.imgid!=None):
                    self.imgidy=self.imgid+1-1
                    self.imgid=None
                
            elif(self.immunityFrames%30>=0):
                if(self.imgid==None):
                    self.imgid=self.imgidy+1-1
                    self.imgidy=None
            self.immunityFrames-=1
        if(self.immunityFrames==0):
            for i in self.images:
                i.set_alpha(255)
    def updateb(self,collideobjs,horiz,vert,fire):
        self.accelerateHoriz(horiz*5/self.mass)
        if(vert):
            self.jump()
        #self.applyVelocity()
        if(self.onGround):
            self.shotsleft=self.attributes['barrels']
            self.firecooldown-=1
        if(fire)&(self.firecooldown<=0):
            self.fire()
        
        self.collideAndMove(collideobjs[0],collideobjs[1])
        self.applyGravity()
        self.friction=0.5*self.onGround+0.1
        self.applyFriction(self.friction)
        
        self.firecooldown-=1
        self.updateRooms(collideobjs)
        self.updateFrame()
        self.updateSafePoint(collideobjs[5],collideobjs[4])
        self.fixNoRooms(collideobjs)
        self.immunityFramesVisuals()
    def fire(self):
        if(self.shotsleft!=0):
            pos1=pg.mouse.get_pos()
            pos1=[pos1[0]-winfo.current_w/2,pos1[1]-winfo.current_h/2]
            x=pos1[0]/((pos1[0]**2+pos1[1]**2)**0.5)
            y=pos1[1]/((pos1[0]**2+pos1[1]**2)**0.5)
            newParticles.append([[self.pos[0]+self.width/2+x*10,self.pos[1]+self.height/2+y*10],[x*50,y*50],[0,0],0,[5,5],1000,0.1,0])
            self.firecooldown=10*FRAMERATE/60
            self.velocity[0]/=(1+(x**2)**0.5)
            self.velocity[1]/=5
            self.velocity[0]-=x*20
            self.velocity[1]-=y*20
            self.shotsleft-=1
            
    def updateSafePoint(self,objs,rooms):
        for obj in objs:
            if type(obj)==SaveMarker:
                if(isColliding((self.pos[0],self.pos[1],self.pos[0]+self.height,self.pos[1]+self.height),(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height))):
                    self.savePos=[obj.pos[0]+30-self.width/2,obj.pos[1]+40-self.height]
                    for i in rooms:
                        if i.id==obj.roomid:
                            self.anticorruptroomandpos=(i.type,i.pos)



class Enemeh(pg.sprite.Sprite):
    speed = 10
    images: List[pg.Surface] = []
    textureIds: List[int] = []
    mass=2
    width=20
    height=35
    gravity=[0,1]
    def __init__(self,x,y, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        for i in range(self.images.__len__()):
            self.images[i]=pg.transform.scale(self.images[i],(20*CAMERA_SCALE,35*CAMERA_SCALE))
        self.image = pg.transform.scale(self.images[0],(20*CAMERA_SCALE/2,35*CAMERA_SCALE/2))
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.facing = -1
        self.velocity=[0,0]
        self.pos=[x,y]
        self.onGround=0
        self.attributes={'barrels':2,'health':10,'maxhealth':10,'stepsize':10}
        self.animationFrame=0
        self.savePos=self.pos
        self.anticorruptroomandpos=(0,[0,-50])
        self.immunityFrames=0
        self.friction=0.1
        self.imgid=self.textureIds[0]
        self.imgidy=None
        self.firecooldown=0
        self.shotsleft=0
        self.wasOnGround=0
    def move(self, direction):
        if direction:
            self.facing = direction
        #self.rect.move_ip(direction * self.speed, 0)
        if direction < 0:
            self.image = self.images[0]
        elif direction > 0:
            self.image = self.images[1]
        self.rect = self.image.get_rect()
    def updatec(self,collideobjs,player):
        move=0
        jump=0
        if(player.pos[0]<self.pos[0]-50):
            move=-1
        if(player.pos[0]>self.pos[0]+50):
            move=1
        if(self.velocity[0]==0):
            jump=1-(not not move)
        self.updateb(collideobjs,move,jump,0)
        #self.rect.top = self.origtop# - (self.rect.left // self.bounce % 2)
    def accelerateHoriz(self,amount):
        self.animationFrame+=0.1
        if(self.animationFrame>=4):
            self.animationFrame=0
        self.velocity[0]+=(self.friction*2)*amount/self.mass
        if self.onGround:
            if amount < 0:
                self.image = self.images[int(self.animationFrame)]
                self.imgid = self.textureIds[int(self.animationFrame)]
            elif amount > 0:
                self.image = self.images[5+int(self.animationFrame)]
                self.imgid = self.textureIds[5+int(self.animationFrame)]
        else:
            if amount < 0:
                self.image = self.images[4+int(self.animationFrame/4)]
                self.imgid = self.textureIds[4+int(self.animationFrame/4)]
            elif amount > 0:
                self.image = self.images[9+int(self.animationFrame/4)]
                self.imgid = self.textureIds[9+int(self.animationFrame/4)]
        #self.rect = self.image.get_rect()
    def applyFriction(self,amount):
        self.velocity[0]-=self.velocity[0]*amount/self.mass*60/FRAMERATE
        self.velocity[1]-=self.velocity[1]*amount/self.mass*60/FRAMERATE
        if(self.velocity[0]**2<0.01):
            self.velocity[0]=0
        if(self.velocity[1]**2<0.01):
            self.velocity[1]=0
    def applyGravity(self):
        self.velocity[0]+=self.gravity[0]*(60/FRAMERATE)**0.5
        self.velocity[1]+=self.gravity[1]*(60/FRAMERATE)**0.5
    def applyVelocity(self):
        self.pos[0]+=self.velocity[0]
        self.pos[1]+=self.velocity[1]
    def jump(self):
        if(self.onGround):
            self.velocity[1]=-13
    def collideAndMove(self,objs,platformobjs=[]):
        objs2=[]
        self.rect.left-=self.rect.size[0]*2
        self.rect.top-=self.rect.size[1]*2
        size1=self.rect.size
        self.rect.size=(self.rect.size[0]*5,self.rect.size[1]*5)
        for i in pg.sprite.spritecollide(self,objs,0):
            objs2.append(i)
        objs=objs2
        self.rect.size=size1
        resetVelocity=[0,0]
        hazardCollision=0
        sendBack=0
        self.pos[0]+=self.velocity[0]*1.5*60/FRAMERATE
        playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
        if(self.velocity[1]<0):
            playerpos=(self.pos[0],self.pos[1]+self.attributes['stepsize'],self.pos[0]+self.width,self.pos[1]+self.height)
        if(self.onGround):
            playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height-self.attributes['stepsize'])
        
        
        farthestDownRoofPosition=-10000000000000000000000000000000000
        for obj in objs:    
            objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
            if(isColliding(objpos,playerpos)):
        
                objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)        
                if(self.velocity[0]<0):
                    self.pos[0]=max(objpos[2],self.pos[0])
                    resetVelocity[0]=1
                elif(self.velocity[0]>0):
                    self.pos[0]=min(self.pos[0],objpos[0]-self.width)
                    resetVelocity[0]=1
                if(type(obj)==Hazard):
                    hazardCollision=obj.damage
                    sendBack=obj.sendBack
        if(resetVelocity[0]):
            self.velocity[0]=0
        canStandOnObjs=[]
        playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
        for obj in platformobjs:
            objpos=(obj.pos[0],obj.pos[1]-self.height+1,obj.pos[0]+obj.width,obj.pos[1]+obj.height-self.height+1)
            if(isColliding(objpos,playerpos)):
                canStandOnObjs.append(obj)
        
        wasOnGround=self.onGround
        self.onGround=0
        leftStairsPos=-100
        self.pos[1]+=self.velocity[1]*1.5*60/FRAMERATE
        playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
        for obj in objs:
            
            objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
            objposb=(obj.pos[0],obj.pos[1]-self.attributes['stepsize'],obj.pos[0]+obj.width,obj.pos[1]+obj.height-self.attributes['stepsize'])
            if(isColliding(objpos,playerpos)):
                objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)        
                if(self.velocity[1]<0)|(farthestDownRoofPosition!=-10000000000000000000000000000000000):
                    farthestDownRoofPosition=max(objpos[3],farthestDownRoofPosition)
                    self.pos[1]=farthestDownRoofPosition+1
                    resetVelocity[1]=1
                elif(self.velocity[1]>0)|((self.velocity[1]==0)&(self.onGround)):
                    self.onGround=1
                    self.pos[1]=min(self.pos[1],objpos[1]-self.height)
                    resetVelocity[1]=1
                if(type(obj)==Hazard):
                    hazardCollision=obj.damage
                    sendBack=obj.sendBack
            if(wasOnGround):
                if not self.onGround:
                    if obj.width==2:
                        if(isColliding(objposb,playerpos)):
                            if self.velocity[0]>0:
                                self.onGround=1
                                self.pos[1]=(self.pos[1],objpos[1]-self.height)[1]
                                self.velocity[1]=0
                            elif self.velocity[0]<0:
                                self.onGround=1
                                self.pos[1]=(self.pos[1],objpos[1]-self.height)[1]
                                self.velocity[1]=0
        if(resetVelocity[1]):
            self.velocity[1]=0
        for obj in canStandOnObjs:
            
            objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
            if(isColliding(objpos,playerpos)):
                
                if(self.velocity[1]<0):
                    self.pos[1]=objpos[3]
                    resetVelocity[1]=1
                else:
                    self.onGround=1
                    self.pos[1]=objpos[1]-self.height
                    resetVelocity[1]=1
                if(type(obj)==Hazard):
                    hazardCollision=obj.damage
                    sendBack=obj.sendBack
        if self.immunityFrames==-1:
            if(hazardCollision!=0):
                self.immunityFrames=90
                self.attributes['health']-=hazardCollision
                for i in range(42):
                    newParticles.append([[self.pos[0]+self.width/2-5,self.pos[1]+self.height/2-5],[random.random()*8-4,random.random()*4-8-self.velocity[1]*4],[0,0.5],0,[5+random.random()*5]*2,120+240*random.random(),2*random.random()-1,2])
                if(sendBack):
                    self.velocity=[0,0]
                    self.pos=self.savePos
                
        if(resetVelocity[1]):
            self.velocity[1]=0
        #    if pg.mixer and boom_sound is not None:
        #        boom_sound.play()
        #    Explosion(alien, all)
        #    Explosion(player, all)
        #    SCORE = SCORE + 1
        #    player.kill()
    def updateFrame(self):
        self.rect.left=(self.pos[0]-CAMERA_POS[0])*CAMERA_SCALE
        self.rect.top=(self.pos[1]-CAMERA_POS[1])*CAMERA_SCALE
        if(self.attributes['health']<=0):
            self.kill()
    #def gunpos(self):
    #    pos = self.facing * self.gun_offset + self.rect.centerx
    #    return pos, self.rect.top
    def immunityFramesVisuals(self):
        if(self.immunityFrames>-1):
            if(self.immunityFrames%30>=15):
                if(self.imgid!=None):
                    self.imgidy=self.imgid+1-1
                    self.imgid=None
                
            elif(self.immunityFrames%30>=0):
                if(self.imgid==None):
                    self.imgid=self.imgidy+1-1
                    self.imgidy=None
            self.immunityFrames-=1
        if(self.immunityFrames==0):
            for i in self.images:
                i.set_alpha(255)
    def updateb(self,collideobjs,horiz,vert,fire):
        self.accelerateHoriz(horiz*5/self.mass)
        if(vert):
            self.jump()
        #self.applyVelocity()
        if(self.onGround):
            self.shotsleft=self.attributes['barrels']
            self.firecooldown-=1
        if(fire)&(self.firecooldown<=0):
            self.fire()
        
        self.collideAndMove(collideobjs[0],collideobjs[1])
        self.applyGravity()
        self.friction=0.5*self.onGround+0.1
        self.applyFriction(self.friction)
        
        self.firecooldown-=1
        self.updateFrame()
        self.immunityFramesVisuals()
    def fire(self):
        if(self.shotsleft!=0):
            pos1=pg.mouse.get_pos()
            pos1=[pos1[0]-winfo.current_w/2,pos1[1]-winfo.current_h/2]
            x=pos1[0]/((pos1[0]**2+pos1[1]**2)**0.5)
            y=pos1[1]/((pos1[0]**2+pos1[1]**2)**0.5)
            newParticles.append([[self.pos[0]+self.width/2+x*10,self.pos[1]+self.height/2+y*10],[x*50,y*50],[0,0],0,[5,5],1000,0.1,0])
            self.firecooldown=10*FRAMERATE/60
            self.velocity[0]/=(1+(x**2)**0.5)
            self.velocity[1]/=5
            self.velocity[0]-=x*20
            self.velocity[1]-=y*20
            self.shotsleft-=1























class PhysicsParticle(pg.sprite.Sprite):
    speed = 10
    images: List[pg.Surface] = []
    textureIds: List[int] = []
    mass=2
    def __init__(self,pos,velocity,gravity,particle,size,life,spin,shouldBounce,shouldStick, *groups):
        pg.sprite.Sprite.__init__(self, *groups)
        #for i in range(self.images.__len__()):
        #    self.images[i]=pg.transform.scale(self.images[i],(20*CAMERA_SCALE,35*CAMERA_SCALE))
        self.image = pg.transform.scale(self.images[particle],(20*CAMERA_SCALE/2,35*CAMERA_SCALE/2))
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.rect.size=size
        self.velocity=velocity
        self.gravity=gravity
        self.width=size[0]
        self.height=size[1]
        self.spin=spin
        self.shouldBounce=shouldBounce
        self.shouldStick=shouldStick
        self.pos=pos
        self.onGround=0
        self.friction=0.1
        self.imgid=self.textureIds[particle]
        self.imgidy=None
        self.life=life
        self.stuck=0
        self.rotation=0
    def applyFriction(self,amount):
        self.velocity[0]-=self.velocity[0]*amount/self.mass*60/FRAMERATE
        self.velocity[1]-=self.velocity[1]*amount/self.mass*60/FRAMERATE
        if(self.velocity[0]**2<0.01):
            self.velocity[0]=0
        if(self.velocity[1]**2<0.01):
            self.velocity[1]=0
    def applyGravity(self):
        self.velocity[0]+=self.gravity[0]*60/FRAMERATE
        self.velocity[1]+=self.gravity[1]*60/FRAMERATE
    def collideAndMove(self,objs):
        resetVelocity=[0,0]
        hazardCollision=0
        sendBack=0
        self.pos[0]+=self.velocity[0]*1.5*60/FRAMERATE
        playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
        self.rect.size=[self.rect.size[0]+((self.velocity[0]*1.5*60/FRAMERATE)**2)**0.5,self.rect.size[1]]
        for obj in pg.sprite.spritecollide(self,objs,0):
                objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                if(self.velocity[0]<0):
                    self.pos[0]=max(objpos[2],self.pos[0])
                    resetVelocity[0]=1
                elif(self.velocity[0]>0):
                    self.pos[0]=min(self.pos[0],objpos[0]-self.width)
                    resetVelocity[0]=1
        if(resetVelocity[0]):
            if(self.shouldStick):
                self.stuck=1
                if(self.velocity[0]>0):
                    self.pos[0]+=self.width
                else:
                    self.pos[0]-=self.width
            self.velocity[0]=0
        self.pos[1]+=self.velocity[1]*1.5*60/FRAMERATE
        playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
        self.onGround=0
        self.updateFrame()
        self.rect.size=[self.width,self.rect.size[1]+((self.velocity[1]*1.5*60/FRAMERATE)**2)**0.5]
        for obj in pg.sprite.spritecollide(self,objs,0):
                objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                if(self.velocity[1]<0):
                    self.pos[1]=max(objpos[3],self.pos[1])
                    resetVelocity[1]=1
                elif(self.velocity[1]>0):
                    self.pos[1]=min(self.pos[1],objpos[1]-self.height)
                    resetVelocity[1]=1
                    self.onGround=1
        if(resetVelocity[1]):
            if(self.shouldStick):
                
                if(self.velocity[1]>0):
                    self.pos[1]+=self.height
                else:
                    self.pos[1]-=self.height
                self.stuck=1
            
            if(self.shouldBounce):
                self.velocity[1]=-self.velocity[1]/2
            else:
                self.velocity[1]=0
        self.rect.size=[self.width,self.height]
        if(type(self.spin) in [float,int]):
            self.rotation+=self.spin*(60/FRAMERATE)
        #    if pg.mixer and boom_sound is not None:
        #        boom_sound.play()
        #    Explosion(alien, all)
        #    Explosion(player, all)
        #    SCORE = SCORE + 1
        #    player.kill()
    def updateFrame(self):
        self.rect.left=(self.pos[0]-CAMERA_POS[0])*CAMERA_SCALE
        self.rect.top=(self.pos[1]-CAMERA_POS[1])*CAMERA_SCALE
    def updateb(self,collideobjs):
        self.life-=(3-self.stuck*2)/3
        if(self.life<=0):
            self.kill()
        else:
            if(self.stuck==0):
                self.collideAndMove(collideobjs[0])
                self.applyGravity()
                self.friction=0.5*self.onGround+0.1
                self.applyFriction(self.friction)
            self.updateFrame()
            if(self.stuck):
                self.velocity=[0,0]
    








































class Wall(pg.sprite.Sprite):
    images: List[pg.Surface] = []
    textureIds: List[int] = []
    def __init__(self,x,y,w,h,v,rid,*groups):
        
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = pg.transform.scale(self.images[v], (20,20))
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.pos=[x,y]
        self.width=w
        self.height=h
        self.roomid=rid
        self.imgid=self.textureIds[v]
        self.rect.size=[20,20]
    def update(self):
        self.rect = self.rect.clamp(SCREENRECT)
        self.rect.left=(self.pos[0]-CAMERA_POS[0])*CAMERA_SCALE
        self.rect.top=(self.pos[1]-CAMERA_POS[1])*CAMERA_SCALE

class Hazard(pg.sprite.Sprite):
    images: List[pg.Surface] = []
    textureIds: List[int] = []
    def __init__(self,x,y,w,h,rid,imgid,*groups):
        
        pg.sprite.Sprite.__init__(self, *groups)
        self.image = pg.transform.scale(self.images[imgid], (w,h))
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.pos=[x,y]
        self.width=w
        self.height=h
        self.roomid=rid
        self.damage=1
        self.sendBack=1
        self.imgid=self.textureIds[imgid]
        self.rect.size=[self.width,self.height]
    def update(self):
        self.rect = self.rect.clamp(SCREENRECT)
        self.rect.left=(self.pos[0]-CAMERA_POS[0])*CAMERA_SCALE
        self.rect.top=(self.pos[1]-CAMERA_POS[1])*CAMERA_SCALE

class RoomBoundary(pg.sprite.Sprite):
    images: List[pg.Surface] = []
    textureIds: List[int] = []
    def __init__(self,x,y,id,rid,*groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.pos=[x,y]
        self.image = pg.transform.scale(self.images[0], (20,20))
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.width=20
        self.height=20
        self.renderOff=[20,20]
        self.boundaryId=id
        self.disabled=0
        self.roomid=rid
        self.imgid=self.textureIds[0]
        self.rect.size=[self.width,self.height]
    def triggerBuildRoom(self,*groups):
        if(self.disabled==0):
            x=getRoomToBuildFromBoundaryId(self.boundaryId,self.pos)
            print(self.boundaryId)
            if(x!=None):
                if not (x[0].isalpha()):
                    rooms[int(x[0])].buildRoom([x[1],x[2]],groups[0],groups[1],groups[2],groups[3],groups[4],groups[5])
                else:
                    rooms[(x[0])].buildRoom([x[1],x[2]],groups[0],groups[1],groups[2],groups[3],groups[4],groups[5])
                pos=(self.pos[0],self.pos[1],self.pos[0]+self.height,self.pos[1]+self.height)
                for i in groups[3]:
                    pos2=(i.pos[0],i.pos[1],i.pos[0]+i.height,i.pos[1]+i.height)
                    if(isColliding(pos,pos2)):
                        i.disabled=1
                self.disabled=1
            else:
                print('Missing Link!')
                self.kill()
    def update(self):
        self.rect = self.rect.clamp(SCREENRECT)
        self.rect.left=(self.pos[0]-CAMERA_POS[0])*CAMERA_SCALE
        self.rect.top=(self.pos[1]-CAMERA_POS[1])*CAMERA_SCALE

class SaveMarker(pg.sprite.Sprite):
    images: List[pg.Surface] = []
    textureIds: List[int] = []
    def __init__(self,x,y,rid,*groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.pos=[x-20,y-20]
        self.image = pg.transform.scale(self.images[0], (20,20))
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.width=60
        self.height=60
        self.roomid=rid
        self.imgid=self.textureIds[0]
        self.rect.size=[20,20]
    def update(self):
        self.rect = self.rect.clamp(SCREENRECT)
        self.rect.left=(self.pos[0]-CAMERA_POS[0]+20)*CAMERA_SCALE
        self.rect.top=(self.pos[1]-CAMERA_POS[1]+20)*CAMERA_SCALE


class barPart(pg.sprite.Sprite):
    images: List[pg.Surface] = []
    textureIds: List[int] = []
    def __init__(self,x,y,imageids,*groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image=pg.transform.scale(self.images[imageids[0]],(10,10))
        self.rect=self.image.get_rect()
        self.pos=[x,y]
        self.state=0
        self.stateVals=imageids
        self.rect.left=self.pos[0]
        self.rect.top=self.pos[1]
        self.imgid=self.textureIds[self.stateVals[0]]
    def setstate(self,state):
        self.rect.left=self.pos[0]
        self.rect.top=self.pos[1]
        self.state=state
        self.imgid=self.textureIds[self.stateVals[state]]
    def update(self):
        self.rect.left=(self.pos[0]-0*CAMERA_POS[0])
        self.rect.top=(self.pos[1]-0*CAMERA_POS[1])

class Bar(pg.sprite.Sprite):
    def __init__(self,x,y,imgs,imgsalterego,w,v,m,sproff,renderGroup,*groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.pos=[x,y]
        self.images: List[pg.Surface] = imgs
        self.imagesalterego: List[int] = imgsalterego
        self.width=w
        self.value=-100
        self.maxValue=m
        self.bgObjects=[]
        self.fgObjects=[]
        self.spriteOffset=sproff
        self.scale=CAMERA_SCALE
        if(barPart.images.__len__()<sproff+1):
            for i in imgs:
                barPart.images.append(i)
            for i in imgsalterego:
                barPart.textureIds.append(i)
        for i in range(self.width):
            if(i==0):
                self.bgObjects.append(barPart(self.pos[0]+10*i*self.scale,self.pos[1],[sproff],renderGroup))
                renderGroup.change_layer(self.bgObjects[-1],30)
            elif(i<(self.width-1)):
                self.bgObjects.append(barPart(self.pos[0]+10*i*self.scale,self.pos[1],[sproff+1],renderGroup))
                renderGroup.change_layer(self.bgObjects[-1],30)
            else:
                self.bgObjects.append(barPart(self.pos[0]+10*i*self.scale,self.pos[1],[sproff+2],renderGroup))
                renderGroup.change_layer(self.bgObjects[-1],30)
        
        for i in range(self.width):
            if(i==0):
                self.fgObjects.append(barPart(self.pos[0]+10*i*self.scale,self.pos[1],[sproff+3,sproff+4,sproff+5],renderGroup))
                renderGroup.change_layer(self.fgObjects[-1],31)
            elif(i<(self.width-1)):
                self.fgObjects.append(barPart(self.pos[0]+10*i*self.scale,self.pos[1],[sproff+6,sproff+7,sproff+8],renderGroup))
                renderGroup.change_layer(self.fgObjects[-1],31)
            else:
                self.fgObjects.append(barPart(self.pos[0]+10*i*self.scale,self.pos[1],[sproff+9,sproff+10,sproff+11],renderGroup))
                renderGroup.change_layer(self.fgObjects[-1],31)
        self.updateV(v)
    def updateV(self,value):
        numObjsOld=self.value/self.maxValue*self.width
        numObjsNew=value/self.maxValue*self.width
        if(numObjsOld!=numObjsNew):
            if(int(numObjsNew)==1):
                self.fgObjects[0].setstate(2)
                for i in range(1,self.width):
                    self.fgObjects[i].setstate(0)
            else:
                for i in range(-int(-numObjsNew),self.width):
                    self.fgObjects[i].setstate(0)
                for i in range(0,-int(-numObjsNew)):
                    self.fgObjects[i].setstate(1)
                if(i!=0):
                    self.fgObjects[-int(-numObjsNew)-1].setstate(2)
class Background(pg.sprite.Sprite):
    images: List[pg.Surface] = []
    textureIds: List[int] = []
    def __init__(self,*groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.image=pg.transform.scale(self.images[0],(3000,2000))
        self.rect=self.image.get_rect()

def getRoomToBuildFromBoundaryId(boundary,roomOffset):
    if(boundary[1])==None:
        return None
    else:
        value0=boundary[0].split('_')
        value0=(int(value0[0]),int(value0[1]))
        value1=boundary[1]
        value2=[]
        value2.append(value1[0:value1.index('_')])
        value1=value1[value1.index('_')+1:]
        value2.append(value1[0:value1.index('_')])
        value1=value1[value1.index('_')+1:]
        value2.append(value1)
        value3=(value2[0],int(value2[1]),int(value2[2]))
        return (value3[0],roomOffset[0]-20*value3[1],roomOffset[1]-20*value3[2])
roomsBuilt=0
class BuiltRoom(pg.sprite.Sprite):
    images: List[pg.Surface] = []
    textureIds: List[int] = []
    def __init__(self,x,y,w,h,id,type,sources,*groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.width=w
        self.height=h
        self.pos=[x,y]
        self.id=id
        self.type=type
        self.image=pg.transform.scale(self.images[0],(w*CAMERA_SCALE,h*CAMERA_SCALE))
        self.rect=self.image.get_rect()
        self.setImages(sources)
        self.rect.size=[self.width,self.height]
        #self.imgid=loadTexture(surface_array(self.image))
    def unbuildRoom(self,allgroup,boundaryGroup):
        for i in allgroup:
            if type(i) in [Wall,Hazard,RoomBoundary,SaveMarker]:
                if i.roomid==self.id:
                    i.kill()
        for i in boundaryGroup:
            if (type(i)==RoomBoundary):
                if i.roomid==self.id:
                    i.kill()
        for i in boundaryGroup:
            if(type(i)==RoomBoundary):
                if i.disabled==1:
                    shouldKeepDisabled=0
                    for j in allgroup:
                        if(type(j)==RoomBoundary):
                            if(i!=j):
                                if(isColliding((i.pos[0],i.pos[1],i.pos[0]+i.height,i.pos[1]+i.height),(j.pos[0],j.pos[1],j.pos[0]+j.height,j.pos[1]+j.height))):
                                    shouldKeepDisabled=1
                    if shouldKeepDisabled==0:
                        i.disabled=shouldKeepDisabled
        self.kill()
    def setImages(self,allgroup):
        newimage=pg.surface.Surface((self.width,self.height))
        for obj in allgroup.sprites():
            if('roomid' in obj.__dict__):
                if obj.roomid==self.id:
                    newimage.blit(obj.image,(obj.pos[0]-self.pos[0],obj.pos[1]-self.pos[1]))
        self.image=pg.transform.scale(newimage,(self.width*CAMERA_SCALE,self.height*CAMERA_SCALE))
        self.image.set_colorkey((0,0,0))
    def update(self):
        self.rect = self.rect.clamp(SCREENRECT)
        self.rect.left=(self.pos[0]-CAMERA_POS[0])*CAMERA_SCALE
        self.rect.top=(self.pos[1]-CAMERA_POS[1])*CAMERA_SCALE
newParticles=[]
class Room(pg.sprite.Sprite):
    def __init__(self,data,w,h,id,*groups):
        pg.sprite.Sprite.__init__(self, *groups)
        self.width=w
        self.height=h
        self.id=id
        self.data=data
        self.boundaryList=[]
    def decompressData(self):
        data=self.data
        data2=[]
        if(type(data)==dict):
            palette=data['palette']
            palettelen=palette.__len__()
            palettelen2=1
            while(2**(palettelen2))<palettelen:
                palettelen2+=1
            data=data['data']
            for i in data:
                data2.append([])
                for j in range(self.width):
                    data2[-1].append(palette[fromBinary(i[j*palettelen2:(j+1)*palettelen2])])
        self.data=data2
        for j in range(self.height):
            for i in range(self.width):
                if(self.data[j][i]==5):
                    self.boundaryList.append([str(i)+"_"+str(j),None])
        #print(self.boundaryList)
    def buildRoom(self,offset,*groups):
        global roomsBuilt
        wallgroup=groups[0]
        platformgroup=groups[1]
        allgroup=groups[5]#[2]
        allgroupt=groups[2]
        boundaryGroup=groups[3]
        builtRoomsGroup=groups[4]
        returns=[]
        boundaryListId=0
        b=BuiltRoom(offset[0],offset[1],self.width*20,self.height*20,roomsBuilt,self.id,allgroup,builtRoomsGroup,allgroupt)
        
        for i in range(self.width):
            for j in range(self.height):
                dataval=self.data[j][i]
                if dataval==1:
                    returns.append(Wall(i*20+offset[0],j*20+offset[1],20,20,0,roomsBuilt,wallgroup,allgroup))
                elif dataval==-1:
                    returns.append(Wall(i*20+offset[0],j*20+offset[1],20,20,0,roomsBuilt,allgroup))
                elif dataval==-2:
                    returns.append(Wall(i*20+offset[0],j*20+offset[1],20,20,6,roomsBuilt,allgroup))
                    allgroup.change_layer(returns[-1],-5)
                elif dataval==2:
                    returns.append(Wall(i*20+offset[0],j*20+offset[1],20,1,0,roomsBuilt,platformgroup,allgroup))
                elif dataval==3:
                    for k in range(10):
                        returns.append(Wall(i*20+k*2+offset[0],j*20+k*2+offset[1],2,20-k*2,[2 if k==0 else 1][0],roomsBuilt,wallgroup,allgroup))
                        if(k==0):
                            allgroup.change_layer(returns[-1],-4)
                elif dataval==4:
                    for k in range(10):
                        returns.append(Wall(i*20+18-k*2+offset[0],j*20+k*2+offset[1],2,20-k*2,1,roomsBuilt,wallgroup,allgroup))
                    returns.append(Wall(i*20+offset[0],j*20+offset[1],0,0,3,roomsBuilt,allgroup))
                    allgroup.change_layer(returns[-1],-4)
                elif dataval==5:
                    returns.append(RoomBoundary(offset[0]+i*20,offset[1]+j*20,self.boundaryList[boundaryListId],roomsBuilt,boundaryGroup,allgroup))
                    allgroup.change_layer(returns[-1],-1)
                    boundaryListId+=1
                elif dataval==6:
                    for k in range(10):
                        returns.append(Wall(i*20+k*2+offset[0],j*20+18-k*2+offset[1],2,20-k*2,0,roomsBuilt,wallgroup,allgroup))
                elif dataval==7:
                    for k in range(10):
                        returns.append(Wall(i*20+19-k*2+offset[0],j*20+offset[1],1,(k+1)*2,1,roomsBuilt,wallgroup,allgroup))
                    returns.append(Wall(i*20+18-9*2+offset[0],j*20+offset[1],1,(9+1)*2,5,roomsBuilt,wallgroup,allgroup))
                    allgroup.change_layer(returns[-1],-4)
                elif dataval==8:
                    returns.append(Hazard(i*20+offset[0],j*20+offset[1],10,20,roomsBuilt,0,wallgroup,allgroup))
                    returns.append(Hazard(i*20+offset[0]+10,j*20+offset[1],10,20,roomsBuilt,0,wallgroup,allgroup))
                elif dataval==9:
                    returns.append(SaveMarker(i*20+offset[0],j*20+offset[1],roomsBuilt,allgroup))
                if dataval in [8,9,5,3,4,6,7]:
                    touchCount=0
                    if(i>0):
                        if self.data[j][i-1]==-2:
                            touchCount+=1
                    if(j>0):
                        if self.data[j-1][i]==-2:
                            touchCount+=1
                    if(i<self.width-1):
                        if self.data[j][i+1]==-2:
                            touchCount+=1
                    if(j<self.height-1):
                        if self.data[j+1][i]==-2:
                            touchCount+=1
                    if touchCount>=2:
                        returns.append(Wall(i*20+offset[0],j*20+offset[1],20,20,6,roomsBuilt,allgroup))
                        allgroup.change_layer(returns[-1],-5)
        allgroupt.change_layer(b,-10)
        roomsBuilt+=1
        #print(allgroupt.sprites().__len__())
    def link(self,other,boundaryId0,boundaryId1):
        self.boundaryList[boundaryId0][1]=str(other.id)+"_"+other.boundaryList[boundaryId1][0]
        #print(self.boundaryList)
        
        
#class Alien(pg.sprite.Sprite):
#    """An alien space ship. That slowly moves down the screen."""
#
#    speed = 13
#    animcycle = 12
#    images: List[pg.Surface] = []
#
#    def __init__(self, *groups):
#        pg.sprite.Sprite.__init__(self, *groups)
#        self.image = self.images[0]
#        self.rect = self.image.get_rect()
#        self.facing = random.choice((-1, 1)) * Alien.speed
#        self.frame = 0
#        if self.facing < 0:
#            self.rect.right = SCREENRECT.right
#
#    def update(self, *args, **kwargs):
#        self.rect.move_ip(self.facing, 0)
#        if not SCREENRECT.contains(self.rect):
#            self.facing = -self.facing
#            self.rect.top = self.rect.bottom + 1
#            self.rect = self.rect.clamp(SCREENRECT)
#        self.frame = self.frame + 1
#        self.image = self.images[self.frame // self.animcycle % 3]

backgroundstrength=(0.3,0.3,0.3,0,0,0)

def main(winstyle=0):
    global winfo
    global newParticles
    animationsList={'player':{'walk':4,'fall':1}}
    # Initialize pygame
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    if pg.mixer and not pg.mixer.get_init():
        print("Warning, no sound")
        pg.mixer = None

    fullscreen = False
    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth,vsync=1)
    pg.display.set_mode(SCREENRECT.size,winstyle|pg.RESIZABLE,vsync=1)
    pg.display.set_mode(SCREENRECT.size,pg.OPENGL|pg.RESIZABLE|pg.DOUBLEBUF)
    setup()
    1+winfo
    winfo=pg.display.Info()
    # Load images, assign to sprite classes
    # (do this before the classes are used, after screen setup)
    img = load_image(r"M:\images\tictactoe\blank2.png")
    img2 = load_image(r"M:\images\tictactoe\blank1.png")
    img3 = load_image(r"M:\images\tictactoe\o.png")
    img4 = load_image(r"M:\images\specialgamev1\builtRoom.png")
    img4.set_colorkey([0,0,0])
    img3.set_colorkey([0,0,0])
    images={'hazard1':"hazard.png","save_marker":"devtextures\\savemarker.png","particle_blood":"devtextures\\savemarker.png",'tile1':"tiles\\bricksFull.png",'tile2':"tiles\\intentionallyempty.png",'tile3':"tiles\\brickStairsLeft.png",'tile4':"tiles\\brickStairsRight.png",'tile5':"tiles\\brickStairsInvertedright.png",'tile6':"tiles\\brickStairsInvertedLeft.png"}
    crops={'tile1':(0,0,20,16)}
    retextures={'tile3':'tile1','tile4':'tile1','tile5':'tile1','tile6':'tile1'}
    backgrounds={'tile-2':'tile1'}
    tints={'particle_blood':[255/255,50/255,50/255]}
    
    for i in images:
        images[i]=load_image("M:\\images\\specialgamev1\\"+images[i])
        images[i].set_colorkey([0,0,0])
    for i in crops:
        image=images[i]
        newrect=crops[i]
        x=pg.surface.Surface((newrect[2]-newrect[0],newrect[3]-newrect[1]))
        x.blit(image,(-newrect[0],-newrect[1]))
        images[i]=x
    for i in retextures:
        image=images[i]
        imagebase=images[retextures[i]]
        w1,h1,w2,h2=image.get_width(),image.get_height(),imagebase.get_width(),imagebase.get_height()
        for x in range(w1):
            for y in range(h1):
                r=image.get_at((x,y))
                if(r[0]+r[1]+r[2])!=0:
                    image.set_at((x,y),imagebase.get_at((int(x/w1*w2),int(y/h1*h2))))
        images[i]=image
    
    for i in backgrounds:
        if i in images:
            image=images[i]
            imagebase=images[backgrounds[i]]
            w1,h1,w2,h2=image.get_width(),image.get_height(),imagebase.get_width(),imagebase.get_height()
            for x in range(w1):
                for y in range(h1):
                    r=image.get_at((x,y))
                    if(r[0]+r[1]+r[2])==0:
                        b=imagebase.get_at((int(x/w1*w2),int(y/h1*h2)))
                        image.set_at((x,y),(b[0]*backgroundstrength[0]+backgroundstrength[3],b[1]*backgroundstrength[1]+backgroundstrength[4],b[2]*backgroundstrength[2]+backgroundstrength[5]))
            images[i]=image
        else:
            imagebase=images[backgrounds[i]]
            image=pg.surface.Surface((imagebase.get_width(),imagebase.get_height()))
            w1,h1,w2,h2=image.get_width(),image.get_height(),imagebase.get_width(),imagebase.get_height()
            for x in range(w1):
                for y in range(h1):
                    r=image.get_at((x,y))
                    b=imagebase.get_at((int(x/w1*w2),int(y/h1*h2)))
                    image.set_at((x,y),(b[0]*backgroundstrength[0]+backgroundstrength[3],b[1]*backgroundstrength[1]+backgroundstrength[4],b[2]*backgroundstrength[2]+backgroundstrength[5]))
            images[i]=image
    for i in tints:
        image=images[i]
        tint=tints[i]
        w1,h1=image.get_width(),image.get_height()
        for x in range(w1):
            for y in range(h1):
                r=image.get_at((x,y))
                if(r[0]+r[1]+r[2])!=0:
                    p=image.get_at((x,y))
                    image.set_at((x,y),(p[0]*tint[0],p[1]*tint[1],p[2]*tint[2],p[3]))
        images[i]=image
    imagesb={}
    for i in images:
        print("LOADING TEXTURE \""+i+"\"")
        imagesb[i]=loadTexture(surface_array(images[i]))
    Background.images.append(img2)
    barTextures=["leftb.png","midb.png","rightb.png","leftf0.png","leftf1.png","leftf2.png","midf0.png","midf1.png","midf2.png","rightf0.png","rightf1.png","rightf1.png"]
    barTextures=[load_image("M:\\images\\specialgamev1\\healthbar\\"+i) for i in barTextures]
    barTexturesb=[loadTexture(surface_array(i)) for i in barTextures]
    for i in barTextures:
        i.set_colorkey([0,0,0])
    animations={}
    for i in animationsList:
        for j in animationsList[i]:
            for k in range(animationsList[i][j]):
                k=k+1
                animations['anim_'+str(i)+"_"+str(j)+"_"+str(k)]=load_image("M:\\images\\specialgamev1\\"+'anim_'+str(i)+"_"+str(j)+"_"+str(k)+".png")
                print('anim_'+str(i)+"_"+str(j)+"_"+str(k))
    n=[i for i in animations]
    for i in n:
        animations[i+'_flip']=pg.transform.flip(animations[i],1,0)
    Player.images = [animations[i] for i in animations if ('player' in i)]
    print([i for i in animations if ('player' in i)]+["flip_"+i for i in animations if ('player' in i)])
    #[pg.transform.scale(img,(Player.width,Player.height)), pg.transform.flip(pg.transform.scale(img,(Player.width,Player.height)), 1, 0)]
    
    Wall.images = [images[i] for i in ["tile1","tile2","tile3","tile4","tile5","tile6",'tile-2']]
    Hazard.images = [images['hazard1']]
    SaveMarker.images = [images['save_marker']]
    RoomBoundary.images.append(img3)
    BuiltRoom.images.append(img4)
    PhysicsParticle.images.append(images['particle_blood'])


    animationsb={}
    for i in animations:
        print("LOADING TEXTURE ANIMATION \""+i+"\"")
        animationsb[i]=loadTexture(surface_array(animations[i]))








    Player.textureIds = [animationsb[i] for i in animationsb if ('player' in i)]
    Wall.textureIds = [imagesb[i] for i in ["tile1","tile2","tile3","tile4","tile5","tile6",'tile-2']]
    Hazard.textureIds = [imagesb['hazard1']]
    SaveMarker.textureIds = [imagesb['save_marker']]
    RoomBoundary.textureIds.append(loadTexture(surface_array(img3)))
    BuiltRoom.textureIds.append(loadTexture(surface_array(img4)))
    PhysicsParticle.textureIds.append(imagesb['particle_blood'])
    # decorate the game window
    #icon = pg.transform.scale(Alien.images[0], (32, 32))
    #pg.display.set_icon(icon)
    #pg.display.set_caption("Pygame Aliens")
    #pg.mouse.set_visible(0)

    Enemeh.images=Player.images
    Enemeh.textureIds=Player.textureIds

    
    # create the background, tile the bgd image
    bgdtile = load_image(r"M:\images\backgroundm.png")
    background = pg.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    screen.blit(background, (0, 0))
    pg.display.flip()

    # load the sound effects
    #sound_id=load_sound(filename)
    #if pg.mixer:
    #    music = os.path.join(main_dir, "data", "house_lo.wav")
    #    pg.mixer.music.load(music)
    #    pg.mixer.music.play(-1)

    # Initialize Game Groups
    walls = pg.sprite.Group()
    platforms = pg.sprite.Group()
    all = pg.sprite.LayeredUpdates()
    allb = all#pg.sprite.LayeredUpdates()
    GUIelements = pg.sprite.LayeredUpdates()
    phyicsparticles=pg.sprite.Group()
    boundaries = pg.sprite.Group()
    builtRooms = pg.sprite.Group()
    healthBarRender=Bar(10,10,barTextures,barTexturesb,10,10,10,0,GUIelements)
    # Create Some Starting Values
    clock = pg.time.Clock()

    
    enemies = pg.sprite.Group()

    # initialize our starting sprites
    #backgroundObject=Background(all)
    #all.change_layer(backgroundObject,-1000)
    player = Player(all)
    Enemeh(200,-50,enemies,all)
    player.pos=[0,-50]
    rooms[0]=Room({'data':["000 000 000 000 000 000 000".replace(' ',''),
                           "000 000 000 000 000 000 000".replace(' ',''),
                           "000 000 000 000 000 000 000".replace(' ',''),
                           "000 000 000 000 000 000 101".replace(' ',''),
                           "000 110 000 000 100 010 010".replace(' ',''),
                           "011 000 000 100 001 000 000".replace(' ',''),
                           "001 001 001 111 001 001 001".replace(' ','')],'palette':[0,1,2,3,4,5,9,-1]},w=7,h=7,id=0)
    rooms[1]=Room({'data':["0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000".replace(' ',''),
                          "0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000".replace(' ',''),
                          "0000 0000 0000 0000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000".replace(' ',''),
                          "0000 0000 0000 0000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000".replace(' ',''),
                          "0000 0000 0000 0000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000".replace(' ',''),
                          "0000 0000 0000 0000 0001 1000 1000 1000 1000 1000 1000 1000 0001 0001 0001 0001 0001 0001 0001 0001".replace(' ',''),
                          "0000 0000 0000 0000 0001 1000 1000 1000 1000 1000 1000 0111 1001 1001 0000 0000 0000 0000 0000 0000".replace(' ',''),
                          "0000 0000 0000 0000 0001 1000 1000 1000 1000 1000 0111 1001 1001 1001 0000 0000 0000 0000 0000 0000".replace(' ',''),
                          "0000 0000 0000 0000 0001 1000 1000 1000 1000 0111 1001 1001 1001 1001 0000 0000 0000 0000 0000 0000".replace(' ',''),
                          "0000 0000 0000 0000 0001 1000 1000 1000 0111 1001 1001 1001 1001 0011 0000 0000 0000 0000 0000 0101".replace(' ',''),
                          "0000 0000 0000 0000 0001 1000 1000 0111 1001 1001 1001 0100 0001 0001 0001 0000 0000 0000 0001 0001".replace(' ',''),
                          "0000 0000 0000 0000 0001 1000 0111 1001 1001 1001 0100 1000 1000 1000 1000 0000 0000 0000 1000 1000".replace(' ',''),
                          "0000 0000 0000 0000 0001 0111 1001 1001 1001 0100 1000 1000 1000 1000 1000 0110 0110 0110 1000 1000".replace(' ',''),
                          "0000 0000 0000 0000 0111 1001 1001 1001 0100 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000".replace(' ',''),
                          "0000 0000 0000 0000 1001 1001 1001 0100 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000".replace(' ',''),
                          "0000 0000 0000 0000 1001 1001 0100 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000".replace(' ',''),
                          "0000 0000 0000 0000 1001 0100 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000".replace(' ',''),
                          "0000 0000 0000 0000 0100 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000".replace(' ',''),
                          "0000 0000 0101 0100 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000".replace(' ',''),
                          "0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000".replace(' ','')],'palette':[0,1,2,9,4,5,8,7,-1,-2]},w=20,h=20,id=1)
    rooms["tallhallway"]=Room({'data':["0001"*50]+["0001"+"1010"*48+"0001"]*3+["0001"*50]+["1011"*50]*19+["0101"+"10110000"*24+"0101"]+["0001"*50]+["0001"+"1010"*48+"0001"]*3+["0001"*50],'palette':[0,1,2,3,4,5,6,7,8,9,-1,-2]},w=50,h=30,id="tallhallway")
    
    rooms[2]=Room({'data':["000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "101 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 011 000".replace(' ',''),
                          "000 000 001 001 001 000 001 000 000 001 000 000 000 000 000 000 000 001 001 001".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "101 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ','')],'palette':[0,1,2,9,4,5,8,7]},w=20,h=20,id=2)
    rooms["spikepit"]=Room({'data':["000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "101 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                          "110 110 110 110 110 110 110 110 110 110 110 110 110 110 110 110 110 110 110 110".replace(' ','')],'palette':[0,1,2,9,4,5,8,7]},w=20,h=20,id="spikepit")
    rooms[0].decompressData()
    rooms[1].decompressData()
    rooms[2].decompressData()
    rooms['spikepit'].decompressData()
    rooms['tallhallway'].decompressData()
    rooms['tallhallway'].link(rooms[0],0,0)
    rooms['tallhallway'].link(rooms[1],1,1)
    rooms[0].link(rooms['tallhallway'],0,0)
    
    rooms[1].link(rooms['tallhallway'],1,1)
    rooms[1].link(rooms[2],1,0)
    rooms[2].link(rooms[1],0,0)
    rooms[2].link(rooms['spikepit'],1,0)
    
    while player.alive():
        winfo=pg.display.Info()
        if walls.__len__()==0:
            rooms[0].buildRoom([0,0],walls,platforms,all,boundaries,builtRooms,allb)
            floors=[]
            print(all.sprites().__len__())
            #for x in range(5):
            #    floors.append(Wall(150-x*20-19,210,20,10,walls,all))
            #for x in range(100):
            #    floors.append(Wall(150+x*2,210+2*x,2,10,walls,all))
            #for x in range(5):
            #    floors.append(Wall(150+x*20+200,210+200,20,10,walls,all))
            #for x in range(9,11):
            #    floors.append(Wall(150+x*20+200,210+200,20,10,walls,all))
            #floors.append(Wall(100,180,40,1,platforms,all))
        # get input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    if not fullscreen:
                        print("Changing to FULLSCREEN")
                        screen_backup = screen.copy()
                        screen = pg.display.set_mode(
                            SCREENRECT.size, winstyle | pg.FULLSCREEN, bestdepth,vsync=1
                        )
                        screen.blit(screen_backup, (0, 0))
                    else:
                        print("Changing to windowed mode")
                        screen_backup = screen.copy()
                        screen = pg.display.set_mode(
                            SCREENRECT.size, winstyle|pg.RESIZABLE, bestdepth,vsync=1
                        )
                        screen.blit(screen_backup, (0, 0))
                    pg.display.flip()
                    fullscreen = not fullscreen

        keystate = pg.key.get_pressed()
        cursorstate = pg.mouse.get_pressed()
        #x=[i for i in range(keystate.__len__()) if keystate[i]!=0]
        #if x!=[]:
        #    print(x)
        # clear/erase the last drawn sprites
        #all.clear(screen, background)

        # update all the sprites
        # handle player input
        
        horizmove = keystate[100] - keystate[97]
        jump = keystate[119]
        down=keystate[115]
        if down==0:
            player.updateb([walls,platforms,all,boundaries,builtRooms,allb],horizmove,jump,cursorstate[0])
        else:
            player.updateb([walls,[],all,boundaries,builtRooms,allb],horizmove,jump,cursorstate[0])
        #player.jump(jump)
        healthBarRender.updateV(player.attributes['health'])
        for i in newParticles:
            PhysicsParticle(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]==1,i[7]==2,all,phyicsparticles)
        newParticles=[]
        for i in phyicsparticles:
            i.updateb([walls])
        for i in enemies:
            i.updatec([walls,platforms,all,boundaries,builtRooms,allb],player)
        all.update()

        
        #collisions?
        #for alien in pg.sprite.spritecollide(player, aliens, 1):
        #    if pg.mixer and boom_sound is not None:
        #        boom_sound.play()
        #    Explosion(alien, all)
        #    Explosion(player, all)
        #    SCORE = SCORE + 1
        #    player.kill()

        # See if shots hit the aliens.
        #for alien in pg.sprite.groupcollide(aliens, shots, 1, 1).keys():
        #    if pg.mixer and boom_sound is not None:
        #        boom_sound.play()
        #    Explosion(alien, all)
        #    SCORE = SCORE + 1

        # draw the scene
        #dirty = all.draw(screen)
        drawAll(all)
        drawGUI(GUIelements)
        pg.display.flip()#update()#dirty)

        # cap the framerate at 40fps. Also called 40HZ or 40 times per second.
        clock.tick(FRAMERATE)

    if pg.mixer:
        pg.mixer.music.fadeout(1000)
    pg.time.wait(1000)


# call the "main" function if running this script
if __name__ == "__main__":
    main(pg.OPENGL)
    pg.quit()
