###############################################
# Important information:                      #
#   This project uses reference duplication.  #
#   Every time you see something like         #
#             a=[b][0]                        #
#   you are seeing an example of reference    #
#   duplication. By editing part of one       #
#   variable (not the whole thing), the other #
#   will always match.                        #
#   Good: a.append(5)    Bad: a+=[5]          #
#                                             #
# If you want an updated version, go to       #
# https://github.com/1101-Grills-Oren/leavethe#
#lightson/blob/6d29680a1e3c60e3d232143f53a1369#
#4943c5401/versions/current.py                #
#                                             #
# This is going to be a continued project.    #
#                                             #
#                                             #
# Startup splash: tkinter on secondary thread #
# Recursion: see command ?while for usage.    #
# Classes: There are many of these.           #
# Functions: Much functions very yes.         #
#                                             #
#  Controls: WASD for movement.               #
#            t for command chat.              #
#    Left click to attack towards the cursor. #
#      esc to leave chat or end game          #
# the command ./terminateProgram does the same#
#                                             #
###############################################

#Commands:
#    declare msg:str                                                                   this does basically nothing
#    tp x:float y:float                                                                teleports the player to x,y
#    setGrav x:float y:float                                                           changes player gravity
#    setVel x:float y:float                                                            changes player velocity
#    player.pos                                                                        command to get player position
#    placeRoom rid:any x:int y:int                                                     Places room with id rid at x,y
#    \summon id:str x:int_opt y:int_opt                                                Summons something with id id at x,y. If x is not supplied, spawns at player position.
#    variable id:var_id(str) attr attribute(str)                                       Returns attribute attribute of variable id. Example: (var 'ex'=[0,4,2,9]) variable ex attr __len__     Example returns: Length of array ex
#    variable id:var_id(str) command cmd:command(str)                                  Sets variable id to return value of command cmd.
#    variable id:var_id(str) value v:str                                               Sets variable id to v (type:string)
#    variable id:var_id(str) value_int v:int                                           Sets variable id to v (type:int)
#    variable id:var_id(str) value_float v:float                                       Sets variable id to v (type:float)
#    variable id:var_id(str) var x:var_id(str)                                         sets variable id to be equal to variable x
#    variable id:var_id(str) append value:str                                          For arrays, appends a new value (type str) to variable id   For other types, crashes
#    variable id:var_id(str) append_var var:var_id(str)                                For arrays, appends the value contained in variable var to variable id   For other types, crashes
#    variable id:var_id(str) pop i:int                                                 returns index of array variable id, removing it at the same time
#    variable id:var_id(str) type newtype[str|int|float]:str                           Changes variable type. new type is determined by newtype
#    variable id:var_id(str) sum var:var_id(str) var:var_id(str)...                    sets variable id to the sum of variables var
#    variable id:var_id(str) subtract var1:var_id(str) var2:var_id(str)                sets variable id to var1-var2
#    variable id:var_id(str) min var1:var_id(str) var2:var_id(str)                     sets variable id to min(var1,var2)
#    variable id:var_id(str) max var1:var_id(str) var2:var_id(str)                     sets variable id to max(var1,var2)
#    variable id:var_id(str) divide var1:var_id(str) var2:var_id(str)                  sets variable id to var1/var2
#    variable id:var_id(str) multiply var1:var_id(str) var2:var_id(str)...             Sets variable id to var1*var2*...
#    variable id:var_id(str) arrayize id2:var_id_opt(str)                              If variable id2 exists, sets variable id to [id2]. Else, sets variable id to []. Useful for making arguments for file commands.
#    variable_get id:var_id(str)                                                       returns the value of variable id
#    get_enemy args                                                                    returns a list of enemies with data args. Options: x,y: center of command execution     d_min,d_max: Min and max distance for the top-right corner of the enemy in tiles.     c_max: maximum number of return values    type: Limit return objects to type type. Can be repeated for multiple types.
#    get_object args                                                                   returns a list of objects with data args. Options match those in get_enemy.
#    get_player                                                                        Returns the current player. Redundant.
#    executeFile fname:str args                                                        executes the command file fname after setting variable args to be args.split(' ')
#    executeFile_argless fname:str                                                     executes the command file fname without setting arguments.
#    a==b,a>b,a>=b,a<b,a<=b,a!=b var:var_id(str) value:int|float                       Similar to if you ran the names as code with "a" being the variable var and "b" being a constant to compare to.
#    a==v,a>v,a>=v,a!=v var1:var_id(str) var2:var_id(str)                              same as above, but with a=var1 and v=var2
#    !v var:var_id(str)                                                                returns inverted value of var var_id. If var is false, returns true, if true, returns false.
#    !execute cmd:command(str)                                                         Executes command cmd and inverts the return value.
#    ?execute condition:var_id(str) cmd:command(str)                                   executes command cmd, but only if variable "condition" is not false.
#    ./programTerminate                                                                Ends the program. Non-recoverable (nothing can stop it)
#    ./protectVariable var:var_id(str)                                                 takes the variable var and makes its main object nonreplaceable (subvalues can change, but not the main object). Non-recoverable.
#    ./lockVariable var:var_id(str)                                                    Makes the variable var (under that alias) read-only. Non-recoverable.
#    
#
#    
#    
#    Symbolic variables:
#       player                                The player. Read Only
#       player.attr                           player attributes such as health, max health, ArithmeticError. Modifiable.
#       player.pos                            player position. Modifiable
#       player.vel                            player velocity. Modifiable
#       player.onGround                       whether the player is on the ground or not. Read Only.
#       player.fireCooldown                   how long until the player will be able to fire again. Read only.
#       player.ducking                        Is the player crouching? Read only.
#       player.shotsLeft                      how many shots the player has left before a reload? Read only.
#       player.reloadTime                     how long does the player need to be on the ground to reload one projectile? Read only.
#    
#    

































import threading
import sys
import subprocess
l=sys.argv.__len__()
shouldpass=0
if(l>1):
    if(sys.argv[1]=='splash'):
        shouldpass=1


#start splash
global splashtext
splashtext='testing'
if shouldpass:
    pass
    
















































#end splash
else:
    def splashfunction():
        import tkinter as tk
        import msvcrt
        window=tk.Tk(screenName='splash',baseName='splash')
        textDisplay=tk.Label(window,text='test',width=100)
        textDisplay.grid(row=0,column=0)
    
        def splashUpdate(*args):
            global splashtext
            x=splashtext
            if(x!=""):
                textDisplay['text']=x
                print(x)
                splashtext=""
            window.after(1,splashUpdate)
        window.after(1,splashUpdate)
        tk.mainloop()

    splashthread=threading.Thread(target=splashfunction)
    splashthread.start()
    #splash=subprocess.Popen("py -m gamev1 splash")
    
    
    #IMAGE FOLDER
    imagefolder="M:\\images"
    
    import os
    import random
    from typing import List
    
    # import basic pygame modules
    global pg
    global key
    global mouse
    import pygame as pg
    key=pg.key
    mouse=pg.mouse
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
        a=surfaceobj.get_alpha()
        if(a==None):
            a=255
        for j in range(h):
            for i in range(w):
                b=surfaceobj.get_at((i,j))
                for c in range(3):
                    x.append(b[c])
                x.append([a if b!=(0,0,0,255) else 0][0])
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
        glTranslatef(0.0, 0.0, -30)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
    def drawAll(all):
        CAMERA_POSX=CAMERA_POS[0],CAMERA_POS[1]
        players=[[[i.rect.left,i.rect.top,i.rect.size[0],i.rect.size[1]],i.imgid] for i in all if type(i)==Player]
        glClear(GL_DEPTH_BUFFER_BIT| GL_COLOR_BUFFER_BIT)
        depth=0
        newdepth=0
        for i in all:
            if('depth' in i.__dict__):
                newdepth=i.depth
            else:
                newdepth=0
            if(newdepth!=depth):
                glTranslatef(0.0, 0.0, depth/4*3)
                depth=newdepth
                glTranslatef(0.0, 0.0, -depth/4*3)
            if((type(i)!=Player)):
                if 'imgid' in i.__dict__:
                    if i.imgid!=None:
                        if(i.rect.left-CAMERA_POSX[0]*CAMERA_SCALE>0-depth*4):
                            if(i.rect.top-CAMERA_POSX[1]*CAMERA_SCALE>0-depth*4):
                                if(i.rect.left+i.rect.size[0]-CAMERA_POSX[0]*CAMERA_SCALE)<940*0+winfo.current_w+depth*4:
                                    if(i.rect.top+i.rect.size[1]-CAMERA_POSX[1]*CAMERA_SCALE)<480+depth*4:
                                        if 'rotation' in i.__dict__:
                                            drawQuadRoated(i.rect.left-CAMERA_POSX[0]*CAMERA_SCALE, i.rect.top-CAMERA_POSX[1]*CAMERA_SCALE,i.rect.size[0],i.rect.size[1], i.imgid,i.rotation)
                                        else:
                                            drawQuad(i.rect.left-CAMERA_POSX[0]*CAMERA_SCALE, i.rect.top-CAMERA_POSX[1]*CAMERA_SCALE,i.rect.size[0],i.rect.size[1], i.imgid)
        glTranslatef(0.0, 0.0, depth/4*3)
        for i in players:
            if i[1]!=None:
                drawQuad(i[0][0]-CAMERA_POSX[0]*CAMERA_SCALE, i[0][1]-CAMERA_POSX[1]*CAMERA_SCALE,i[0][2],i[0][3], i[1],1)
    def drawGUI(elements):
        glTranslatef(0.0, 0.0, 0)
        for i in elements:
            if 'imgid' in i.__dict__:
                if i.imgid!=None:
                    drawQuadStatic(i.rect.left/20-8*3, i.rect.top/20-4.08510638*3,i.rect.size[0]/20,i.rect.size[1]/20, i.imgid)
        glTranslatef(0.0, 0.0, 0)
    
    
    
    
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
            self.ducking=0
            self.shotsleft=0
            self.wasOnGround=0
            self.reloadTime=0
            self.wasDucking=0
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
            if amount<0:
                self.facing=-1
            elif amount>0:
                self.facing=1
            #self.rect = self.image.get_rect()
        def applyFriction(self,amount):
            self.velocity[0]-=self.velocity[0]*amount/self.mass*60/FRAMERATE
            self.velocity[1]-=self.velocity[1]*amount/self.mass*60/FRAMERATE
            #if(self.velocity[0]**2<0.01):
            #    self.velocity[0]=0
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
            if(self.ducking):
                self.pos[1]+=15
                self.height-=15
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
                        newParticles.append([[self.pos[0]+self.width/2-5,self.pos[1]+self.height/2-5],[random.random()*8-4,random.random()*4-8-self.velocity[1]*4],[0,0.5],0,[5+random.random()*5]*2,120+240*random.random(),2*random.random()-1,2,1,120])
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
        
            if(self.ducking):
                self.pos[1]-=15
                self.height+=15
        
        
        def duckingChecks(self,objs):
            objs2=[]
            if(self.ducking==0)&(self.wasDucking==1):
                playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
            
                self.rect.left-=self.rect.size[0]*2
                self.rect.top-=self.rect.size[1]*2
                size1=self.rect.size
                self.rect.size=(self.rect.size[0]*5,self.rect.size[1]*5)
                for i in pg.sprite.spritecollide(self,objs,0):
                    objs2.append(i)
                objs=objs2
                self.rect.size=size1
                self.rect.left+=self.rect.size[0]*2
                self.rect.top+=self.rect.size[1]*2
                for obj in objs:    
                    objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                    if(isColliding(objpos,playerpos)):
                        self.ducking=1
                
        
        
        
        
        
        
        
        
        
        
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
            self.rect.left=(self.pos[0])*CAMERA_SCALE
            self.rect.top=(self.pos[1])*CAMERA_SCALE
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
            if(vert):
                self.jump()
            self.wasDucking=self.ducking
            if(collideobjs[1]==[]):
                if(self.onGround):
                    self.ducking=1
                else:
                    self.ducking=0
            else:
                self.ducking=0
            self.duckingChecks(collideobjs[0])
            self.accelerateHoriz(horiz*5/self.mass/(1+self.ducking))
            #self.applyVelocity()
            if(self.onGround):
                if self.reloadTime<=0:
                    self.shotsleft=min(self.shotsleft+1,self.attributes['barrels'])
                    self.reloadTime=0
                self.reloadTime-=1
            if(fire)&(self.firecooldown<=0):
                self.fire()
            
            self.collideAndMove(collideobjs[0],collideobjs[1])
            self.applyGravity()
            self.friction=0.5*self.onGround+0.1
            self.applyFriction(self.friction)
            
            self.firecooldown-=1
            self.updateRooms(collideobjs)
            self.takeDamages(collideobjs[6])
            self.updateFrame()
            self.updateSafePoint(collideobjs[5],collideobjs[4])
            self.fixNoRooms(collideobjs)
            self.immunityFramesVisuals()
        def fire(self):
            global newObjects
            if(self.shotsleft!=0):
                pos1=pg.mouse.get_pos()
                pos1=[pos1[0]-winfo.current_w/2,pos1[1]-winfo.current_h/2]
                x=pos1[0]/((pos1[0]**2+pos1[1]**2)**0.5)
                y=pos1[1]/((pos1[0]**2+pos1[1]**2)**0.5)
                #newParticles.append([[self.pos[0]+self.width/2+x*10,self.pos[1]+self.height/2+y*10],[x*50,y*50],[0,0],0,[5,5],1000,0.1,0])
                newObjects.append([0,[self.pos[0]+self.width/2+x*10,self.pos[1]+self.height/2+y*10],[x*20,y*20],0,[5,5],1000,0.1,0])
                self.firecooldown=10*FRAMERATE/60
                #self.velocity[0]/=(1+(x**2)**0.5)
                #self.velocity[1]/=5
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
        def takeDamages(self,bullets):
            if(self.ducking):
                self.pos[1]+=15
                self.height-=15
            if(self.immunityFrames<=0):
                playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
                for obj in bullets:
                    objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                    if(isColliding(playerpos,objpos)):
                        self.attributes['health']-=1
                        self.velocity[0]=-self.facing*5
                        self.velocity[1]=-10
                        obj.kill()
                        self.immunityFrames=10
            if(self.ducking):
                self.pos[1]-=15
                self.height+=15
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    class Enemeh(pg.sprite.Sprite):
        speed = 10
        textureIdsAll: List[List[int]] = []
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
            self.attributes={'barrels':2,'health':2,'maxhealth':2,'stepsize':10}
            self.animationFrame=0
            self.savePos=self.pos
            self.anticorruptroomandpos=(0,[0,-50])
            self.immunityFrames=0
            self.friction=0.1
            self.textureIds: List[int] = self.textureIdsAll[0]
            self.imgid=self.textureIds[0]
            self.imgidy=None
            self.firecooldown=0
            self.shotsleft=0
            self.wasOnGround=0
            self.aggro=0
            self.aiData=[0,0]
            self.attackFrame=0
            self.isAttacking=0
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
            if(self.isAttacking==0):
                if self.aggro:
                    if(player.pos[0]<self.pos[0]-50*(self.facing==-1)):
                        move=-.5
                    elif(player.pos[0]>self.pos[0]+50*(self.facing==1)):
                        move=0.5
                    else:
                        self.isAttacking=1
                        self.attackFrame=0
                    if(self.velocity[0]==0):
                        jump=1-(not not move)
                    if(self.isAttacking):
                        jump=0
                else:
                    if(self.aiData[0]<0):
                        self.aiData[0]+=1
                        move=0.25
                    elif(self.aiData[0]>0):
                        self.aiData[0]-=1
                        if(self.aiData[1]==0):
                            move=-0.25
                    else:
                        if(self.aiData[1]==1):
                            self.aiData[0]=90
                            self.aiData[1]=0
                        elif(self.aiData[1]==0):
                            self.aiData[0]=-90
                            self.aiData[1]=1
                    if((player.pos[0]-self.pos[0])**2+(player.pos[1]-self.pos[1])**2)<120**2:
                        self.aggro=1
            self.updateb(collideobjs,move,jump,0)
            if(self.isAttacking):
                #newParticles.append([[self.pos[0]+self.width/2+math.cos(2-(self.attackFrame/30)**2/2)*self.facing*10-10,self.pos[1]+self.height/2-10-math.sin(2-(self.attackFrame/30)**2/2)*10],[0,0],[0,0],0,[20,20],2,0,0])
                for i in range(6):
                    newParticles.append([[self.pos[0]+self.width/2+math.cos(2-(self.attackFrame/20)**2/2)*self.facing*(10-i)*4-i*1,self.pos[1]+self.height/2-i*1-math.sin(2-(self.attackFrame/20)**2/2)*(10-i)*4],[0,0],[0,0],0,[i*2,i*2],2,0,0])
                self.attackFrame+=1
                if(self.attackFrame>40):
                    self.isAttacking=0
                    newObjects.append([1,self.pos[0]+self.width/2+self.facing*25-10,self.pos[1]+self.height/2,20,1,0])
        #self.rect.top = self.origtop# - (self.rect.left // self.bounce % 2)
        def accelerateHoriz(self,amount):
            self.animationFrame+=0.1
            if(self.animationFrame>=4):
                self.animationFrame=0
            self.velocity[0]+=(self.friction*2)*amount/self.mass
            if self.onGround:
                if self.velocity[0] < 0:
                    self.image = self.images[int(self.animationFrame)]
                    self.imgid = self.textureIds[int(self.animationFrame)]
                    self.facing=-1
                elif self.velocity[0] > 0:
                    self.image = self.images[5+int(self.animationFrame)]
                    self.imgid = self.textureIds[5+int(self.animationFrame)]
                    self.facing=1
            else:
                if self.velocity[0] < 0:
                    self.image = self.images[4+int(self.animationFrame/4)]
                    self.imgid = self.textureIds[4+int(self.animationFrame/4)]
                    self.facing=-1
                elif self.velocity[0] > 0:
                    self.image = self.images[9+int(self.animationFrame/4)]
                    self.imgid = self.textureIds[9+int(self.animationFrame/4)]
                    self.facing=1
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
                        newParticles.append([[self.pos[0]+self.width/2-5,self.pos[1]+self.height/2-5],[random.random()*8-4,random.random()*4-8-self.velocity[1]*4],[0,0.5],0,[5+random.random()*5]*2,120+240*random.random(),2*random.random()-1,2,1,120])
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
            self.rect.left=(self.pos[0])*CAMERA_SCALE
            self.rect.top=(self.pos[1])*CAMERA_SCALE
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
            self.takeDamages(collideobjs[6])
            self.firecooldown-=1
            self.updateFrame()
            self.immunityFramesVisuals()
        def takeDamages(self,bullets):
            playerpos=(self.pos[0],self.pos[1],self.pos[0]+self.width,self.pos[1]+self.height)
            for obj in bullets:
                objpos=(obj.pos[0],obj.pos[1],obj.pos[0]+obj.width,obj.pos[1]+obj.height)
                if(isColliding(playerpos,objpos)):
                    self.aggro=1
                    self.attributes['health']-=1
                    self.velocity[0]+=obj.velocity[0]
                    self.velocity[1]+=obj.velocity[1]
                    obj.kill()
                    for i in range(40):
                        b=5-random.random()*20+15
                        newParticles.append([[self.pos[0]+self.width/2-obj.velocity[0],self.pos[1]+self.height/2-obj.velocity[1]],[-obj.velocity[0]/(3+random.random())+4*random.random()-2,-obj.velocity[1]/(3+random.random())+4*random.random()-2],[0,1],0,[b,b],500+100*random.random(),0.1+0.1*random.random(),2,1,120])
                
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
        images: List[List[pg.Surface]] = []
        textureIds: List[List[int]] = []
        mass=2
        def __init__(self,pos,velocity,gravity,particle,size,life,spin,shouldBounce,shouldStick,fadeType=1,fadeDuration=120, *groups):
            pg.sprite.Sprite.__init__(self, *groups)
            #for i in range(self.images.__len__()):
            #    self.images[i]=pg.transform.scale(self.images[i],(20*CAMERA_SCALE,35*CAMERA_SCALE))
            self.image = pg.transform.scale(self.images[particle][0],(20*CAMERA_SCALE/2,35*CAMERA_SCALE/2))
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
            self.imgid=self.textureIds[particle][0]
            self.particle=particle
            self.imgidy=None
            self.life=life
            self.stuck=0
            self.rotation=0
            self.fadeFrame=0
            self.fadeType=fadeType
            self.fadeDuration=fadeDuration
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
            self.rect.left=(self.pos[0])*CAMERA_SCALE
            self.rect.top=(self.pos[1])*CAMERA_SCALE
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
                    if(self.fadeType==1):
                        self.fadeFrame+=self.fadeDuration*60/FRAMERATE/(self.textureIds[self.particle].__len__())
                        if(self.fadeFrame>self.textureIds[self.particle].__len__()):
                            self.kill()
                        else:
                            self.imgid=self.textureIds[self.particle][int(self.fadeFrame)]
    
    
    
    class LaPew(pg.sprite.Sprite):
        speed = 10
        images: List[pg.Surface] = []
        textureIds: List[int] = []
        mass=2
        def __init__(self,pos,velocity,particle,size,life,spin,rotation, *groups):
            pg.sprite.Sprite.__init__(self, *groups)
            #for i in range(self.images.__len__()):
            #    self.images[i]=pg.transform.scale(self.images[i],(20*CAMERA_SCALE,35*CAMERA_SCALE))
            self.image = pg.transform.scale(self.images[particle],(20*CAMERA_SCALE/2,35*CAMERA_SCALE/2))
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
            self.rect.size=size
            self.velocity=velocity
            self.gravity=[0,0]
            self.width=size[0]
            self.height=size[1]
            self.spin=spin
            self.pos=pos
            self.onGround=0
            self.friction=0
            self.imgid=self.textureIds[particle]
            self.imgidy=None
            self.life=life
            self.stuck=0
            self.rotation=rotation
        def applyFriction(self,amount):
            if(self.velocity[0]**2<0.01):
                self.velocity[0]=0
            if(self.velocity[1]**2<0.01):
                self.velocity[1]=0
        def applyGravity(self):
            self.velocity[0]+=self.gravity[0]*60/FRAMERATE
            self.velocity[1]+=self.gravity[1]*60/FRAMERATE
        def collideAndMove(self,objs):
            objs2=[]
            self.rect.left-=self.rect.size[0]*11
            self.rect.top-=self.rect.size[1]*11
            size1=self.rect.size
            self.rect.size=(self.rect.size[0]*23,self.rect.size[1]*23)
            for i in pg.sprite.spritecollide(self,objs,0):
                objs2.append(i)
            objs=objs2
            self.rect.size=size1
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
                self.kill()
                return
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
                self.kill()
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
            self.rect.left=(self.pos[0])*CAMERA_SCALE
            self.rect.top=(self.pos[1])*CAMERA_SCALE
            if(self.rect.left<-1000)|(self.rect.left>2000)|(self.rect.top<-1000)|(self.rect.top>2000):
                self.kill()
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
        
    class GenericSingleFrameAttack(pg.sprite.Sprite):
        images: List[pg.Surface] = []
        textureIds: List[int] = []
        def __init__(self,x,y,w,h,v,*groups):
            pg.sprite.Sprite.__init__(self, *groups)
            self.image = pg.transform.scale(self.images[v], (20,20))
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
            self.pos=[x,y]
            self.width=w
            self.height=h
            self.imgid=self.textureIds[v]
            self.rect.size=[w,h]
            self.life=3
        def update(self):
            self.rect = self.rect.clamp(SCREENRECT)
            self.rect.left=(self.pos[0])*CAMERA_SCALE
            self.rect.top=(self.pos[1])*CAMERA_SCALE
            self.life-=1
            if(self.life<=0):
                self.kill()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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
            self.depth=0
        def update(self):
            if 'rect' in self.__dict__:
                self.rect = self.rect.clamp(SCREENRECT)
                self.rect.left=(self.pos[0])*CAMERA_SCALE
                self.rect.top=(self.pos[1])*CAMERA_SCALE
    
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
            self.depth=0
            self.imgid=self.textureIds[imgid]
            self.rect.size=[self.width,self.height]
        def update(self):
            if 'rect' in self.__dict__:
                self.rect = self.rect.clamp(SCREENRECT)
                self.rect.left=(self.pos[0])*CAMERA_SCALE
                self.rect.top=(self.pos[1])*CAMERA_SCALE
    
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
            self.depth=0
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
            if 'rect' in self.__dict__:
                self.rect = self.rect.clamp(SCREENRECT)
                self.rect.left=(self.pos[0])*CAMERA_SCALE
                self.rect.top=(self.pos[1])*CAMERA_SCALE
    
    class SaveMarker(pg.sprite.Sprite):
        images: List[pg.Surface] = []
        textureIds: List[int] = []
        def __init__(self,x,y,rid,*groups):
            pg.sprite.Sprite.__init__(self, *groups)
            self.pos=[x-20,y-20]
            self.depth=0
            self.image = pg.transform.scale(self.images[0], (20,20))
            self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
            self.width=60
            self.height=60
            self.roomid=rid
            self.imgid=self.textureIds[0]
            self.rect.size=[20,20]
        def update(self):
            if 'rect' in self.__dict__:
                self.rect = self.rect.clamp(SCREENRECT)
                self.rect.left=(self.pos[0]+20)*CAMERA_SCALE
                self.rect.top=(self.pos[1]+20)*CAMERA_SCALE
    
    
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
            if 'rect' in self.__dict__:
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
            if 'rect' in self.__dict__:
                self.rect = self.rect.clamp(SCREENRECT)
                self.rect.left=(self.pos[0])*CAMERA_SCALE
                self.rect.top=(self.pos[1])*CAMERA_SCALE
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
                        returns.append(Wall(i*20+offset[0],j*20+offset[1],20,20,6,roomsBuilt,allgroup))
                        returns[-1].depth=5
                        allgroup.change_layer(returns[-1],-5)
                    elif dataval==-1:
                        returns.append(Wall(i*20+offset[0],j*20+offset[1],20,20,0,roomsBuilt,allgroup))
                        #returns.append(Wall(i*20+offset[0],j*20+offset[1],20,20,6,roomsBuilt,allgroup))
                        #allgroup.change_layer(returns[-1],-5)
                    elif dataval==-2:
                        returns.append(Wall(i*20+offset[0],j*20+offset[1],20,20,6,roomsBuilt,allgroup))
                        returns[-1].depth=5
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
                            returns[-1].depth=5
                    if dataval in [-1]:
                        touchCount=0
                        n=[-1,6,7]
                        if(i>0):
                            if self.data[j][i-1] in n:
                                touchCount+=1
                        if(j>0):
                            if self.data[j-1][i] in n:
                                touchCount+=1
                        if(i<self.width-1):
                            if self.data[j][i+1] in n:
                                touchCount+=1
                        if(j<self.height-1):
                            if self.data[j+1][i] in n:
                                touchCount+=1
                        if(touchCount!=0):
                            returns.append(Wall(i*20+offset[0],j*20+offset[1],20,20,6,roomsBuilt,allgroup))
                            returns[-1].depth=5
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
    global newObjects
    newObjects=[]
    global newEattacks
    newEattacks=[]


    COMMAND_ARGUMENT_INT=21833
    COMMAND_ARGUMENT_FLOAT=21834
    COMMAND_ARGUMENT_STRING=21835
    COMMAND_ARGUMENT_STRING_GREEDY=21839

    COMMAND_ARGUMENT_INT_OPTIONAL=21836
    COMMAND_ARGUMENT_FLOAT_OPTIONAL=21837
    COMMAND_ARGUMENT_STRING_OPTIONAL=21838
    
    COMMAND_ARGUMENT_SPECIAL_VARIABLE=21701
    
    COMMAND_ARGUMENT_INVALID=21900
    COMMAND_ARGUMENT_MISSING=21901
    COMMAND_ARGUMENT_SPECIAL_VARIABLE_DNE=21901
    COMMAND_NONEXISTENT=21902
    COMMAND_ALREADY_EXISTS=21903


    global commandStorages
    commandStorages={}
    
    
    class invalidCommandError(Exception):
        pass
    class commandArgument:
        def __init__(self,type:int,name:str):
            self.type=type
            self.name=name
        def get_value(self,command,index):
            c=command.split(' ')
            if(c.__len__()<=index):
                if self.type in [COMMAND_ARGUMENT_INT_OPTIONAL,COMMAND_ARGUMENT_FLOAT_OPTIONAL,COMMAND_ARGUMENT_STRING_OPTIONAL]:
                    return None
                return COMMAND_ARGUMENT_MISSING
            b=c[index]
            if(self.type==COMMAND_ARGUMENT_INT)|(self.type==COMMAND_ARGUMENT_INT_OPTIONAL):
                if b.isdecimal():
                    return int(b)
                elif (b.count('-')==1)&(b[0]=='-')&b[1:].isdecimal()&(b.count('.')<=1):
                    return int(b)
                else:
                    return COMMAND_ARGUMENT_INVALID
            elif(self.type==COMMAND_ARGUMENT_FLOAT)|(self.type==COMMAND_ARGUMENT_FLOAT_OPTIONAL):
                if "".join(b.split('.')).isdecimal()&(b.count('.')<=1):
                    return float(b)
                elif (b.count('-')==1)&(b[0]=='-')&"".join(b[1:].split('.')).isdecimal()&(b.count('.')<=1):
                    return float(b)
                else:
                    return COMMAND_ARGUMENT_INVALID
            elif(self.type==COMMAND_ARGUMENT_STRING)|(self.type==COMMAND_ARGUMENT_STRING_OPTIONAL):
                return b
            elif self.type==COMMAND_ARGUMENT_SPECIAL_VARIABLE:
                if b.__len__()>3:
                    if [b[0]=='v',b[1]=='a',b[2]=='r',b[3]=='_']:
                        try: 
                            return getVariableValue(b[4:])
                        except:
                            return COMMAND_ARGUMENT_SPECIAL_VARIABLE_DNE
                    else:
                        return COMMAND_ARGUMENT_INVALID
                else:
                    return COMMAND_ARGUMENT_INVALID
            elif self.type==COMMAND_ARGUMENT_STRING_GREEDY:
                return " ".join(c[index:])

    class command:
        def __init__(self,**kwargs):
            self.name=kwargs['name']
            self.arguments=[]
            self.trigger=kwargs['triggerCommand']
            for i in kwargs['args'].split(" "):
                j=i.split(':')
                n=j[0]
                if j.__len__()>1:
                    ts=j[1]
                    if '|' not in ts:
                        if ts=='int':
                            self.arguments.append(commandArgument(COMMAND_ARGUMENT_INT,n))
                        elif ts=='float':
                            self.arguments.append(commandArgument(COMMAND_ARGUMENT_FLOAT,n))
                        elif ts=='str':
                            self.arguments.append(commandArgument(COMMAND_ARGUMENT_STRING,n))
                        elif ts=='str_greedy':
                            self.arguments.append(commandArgument(COMMAND_ARGUMENT_STRING_GREEDY,n))
                        elif ts=='int_opt':
                            self.arguments.append(commandArgument(COMMAND_ARGUMENT_INT_OPTIONAL,n))
                        elif ts=='float_opt':
                            self.arguments.append(commandArgument(COMMAND_ARGUMENT_FLOAT_OPTIONAL,n))
                        elif ts=='str_opt':
                            self.arguments.append(commandArgument(COMMAND_ARGUMENT_STRING_OPTIONAL,n))
                        elif ts=='var':
                            self.arguments.append(commandArgument(COMMAND_ARGUMENT_SPECIAL_VARIABLE,n))
                        else:
                            raise invalidCommandError
                    else:
                        self.arguments.append([])
                        for ts2 in ts.split('|'):
                            if ts2=='int':
                                self.arguments[-1].append(commandArgument(COMMAND_ARGUMENT_INT,n))
                            elif ts2=='float':
                                self.arguments[-1].append(commandArgument(COMMAND_ARGUMENT_FLOAT,n))
                            elif ts2=='str':
                                self.arguments[-1].append(commandArgument(COMMAND_ARGUMENT_STRING,n))
                            elif ts2=='str_greedy':
                                self.arguments[-1].append(commandArgument(COMMAND_ARGUMENT_STRING_GREEDY,n))
                            elif ts2=='int_opt':
                                self.arguments[-1].append(commandArgument(COMMAND_ARGUMENT_INT_OPTIONAL,n))
                            elif ts2=='float_opt':
                                self.arguments[-1].append(commandArgument(COMMAND_ARGUMENT_FLOAT_OPTIONAL,n))
                            elif ts2=='str_opt':
                                self.arguments[-1].append(commandArgument(COMMAND_ARGUMENT_STRING_OPTIONAL,n))
                            elif ts2=='var':
                                self.arguments[-1].append(commandArgument(COMMAND_ARGUMENT_SPECIAL_VARIABLE,n))
                            else:
                                raise invalidCommandError
        def execute(self,input):
            arg2=[(self.arguments[i].get_value(input,i+1) if type(self.arguments[i])==commandArgument else [self.arguments[i][j].get_value(input,i+1) for j in range(self.arguments[i].__len__())]) for i in range(self.arguments.__len__())]
            for i in range(arg2.__len__()):
                if type(self.arguments[i])!=commandArgument:
                    b=arg2[i]
                    for j in b:
                        if j not in [COMMAND_ARGUMENT_INVALID,COMMAND_ARGUMENT_MISSING,COMMAND_ARGUMENT_SPECIAL_VARIABLE_DNE,None]:
                            arg2[i]=j
                            break
                    if arg2[i]==b:
                        arg2[i]=COMMAND_ARGUMENT_INVALID
            if sum([i in [COMMAND_ARGUMENT_INVALID,COMMAND_ARGUMENT_MISSING,COMMAND_ARGUMENT_SPECIAL_VARIABLE_DNE] for i in arg2])!=0:
                return COMMAND_ARGUMENT_INVALID
            return self.trigger(arg2)

    class commandSystem:
        def __init__(self):
            self.commands={}
        def executeBase(self,commandI):
            
            cname=commandI.split(" ")[0]
            if cname not in self.commands:
                return COMMAND_NONEXISTENT
            else:
                return self.commands[cname].execute(commandI)
        def addCommand(self,commandD,toRun):
            
            cname=commandD.split(" ")[0]
            if cname in self.commands:
                return COMMAND_ALREADY_EXISTS
            cargs=' '.join(commandD.split(" ")[1:])
            self.commands[cname]=command(name=cname,args=cargs,triggerCommand=toRun)

    class renderObject(pg.sprite.Sprite):
        def __init__(self,pos,size,id,*groups):
            pg.sprite.Sprite.__init__(self, *groups)
            self.imgid=id
            self.rect=pg.Rect(*pos,*size)
    
    class textRenderer:
        textureIds:List[int]=[]
        charSizes:List[int]=[]
        chars:List[str]=[]
        def __init__(self,pos,size,renderGroup):
            self.pos=pos
            self.size=size
            self.rect=pg.Rect(*pos,*size)
            self.objects=[]
            self.rGroup=renderGroup
        def setText(self,text):
            for i in self.objects:
                i.kill()
            self.objects=[]
            pos=[0,0]
            for char in text:
                self.objects.append(renderObject((self.pos[0]+pos[0]+self.charSizes[self.chars.index(char)],self.pos[1]+pos[1]),(self.charSizes[self.chars.index(char)],10),self.textureIds[self.chars.index(char)],self.rGroup))
                pos[0]+=self.charSizes[self.chars.index(char)]*2







    def getVariableValue(source):
            global commandStorages

            a=None
            b=[]
            c=None
            d=None
            if('[' in source):
                a=source.split('[')[0]
                for x in source.split('[')[1:]:
                    if x[0] in '"\'':
                        x=x[1:-2]
                        b.append(x)
                    else:
                        x=x[:-1]
                        x=int(x)
                        b.append(x)
                c=[commandStorages[a]][0]
                for n in b[:-1]:
                    c=[c[n]][0]
                d=b[-1]
            else:
                c=[commandStorages][0]
                d=source
            return c[d]







    
    def main(winstyle=0):
        #global all
        global GUIelements
        #global winfo
        #global newParticles
        #global newObjects
        global splashtext
        global winfo,player,enemies,walls,platforms,all,boundaries,builtRooms,allb,enemyAttacks,healthBarRender,newParticles,newObjects,phyicsparticles,playerPewGroup,enemyAttacks
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
        img = load_image(imagefolder+r"\tictactoe\blank2.png")
        img2 = load_image(imagefolder+r"\tictactoe\blank1.png")
        img3 = load_image(imagefolder+r"\tictactoe\o.png")
        img4 = load_image(imagefolder+r"\specialgamev1\builtRoom.png")
        img4.set_colorkey([0,0,0])
        img3.set_colorkey([0,0,0])
        images={'hazard1':"hazard.png","save_marker":"devtextures\\savemarker.png","particle_blood":"devtextures\\savemarker.png",'tile1':"tiles\\bricksFull.png",'tile2':"tiles\\intentionallyempty.png",'tile3':"tiles\\brickStairsLeft.png",'tile4':"tiles\\brickStairsRight.png",'tile5':"tiles\\brickStairsInvertedright.png",'tile6':"tiles\\brickStairsInvertedLeft.png"}
        crops={'tile1':(0,0,20,16)}
        retextures={'tile3':'tile1','tile4':'tile1','tile5':'tile1','tile6':'tile1'}
        backgrounds={'tile-2':'tile1'}
        tints={'particle_blood':[255/255,50/255,50/255]}
        retransparency={'particle_blood':64}
    
    
    
    
    
    
        
    
    
    
        
        for i in images:
            images[i]=load_image(imagefolder+"\\specialgamev1\\"+images[i])
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
        for i in retransparency:
            baseimage=images[i]
            for j in range(retransparency[i]):
                z=baseimage.copy()
                z.set_alpha(255*(retransparency[i]-j)/retransparency[i])
                images[i+"_trans_"+str(j)]=z
        imagesb={}
        for i in images:
            print("LOADING TEXTURE \""+i+"\"")
            splashtext=("LOADING TEXTURE \""+i+"\"")
            imagesb[i]=loadTexture(surface_array(images[i]))
            pg.time.wait(10)
        font=pg.font.Font(None,60)
        for i in "asdfghjklqwertyuiopzxcvbnm 1234567890-=`~!@#$%^&*()_+QWERTYUIOP{}[]ASDFGHJKL:ZXCVBNM<>?,./\\|;'\"":
            print("LOADING FONT CHAR "+i+"")
            splashtext=("LOADING FONT CHAR "+i+"")
            z=font.render(i,True,(0,255,0),(0,1,0))
            
            textRenderer.textureIds.append(loadTexture(surface_array(z)))
            textRenderer.chars.append(i)
            textRenderer.charSizes.append(z.get_rect().size[0]/3)
            pg.time.wait(10)
        Background.images.append(img2)
        barTextures=["leftb.png","midb.png","rightb.png","leftf0.png","leftf1.png","leftf2.png","midf0.png","midf1.png","midf2.png","rightf0.png","rightf1.png","rightf1.png"]
        barTextures=[load_image(imagefolder+"\\specialgamev1\\healthbar\\"+i) for i in barTextures]
        barTexturesb=[loadTexture(surface_array(i)) for i in barTextures]
        for i in barTextures:
            i.set_colorkey([0,0,0])
        animations={}
        for i in animationsList:
            for j in animationsList[i]:
                for k in range(animationsList[i][j]):
                    k=k+1
                    animations['anim_'+str(i)+"_"+str(j)+"_"+str(k)]=load_image(imagefolder+"\\specialgamev1\\"+'anim_'+str(i)+"_"+str(j)+"_"+str(k)+".png")
                    print('anim_'+str(i)+"_"+str(j)+"_"+str(k))
                    splashtext="Loading Image "+('anim_'+str(i)+"_"+str(j)+"_"+str(k))            
                    pg.time.wait(10)
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
        PhysicsParticle.images.append([images[i] for i in images if 'particle_blood' in i])
        LaPew.images.append(images['particle_blood'])
        GenericSingleFrameAttack.images.append(images['particle_blood'])
    
    
        animationsb={}
        for i in animations:
            print("LOADING TEXTURE ANIMATION \""+i+"\"")
            animationsb[i]=loadTexture(surface_array(animations[i]))
            splashtext="Finalizing Texture"+(i)
            pg.time.wait(10)
    
    
    
    
    
    
    
        Player.textureIds = [animationsb[i] for i in animationsb if ('player' in i)]
        Wall.textureIds = [imagesb[i] for i in ["tile1","tile2","tile3","tile4","tile5","tile6",'tile-2']]
        Hazard.textureIds = [imagesb['hazard1']]
        SaveMarker.textureIds = [imagesb['save_marker']]
        RoomBoundary.textureIds.append(loadTexture(surface_array(img3)))
        BuiltRoom.textureIds.append(loadTexture(surface_array(img4)))
        PhysicsParticle.textureIds.append([imagesb[i] for i in imagesb if 'particle_blood' in i])
        LaPew.textureIds.append(imagesb['particle_blood'])
        GenericSingleFrameAttack.textureIds.append(imagesb['particle_blood'])
        # decorate the game window
        #icon = pg.transform.scale(Alien.images[0], (32, 32))
        #pg.display.set_icon(icon)
        #pg.display.set_caption("Pygame Aliens")
        #pg.mouse.set_visible(0)
    
        Enemeh.images=Player.images
        Enemeh.textureIdsAll=[Player.textureIds]
    
        
        # create the background, tile the bgd image
        bgdtile = load_image(imagefolder+r"\backgroundm.png")
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
        playerPewGroup=pg.sprite.Group()
        enemyAttacks=pg.sprite.Group()
        boundaries = pg.sprite.Group()
        builtRooms = pg.sprite.Group()
        healthBarRender=Bar(10,10,barTextures,barTexturesb,10,10,10,0,GUIelements)
        # Create Some Starting Values
        clock = pg.time.Clock()
    
        




















        global fps
        fps=[0]
        commandStorages['fps']=[fps][0]

        global tickingFiles
        tickingFiles=[]
        global initFiles
        initFiles=[]
        global protectedVariables
        protectedVariables=[]
        global rOnlyVariables
        rOnlyVariables=['fps']
        global files
        files={}

        files['tpRelative']='\n'.join(["variable playerpos_old command player.pos",
        "variable playerpos_new arrayize ???",
        "variable playerpos_new append_var playerpos_old[0]",
        "variable playerpos_new append_var playerpos_old[1]",
        "variable xoffset arrayize args[0]",
        "variable xoffset append 0",
        "variable xoffset var xoffset[0]",
        "variable xoffset type float",
        "variable yoffset arrayize args[1]",
        "variable yoffset append 0",
        "variable yoffset var yoffset[0]",
        "variable yoffset type float",
        "variable playerpos_new[0] sum playerpos_new[0] xoffset",
        "variable playerpos_new[1] sum playerpos_new[1] yoffset",
        "tp var_playerpos_new[0] var_playerpos_new[1]"
        ])

        files['setPlayerHealth']='\n'.join(["variable player command get_player",
        'variable playerAttr command variable player attr attributes',
        "variable args[0] type int",
        "variable playerAttr['health'] var args[0]"
        ])

        files['healPlayer']='\n'.join(["variable player command get_player",
        'variable playerAttr command variable player attr attributes',
        "variable args[0] type int",
        "variable playerAttr['health'] sum playerAttr['health'] args[0]",
        "variable playerAttr['health'] min playerAttr['health'] playerAttr['maxhealth']"
        ])


        
        files['loadPlayerVariables']='\n'.join(["variable player command get_player",
        'variable player.attr command variable player attr attributes',
        'variable player.pos command variable player attr pos',
        'variable player.vel command variable player attr velocity',
        'variable player.onGround command variable player attr onGround',
        'variable player.fireCooldown command variable player attr firecooldown',
        'variable player.ducking command variable player attr ducking',
        'variable player.shotsLeft command variable player attr shotsleft',
        'variable player.reloadTime command variable player attr reloadTime',
        './lockVariable player',
        './protectVariable player.attr',
        './protectVariable player.pos',
        './protectVariable player.vel',
        './lockVariable player.onGround',
        './lockVariable player.fireCooldown',
        './lockVariable player.ducking',
        './lockVariable player.shotsLeft',
        './lockVariable player.reloadTime'
        ])

        initFiles.append('loadPlayerVariables')
        
        files['terminateIfPlayerDead']='\n'.join([
        'variable isDead command a<=b player.attr[\'health\'] 0',
        "?execute isDead ./programTerminate"
        ])

        tickingFiles.append('terminateIfPlayerDead')
        
        def executeFile(fname):
            n=files[fname]
            n=n.split('\n')
            for m in n:
                #print(m)
                #print(cmdsys.executeBase(m))
                cmdsys.executeBase(m)
                
        global cmdsys
        cmdsys=commandSystem()
        cmdsys.addCommand("declare x:str",lambda x:print(x))
        def tpCommand(args):
            global player
            player.pos[0]=args[0]*20
            player.pos[1]=args[1]*20
            player.velocity=[0,0]
            return (int(player.pos[0])/20,int(player.pos[1])/20)
        def playerPos(args):
            global player
            return (int(player.pos[0])/20,int(player.pos[1])/20)
        def setGravCommand(args):
            global player
            player.gravity[0]=args[0]
            player.gravity[1]=args[1]
        def setVelocityCommand(args):
            global player
            player.velocity[0]=args[0]
            player.velocity[1]=args[1]
        def summonCommand(args):
            global player
            p=playerPos([])
            if(args[1]==None):
                args[1]=p[0]
                args[2]=p[1]
            if args[0]=="meh":
                x=Enemeh(args[1]*20,args[2]*20,enemies,all)
            else:
                return "Eh, the enemy "+str(args[0])+" doesnt exist yet."
        def placeRoomCommand(args):
            global player
            global rooms
            if args[0] in rooms:
                rooms[args[0]].buildRoom([int(args[1])*20,int(args[2])*20],walls,platforms,all,boundaries,builtRooms,allb)
            elif int(args[0]) in rooms:
                rooms[int(args[0])].buildRoom([int(args[1])*20,int(args[2])*20],walls,platforms,all,boundaries,builtRooms,allb)
            else:
                return "Error! Room "+args[0]+" nonexistent!"


        """def getVariableValue(source):
            global commandStorages

            a=None
            b=[]
            c=None
            d=None
            if('[' in source):
                a=source.split('[')[0]
                for x in source.split('[')[1:]:
                    if x[0] in '"\'':
                        x=x[1:-2]
                        b.append(x)
                    else:
                        x=x[:-1]
                        x=int(x)
                        b.append(x)
                c=[commandStorages[a]][0]
                for n in b[:-1]:
                    c=[c[n]][0]
                d=b[-1]
            else:
                c=[commandStorages][0]
                d=source
            return c[d]"""
        
        def variableCommand(args):
            global commandStorages
            global cmdsys
            global protectedVariables
            global rOnlyVariables
            
            a=None
            b=[]
            c=None
            d=None
            if('[' in args[0]):
                a=args[0].split('[')[0]
                for x in args[0].split('[')[1:]:
                    if x[0] in '"\'':
                        x=x[1:-2]
                        b.append(x)
                    else:
                        x=x[:-1]
                        x=int(x)
                        b.append(x)
                c=[commandStorages[a]][0]
                for n in b[:-1]:
                    c=[c[n]][0]
                d=b[-1]
            else:
                c=[commandStorages][0]
                d=args[0]

            if args[1]=='attr':
                a=c[d].__getattribute__(args[2])
                if(type(a) in [str,list,dict,tuple,int,float]):
                    return a
                else:
                    return a()

            if args[0].split('[')[0] in rOnlyVariables:
                return COMMAND_ARGUMENT_SPECIAL_VARIABLE_DNE
            if args[0] in protectedVariables:
                return COMMAND_ARGUMENT_SPECIAL_VARIABLE_DNE
            if(args[1]=='var'):
                c[d]=getVariableValue(args[2])
            elif(args[1]=='command'):
                c[d]=cmdsys.executeBase(args[2])
            elif(args[1]=='value'):
                c[d]=args[2]
            elif(args[1]=='value_int'):
                c[d]=int(args[2])
            elif(args[1]=='value_float'):
                c[d]=float(args[2])
            elif(args[1]=='append'):
                c[d].append(args[2])
            elif(args[1]=='append_var'):
                c[d].append(getVariableValue(args[2]))
            elif(args[1]=='pop'):
                return c[d].pop(int(args[2]))
            elif(args[1]=='type'):
                if args[2]=='str':
                    c[d]=str(c[d])
                elif args[2]=='int':
                    c[d]=int(c[d])
                elif args[2]=='float':
                    c[d]=float(c[d])
            elif args[1]=='sum':
                m=args[2].split(' ')
                c[d]=sum([getVariableValue(i) for i in m])
            elif args[1]=='subtract':
                m=args[2].split(' ')
                c[d]=getVariableValue(m[0])-getVariableValue(m[1])
            elif args[1]=='min':
                m=args[2].split(' ')
                c[d]=min(getVariableValue(m[0]),getVariableValue(m[1]))
            elif args[1]=='max':
                m=args[2].split(' ')
                c[d]=max(getVariableValue(m[0]),getVariableValue(m[1]))
            elif args[1]=='divide':
                m=args[2].split(' ')
                c[d]=getVariableValue(m[0])/getVariableValue(m[1])
            elif args[1]=='multiply':
                m=args[2].split(' ')
                y=1
                for i in m:
                    y*=getVariableValue(i)
                c[d]=y
            elif args[1]=='arrayize':
                try:
                    c[d]=[getVariableValue(args[2])]
                except:
                    c[d]=[]
        
        def getVariableCommand(args):
            return getVariableValue(args[0])
        def runFileCommand(args):
            global commandStorages
            commandStorages['args']=args[1].split(' ')
            return executeFile(args[0])
        def runFileCommand_argless(args):
            return executeFile(args[0])

        def getEnemyCommand(args):
            global enemies
            retval=[]

            capAmount=99999999
            startpos=[0,0]
            distanceMin=0
            distanceMax=99999999
            typeRequirements=[]
            l=args[0].split(' ')
            for i in l:
                if(i.split('=')[0]=='x'):
                    startpos[0]=float(i.split('=')[1])
                elif(i.split('=')[0]=='y'):
                    startpos[1]=float(i.split('=')[1])
                elif(i.split('=')[0]=='d_min'):
                    distanceMin=float(i.split('=')[1])
                elif(i.split('=')[0]=='d_max'):
                    distanceMax=float(i.split('=')[1])
                elif(i.split('=')[0]=='c_max'):
                    capAmount=int(i.split('=')[1])
                elif(i.split('=')[0]=='type'):
                    typeRequirements.append(i.split('=')[1])
            for i in enemies:
                dist=((startpos[0]-i.pos[0])**2+(startpos[1]-i.pos[1])**2)**0.5
                if dist/20>=distanceMin:
                    if dist/20<=distanceMax:
                        if typeRequirements!=[]:
                            if type(i).__name__ in typeRequirements:
                                retval.append([i][0])
                                if retval.__len__()>=capAmount:
                                    break
                            
            return retval
        def getPlayerCommand(args):
            global player
            return [player][0]
        def getRenderableObjectCommand(args):
            global all
            retval=[]

            capAmount=99999999
            startpos=[0,0]
            distanceMin=0
            distanceMax=99999999
            typeRequirements=[]
            l=args[0].split(' ')
            for i in l:
                if(i.split('=')[0]=='x'):
                    startpos[0]=float(i.split('=')[1])
                elif(i.split('=')[0]=='y'):
                    startpos[1]=float(i.split('=')[1])
                elif(i.split('=')[0]=='d_min'):
                    distanceMin=float(i.split('=')[1])
                elif(i.split('=')[0]=='d_max'):
                    distanceMax=float(i.split('=')[1])
                elif(i.split('=')[0]=='c_max'):
                    capAmount=int(i.split('=')[1])
                elif(i.split('=')[0]=='type'):
                    typeRequirements.append(i.split('=')[1])
            #print(typeRequirements)
            for i in all:
                dist=((startpos[0]-i.pos[0])**2+(startpos[1]-i.pos[1])**2)**0.5
                if dist/20>=distanceMin:
                    if dist/20<=distanceMax:
                        if typeRequirements!=[]:
                            if type(i).__name__ in typeRequirements:
                                retval.append([i][0])
                                if retval.__len__()>=capAmount:
                                    break
                            else:
                                pass#print(type(i).__name__)

        def checkMatchesVariableValueCommand(args):
            if getVariableValue(args[0])==args[1]:
                return True
            return False
        def checkMatchesVariableVarCommand(args):
            if getVariableValue(args[0])==getVariableValue(args[1]):
                return True
                
            return False
        def checkComparegVariableVarCommand(args):
            if getVariableValue(args[0])>getVariableValue(args[1]):
                return True
            return False
        def checkComparegeqVariableVarCommand(args):
            if getVariableValue(args[0])>=getVariableValue(args[1]):
                return True
            return False
        def checkCompareneqVariableVarCommand(args):
            if getVariableValue(args[0])!=getVariableValue(args[1]):
                return True
            return False
        def checkComparegVariableValueCommand(args):
            if getVariableValue(args[0])>(args[1]):
                return True
            return False
        def checkComparegeqVariableValueCommand(args):
            if getVariableValue(args[0])>=(args[1]):
                return True
            return False
        def checkComparelVariableValueCommand(args):
            if getVariableValue(args[0])<(args[1]):
                return True
            return False
        def checkCompareleqVariableValueCommand(args):
            if getVariableValue(args[0])<=(args[1]):
                return True
            return False
        def checkCompareneqVariableValueCommand(args):
            if getVariableValue(args[0])!=(args[1]):
                return True
            return False
        def invertValue(args):
            return not getVariableValue(args[0])
        def invertCommandResult(args):
            global cmdsys
            return not cmdsys.executeBase(args[0])
        def terminateCommand(args):
            global player,inCmdConsole
            inCmdConsole=-1
            player.kill()

        def conditionalRunCommand(args):
            if(getVariableValue(args[0])):
                cmdsys.executeBase(args[1])

        def conditionalRunCommandWhileLoop(args):
            if(getVariableValue(args[0])):
                cmdsys.executeBase(args[1])
                conditionalRunCommandWhileLoop(args)
        def addProtectedVariableCommand(args):
            global protectedVariables
            protectedVariables.append(args[0])
        def addReadOnlyVariableCommand(args):
            global rOnlyVariables
            rOnlyVariables.append(args[0])
        
        cmdsys.addCommand("tp target:var x:float|var y:float|var",tpCommand)
        cmdsys.addCommand("setGrav x:float|var y:float|var",setGravCommand)
        cmdsys.addCommand("setVel x:float|var y:float|var",setVelocityCommand)
        
        cmdsys.addCommand("player.pos",playerPos)
        cmdsys.addCommand("placeRoom id:str x:int y:int",placeRoomCommand)
        cmdsys.addCommand("\summon id:str x:int_opt y:int_opt",summonCommand)

        
        cmdsys.addCommand("variable varname:str operation:str with:str_greedy",variableCommand)
        cmdsys.addCommand("variable_get varname:str",getVariableCommand)
        cmdsys.addCommand("get_enemy args:str_greedy",getEnemyCommand)
        cmdsys.addCommand("get_object args:str_greedy",getRenderableObjectCommand)
        cmdsys.addCommand("get_player",getPlayerCommand)
        
        cmdsys.addCommand("executeFile filename:str args:str_greedy",runFileCommand)
        cmdsys.addCommand("executeFile_argless filename:str",runFileCommand_argless)

        
        
        cmdsys.addCommand("a==b variable:str value:int|float|str",checkMatchesVariableValueCommand)
        cmdsys.addCommand("a==v variable:str var:str",checkMatchesVariableVarCommand)
        cmdsys.addCommand("a>b a:str b:int|float|str",checkComparegVariableValueCommand)
        cmdsys.addCommand("a>=b a:str b:int|float|str",checkComparegeqVariableValueCommand)
        cmdsys.addCommand("a<b a:str b:int|float|str",checkComparelVariableValueCommand)
        cmdsys.addCommand("a<=b a:str b:int|float",checkCompareleqVariableValueCommand)
        cmdsys.addCommand("a!=b a:str b:int|float|str",checkCompareneqVariableValueCommand)

        cmdsys.addCommand("a>v a:str b:str",checkComparegVariableVarCommand)
        cmdsys.addCommand("a>=v a:str b:str",checkComparegeqVariableVarCommand)
        cmdsys.addCommand("a!=v a:str b:str",checkCompareneqVariableVarCommand)

        cmdsys.addCommand("!v v:str",invertValue)
        cmdsys.addCommand("!execute v:str_greedy",invertCommandResult)
        cmdsys.addCommand("?execute c:str v:str_greedy",conditionalRunCommand)
        cmdsys.addCommand("?while c:str v:str_greedy",conditionalRunCommandWhileLoop)
        cmdsys.addCommand("./programTerminate",terminateCommand)
        cmdsys.addCommand("./protectVariable variable:str",addProtectedVariableCommand)
        cmdsys.addCommand("./lockVariable variable:str",addReadOnlyVariableCommand)
        
        












        global cmdconsoletext,cmdconsole,inCmdConsole,cmdconsoledata,chatOldDisplay,chatStorage

        chatOldDisplay=[textRenderer([100,100+20*_],[500,100],GUIelements) for _ in range(5)]
        cmdconsole=textRenderer([100,200],[500,100],GUIelements)
        cmdconsoletext="mewo"
        cmdconsoledata=[[""],[0,0]]
        chatStorage=["","","","","Welcome to the chat!"]
        cmdconsole.setText(cmdconsoletext)
        inCmdConsole=False









        
        enemies = pg.sprite.Group()
    
        # initialize our starting sprites
        #backgroundObject=Background(all)
        #all.change_layer(backgroundObject,-1000)
        global player
        player = Player(all)
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
                              "000 000 000 000 000 000 000 000 001 000 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "000 000 000 000 000 000 000 000 000 001 000 000 000 000 000 000 000 000 000 000".replace(' ',''),
                              "101 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 011 000".replace(' ',''),
                              "000 000 001 001 001 000 001 001 001 001 000 000 000 000 000 000 000 001 001 001".replace(' ',''),
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
        splashtext="Loading Complete!"
        pg.time.wait(1000)
        import pyautogui
        i=pyautogui.getWindowsWithTitle('tk')
        i[0].close()
        
        #splashthread._stop()
        global events
        events=[]
        def updateLoop():
            global pg
            global key
            global mouse
            global events
            global inCmdConsole
            global winfo,player,enemies,walls,platforms,all,boundaries,builtRooms,allb,enemyAttacks,healthBarRender,newParticles,newObjects,phyicsparticles,playerPewGroup,enemyAttacks
            while player.alive():
                winfo=pg.display.Info()
                if walls.__len__()==0:
                    rooms[0].buildRoom([0,0],walls,platforms,all,boundaries,builtRooms,allb)
                    floors=[]
                    print(all.sprites().__len__())
                # get input
                for event in events:
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
                    if event.type == pg.KEYUP:
                        if(event.key==pg.K_t):
                            inCmdConsole=1
                            #cmdsys.executeBase("declare mewo")
                #<Event(769-KeyUp {'unicode': 'a', 'key': 97, 'mod': 36864, 'scancode': 4, 'window': None})>,
                events=[]
                keystate = pg.key.get_pressed()
                cursorstate = pg.mouse.get_pressed()
                if inCmdConsole:
                    keystate=[0 for i in keystate]
                    cursorstate=[0 for i in cursorstate]
                #x=[i for i in range(keystate.__len__()) if keystate[i]!=0]
                #if x!=[]:
                #    print(x)
                # clear/erase the last drawn sprites
                #all.clear(screen, background)
        
                # update all the sprites
                # handle player input
                if inCmdConsole==0:
                    horizmove = keystate[100] - keystate[97]
                    jump = keystate[119]
                    down=keystate[115]
                    if down==0:
                        player.updateb([walls,platforms,all,boundaries,builtRooms,allb,enemyAttacks],horizmove,jump,cursorstate[0])
                    else:
                        player.updateb([walls,[],all,boundaries,builtRooms,allb,enemyAttacks],horizmove,jump,cursorstate[0])
                    #player.jump(jump)
                    healthBarRender.updateV(player.attributes['health'])
                    for i in newParticles:
                        PhysicsParticle(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]==1,i[7]==2,[0 if i.__len__()<9 else i[8]][0],[0 if i.__len__()<10 else i[9]][0],all,phyicsparticles)
                    for i in newObjects:
                        if i[0]==0:
                            LaPew(i[1],i[2],i[3],i[4],i[5],i[6],i[7], all,playerPewGroup)
                        if i[0]==1:
                            GenericSingleFrameAttack(i[1],i[2],i[3],i[4],i[5], all,enemyAttacks)
                        if i[0]==2:
                            x=Enemeh(i[1],i[2],enemies,all)
                            x.textureIds= x.textureIdsAll[i[3]]
                    newObjects=[]
                    newParticles=[]
                    if(phyicsparticles.sprites().__len__()>1000):
                        phyicsparticles.sprites()[0].kill()
                    for i in phyicsparticles:
                        i.updateb([walls])
                    for i in playerPewGroup:
                        i.updateb([walls])
                        #print('playerpewupdate')
                    for i in enemies:
                        i.updatec([walls,platforms,all,boundaries,builtRooms,allb,playerPewGroup],player)
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
                #drawAll(all)
                #drawGUI(GUIelements)
                #pg.display.flip()#update()#dirty)
        
                # cap the framerate at 40fps. Also called 40HZ or 40 times per second.
                clock.tick(FRAMERATE)
        global events2
        events2=[]
        def executeCmdConsoleupdate():
            global events2
            global inCmdConsole,cmdconsole,cmdconsoletext,cmdconsoledata,chatOldDisplay,chatStorage
            
            global tickingFiles
            
            while inCmdConsole!=-1:
                
                for event in events2:
                    if event.type == pg.QUIT:
                        return
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            if cmdconsoletext!="":
                                cmdconsoletext=''.join([i for i in cmdconsoletext][:-1])
                        elif event.key==pg.K_RETURN:
                            x=cmdsys.executeBase(cmdconsoletext)
                            cmdconsoledata[0].append(cmdconsoletext)
                            cmdconsoledata[1][1]=cmdconsoledata[0].__len__()
                            chatStorage.append(cmdconsoletext)
                            if x!=None:
                                chatStorage.append(str(x))
                            cmdconsoletext=""
                            






                        
                        elif event.key == pg.K_ESCAPE:
                            cmdconsoletext=""
                            inCmdConsole=False
                            [chatOldDisplay[i].setText("#") for i in range(5)]
                        elif event.key == pg.K_UP:
                            cmdconsoledata[1][1]=max(0,cmdconsoledata[1][1]-1)
                            cmdconsoletext=cmdconsoledata[0][cmdconsoledata[1][1]]
                        elif event.key == pg.K_DOWN:
                            cmdconsoledata[1][1]=min(cmdconsoledata[0].__len__(),cmdconsoledata[1][1]+1)
                            if(cmdconsoledata[1][1]!=cmdconsoledata[0].__len__()):
                                cmdconsoletext=cmdconsoledata[0][cmdconsoledata[1][1]]
                            else:
                                cmdconsoletext=""
                        else:
                            cmdconsoletext+=event.unicode        
                        cmdconsole.setText(cmdconsoletext)
                if(inCmdConsole):
                    pass
                    [chatOldDisplay[i].setText(chatStorage[i-5]) for i in range(5)]
                #<Event(769-KeyUp {'unicode': 'a', 'key': 97, 'mod': 36864, 'scancode': 4, 'window': None})>,
                events2=[]
                clock.tick(FRAMERATE)
                for f in tickingFiles:
                    executeFile(f)
        global key
        global mouse
        key=pg.key
        mouse=pg.mouse
        def renderLoop(*threads):
            global fps
            global all
            global GUIelements
            global events,events2
            global key
            global mouse
            import time
            global inCmdConsole
            global player
            lastFrameStart=time.time()
            frameStart=time.time()+1
            try:
                while player.alive():
                    lastFrameStart=frameStart
                    frameStart=time.time()
                    x=pg.event.get()
                    if(inCmdConsole):
                        events2=x
                    else:
                        events=x
                    drawAll(all)
                    drawGUI(GUIelements)
                    pg.display.flip()
                    spf=frameStart-lastFrameStart
                    if spf!=0:
                        fps[0]=1/spf
                    else:
                        fps[0]=100000
                    #print(fps)
                    #clock.tick(FRAMERATE)
                    stopall=0
                    for i in threads:
                        if i._is_stopped==1:
                            stopall=1
                    if stopall:
                        for i in threads:
                            if i._is_stopped==0:
                                i._stop()
                        return
            except:
                inCmdConsole=-1
                player.kill()
                return
        for i in cmdsys.commands:
            print(i)
        for i in initFiles:
            executeFile(i)
        chatthread=threading.Thread(target=executeCmdConsoleupdate)
        chatthread.start()
        updatethread=threading.Thread(target=updateLoop)
        updatethread.start()

        
        
        renderLoop(chatthread,updatethread)
        """while player.alive():
            winfo=pg.display.Info()
            if walls.__len__()==0:
                rooms[0].buildRoom([0,0],walls,platforms,all,boundaries,builtRooms,allb)
                floors=[]
                print(all.sprites().__len__())
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
            #if(enemies.sprites().__len__()<1):
            #    Enemeh(200,-50,enemies,all)
            horizmove = keystate[100] - keystate[97]
            jump = keystate[119]
            down=keystate[115]
            if down==0:
                player.updateb([walls,platforms,all,boundaries,builtRooms,allb,enemyAttacks],horizmove,jump,cursorstate[0])
            else:
                player.updateb([walls,[],all,boundaries,builtRooms,allb,enemyAttacks],horizmove,jump,cursorstate[0])
            #player.jump(jump)
            healthBarRender.updateV(player.attributes['health'])
            for i in newParticles:
                PhysicsParticle(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]==1,i[7]==2,[0 if i.__len__()<9 else i[8]][0],[0 if i.__len__()<10 else i[9]][0],all,phyicsparticles)
            for i in newObjects:
                if i[0]==0:
                    LaPew(i[1],i[2],i[3],i[4],i[5],i[6],i[7], all,playerPewGroup)
                if i[0]==1:
                    GenericSingleFrameAttack(i[1],i[2],i[3],i[4],i[5], all,enemyAttacks)
                if i[0]==2:
                    x=Enemeh(i[1],i[2],enemies,all)
                    x.textureIds= x.textureIdsAll[i[3]]
            newObjects=[]
            newParticles=[]
            if(phyicsparticles.sprites().__len__()>1000):
                phyicsparticles.sprites()[0].kill()
            for i in phyicsparticles:
                i.updateb([walls])
            for i in playerPewGroup:
                i.updateb([walls])
                #print('playerpewupdate')
            for i in enemies:
                i.updatec([walls,platforms,all,boundaries,builtRooms,allb,playerPewGroup],player)
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
            clock.tick(FRAMERATE)"""
        
        if pg.mixer:
            pg.mixer.music.fadeout(1000)
        pg.time.wait(1000)
    
    
    # call the "main" function if running this script
    if __name__ == "__main__":
        main(pg.OPENGL)
        pg.quit()
