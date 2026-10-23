#rpg    version  1. 6.0
#version erklärt:
#first: 1=pre version,2=Alpha,3=Beta,4=Fullgame
#second: days of worktime on that version 1min a day== 4hours a day
#third:  a bugged version of the previous (temporary)
# instead of comments the funcions are named
import tkinter as tk
import random
import math
import time

fehler=0
def settings():
    global admin,scale,delay,brush,ot,nt,mapx,mapy,size2,mx,my,animate,sx,sy,cx,cy,px,py,pdir,layer,d,layermode,speed,dimention,hints
    #real settings
    hints=1     #-1 for never 0 for off but tooglable 1 for on but togglable
    admin=0     #toggles a lot of debug features and mapmaking features
    scale=2         #also supports floats blub :O(floats over 1 sometimes buggy and 0.5<scale<1 doesnt work complettly)
    #engine settings
    delay =10   #dont change

    #drawing
    brush=55
    layer=1
    layermode=0
    #time stuff
    ot=time.time()
    nt=time.time()
    #map
    dimention=0
    mapx=200    #only change if you dont want to draw
    mapy=200     #only change if you dont want to draw
    size2 =mapx*mapy
    #mouse pos
    mx=0
    my=0
    #animation yipeee
    animate=[0,0,0,0,0,0,0,0,0]
    #screen
    d=1        #viewing range
    sx=17*d     #screensize x yk
    sy=13*d     #screensize y yk

    #player
    cx=0        #camera x pos bleh
    cy=0        #camera y pos bleh
    px=mapx//2     #player pos x
    py=mapy//2    #player pos x
    pdir=3          #starting direction
    speed=2
    if admin==1:    #makes sure settings are right for admin
        scale=1
        sx=sx//d
        sy=sy//d
        d=1


settings()
try:
    global scale,admin,d,wm
    #window setup
    window = tk.Tk()
    window.title("BLEH")
    window.geometry(str(int(480*scale+(32*20*scale*admin)-16*scale)*d)+"x"+str(int(360*scale+admin*64)*d))
    canvas = tk.Canvas(window, width=(int(480*scale+(32*20*scale*admin)-16*scale)*d), height=(int(360*scale+admin*64)*d), bg="black")
    canvas.pack()
    wm=0    #window move???
except:
    print("WINDOW ERROR")
    exit ("WINDOW ERROR")

def correctpath(file):
    import os
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, file)
    return path

#load tileset
def load_img():
    global images,p_img,scale,gridback,tileanim
    images=[]
    p_img=[]
    for i in range(13):
        for i2 in range(18):
            png="BILDER/TILESETCUT/TILES/"+"row-"+str(i+1)+"-column-"+str(i2+1)+".png"
            png=correctpath(png)
            png = tk.PhotoImage(file=png)
            if scale >=0.5:
                png = png.zoom(int(2*scale), int(2*scale))
            else:
                png = png.subsample(int(0.5/scale),int(0.5/scale))
            images.append(png)
    png="BILDER/TILESETCUT/TILES/background.png"
    png=correctpath(png)
    png = tk.PhotoImage(file=png)
    if scale >=0.5:
        png = png.zoom(int(2*scale), int(2*scale))
    else:
        png = png.subsample(int(0.5/scale),int(0.5/scale))
    gridback=png

    tileanim=[]
    for i in range(8):
        png="BILDER/TILESETCUT/ANIMATION/water"+str(i+1)+".png"
        png=correctpath(png)
        png = tk.PhotoImage(file=png)
        if scale >=0.5:
            png = png.zoom(int(2*scale), int(2*scale))
        else:
            png = png.subsample(int(0.5/scale),int(0.5/scale))
        tileanim.append(png)
    for i in range(8):
        png="BILDER/TILESETCUT/ANIMATION/waterside"+str(i+1)+".png"
        png=correctpath(png)
        png = tk.PhotoImage(file=png)
        if scale >=0.5:
            png = png.zoom(int(2*scale), int(2*scale))
        else:
            png = png.subsample(int(0.5/scale),int(0.5/scale))
        tileanim.append(png)

    names=("run","idle")
    for i3 in names:
        for i in range(4):
            for i2 in range(6):
                png="BILDER/TILESETCUT/PLAYER/player_"+i3+"_dir_"+str(i+1)+"."+str(i2)+".png"
                png=correctpath(png)
                png = tk.PhotoImage(file=png)
                if scale >=0.5:
                    png = png.zoom(int(2*scale), int(2*scale))
                else:
                    png = png.subsample(int(0.5/scale),int(0.5/scale))
                p_img.append(png)
#resets
def reset():
    global blocks,images,size2,mapx,mapy,dim,dimention,block,block2,block3
    block=[]
    block2=[]
    block3=[]
    blocks=[block,block2,block3]
    border = 7
    for ii in range(1):
        for y in range(mapy):
            for x in range(mapx):
                # outer 6 layers
                if x < border-1 or x >= mapx-(border-1) or y < border-1 or y >= mapy-(border-1):
                    blocks[ii].append(300)
                # innermost border (7th layer)
                elif x == border-1 or x == mapx-border or y == border-1 or y == mapy-border:
                    # corners
                    if (x == border-1 and y == border-1):
                        blocks[ii].append(308)  # top-left
                    elif (x == mapx-border and y == border-1):
                        blocks[ii].append(308)  # top-right
                    elif (x == border-1 and y == mapy-border):
                        blocks[ii].append(0)  # bottom-left
                    elif (x == mapx-border and y == mapy-border):
                        blocks[ii].append(3)  # bottom-right
                    # edges
                    elif y == border-1:
                        blocks[ii].append(308)  # top edge
                    elif y == mapy-border:
                        blocks[ii].append(1)  # bottom edge
                    elif x == border-1:
                        blocks[ii].append(18)  # left edge
                    elif x == mapx-border:
                        blocks[ii].append(21)  # right edge
                # inside
                else:
                    blocks[ii].append(-1)



def loadworld():
    global images,size2,mapx,mapy,blocks,block,block2,block3,mapx,mapy
    block = []
    block2=[]
    block3=[]
    file="WORLD/WORLD.txt"
    file=correctpath(file)
    thefile = open(file, "r")
    all_lines = thefile.readlines()
    thefile.close()
    for i in all_lines:
        fn=i.strip().split(" ")
        i2=0
        for i in fn:
            fn2=i.split("/")[0]
            if i2<40000:
                block.append(int(fn2))
            elif i2<80000:
                block2.append(int(fn2))
            elif i2<120000:
                block3.append(int(fn2))
            i2+=1
    blocks=[block,block2,block3]

def save():
    global block,block2,block3
    a=""
    for i in block:
        a+=str(i)+" "
    for i in block2:
        a+=str(i)+" "
    for i in block3:
        a+=str(i)+" "
    file="WORLD/WORLD.txt"
    file=correctpath(file)
    thefile=open(file, "w")
    thefile.writelines(a)
    thefile.close()

#main loop
def Main():
    global delay,fehler,wm
    try:
        tick()
        render()
    except:
        fehler=fehler+1
        print("ERROR IN MAINLOOP")
        print("RESETING GAME")
        print()
        time.sleep(0.3)
        if fehler<5:
            fullreset()
        else:
            canvas.delete("all")
            exit("ERROR: Main not responding")
    else:
        fehler=0
    if wm==0:
        window.after(delay, Main)
    else:
        window.after(delay*15, Main)
    if wm>0:
        wm-=1


def render():
    global blocks,layermode,dimention,hints
    canvas.delete("all")
    if dimention==0:
        if admin==1:
            if layermode==0:
                tile_render(blocks[0],0,24)
                player_render()
                tile_render(blocks[1],1,24)
                tile_render(blocks[2],2,24)
            else:
                if layer==1:
                    tile_render(blocks[0],0,24)
                player_render()
                if layer==2:
                    tile_render(blocks[1],0,24)
                elif layer==3:
                    tile_render(blocks[2],0,24)
            AdMin()
        else:
            tile_render(blocks[0],0,24)
            player_render()
            tile_render(blocks[1],1,24)
            tile_render(blocks[2],2,24)
    elif dimention==1:
        if admin==1:
            if layermode==0:
                tile_render(dim[0],0,216)
                player_render()
                tile_render(dim[1],1,216)
                tile_render(dim[2],2,216)
            else:
                if layer==1:
                    tile_render(dim[0],0,216)
                player_render()
                if layer==2:
                    tile_render(dim[1],0,216)
                elif layer==3:
                    tile_render(dim[2],0,216)
            AdMin()
        else:
            tile_render(dim[0],0,216)
            player_render()
            tile_render(dim[1],1,216)
            tile_render(dim[2],2,216)
    if hints==1:
        hint()

#renders the background
def tile_render(block,rr,bb):
    global tileanim,animate,cube,delay,images,sx,sy,mapx,mapy,px,py,cx,cy,admin,ot,nt,d
    if px-sx//2>0:
        cx=px-sx//2
    else:
        cx=0
    if py-sy//2>0:
        cy=py-sy//2
    else:
        cy=0

    xc=-round((cx-cx//1)*32*scale)
    if xc == -(32*scale):
        xc=0
    yc=round((cy-cy//1)*32*scale)
    x = xc
    y = 360*scale*d+yc
    weg = math.floor(cx+math.floor(cy)*200)
    # RENDER BLOCKS
    for i in range(sy):
        for i in range(sx):
            if weg<len(block):
                if rr==0:
                    if bb<300:
                        img=images[bb]
                    else:
                        img=tileanim[bb-300+int(animate[6])]
                    canvas.create_image(x, y, image=img, anchor=tk.CENTER)
                if block[weg]!=-1:
                    if block[weg]<len(images) or block[weg]-300<len(tileanim):
                        if block[weg]<300:
                            img=images[block[weg]]
                        else:
                            img=tileanim[block[weg]-300+int(animate[6])]
                        canvas.create_image(x, y, image=img, anchor=tk.CENTER)
                    else:
                        block[weg]=-1
                        print("NOT LOADED")
            else:
                print("NOT IN BOUNDS")
            weg = weg + 1
            x = x + (32*scale)
        weg+=mapx-sx
        x = xc
        y -= 32*scale

#renders the player obisly
def player_render():
    global p_img,pdir,animate,px,py,sx,sy,scale,d
    if px-sx//2>0:
        ppx=480*d*scale//2
    else:
        ppx=(px*32*scale-32*scale//2)
    if py-sy//2>0:
        ppy=360*d*scale//2-16*scale
    else:
        ppy=(sy*32*scale-32*scale*1.85)-(py*32*scale-32*scale//2)-16*scale

    #see when player moved
    if tt>=0.25:
        img=p_img[(pdir-1)*6+math.floor(animate[4])+24]
    else:
        img=p_img[(pdir-1)*6+math.floor(animate[4])]
    canvas.create_image(ppx,ppy, image=img, anchor=tk.CENTER)


#level editing
def AdMin():
    global scale,images,px,py,layer,brush,gridback
    cube = canvas.create_rectangle(480*scale+32*scale-10, 0, 480*scale+32*scale+15, 360*scale, fill="white",outline="white")
    cube = canvas.create_rectangle(0, 360*scale, 480*scale+32*scale+15, 360*scale+64*scale, fill="white",outline="white")
    x = 480*scale+32*scale+15+16*scale+1
    y = 16*scale+1
    weg=0
    if dimention==0:
        a="black"
    elif dimention==1:
        a="white"
    canvas.create_text(60, 25, text=(px,"X",py,"Y"), fill=a, font=("Arial", 10))
    canvas.create_text(72, 50, text=("Layer:",layer,"Brushid:",brush), fill=a, font=("Arial", 10))
    canvas.create_text(60, 360*scale+20, text=("SAVE"), fill=a, font=("Arial", 30))
    for i in range(13):
        for i2 in range(18):
            img=gridback
            canvas.create_image(x, y, image=img, anchor=tk.CENTER)
            img=images[weg]
            canvas.create_image(x, y, image=img, anchor=tk.CENTER)
            if brush==weg:
                cube = canvas.create_rectangle(x-16*scale+1, y-16*scale+1, x+16*scale-1, y+16*scale-1, fill="",outline="purple")
            weg = weg + 1
            x = x + (32*scale)
        x = 480*scale+32*scale+15+16*scale+1
        y += 32*scale

def hint():
    if dimention==0:
        a="black"
    elif dimention==1:
        a="white"
    canvas.create_text(60, 360*scale-10, text=("H to toggle hints"), fill=a, font=("Arial", 10))
    canvas.create_text(60, 360*scale-30, text=("W A S D to Move"), fill=a, font=("Arial", 10))
#makes the logik
def tick():
    global cx,cy,px,py,mapy,mapx,animate,tt,nt,ot
    nt=time.time()
    tt=nt-ot
    if py<0:
        py=0
    elif py>mapy:
        py=0
    if px<0:
        px=0
    elif px>mapy:
        px=0
    px=round(px*10)/10
    py=round(py*10)/10
    for i in range(len(animate)):
        animate[i]+=0.2
        animate[i]=round(animate[i]*10)/10
        if animate[i]==i+2:
            animate[i]=0


#TASTEN
def move(event):
    global px,py,pdir,tt,ot,nt,layer,layermode,speed,hints
    if event.keysym == "Up" or event.keysym == "w":
        py+=0.2*speed
        pdir=1
        ot=nt
    if event.keysym == "Down" or event.keysym == "s":
        py-=0.2*speed
        pdir=2
        ot=nt
    if event.keysym == "Right" or event.keysym == "d":
        px+=0.2*speed
        pdir=3
        ot=nt
    if event.keysym == "Left" or event.keysym == "a":
        px-=0.2*speed
        pdir=4
        ot=nt
    if hints!=-1 and event.keysym == "h":
        hints=1-hints
    if admin==1:
        if event.keysym == "1" or event.keysym == "2" or event.keysym == "3":
            layer=int(event.keysym)
        elif event.keysym == "0":
            layermode=1-layermode
window.bind("<Key>", move)

#mouse pos
def mouse_pos(event):
    global mx, my
    mx, my = event.x, event.y
canvas.bind("<Motion>", mouse_pos)

#click detect
def brushing(event):
    global mx, my,scale,brush,sx,sy,px,py,mapx,block,block2,block3,layer,dim,dimention
    if admin==1:
        MX=mx-(480*scale+32*scale-10)
        MY=my
        MX=round(MX/(32*scale)-0.5)
        MY=round(MY/(32*scale)-0.5)
        if MX>=0:
            brush=MX+MY*18-1
            print(brush)
        elif my<360:
            MX=mx-(480*scale+32*scale-10)
            MY=my
            MX=round(MX/(32*scale)-0.2)
            MY=round(MY/(32*scale))
            id0=int(math.floor(px)+MX+(sx//2+1)-1+((math.floor(py)+0-(MY-5))*mapx))
            print(px,py,id0,MX,MY)
            if dimention==0:
                blocks[layer-1][id0]=brush
            elif dimention==1:
                dim[layer-1][id0]=brush
            render()
        else:
            save()

canvas.bind("<Button-1>", brushing)

last_pos = [window.winfo_x(), window.winfo_y()]

def windowmove(event):
    global wm
    x, y = window.winfo_x(), window.winfo_y()
    if (x, y) != tuple(last_pos):
        last_pos[0], last_pos[1] = x, y
        wm=5

window.bind("<Configure>", windowmove)


def fullreset():
    settings()
    canvas.delete("all")
    load_img()
    loadworld()
fullreset()
Main()

window.mainloop()
"""
plans
make more demition(house btw)
make mobs bleh pathfinder already there
"""
