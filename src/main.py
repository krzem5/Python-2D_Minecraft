from PIL import Image, ImageTk
from tkinter import *
import glob
import json
import math
import random
import time



class Block:
    all_blocks=[]
    all_blocks_d={}
    all_blocks_img=[]
    blocks={}
    all_names=[]
    all_names_add=[]
    def __init__(self,n,img=None):
        if not n.startswith('_'):
            if img==None:self.img=ImageTk.PhotoImage(Image.open(f'data\\img\\blocks\\{n}.png'))
            else:self.img=img
            self.n=n
            self.__class__.all_blocks.append(self)
            self.__class__.all_blocks_d[n]=self.img
            self.__class__.all_blocks_img.append(self.img)
            self.__class__.blocks[n]=self
            if not img==None:self.__class__.all_names_add.append(self.n)
        else:
            n=n[1:]
            for type_ in {'chestL':[('chestL',-1),('shestR',0)],'stairL':[('stairL',-1),('stairLU',1),('stairRU',3),('stairR',0)],'torchL':[('torchL',-1),('torchR',0)],'waterL':[('waterL',-1),('waterR',0),('waterB',[('waterL',-1),('waterL',0)])],'slabD':[('slabD',-1),('slabU',1),('slabR',2),('slabL',4)]}[n]:#flip t-b:1,flip r-l:0,rot 90-2,rot 180-3,rot 270-4
                if type(type_[1])==list:
                    bg,l=Image.open(f'data\\img\\blocks\\{type_[1][0][0]}.png').convert('RGBA'),[]
                    for tp_ in type_[1][1:]:
                        if not tp_[1]==-1:l.append(Image.open(f'data\\img\\blocks\\{tp_[0]}.png').convert('RGBA').transpose(tp_[1]))
                        else:l.append(Image.open(f'data\\img\\blocks\\{tp_[0]}.png').convert('RGBA'))
                    for img in l:bg=Image.alpha_composite(bg,img)
                    Block(type_[0],img=ImageTk.PhotoImage(bg))
                elif not type_[1]==-1:Block(type_[0],img=ImageTk.PhotoImage(Image.open(f'data\\img\\blocks\\{n}.png').transpose(type_[1])))
                else:Block(type_[0],img=ImageTk.PhotoImage(Image.open(f'data\\img\\blocks\\{n}.png')))
    def get(self):return self.img
class Item:
    all_items=[]
    all_items_d={}
    all_items_img=[]
    items={}
    all_names=[]
    def __init__(self,n,stack_count=64,block=None,tool=None):
        self.img,self.n,self.stack_count,self.block,self.tool,self.food_heal,self.eat_time=ImageTk.PhotoImage(Image.open(f'data\\img\\items\\{n}.png')),n,stack_count,block,tool,0,0
        self.__class__.all_items.append(self)
        self.__class__.all_items_d[n]=self.img
        self.__class__.all_items_img.append(self.img)
        self.__class__.items[n]=self
    def get(self):return self.img
class Player:
    def __init__(self,cnv,gm):
        self.cnv,self.poses,self.hp,self.food,self.pos,self.gm=cnv,{'standRU':ImageTk.PhotoImage(Image.open('data\\img\\skin\\standRU.png')),'standRD':ImageTk.PhotoImage(Image.open('data\\img\\skin\\standRD.png')),'standLU':ImageTk.PhotoImage(Image.open('data\\img\\skin\\standLU.png')),'standLD':ImageTk.PhotoImage(Image.open('data\\img\\skin\\standLD.png'))},10,10,[0,0],gm
    def jump(self):
        pass
    def right(self):
        pass
    def left(self):
        pass
    def look(self):
        lb=[gm.looking_block[0]*50,gm.looking_block[1]*50]
        if lb[0]>0:
            pass
class Shader:
    def __init__(self,cnv):
        self.cnv,self.sh_l,self.light_blks,self.start_shader=cnv,[ImageTk.PhotoImage(Image.open(f'data\\img\\misc\\shade_{sh_idx}.png')) for sh_idx in range(0,6)],{'torch':(5,'url'),'torchL':(5,'udr'),'torchR':(5,'udl'),'glowstone':(5,'udrl')},False
        self.sh_map={col:{row:[3,cnv.create_image(col*50,row*50,image=self.sh_l[5],anchor='nw')] for row in range(21)} for col in range(37)}
    def update(self,mp):
        if self.start_shader:
            for y in range(21):
                for x in range(37):
                    self.sh_map[x][y][0]=0
                    self.cnv.delete(self.sh_map[x][y][1])
                    self.sh_map[x][y][1]=self.cnv.create_image(x*50,y*50,image=self.sh_l[0],anchor='nw')
            for y in range(0,21):
                for x in range(0,37):
                    if mp[(x,y)] in list(self.light_blks.keys()):
                        def light(point,lvl):
                            if self.sh_map[point[0]][point[2]][0]<lvl:
                                self.sh_map[point[0]][point[2]][0]=lvl
                                self.cnv.delete(self.sh_map[point[0]][point[2]][1])
                                self.sh_map[point[0]][point[2]][1]=self.cnv.create_image(point[0]*50,point[2]*50,image=self.sh_l[self.sh_map[point[0]][point[2]][0]],anchor='nw')
                        sp=[x,y]
                        light([x,y],5)
                        ds={1:{'u':[[0,-1]],'d':[[0,1]],'r':[[1,0]],'l':[[-1,0]]},2:{'u':[[0,-2]],'d':[[0,2]],'r':[[2,0]],'l':[[-2,0]]},3:{'u':[[0,-3]],'d':[[0,3]],'r':[[3,0]],'l':[[-3,0]]},4:{'u':[[0,-4]],'d':[[0,4]],'r':[[4,0]],'l':[[-4,0]]}}
                        ds_corner={1:{'ul':[[-1,-1]],'ur':[[1,-1]],'dl':[[-1,1]],'dr':[[1,1]]},2:{'ul':[[-2,-1],[-1,-2]],'ur':[[2,-1],[1,-2]],'dl':[[-2,1],[-1,2]],'dr':[[2,1],[1,2]]},3:{'ul':[[-3,-1],[-2,-2],[-1,-3]],'ur':[[3,-1],[2,-2],[1,-3]],'dl':[[-3,1],[-2,2],[-1,3]],'dr':[[3,1],[2,2],[1,3]]}}
                        ds_back={'udl':[([1,0],4),([1,1],3),([1,-1],3),([1,2],2),([1,-2],2),([1,3],1),([1,-3],1)],'udr':[([-1,0],4),([-1,1],3),([-1,-1],3),([-1,2],2),([-1,-2],2),([-1,3],1),([-1,-3],1)],'url':[([0,1],4),([1,1],3),([-1,1],3),([2,1],2),([-2,1],2),([3,1],1),([-3,1],1)]}
                        for r in range(1,self.light_blks[mp[tuple(sp)]][0]):
                            d=ds[r]
                            for blk in self.light_blks[mp[tuple(sp)]][1]:
                                for d_ in d[blk]:
                                    x_,y_=d_[0]+sp[0],d_[1]+sp[1]
                                    if x_>-1 and y_>-1:
                                        light([x_,y_],5-r)
                            if r<5 and r<self.light_blks[mp[tuple(sp)]][0]-1:
                                d=ds_corner[r]
                                for key in list(d.keys()):
                                    if key[0] in self.light_blks[mp[tuple(sp)]][1] and key[1] in self.light_blks[mp[tuple(sp)]][1]:
                                        for d_ in d[key]:
                                            x_,y_=d_[0]+sp[0],d_[1]+sp[1]
                                            if x_>-1 and y_>-1:
                                                light([x_,y_],5-r-1)
                        if len(list(self.light_blks[mp[tuple(sp)]][1]))==3:
                            d_l=ds_back[self.light_blks[mp[tuple(sp)]][1]]
                            for d in d_l:
                                x_,y_=d[0][0]+sp[0],d[0][1]+sp[1]
                                if x_>-1 and y_>-1:
                                    light([x_,y_],d[1])

    def enable_shader(self,mp):
        self.start_shader=True
        self.update(mp)
    def disable_shader(self):
        self.start_shader=False
        for y in range(21):
                for x in range(37):
                    self.sh_map[x][y][0]=5
                    self.cnv.delete(self.sh_map[x][y][1])
                    self.sh_map[x][y][1]=self.cnv.create_image(x*50,y*50,image=self.sh_l[5],anchor='nw')
class Inventory:
    img=''
    sidebar=''
    marker=''
    def __init__(self,cnv,gm):
        self.cnv=cnv
        self.__class__.img=ImageTk.PhotoImage(Image.open('data\\img\\misc\\inv.png'))
        self.__class__.sidebar=ImageTk.PhotoImage(Image.open('data\\img\\misc\\sidebar.png'))
        self.__class__.marker=ImageTk.PhotoImage(Image.open('data\\img\\misc\\marker.png'))
        self.marker=ImageTk.PhotoImage(Image.open('data\\img\\misc\\marker.png'))
        self.s_slot=1
        self.itembar=[]
        self.itembar_obj=[]
        self.inventory={}
        self.game=gm
    def make_(self):
        self.s_slot_marker=self.cnv.create_image(1850,0,image=self.marker,anchor='nw')
        self.itembar_obj=[self.cnv.create_image(1860,10,image=Item.all_items_d['air'],anchor='nw'),self.cnv.create_image(1860,60,image=Item.all_items_d['air'],anchor='nw'),self.cnv.create_image(1860,110,image=Item.all_items_d['air'],anchor='nw'),self.cnv.create_image(1860,160,image=Item.all_items_d['air'],anchor='nw'),self.cnv.create_image(1860,210,image=Item.all_items_d['air'],anchor='nw'),self.cnv.create_image(1860,260,image=Item.all_items_d['air'],anchor='nw'),self.cnv.create_image(1860,310,image=Item.all_items_d['air'],anchor='nw'),self.cnv.create_image(1860,360,image=Item.all_items_d['air'],anchor='nw'),self.cnv.create_image(1860,410,image=Item.all_items_d['air'],anchor='nw')]
        self.slot_itm_cnt_obj=[self.cnv.create_text(1880,25,text='  ',anchor='nw',fill='#0C0C0C',font=('Tempus Sans ITC',10)),self.cnv.create_text(1880,75,text='  ',anchor='nw',fill='#0C0C0C',font=('Tempus Sans ITC',10)),self.cnv.create_text(1880,125,text='  ',anchor='nw',fill='#0C0C0C',font=('Tempus Sans ITC',10)),self.cnv.create_text(1880,175,text='  ',anchor='nw',fill='#0C0C0C',font=('Tempus Sans ITC',10)),self.cnv.create_text(1880,225,text='  ',anchor='nw',fill='#0C0C0C',font=('Tempus Sans ITC',10)),self.cnv.create_text(1880,275,text='  ',anchor='nw',fill='#0C0C0C',font=('Tempus Sans ITC',10)),self.cnv.create_text(1880,325,text='  ',anchor='nw',fill='#0C0C0C',font=('Tempus Sans ITC',10)),self.cnv.create_text(1880,375,text='  ',anchor='nw',fill='#0C0C0C',font=('Tempus Sans ITC',10)),self.cnv.create_text(1880,425,text='  ',anchor='nw',fill='#0C0C0C',font=('Tempus Sans ITC',10))]
    def s1(self,arg):self.slot(1)
    def s2(self,arg):self.slot(2)
    def s3(self,arg):self.slot(3)
    def s4(self,arg):self.slot(4)
    def s5(self,arg):self.slot(5)
    def s6(self,arg):self.slot(6)
    def s7(self,arg):self.slot(7)
    def s8(self,arg):self.slot(8)
    def s9(self,arg):self.slot(9)
    def slot(self,s):
        if not self.game.gui.open:
            m=-50*(self.s_slot-s)
            self.cnv.move(self.s_slot_marker,0,m)
            self.s_slot=s
    def update(self):
        if ['',0] in self.itembar:self.itembar.remove(['',0])
        while len(self.itembar)<9:self.itembar.append(['air',0])
        for s in range(9):
            item=self.itembar[s][0]
            self.cnv.itemconfig(self.itembar_obj[s],image=Item.all_items_d[item])
            if self.itembar[s][1]<2:t='  '
            elif 1<self.itembar[s][1]<10:t=f' {self.itembar[s][1]}'
            else:t=str(self.itembar[s][1])
            self.cnv.itemconfig(self.slot_itm_cnt_obj[s],text=t)
        if len(self.inventory)<27:
            for x in range(9):
                for y in range(3):
                    if (x,y) not in list(self.inventory.keys()):self.inventory[(x,y)]=['air',0]
    def clear(self):self.itembar=[['air',0]]
class Generation:
    def __init__(self,cnv):self.cnv,self.wb,self.sb,self.gb,self.tb,self.map,self.obj,self.shader,self.stop_time,self.items,self.metadata_map=cnv,[],[],[],[],{},{},Shader(cnv),False,[],{}
    def img(self,img,x,y,inc=0):
        if (x,y) in list(self.obj.keys()):self.cnv.delete(self.obj[(x,y)])
        self.obj[(x,y)]=self.cnv.create_image(x*50,y*50+inc,image=Block.all_blocks_d[img],anchor='nw')
        self.shader.update(self.map)
    def img_(self,blk,x,y,inc=0,metadata=None):
        if 'chest' in blk and type(metadata)!=str:
            if len(list(metadata.keys()))<27:
                for x_ in range(9):
                    for y_ in range(3):
                        if (x_,y_) not in list(metadata.keys()):metadata[(x_,y_)]=['air',0]
        self.map[(x,y)]=blk
        self.metadata_map[(x,y)]=metadata
        if not self.stop_time:
            if blk.startswith('water'):
                if (x,y) not in self.wb:self.wb.append((x,y))
            elif blk=='sand':
                if (x,y) not in self.sb:self.sb.append((x,y))
            elif blk=='gravel':
                if (x,y) not in self.gb:self.gb.append((x,y))
            elif blk.startswith('torch'):
                if (x,y) not in self.tb:self.tb.append((x,y))
            else:
                if (x,y) in self.wb:self.wb.remove((x,y))
                if (x,y) in self.sb:self.sb.remove((x,y))
                if (x,y) in self.gb:self.gb.remove((x,y))
                if (x,y) in self.tb:self.tb.remove((x,y))
            if blk in ['sand','gravel'] and inc>0:self.img(blk,x,y,inc=(inc/2))
            else:self.img(blk,x,y)
        else:self.img(blk,x,y)
    def tree(self,x,y):
        height=random.randint(3,6)
        leaf_top=random.randint(1,2)
        if height<5:leaf_side_layers=random.randint(1,height-2)
        else:leaf_side_layers=random.randint(2,height-3)
        for h_ in range(0,height):self.img('log',x,y-h_)
        for l_ in range(0,leaf_top):self.img('leaf',x,y-height-l_)
        for ls_ in range(0,leaf_side_layers):
            for l_ in range(0,ls_+1):self.img('leaf',x-1-l_,y-height+ls_+2-leaf_top)
            for r_ in range(0,ls_+1):self.img('leaf',x+1+r_,y-height+ls_+2-leaf_top)
    def test(self,gm):
        self.shader.disable_shader()
        x,y=0,0
        for blk in Block.all_blocks:
            self.cnv.create_image(x*50,y*50,image=blk.img,anchor='nw')
            x+=1
            if x==37:x,y=0,y+1
        x,y=0,y+1
        for itm in Item.all_items:
            self.cnv.create_image(x*50+10,y*50+10,image=itm.img,anchor='nw')
            x+=1
            if x==37:x,y=0,y+1
        x,y=0,y+1
        for sh in self.shader.sh_l:
            self.cnv.create_image(x*50,y*50,image=sh,anchor='nw')
            x+=1
        x,y=0,y+1
        for obj in [Inventory.img,Inventory.sidebar,Inventory.marker,gm.heart_img[0],gm.heart_img[0.5],gm.heart_img[1],gm.heart_img[2],gm.heart_img[2.5],gm.heart_img[3],gm.food_img[0],gm.food_img[0.5],gm.food_img[1],gm.food_img[2],gm.food_img[2.5],gm.food_img[3]]:
            self.cnv.create_image(x*50,y*50,image=obj,anchor='nw')
            x+=1
        x,y=0,y+1
        for obj in list(gm.player.poses.values()):
            self.cnv.create_image(x*50,y*50,image=obj,anchor='nw')
            x+=1
    def fill(self,p1,p2,blk,metadata=None):
        def swap(a,b):return b,a
        p1,p2=list(p1),list(p2)
        if p1[0]>p2[0]:p1[0],p2[0]=swap(p1[0],p2[0])
        if p1[1]>p2[1]:p1[1],p2[1]=swap(p1[1],p2[1])
        for y in range(p1[1],p2[1]+1):
            for x in range(p1[0],p2[0]+1):
                self.img_(blk,x,y,0,metadata=metadata)
    def give_item(self,itm,count,gm,coords):
        for slt in range(len(gm.inv.itembar)):
            while True:
                if count==0 or gm.inv.itembar[slt][1]==64 or gm.inv.itembar[slt][0]not in ['air',itm]:break
                if gm.inv.itembar[slt][0] in [itm,'air'] and gm.inv.itembar[slt][1]<64:gm.inv.itembar[slt],count=[itm,gm.inv.itembar[slt][1]+1],count-1
        if count>0:self.item(coords,itm,count)
    def item(self,crds,itm,cnt):self.items.append([itm,cnt,0,crds,None,['',0]])
    def decrypt(self,txt):
        text,key_,key,txt='',txt.split(' ')[0],'',txt.split(' ')[1:]
        for chr_ in key_:
            key+=chr(ord(chr_)-2)
        key=int(key)
        for i in txt:
            if i!='':text+=chr(ord(i)-2)
        col,row=math.ceil(len(text)/key),key
        eb,txt,c,r=(col*row)-len(text),['']*col,0,0
        for symbol in text:
            txt[c],c=txt[c]+symbol,c+1
            if(c==col)or(c==col-1 and r>=row-eb):c,r=0,r+1
        return ''.join(txt)
    def encrypt(self,text):
        key=random.randint(round(len(text)/3),round(len(text)/3*2))
        txt,text_=['']*key,f''
        for c in range(key):
            p=c
            while p<len(text):
                txt[c]+=text[p]
                p+=key
        for chr_ in str(key):text_+=chr(ord(chr_)+2)
        for i in str(''.join(txt)):text_+=f' {chr(ord(i)+2)}'
        return text_
    def terrain(self,fn):
        def block(i,x,y,metadata):
            index=Block.all_names.index(i)
            if metadata=='-':metadata=None
            self.img_(Block.all_names[index],x,y,metadata=metadata)
        with open(f'saves/{fn}.world','r') as f:
            t=self.decrypt(f.read())
            t=t.replace('\n','').split(';;')
            t[0]=t[0].split(';')
            for t_ in t[0]:t[0][t[0].index(t_)]=t_.split(',')
            for y in range(21):
                for x in range(38):
                    if x<37:block(t[0][y][x].split(':')[0],x,y,t[0][y][x].split(':')[1])
                    if x==37 and y<9:self.cnv.create_image(x*50,y*50,image=Inventory.img,anchor='nw')
                    if x==37 and y>=9:self.cnv.create_image(x*50,y*50,image=Inventory.sidebar,anchor='nw')
            t[1]=[float(t[1].split(',')[0]),float(t[1].split(',')[1])]
            t[2]=[int(t[2].split(',')[0]),int(t[2].split(',')[1])]
            t[3]=t[3].split(';')
            for t_ in t[3]:t[3][t[3].index(t_)]=[t_.split(',')[0],int(t_.split(',')[1])]
            t[4]=int(t[4])
            t[5]=[float(t[5].split(',')[0]),float(t[5].split(',')[1])]
            if t[6]!='-':
                t[6]=t[6].split(',')
                for t_ in t[6]:
                    t[6][t[6].index(t_)]=float(t_)
            else:t[6]=[]
            if t[7]!='-':t[7]=[float(t[7].split(',')[0]),float(t[7].split(',')[1])]
            else:t[7]=[0,0]
            if t[8]!='-':t[8]=[float(t[8].split(',')[0]),float(t[8].split(',')[1])]
            else:t[8]=[0,0]
            self.shader.enable_shader(self.map)
            return t[1],t[2],t[3],t[4],t[5][0],t[5][1],t[6],t[7][0],t[7][1],t[8][0],t[8][1]
    def _stop_time(self):self.stop_time=True
    def _start_time(self):self.stop_time=False
    def get(self):return self.map,self.wb,self.sb,self.gb,self.tb
    def format_metadata(self,metadata):
        if metadata==None:return '-'
    def save(self,gm):
        with open(f'saves/{gm.file_name}.world','w') as f:
            txt=''
            for y in range(21):
                for x in range(37):txt+=f'{self.map[(x,y)]}:{self.format_metadata(self.metadata_map[(x,y)])},'
                txt=txt[:len(txt)-1]
                if y<20:txt+=';'
            txt+=f';;{gm.player.pos[0]},{gm.player.pos[1]};;{gm.looking_block[0]},{gm.looking_block[1]};;'
            for itm in gm.inv.itembar:
                txt+=f'{itm[0]},{itm[1]};'
            txt+=f';{gm.inv.s_slot};;{gm.player.hp},{gm.player.food};;'
            for tm in gm.chocolate_hunger:txt+=f'{tm},'
            if len(gm.chocolate_hunger)>0:txt=txt[:len(txt)-1]
            else:txt+='-'
            if gm.golden_apple_boost>0:txt+=f';;{gm.golden_apple_boost},{-gm.golden_apple_boost_tm}'
            else:txt+=';;-'
            if gm.enchanted_golden_apple_boost>0:txt+=f';;{gm.enchanted_golden_apple_boost},{gm.enchanted_golden_apple_boost_tm}'
            else:txt+=';;-'
            f.write(self.encrypt(txt))
    def clear(self):self.fill((0,0),(37,21),'air')
    def proces_str_n(self,n):
        if n<2:return '  '
        elif 1<n<10:return f' {n}'
        else:return str(n)
class GUI:
    def __init__(self,cnv,gm):self.cnv,self.game,self.open,self.gui_textures,self.itm_bg_texture,self.bg_shade,self.blk_gui_textures,self.gui_itembar,self.left_click,self.right_click,self.mouse,self.itembar,self.inventory,self.gui_item,self.l_click,self.itm,self.blk_n_gui_textures,self.loaded=cnv,gm,False,[],gm.inv.img,gm.gen.shader.sh_l[4],{},[],False,False,[-1,-1],[None]*9,{},[],False,['air',0,[None,None],['bar',0]],{},False
    def open_gui(self,gui_name,crds):
        self.game.is_breaking_block,self.open,self.gui_textures,self.crds,self.itm,self.blk,self.loaded=False,True,[],crds,['air',0,[None,None]],gui_name,False
        if 'inv'==gui_name:
            self.gui_items={}
            for x in range(38):
                for y in range(22):
                    if 13<x<23 and (6<y<10 or y==11):self.gui_textures.append(self.cnv.create_image(x*50,y*50,image=self.itm_bg_texture,anchor='nw'))
                    else:self.gui_textures.append(self.cnv.create_image(x*50,y*50,image=self.bg_shade,anchor='nw'))
        elif 'chest' in gui_name:
            self.gui_items={}
            for x in range(38):
                for y in range(22):
                    if 13<x<23 and (2<y<6 or 6<y<10 or y==11):
                        self.gui_textures.append(self.cnv.create_image(x*50,y*50,image=self.itm_bg_texture,anchor='nw'))
                        if 13<x<23 and 2<y<6:self.blk_gui_textures[(x,y)],self.blk_n_gui_textures[(x,y)],self.gui_items[(x-14,y-3)]=self.cnv.create_image(x*50+10,y*50+10,image=Item.all_items[Item.all_names.index(self.game.gen.metadata_map[tuple(crds)][(x-14,y-3)][0])].img,anchor='nw'),self.cnv.create_text(x*50+30,y*50+30,text=self.game.gen.proces_str_n(self.game.gen.metadata_map[tuple(crds)][(x-14,y-3)][1]),anchor='nw',fill='#0C0C0C',font=('Tempus Sans ITC',10)),self.game.gen.metadata_map[tuple(crds)][(x-14,y-3)]
                    else:self.gui_textures.append(self.cnv.create_image(x*50,y*50,image=self.bg_shade,anchor='nw'))
        elif 'furnace'==gui_name:
            self.gui_items={}
            for x in range(38):
                for y in range(22):
                    if (13<x<23 and (6<y<10 or y==11)) or [y,x] in [[3,16],[5,16],[4,20]]:
                        self.gui_textures.append(self.cnv.create_image(x*50,y*50,image=self.itm_bg_texture,anchor='nw'))
                        if [y,x] in [[3,16],[5,16],[4,20]]:self.blk_gui_textures[(x,y)],self.blk_n_gui_textures[(x,y)],self.gui_items[list([[3,16],[5,16],[4,20]]).index([y,x])]=self.cnv.create_image(x*50+10,y*50+10,image=Item.all_items[Item.all_names.index(self.game.gen.metadata_map[tuple(crds)][list([[3,16],[5,16],[4,20]]).index([y,x])][0])].img,anchor='nw'),self.cnv.create_text(x*50+30,y*50+30,text=self.game.gen.proces_str_n(self.game.gen.metadata_map[tuple(crds)][list([[3,16],[5,16],[4,20]]).index([y,x])][1]),anchor='nw',fill='#0C0C0C',font=('Tempus Sans ITC',10)),self.game.gen.metadata_map[tuple(crds)][list([[3,16],[5,16],[4,20]]).index([y,x])]
                    else:self.gui_textures.append(self.cnv.create_image(x*50,y*50,image=self.bg_shade,anchor='nw'))
        for x in range(9):
            for y in range(3):self.blk_gui_textures[(14+x,7+y)],self.blk_n_gui_textures[(14+x,7+y)],self.inventory[(x,y)]=self.cnv.create_image((14+x)*50+10,(7+y)*50+10,image=Item.all_items[Item.all_names.index(self.game.inv.inventory[(x,y)][0])].img,anchor='nw'),self.cnv.create_text((14+x)*50+30,(7+y)*50+30,text=self.game.gen.proces_str_n(self.game.inv.inventory[(x,y)][1]),anchor='nw',fill='#0C0C0C',font=('Tempus Sans ITC',10)),self.game.inv.inventory[(x,y)]
        for idx in range(9):self.blk_gui_textures[(14+idx,11)],self.blk_n_gui_textures[(14+idx,11)],self.itembar[idx]=self.cnv.create_image((14+idx)*50+10,560,image=Item.all_items[Item.all_names.index(self.game.inv.itembar[idx][0])].img,anchor='nw'),self.cnv.create_text((14+idx)*50+30,580,text=self.game.gen.proces_str_n(self.game.inv.itembar[idx][1]),anchor='nw',fill='#0C0C0C',font=('Tempus Sans ITC',10)),self.game.inv.itembar[idx]
        self.loaded=True
    def close_gui(self):
        if self.loaded:
            self.game.inv.itembar=list(self.itembar)
            self.game.inv.inventory=dict(self.inventory)
            if self.blk in ['chestL','chestR','furnace']:self.game.gen.metadata_map[tuple(self.crds)]=dict(self.gui_items)
            elif self.blk=='crafting_table':
                for itm in list(self.gui_items.values()):self.game.gen.item(self.crds,itm[0],itm[1])
            del self.itembar,self.inventory,self.gui_items
            for obj in self.gui_textures:self.cnv.delete(obj)
            for obj in list(self.blk_gui_textures.values()):self.cnv.delete(obj)
            for obj in list(self.blk_n_gui_textures.values()):self.cnv.delete(obj)
            self.open,self.left_click,self.right_click,self.mouse,self.itembar,self.inventory,self.l_click,self.game.looking_block,self.loaded=False,False,False,[-1,-1],[None]*9,{},True,self.crds,False
    def update(self):
        if self.left_click:
            if (not self.l_click) and self.mouse[0]//50 in [14+n for n in range(9)] and self.mouse[1]//50==11 and self.itm==['air',0,self.itm[2]]:
                if self.itembar[self.mouse[0]//50-14]!=['air',0]:
                    self.itm=[self.itembar[self.mouse[0]//50-14][0],self.itembar[self.mouse[0]//50-14][1],[None,None]]
                    self.cnv.itemconfig(self.blk_gui_textures[(self.mouse[0]//50,self.mouse[1]//50)],image=Item.all_items[Item.all_names.index('air')].img)
                    self.cnv.itemconfig(self.blk_n_gui_textures[(self.mouse[0]//50,self.mouse[1]//50)],text=self.game.gen.proces_str_n(0))
                    self.itembar[self.mouse[0]//50-14]=['air',0]
            elif (not self.l_click) and self.mouse[0]//50 in [14+n for n in range(9)] and self.mouse[1]//50 in [7,8,9] and self.itm==['air',0,self.itm[2]]:
                if self.inventory[(self.mouse[0]//50-14,self.mouse[1]//50-7)]!=['air',0]:
                    self.itm=[self.inventory[(self.mouse[0]//50-14,self.mouse[1]//50-7)][0],self.inventory[(self.mouse[0]//50-14,self.mouse[1]//50-7)][1],[None,None]]
                    self.cnv.itemconfig(self.blk_gui_textures[(self.mouse[0]//50,self.mouse[1]//50)],image=Item.all_items[Item.all_names.index('air')].img)
                    self.cnv.itemconfig(self.blk_n_gui_textures[(self.mouse[0]//50,self.mouse[1]//50)],text=self.game.gen.proces_str_n(0))
                    self.inventory[(self.mouse[0]//50-14,self.mouse[1]//50-7)]=['air',0]
            elif (not self.l_click) and [self.mouse[1]//50,self.mouse[0]//50] in [[3,16],[5,16],[4,20]] and self.itm==['air',0,self.itm[2]] and self.blk=='furnace':
                if self.gui_items[list([[3,16],[5,16],[4,20]]).index([self.mouse[1]//50,self.mouse[0]//50])]!=['air',0]:
                    self.itm=[self.gui_items[list([[3,16],[5,16],[4,20]]).index([self.mouse[1]//50,self.mouse[0]//50])][0],self.gui_items[list([[3,16],[5,16],[4,20]]).index([self.mouse[1]//50,self.mouse[0]//50])][1],[None,None]]
                    self.cnv.itemconfig(self.blk_gui_textures[(self.mouse[0]//50,self.mouse[1]//50)],image=Item.all_items[Item.all_names.index('air')].img)
                    self.cnv.itemconfig(self.blk_n_gui_textures[(self.mouse[0]//50,self.mouse[1]//50)],text=self.game.gen.proces_str_n(0))
                    self.gui_items[list([[3,16],[5,16],[4,20]]).index([self.mouse[1]//50,self.mouse[0]//50])]=['air',0]
            elif (not self.l_click) and 2<self.mouse[1]//50<6 and 13<self.mouse[0]//50<23 and self.itm==['air',0,self.itm[2]] and 'chest' in self.blk:
                if self.gui_items[(self.mouse[0]//50-14,self.mouse[1]//50-3)]!=['air',0]:
                    self.itm=[self.gui_items[(self.mouse[0]//50-14,self.mouse[1]//50-3)][0],self.gui_items[(self.mouse[0]//50-14,self.mouse[1]//50-3)][1],[None,None]]
                    self.cnv.itemconfig(self.blk_gui_textures[(self.mouse[0]//50,self.mouse[1]//50)],image=Item.all_items[Item.all_names.index('air')].img)
                    self.cnv.itemconfig(self.blk_n_gui_textures[(self.mouse[0]//50,self.mouse[1]//50)],text=self.game.gen.proces_str_n(0))
                    self.gui_items[(self.mouse[0]//50-14,self.mouse[1]//50-3)]=['air',0]
            if self.itm[2][0]==None:self.itm[2]=[self.cnv.create_image(0,0,image=Item.all_items[Item.all_names.index(self.itm[0])].img,anchor='nw'),self.cnv.create_text(0,0,text=self.game.gen.proces_str_n(self.itm[1]),anchor='nw',fill='#0C0C0C',font=('Tempus Sans ITC',10))]
            if self.cnv.coords(self.itm[2][0])!=[self.mouse[0]-15,self.mouse[1]-15]:self.cnv.move(self.itm[2][0],self.mouse[0]-15-self.cnv.coords(self.itm[2][0])[0],self.mouse[1]-15-self.cnv.coords(self.itm[2][0])[1])
            if self.cnv.coords(self.itm[2][1])!=[self.mouse[0]+5,self.mouse[1]+5]:self.cnv.move(self.itm[2][1],self.mouse[0]+5-self.cnv.coords(self.itm[2][1])[0],self.mouse[1]+5-self.cnv.coords(self.itm[2][1])[1])
            self.l_click=True
        else:
            if self.l_click and self.mouse[0]//50 in [14+n for n in range(9)] and self.mouse[1]//50==11 and self.itm!=['air',0,self.itm[2]]:
                if self.itembar[self.mouse[0]//50-14]==['air',0]:
                    self.itembar[self.mouse[0]//50-14]=[self.itm[0],self.itm[1]]
                    self.cnv.itemconfig(self.blk_gui_textures[(self.mouse[0]//50,self.mouse[1]//50)],image=Item.all_items[Item.all_names.index(self.itm[0])].img)
                    self.cnv.itemconfig(self.blk_n_gui_textures[(self.mouse[0]//50,self.mouse[1]//50)],text=self.game.gen.proces_str_n(self.itm[1]))
                    for obj in self.itm[2]:self.cnv.delete(obj)
                    self.itm=['air',0,[None,None]]
            elif self.l_click and self.mouse[0]//50 in [14+n for n in range(9)] and self.mouse[1]//50 in [7,8,9] and self.itm!=['air',0,self.itm[2]]:
                if self.inventory[(self.mouse[0]//50-14,self.mouse[1]//50-7)]==['air',0]:
                    self.inventory[(self.mouse[0]//50-14,self.mouse[1]//50-7)]=[self.itm[0],self.itm[1]]
                    self.cnv.itemconfig(self.blk_gui_textures[(self.mouse[0]//50,self.mouse[1]//50)],image=Item.all_items[Item.all_names.index(self.itm[0])].img)
                    self.cnv.itemconfig(self.blk_n_gui_textures[(self.mouse[0]//50,self.mouse[1]//50)],text=self.game.gen.proces_str_n(self.itm[1]))
                    for obj in self.itm[2]:self.cnv.delete(obj)
                    self.itm=['air',0,[None,None]]
            elif self.l_click and [self.mouse[1]//50,self.mouse[0]//50] in [[3,16],[5,16],[4,20]] and self.itm!=['air',0,self.itm[2]] and self.blk=='furnace':
                if self.gui_items[list([[3,16],[5,16],[4,20]]).index([self.mouse[1]//50,self.mouse[0]//50])]==['air',0]:
                    self.gui_items[list([[3,16],[5,16],[4,20]]).index([self.mouse[1]//50,self.mouse[0]//50])]=[self.itm[0],self.itm[1]]
                    self.cnv.itemconfig(self.blk_gui_textures[(self.mouse[0]//50,self.mouse[1]//50)],image=Item.all_items[Item.all_names.index(self.itm[0])].img)
                    self.cnv.itemconfig(self.blk_n_gui_textures[(self.mouse[0]//50,self.mouse[1]//50)],text=self.game.gen.proces_str_n(self.itm[1]))
                    for obj in self.itm[2]:self.cnv.delete(obj)
                    self.itm=['air',0,[None,None]]
            elif self.l_click and 2<self.mouse[1]//50<6 and 13<self.mouse[0]//50<23 and self.itm!=['air',0,self.itm[2]] and 'chest' in self.blk:
                if self.gui_items[(self.mouse[0]//50-14,self.mouse[1]//50-3)]==['air',0]:
                    self.gui_items[(self.mouse[0]//50-14,self.mouse[1]//50-3)]=[self.itm[0],self.itm[1]]
                    self.cnv.itemconfig(self.blk_gui_textures[(self.mouse[0]//50,self.mouse[1]//50)],image=Item.all_items[Item.all_names.index(self.itm[0])].img)
                    self.cnv.itemconfig(self.blk_n_gui_textures[(self.mouse[0]//50,self.mouse[1]//50)],text=self.game.gen.proces_str_n(self.itm[1]))
                    for obj in self.itm[2]:self.cnv.delete(obj)
                    self.itm=['air',0,[None,None]]
            elif self.l_click and [self.mouse[0]//50,self.mouse[1]//50] not in list(self.blk_gui_textures.keys()) and self.itm!=['air',0,self.itm[2]]:
                self.game.gen.item(self.crds,self.itm[0],self.itm[1])
                for obj in self.itm[2]:self.cnv.delete(obj)
                self.itm=['air',0,[None,None]]
            self.l_click=False
class Game:
    def __init__(self):
        self.tk=Tk()
        self.tk.title('2D')
        self.tk['background']='black'
        self.tk.resizable(0,0)
        self.tk.minsize(width=100,height=100)
        self.tk.geometry('1910x1030+-5+-25')
        self.cv_fr=Frame(self.tk,bg='black')
        self.canvas=Canvas(self.cv_fr,bg='#00B2EE',width=10,height=10,borderwidth=0,highlightbackgroun='black',highlightthickness=0,highlightcolor='black')#'#00B2EE';'#000000'
        self.cv_fr.grid(row=0,column=0)
        self.canvas.grid(row=0,column=0)
        self.canvas['height']=1020
        self.canvas['width']=1900
        Block.all_names,l_remove=['air','grass_block','dirt','farmland','stone','coal_ore','log','leaf','water','_waterL','sand','glass','crafting_table','furnace','lit_furnace','torch','_torchL','gravel','planks','brick_block','diamond_ore','gold_ore','iron_ore','_stairL','unwatered_farmland','glowstone','cobblestone','_slabD','coal_block','diamond_block','gold_block','iron_block','grass','_chestL'],[]
        Block.all_names.sort()
        for n in Block.all_names:
            if n.startswith('_'):l_remove.append(n)
            Block(n)
        for blk in l_remove:Block.all_names.remove(blk)
        for blk in Block.all_names_add:Block.all_names.append(blk)
        Block.all_names.sort()
        del l_remove
        Item.all_names=['air','dirt','grass_block','stone','coal_ore','coal','log','leaf','water_bucket','bucket','sand','glass','furnace','torch','crafting_table','stone_pickaxe','farmland','gravel','planks','stick','brick','golden_ingot','iron_ingot','wooden_pickaxe','iron_pickaxe','diamond_pickaxe','brick_block','diamond_ore','gold_ore','iron_ore','diamond','stair','golden_pickaxe','wooden_sword','stone_sword','iron_sword','golden_sword','diamond_sword','glowstone','wooden_shovel','stone_shovel','iron_shovel','golden_shovel','diamond_shovel','wooden_axe','stone_axe','iron_axe','golden_axe','diamond_axe','wooden_hoe','stone_hoe','iron_hoe','golden_hoe','diamond_hoe','cobblestone','slab','string','fishing_rod','bow','carrot','carrot_on_a_stick','coal_block','diamond_block','gold_block','iron_block','apple','chocolate','golden_apple','enchanted_golden_apple','chest']
        Item.all_names.sort()
        for n in Item.all_names:Item(n)
        stack_cnt_1=['air','water_bucket','wooden_pickaxe','stone_pickaxe','iron_pickaxe','diamond_pickaxe','golden_pickaxe','wooden_sword','stone_sword','iron_sword','golden_sword','diamond_sword','wooden_shovel','stone_shovel','iron_shovel','golden_shovel','diamond_shovel','wooden_axe','stone_axe','iron_axe','golden_axe','diamond_axe','wooden_hoe','stone_hoe','iron_hoe','golden_hoe','diamond_hoe','fishing_rod','bow','carrot_on_a_stick']
        for itm in stack_cnt_1:Item.all_items[Item.all_names.index(itm)].stack_count=1
        blocks=['coal_block','farmland','gravel','brick_block','stair','glowstone','cobblestone','slab','sand','glass','furnace','torch','dirt','grass_block','stone','coal_ore','log','leaf','diamond_block','gold_block','iron_block','chest']
        for itm in blocks:Item.all_items[Item.all_names.index(itm)].block=itm
        Item.all_items[Item.all_names.index('carrot_on_a_stick')].tool='carrot_on_a_stick'
        Item.all_items[Item.all_names.index('fishing_rod')].tool='fishing_rod'
        Item.all_items[Item.all_names.index('wooden_hoe')].tool='wooden_hoe'
        Item.all_items[Item.all_names.index('stone_hoe')].tool='stone_hoe'
        Item.all_items[Item.all_names.index('iron_hoe')].tool='iron_hoe'
        Item.all_items[Item.all_names.index('golden_hoe')].tool='golden_hoe'
        Item.all_items[Item.all_names.index('diamond_hoe')].tool='diamond_hoe'
        Item.all_items[Item.all_names.index('wooden_axe')].tool='wooden_axe'
        Item.all_items[Item.all_names.index('stone_axe')].tool='stone_axe'
        Item.all_items[Item.all_names.index('iron_axe')].tool='iron_axe'
        Item.all_items[Item.all_names.index('golden_axe')].tool='golden_axe'
        Item.all_items[Item.all_names.index('diamond_axe')].tool='diamond_axe'
        Item.all_items[Item.all_names.index('wooden_shovel')].tool='wooden_shovel'
        Item.all_items[Item.all_names.index('stone_shovel')].tool='stone_shovel'
        Item.all_items[Item.all_names.index('iron_shovel')].tool='iron_shovel'
        Item.all_items[Item.all_names.index('golden_shovel')].tool='golden_shovel'
        Item.all_items[Item.all_names.index('diamond_shovel')].tool='diamond_shovel'
        Item.all_items[Item.all_names.index('wooden_sword')].tool='wooden_sword'
        Item.all_items[Item.all_names.index('stone_sword')].tool='stone_sword'
        Item.all_items[Item.all_names.index('iron_sword')].tool='iron_sword'
        Item.all_items[Item.all_names.index('golden_sword')].tool='golden_sword'
        Item.all_items[Item.all_names.index('diamond_sword')].tool='diamond_sword'
        Item.all_items[Item.all_names.index('crafting_table')].block='crafting_table'
        Item.all_items[Item.all_names.index('wooden_pickaxe')].tool='wooden_pickaxe'
        Item.all_items[Item.all_names.index('stone_pickaxe')].tool='stone_pickaxe'
        Item.all_items[Item.all_names.index('iron_pickaxe')].tool='iron_pickaxe'
        Item.all_items[Item.all_names.index('diamond_pickaxe')].tool='diamond_pickaxe'
        Item.all_items[Item.all_names.index('golden_pickaxe')].tool='golden_pickaxe'
        Item.all_items[Item.all_names.index('bow')].tool='bow'
        Item.all_items[Item.all_names.index('water_bucket')].block='water'
        Item.all_items[Item.all_names.index('carrot')].food_heal=2
        Item.all_items[Item.all_names.index('apple')].food_heal=2.5
        Item.all_items[Item.all_names.index('chocolate')].food_heal=0.5
        Item.all_items[Item.all_names.index('golden_apple')].food_heal=0
        Item.all_items[Item.all_names.index('enchanted_golden_apple')].food_heal=0
        Item.all_items[Item.all_names.index('carrot')].eat_time=1.9
        Item.all_items[Item.all_names.index('apple')].eat_time=1.25
        Item.all_items[Item.all_names.index('chocolate')].eat_time=1.1
        Item.all_items[Item.all_names.index('golden_apple')].eat_time=1.4
        Item.all_items[Item.all_names.index('enchanted_golden_apple')].eat_time=1.4
        self.destr_stages,self.sl_frame,self.blk_break_map,self.breaking_tm,self.looking_marker_img,self.bounding_box,self.heart_img,self.heart_objs,self.food_img,self.food_objs,self.old_hp,self.old_food,self.tm_hp_regen,self.last_tm_hp_reg,self.regen_rm_food,self.tm_food_rm,self.last_tm_food_rm,self.tm_damage_hunger,self.last_tm_damage_hunger,self.eating,self.eating_object,self.chocolate_hunger,self.golden_apple_boost,self.golden_apple_boost_tm,self.enchanted_golden_apple_boost,self.enchanted_golden_apple_boost_tm,self.file_name,self.use_left_click,self.use_right_click=\
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           [Image.open(f'data\\img\\misc\\destroy_{n}.png') for n in range(1,9)],ImageTk.PhotoImage(Image.open(f'data\\img\\misc\\selected.png')),{'normal':[(0,0,50,50)],'stairL':[(0,0,25,25),(0,25,50,25)],'stairR':[(25,0,25,25),(0,25,50,25)],'torch':[(20,8,11,12),(20,20,11,30)],'torchL':[(3,8,11,12),(3,20,11,25),(0,22,3,3),(0,40,3,3)],'torchR':[(36,8,11,12),(36,20,11,25),(47,22,3,3),(47,40,3,3)],'farmland':[(0,7,50,43)],'unwatered_farmland':[(0,7,50,43)],'grass':[(1,5,46,45)]},{'normal':0.1,'grass':0.06},Image.open('data\\img\\misc\\selected.png'),{'normal':(0,0,50,50),'torch':(20,8,11,42),'torchL':(3,8,11,37),'torchR':(36,8,11,37),'farmland':(0,7,50,43),'unwatered_farmland':(0,7,50,43),'air':(0,0,1,1),'grass':(1,5,46,45)},{1:ImageTk.PhotoImage(Image.open('data\\img\\misc\\heart.png')),0.5:ImageTk.PhotoImage(Image.open('data\\img\\misc\\half_heart.png')),0:ImageTk.PhotoImage(Image.open('data\\img\\misc\\empty_heart.png')),3:ImageTk.PhotoImage(Image.open('data\\img\\misc\\heart_gold.png')),2.5:ImageTk.PhotoImage(Image.open('data\\img\\misc\\half_heart_gold.png')),2:ImageTk.PhotoImage(Image.open('data\\img\\misc\\empty_heart_gold.png'))},[],{1:ImageTk.PhotoImage(Image.open('data\\img\\misc\\food.png')),0.5:ImageTk.PhotoImage(Image.open('data\\img\\misc\\half_food.png')),0:ImageTk.PhotoImage(Image.open('data\\img\\misc\\empty_food.png')),3:ImageTk.PhotoImage(Image.open('data\\img\\misc\\food_gold.png')),2.5:ImageTk.PhotoImage(Image.open('data\\img\\misc\\half_food_gold.png')),2:ImageTk.PhotoImage(Image.open('data\\img\\misc\\empty_food_gold.png'))},[],0,0,None,time.time(),0,None,time.time(),None,time.time(),False,[None,None],[],0,0,0,0,'test',False,False
        self.looking_block,self.breaking_block,self.is_breaking_block=[-1,-1],[None],False
        self.player=Player(self.canvas,self)
        self.receipes()
        self.inv=Inventory(self.canvas,self)
        self.gen=Generation(self.canvas)
        self.gui=GUI(self.canvas,self)
        self.player.pos,self.looking_block,self.inv.itembar,slt,self.player.hp,self.player.food,self.chocolate_hunger,self.golden_apple_boost,self.golden_apple_boost_tm,self.enchanted_golden_apple_boost,self.enchanted_golden_apple_boost_tm=self.gen.terrain(self.file_name)
        self.inv.make_()
        self.inv.slot(slt)
        self.inv.update()
        del slt
        self.looking_marker_img_formatted=ImageTk.PhotoImage(self.looking_marker_img)
        self.looking_marker=self.canvas.create_image(-50,-50,image=self.looking_marker_img_formatted,anchor='nw')
        with open('binds.txt','r') as binds:
            d={l.replace('\n','').split(':')[0]:l.replace('\n','').split(':')[1] for l in binds if not l.startswith('\n') or l.startswith(' ')}
            self.canvas.bind_all(f'{d["escape"]}',func=self.quit_)
            self.canvas.bind_all(f'{d["left"]}',func=self.left)
            self.canvas.bind_all(f'{d["right"]}',func=self.right)
            self.canvas.bind_all(f'{d["jump"]}',func=self.jump)
            self.canvas.bind_all(f'{d["break_block"]}',func=self.break_block)
            self.canvas.bind_all(f'{d["break_block_release"]}',func=self.stop_break_block)
            self.canvas.bind_all(f'{d["place_block"]}',func=self.place_block)
            self.canvas.bind_all(f'{d["place_block_release"]}',func=self.stop_place_block)
            self.canvas.bind_all(f'{d["inv_open"]}',func=self.inv_open)
            self.canvas.bind_all(f'{d["slot1"]}',func=self.inv.s1)
            self.canvas.bind_all(f'{d["slot2"]}',func=self.inv.s2)
            self.canvas.bind_all(f'{d["slot3"]}',func=self.inv.s3)
            self.canvas.bind_all(f'{d["slot4"]}',func=self.inv.s4)
            self.canvas.bind_all(f'{d["slot5"]}',func=self.inv.s5)
            self.canvas.bind_all(f'{d["slot6"]}',func=self.inv.s6)
            self.canvas.bind_all(f'{d["slot7"]}',func=self.inv.s7)
            self.canvas.bind_all(f'{d["slot8"]}',func=self.inv.s8)
            self.canvas.bind_all(f'{d["slot9"]}',func=self.inv.s9)
            self.canvas.bind_all('<Motion>',func=self.look)
            if not d["place_block"]=='<Button-3>':
                self.canvas.bind_all('<Button-3>',func=self.r_click)
                self.canvas.bind_all('<ButtonRelease-3>',func=self.stop_r_click)
            else:self.use_right_click=True
            if not d["break_block"]=='<Button-1>':
                self.canvas.bind_all('<Button-1>',func=self.l_click)
                self.canvas.bind_all('<ButtonRelease-1>',func=self.stop_l_click)
            else:self.use_left_click=True
        self.map,self.water_blocks,self.sand_blocks,self.gravel_blocks,self.torch_blocks=self.gen.get()
        self.l_update_wb={}
        self.l_update_wb_={}
        self.l_blk_parents_wb={}
        self.l_fall_stage_sb={}
        self.l_fall_stage_gb={}
        self.gen.shader.disable_shader()
        self.start()
        #---test---
        self.gen.clear()
        self.inv.clear()
        self.inv.update()
        self.player.food=self.player.hp=10.0
        self.gen.fill((0,7),(36,7),'chestL',{(4,2):['leaf',6]})
        self.gen.fill((0,8),(36,8),'furnace',{0:['log',2],1:['coal',64],2:['air',0]})
        self.inv.inventory={(6,1):['log',63],(5,2):['diamond_sword',1]}
        self.inv.itembar=[['golden_sword',1]]
        self.tk.deiconify()
    def quit_(self,arg):
        if self.gui.open:self.gui.close_gui()
        else:
            self.gen.save(self)
            self.tk.destroy()
            quit()
    def r_click(self,arg):self.gui.right_click=True
    def l_click(self,arg):self.gui.left_click=True
    def stop_r_click(self,arg):self.gui.right_click=False
    def stop_l_click(self,arg):self.gui.left_click=False
    def left(self,arg):
        if not self.gui.open:self.player.left()
    def right(self,arg):
        if not self.gui.open:self.player.right()
    def inv_open(self,arg):
        if not self.gui.open:self.gui.open_gui('inv',self.looking_block)
    def look(self,arg):
        if not self.gui.open:self.looking_block=[arg.x//50,arg.y//50]
        else:self.gui.mouse=[arg.x,arg.y]
    def break_block(self,arg):
        if not self.gui.open:self.is_breaking_block=True
        if self.gui.open and self.use_left_click:self.gui.left_click=True
    def stop_break_block(self,arg):
        if not self.gui.open:self.is_breaking_block=False
        if self.gui.open and self.use_left_click:self.gui.left_click=False
    def place_block(self,arg):
        if (not self.gui.open) and self.player.food<10 and Item.all_items[Item.all_names.index(self.inv.itembar[self.inv.s_slot-1][0])].eat_time>0:self.eating=True
        if (not self.gui.open) and (not self.eating) and self.map[tuple(self.looking_block)] in ['crafting_table','furnace','chestL','chestR']:self.gui.open_gui(self.map[tuple(self.looking_block)],self.looking_block)
        if self.gui.open and self.use_right_click:self.gui.right_click=True
    def stop_place_block(self,arg):
        self.eating=False
        if self.gui.open and self.use_right_click:self.gui.right_click=False
    def jump(self,arg):
        # if not self.gui.open:self.player.jump()
        print(self.gui.open,self.gen.items)
    def receipes(self):
        self.receipes_ct=[]
        self.receipes_f=[]
        for fn in glob.iglob('data\\receipes\\*.json'):
            with open(fn,'r') as f:
                r=json.loads(f.read())
                if r['type']=='crafting_table':
                    map_r_l=[]
                    key=r['key']
                    key[' ']=' '
                    for rc in r['receipe']:
                        map_r=[]
                        for it in rc:
                            map_r.append(key[it])
                        map_r_l.append(map_r)
                    self.receipes_ct.append([map_r_l,r['reward']])
                elif r['type']=='furnace':self.receipes_f.append([r['input'],r['reward']])
    def start(self):
        for wb in self.water_blocks:
            if not (wb[0],wb[1]) in self.l_update_wb_.keys():self.l_update_wb_[(wb[0],wb[1])]=-1
            self.l_update_wb_[(wb[0],wb[1])]=self.l_update_wb_[(wb[0],wb[1])]+1
            if self.l_update_wb_[(wb[0],wb[1])]==10:
                self.l_update_wb_[(wb[0],wb[1])]=0
                s_=tuple(wb)
                if s_ in self.l_blk_parents_wb.keys():
                    for blk in self.l_blk_parents_wb[s_]:
                        if not self.map[blk].startswith('water'):
                            self.l_blk_parents_wb[s_].remove(blk)
                            if len(self.l_blk_parents_wb[s_])==1:
                                if self.l_blk_parents_wb[s_][0][0]<s_[0]:self.gen.img_('waterR',s_[0],s_[1])
                                if self.l_blk_parents_wb[s_][0][0]>s_[0]:self.gen.img_('waterL',s_[0],s_[1])
                            if len(self.l_blk_parents_wb[s_])==2:
                                if self.l_blk_parents_wb[s_][0][0]>s_[0] and self.l_blk_parents_wb[s_][1][0]<s_[0]:self.gen.img_('waterB',s_[0],s_[1])
                            if len(self.l_blk_parents_wb[s_])>0:
                                if self.l_blk_parents_wb[s_][0][1]<s_[1]:self.gen.img_('water',s_[0],s_[1])
                    if len(self.l_blk_parents_wb[s_])==0:
                        self.water_blocks.remove(s_)
                        self.l_update_wb.pop(s_)
                        self.l_update_wb_.pop(s_)
                        self.l_blk_parents_wb.pop(s_)
                        self.gen.img_('air',s_[0],s_[1])
        self.map,self.water_blocks,self.sand_blocks,self.gravel_blocks,self.torch_blocks=self.gen.get()
        for wb in self.water_blocks:
            if not (wb[0],wb[1]) in self.l_update_wb.keys():self.l_update_wb[(wb[0],wb[1])]=-1
            self.l_update_wb[(wb[0],wb[1])]=self.l_update_wb[(wb[0],wb[1])]+1
            if self.l_update_wb[(wb[0],wb[1])]==3:
                self.l_update_wb[(wb[0],wb[1])]=0
                s_=tuple([wb[0],wb[1]+1])
                if -1<s_[0]<37 and -1<s_[1]<21:
                    if self.map[s_] in ['air','torch','torchR','torchL']:
                        self.gen.img_('water',s_[0],s_[1])
                        if not s_ in self.l_blk_parents_wb.keys():self.l_blk_parents_wb[s_]=[]
                        self.l_blk_parents_wb[s_].append((s_[0],s_[1]-1))
                    if self.map[s_] not in ['water','waterB','air']:
                        d=[(1,0),(-1,0)]
                        s=[wb[0],wb[1]]
                        for d_ in d:
                            s_=tuple([s[0]+d_[0],s[1]+d_[1]])
                            if -1<s_[0]<37 and -1<s_[1]<21:
                                if self.map[s_]in ['air','waterR','waterL','torch','torchR','torchL']:
                                    s__=tuple(s)
                                    p=0
                                    try:
                                        if self.map[s__]=='water' and d_==d[1] and self.map[tuple([s[0]-1,s[1]+1])] in ['air','water']:
                                            self.gen.img_('waterL',s_[0],s_[1])
                                            if not s_ in self.l_blk_parents_wb.keys():self.l_blk_parents_wb[s_]=[]
                                            self.l_blk_parents_wb[s_].append((s_[0]+1,s_[1]))
                                        else:p+=1
                                    except:
                                        p+=1
                                    try:
                                        if self.map[s__]=='water' and d_==d[0] and self.map[tuple([s[0]+1,s[1]+1])] in ['air','water']:
                                            self.gen.img_('waterR',s_[0],s_[1])
                                            if not s_ in self.l_blk_parents_wb.keys():self.l_blk_parents_wb[s_]=[]
                                            self.l_blk_parents_wb[s_].append((s_[0]-1,s_[1]))
                                        else:p+=1
                                    except:
                                        p+=1
                                    try:
                                        if self.map[s__]=='water' and ((d_==d[0] and self.map[tuple([s[0]+2,s[1]])]=='water' and self.map[tuple([s[0]+1,s[1]+1])] in ['air','water']) or (d_==d[1] and self.map[tuple([s[0]-2,s[1]])]=='water' and self.map[tuple([s[0]-1,s[1]+1])] in ['air','water'])):
                                            self.gen.img_('waterB',s_[0],s_[1])
                                            if not s_ in self.l_blk_parents_wb.keys():self.l_blk_parents_wb[s_]=[]
                                            self.l_blk_parents_wb[s_].append((s_[0]+1,s_[1]))
                                            self.l_blk_parents_wb[s_].append((s_[0]-1,s_[1]))
                                        else:p+=1
                                    except:
                                        p+=1
                                    if p==3:self.gen.img_('water',s_[0],s_[1])
        self.map,self.water_blocks,self.sand_blocks,self.gravel_blocks,self.torch_blocks=self.gen.get()
        for sb in self.sand_blocks:
            s_=tuple([sb[0],sb[1]+1])
            if -1<s_[0]<37 and 0<s_[1]<21:
                s=tuple([sb[0],sb[1]])
                if self.map[tuple(s_)] in ['air','water','waterL','waterR','waterB'] or s in self.l_fall_stage_sb.keys():
                    if s not in self.l_fall_stage_sb.keys():self.l_fall_stage_sb[s]=0
                    self.l_fall_stage_sb[s]=self.l_fall_stage_sb[s]+50
                    if self.l_fall_stage_sb[s]<101:
                        self.gen.img_('sand',s[0],s[1],(self.l_fall_stage_sb[s]))
                    else:
                        self.l_fall_stage_sb.pop(s)
                        if not self.map[tuple(sb)].startswith('water'):self.gen.img_('air',s[0],s[1])
                        self.gen.img_('sand',s[0],s[1]+1,0)
        self.map,self.water_blocks,self.sand_blocks,self.gravel_blocks,self.torch_blocks=self.gen.get()
        for gb in self.gravel_blocks:
            s_=tuple([gb[0],gb[1]+1])
            if -1<s_[0]<37 and 0<s_[1]<21:
                s=tuple([gb[0],gb[1]])
                if self.map[tuple(s_)] in ['air','water','waterL','waterR','waterB'] or s in self.l_fall_stage_gb.keys():
                    if s not in self.l_fall_stage_gb.keys():self.l_fall_stage_gb[s]=0
                    self.l_fall_stage_gb[s]=self.l_fall_stage_gb[s]+50
                    if self.l_fall_stage_gb[s]<101:
                        self.gen.img_('gravel',s[0],s[1],(self.l_fall_stage_gb[s]))
                    else:
                        self.l_fall_stage_gb.pop(s)
                        if not self.map[tuple(gb)].startswith('water'):self.gen.img_('air',s[0],s[1])
                        self.gen.img_('gravel',s[0],s[1]+1,0)
        self.map,self.water_blocks,self.sand_blocks,self.gravel_blocks,self.torch_blocks=self.gen.get()
        for tb in self.torch_blocks:
            if self.map[tuple(tb)]=='torch' and self.map[(tb[0],tb[1]+1)] in ['air','torchR','torchL','torch','water','waterR','waterL','waterB']:self.gen.img_('air',tb[0],tb[1])
            elif self.map[tuple(tb)]=='torchR' and self.map[(tb[0]+1,tb[1])] in ['air','torchR','torchL','torch','water','waterR','waterL','waterB']:self.gen.img_('air',tb[0],tb[1])
            elif self.map[tuple(tb)]=='torchL' and self.map[(tb[0]-1,tb[1])] in ['air','torchR','torchL','torch','water','waterR','waterL','waterB']:self.gen.img_('air',tb[0],tb[1])
        self.map,self.water_blocks,self.sand_blocks,self.gravel_blocks,self.torch_blocks=self.gen.get()
        if self.is_breaking_block and -1<self.looking_block[0]<37 and -1<self.looking_block[1]<21:
            if not self.map[tuple(self.looking_block)]=='air':
                def destroy(blk):
                    if self.map[tuple(blk[0])] in list(self.blk_break_map.keys()):l=self.blk_break_map[self.map[tuple(blk[0])]]
                    else:l=self.blk_break_map['normal']
                    for obj in blk[2]:self.canvas.delete(obj)
                    blk[2],blk[4]=[],[]
                    for mp in l:
                        self.temp_break_img=ImageTk.PhotoImage(self.destr_stages[blk[1]-1].resize((mp[2],mp[3]),Image.ANTIALIAS))
                        self.destr_stages=[Image.open(f'data\\img\\misc\\destroy_{n}.png') for n in range(1,9)]
                        blk[2].append(self.canvas.create_image(blk[0][0]*50+mp[0],blk[0][1]*50+mp[1],image=self.temp_break_img,anchor='nw'))
                        blk[4].append(self.temp_break_img)
                        self.tk.update()
                        self.tk.update_idletasks()
                    blk[3]=0
                    return blk
                if self.breaking_block[0]==None or self.breaking_block[0]!=self.looking_block:
                    self.breaking_block=[self.looking_block,1,[],0,[]]
                    self.breaking_block=destroy(self.breaking_block)
                else:
                    if self.map[tuple(self.breaking_block[0])] in list(self.breaking_tm.keys()):tm=self.breaking_tm[self.map[tuple(self.breaking_block[0])]]
                    else:tm=self.breaking_tm['normal']
                    if self.breaking_block[0]==self.looking_block and self.breaking_block[3]>=tm:
                        self.breaking_block[1]+=1
                        if self.breaking_block[1]>8:
                            for obj in self.breaking_block[2]:self.canvas.delete(obj)
                            while self.map[tuple(self.breaking_block[0])][len(self.map[tuple(self.breaking_block[0])])-1].isupper():self.map[tuple(self.breaking_block[0])]=self.map[tuple(self.breaking_block[0])][:len(self.map[tuple(self.breaking_block[0])])-1]
                            self.gen.give_item(self.map[tuple(self.breaking_block[0])],1,self,[self.breaking_block[0][0]*50+25+random.randint(-5,5),self.breaking_block[0][1]*50+50])
                            if self.gen.metadata_map[tuple(self.breaking_block[0])]!=None:
                                for itm in list(self.gen.metadata_map[tuple(self.breaking_block[0])].values()):self.gen.item([self.breaking_block[0][0]*50+25+random.randint(-5,5),self.breaking_block[0][1]*50+50],itm[0],itm[1])
                            self.gen.img_('air',self.breaking_block[0][0],self.breaking_block[0][1])
                            self.canvas.move(self.looking_marker,-50,-50)
                            self.breaking_block=[None]
                        else:self.breaking_block=destroy(self.breaking_block)
            else:
                if len(self.breaking_block)>1:
                    for obj in self.breaking_block[2]:self.canvas.delete(obj)
                self.breaking_block=[None]
        else:
            if len(self.breaking_block)>1:
                for obj in self.breaking_block[2]:self.canvas.delete(obj)
            self.breaking_block=[None]
        def marker_coords(m,cnv):
            coords=cnv.coords(m)
            coords[0]//=50
            coords[1]//=50
            return coords
        if not self.gui.open:
            if (not marker_coords(self.looking_marker,self.canvas)==self.looking_block) and self.looking_block[0]>-1 and self.looking_block[1]>-1:
                if -1<self.looking_block[0]<37 and -1<self.looking_block[1]<21:
                    self.canvas.delete(self.looking_marker)
                    if self.map[tuple(self.looking_block)] in list(self.bounding_box.keys()):b_b=self.bounding_box[self.map[tuple(self.looking_block)]]
                    else:b_b=self.bounding_box['normal']
                    self.looking_block_img_formatted=ImageTk.PhotoImage(self.looking_marker_img.resize((b_b[2],b_b[3])))
                    self.looking_marker=self.canvas.create_image(self.looking_block[0]*50+b_b[0],self.looking_block[1]*50+b_b[1],image=self.looking_block_img_formatted,anchor='nw')
                else:self.canvas.move(self.looking_marker,-2000,-2000)
        else:self.canvas.move(self.looking_marker,-2000,-2000)
        if not(-1<self.looking_block[0]<37 and -1<self.looking_block[1]<21):self.canvas.move(self.looking_marker,-2000,-2000)
        if self.player.hp>10:self.player.hp=10
        if self.player.hp<0:self.player.hp=0
        if self.player.hp!=self.old_hp-1 or self.enchanted_golden_apple_boost>0:
            self.old_hp=self.player.hp+1
            for obj in self.heart_objs:self.canvas.delete(obj)
            y_pos,half,hp_color=685,False,0
            if self.enchanted_golden_apple_boost>0:hp_color=2
            for i in range(1,11):
                if i<=self.player.hp:self.heart_objs.append(self.canvas.create_image(37*50,y_pos,image=self.heart_img[hp_color+1],anchor='nw'))
                elif str(self.player.hp).endswith('.5') and half==False:
                    self.heart_objs.append(self.canvas.create_image(37*50,y_pos,image=self.heart_img[hp_color+0.5],anchor='nw'))
                    half=True
                else:self.heart_objs.append(self.canvas.create_image(37*50,y_pos,image=self.heart_img[hp_color],anchor='nw'))
                y_pos-=25
        if self.player.food>10:self.player.food=10
        if self.player.food<0:self.player.food=0
        if self.player.food!=self.old_food-1 or self.golden_apple_boost>0:
            self.old_food=self.player.food+1
            for obj in self.food_objs:self.canvas.delete(obj)
            y_pos,half,food_color=685,False,0
            if self.golden_apple_boost>0:food_color=2
            for i in range(1,11):
                if i<=self.player.food:self.food_objs.append(self.canvas.create_image(37*50+25,y_pos,image=self.food_img[food_color+1],anchor='nw'))
                elif str(self.player.food).endswith('.5') and half==False:
                    self.food_objs.append(self.canvas.create_image(37*50+25,y_pos,image=self.food_img[food_color+0.5],anchor='nw'))
                    half=True
                else:self.food_objs.append(self.canvas.create_image(37*50+25,y_pos,image=self.food_img[food_color],anchor='nw'))
                y_pos-=25
        if self.player.food>9 and self.player.hp<10 and self.tm_hp_regen==None:self.tm_hp_regen=random.randint(25,65)/10
        if self.player.food>9 and self.player.hp<10 and self.last_tm_hp_reg+self.tm_hp_regen<=time.time() and not self.tm_hp_regen==None:self.player.hp,self.tm_hp_regen,self.last_tm_hp_reg,self.player.food=self.player.hp+random.choice([0.5,1]),None,time.time(),self.player.food-random.choice([0,0,0,0,0.5])
        if self.player.food>0 and self.tm_food_rm==None:self.tm_food_rm=random.randint(60,120)
        if self.player.food>0 and self.last_tm_food_rm+self.tm_food_rm<=time.time() and not self.tm_food_rm==None:self.player.food,self.tm_food_rm,self.last_tm_food_rm=self.player.food-0.5,None,time.time()
        if self.player.food==0.5 and self.player.hp>0:self.tm_damage_hunger=random.randint(5,35)/10
        if self.player.food==0.5 and self.player.hp>0 and self.last_tm_damage_hunger+self.tm_damage_hunger<=time.time() and not self.tm_damage_hunger==None:self.player.hp,self.tm_damage_hunger,self.last_tm_damage_hunger=self.player.hp-random.choice([0.5,0.5,1]),None,time.time()
        if self.player.food==0 and self.player.hp>0:self.tm_damage_hunger=random.randint(5,35)/33
        if self.player.food==0 and self.player.hp>0 and self.last_tm_damage_hunger+self.tm_damage_hunger<=time.time() and not self.tm_damage_hunger==None:self.player.hp,self.tm_damage_hunger,self.last_tm_damage_hunger=self.player.hp-random.choice([1,1.5]),None,time.time()
        if (self.eating_object!=[None,None] or self.eating_object[0]!=self.inv.itembar[self.inv.s_slot-1][0]) and not self.eating:self.eating_object=[None,None]
        if self.eating:
            if self.eating_object==[None,None]:self.eating_object=[self.inv.itembar[self.inv.s_slot-1][0],time.time()+Item.all_items[Item.all_names.index(self.inv.itembar[self.inv.s_slot-1][0])].eat_time]
            if self.eating_object[1]<=time.time():
                self.player.food+=Item.all_items[Item.all_names.index(self.eating_object[0])].food_heal
                if self.inv.itembar[self.inv.s_slot-1][1]>1:self.inv.itembar[self.inv.s_slot-1][1]-=1
                else:self.inv.itembar[self.inv.s_slot-1]=['air',0]
                if self.eating_object[0]=='chocolate':self.chocolate_hunger.append(random.randint(45,90))
                elif self.eating_object[0]=='golden_apple':self.golden_apple_boost=random.randint(15,20)
                elif self.eating_object[0]=='enchanted_golden_apple':self.enchanted_golden_apple_boost=random.randint(19,24)
                self.eating_object=[None,None]
                if self.inv.itembar[self.inv.s_slot-1][0]=='air' or self.player.food>=10:self.eating=False
        for tm in self.chocolate_hunger:
            if tm==0:
                self.chocolate_hunger.remove(tm)
                self.player.food-=random.choice([0.5,1,1.5])
        if self.golden_apple_boost>0 and self.golden_apple_boost_tm==0.33:
            self.player.food+=0.5
            self.golden_apple_boost_tm=0
        if self.enchanted_golden_apple_boost>0 and self.enchanted_golden_apple_boost_tm==0.33:
            self.player.hp+=0.5
            self.enchanted_golden_apple_boost_tm=0
        if not self.gui.open:
            itm_rm_list_idx=[]
            for itm in self.gen.items:
                if -1<itm[3][0]//50<37 and -1<itm[3][1]//50<21:
                    if itm[2]==0 and itm[4]!=None:itm_rm_list_idx.append(itm)
                    if itm[4]==None:itm[4],itm[2]=self.canvas.create_image(itm[3][0],itm[3][1],image=Item.all_items[Item.all_names.index(itm[0])].img,anchor='s'),120
                    if self.map[(itm[3][0]//50,itm[3][1]//50)]=='air' or itm[5][0]=='air':itm[5][0],itm[3][1],itm[5][1],_='air',itm[3][1]+5,itm[5][1]+5,self.canvas.move(itm[4],0,5)
                    elif (self.map[(itm[3][0]//50,itm[3][1]//50)]=='slabD' or itm[5][0]=='slabD') and itm[5][1]<25:itm[5][0],itm[3][1],itm[5][1],_='slabD',itm[3][1]+5,itm[5][1]+5,self.canvas.move(itm[4],0,5)
                    if itm[5][0]=='air' and itm[5][1]>=50:itm[5]=['',0]
                    for itm_ in self.gen.items:
                        while True:
                            if itm_[4]!=None and itm_[4]!=itm[4] and itm[1]>0 and 0<itm_[1]<64 and itm_[0]==itm[0] and itm[3][0]-60<itm_[3][0]<itm[3][0]+60 and itm[3][1]-40<itm_[3][1]<itm[3][1]+40:itm[1],itm_[1]=itm[1]-1,itm_[1]+1
                            else:break
                    if itm[1]<=0:itm_rm_list_idx.append(itm)
            for itm_rm in itm_rm_list_idx:
                print(f'-{itm_rm[1]} {itm_rm[0]} ({itm_rm[2]-time.time()};{itm_[4]})')
                self.canvas.delete(itm_rm[4])
                self.gen.items.remove(itm_rm)
        if not self.gui.open:
            if len(self.breaking_block)>=3:self.breaking_block[3]+=0.001
            for itm in self.chocolate_hunger:itm-=0.001
            if self.golden_apple_boost>0:self.golden_apple_boost-=0.001
            if self.enchanted_golden_apple_boost>0:self.enchanted_golden_apple_boost-=0.001
            if self.golden_apple_boost>0:self.golden_apple_boost_tm+=0.001
            if self.enchanted_golden_apple_boost>0:self.enchanted_golden_apple_boost_tm+=0.001
            for itm in self.gen.items:itm[2]-=0.001
        self.inv.update()
        self.gui.update()
        self.tk.after(1,self.start)
Game()
