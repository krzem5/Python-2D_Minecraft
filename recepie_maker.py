import glob
import json
import os



all_items=[]
for f in glob.iglob("data\\img\\items\\*.png"):all_items.append(f.replace('data\\img\\items\\','').replace('.png',''))
def receipe(itm):
    name=str(itm)
    type_=input('F-furnace C-crafting_table')
    if type_.lower() in ['c','f']:
        if type_.lower().startswith('c'):
            all_={'type':'crafting_table'}
            retry=True
            receipes=[]
            finish=False
            while not finish:
                retry=True
                while retry:
                    letters,used_keys,receipe,last_used_key=list('_ABCDEFGHI'),{},'','_'
                    for x in range(3):
                        for y in range(3):
                            itm=input(f'Item at ({x},{y})?').lower()
                            if itm in list(used_keys.keys()):itm=used_keys[itm]
                            else:
                                if itm.replace(' ','') not in ['air','']:
                                    key=letters[letters.index(last_used_key)+1]
                                    last_used_key=letters[letters.index(last_used_key)+1]
                                    used_keys[itm]=key
                                    itm=key
                                else:itm=' '
                            receipe+=itm
                        if x<2:receipe+=';'
                    if str(input('Shaped crafting receipe?')).lower().startswith('y'):
                        for str_ in receipe.split(';'):print(f"\t{str_.replace(' ','-')}")
                        for k in list(used_keys.keys()):print(f'{k}-->{used_keys[k]}')
                        receipes_=[str(receipe.replace(';',''))]
                    else:
                        w_min=2
                        h_min=2
                        w_max=0
                        h_max=0
                        h_l,w_l,d_l=['','',''],receipe.split(';'),['','','']
                        for i in range(len(w_l)):d_l[i]=w_l[i]
                        for str_ in w_l:
                            for i in range(3):
                                if (not str_[i]==' ') and w_min>i:w_min=int(i)
                                if (not str_[i]==' ') and w_max<i:w_max=int(i)
                                h_l[i]+=str_[i]
                        for str_ in h_l:
                            for i in range(3):
                                if (not str_[i]==' ') and h_min>i:h_min=int(i)
                                if (not str_[i]==' ') and h_max<i:h_max=int(i)
                        w_start,h_start=w_min+1,h_min+1
                        w_start,h_start=w_start-1,h_start-1
                        while w_min>0:w_min,w_max=w_min-1,w_max-1
                        while h_min>0:h_min,h_max=h_min-1,h_max-1
                        moves=[0,1,2]
                        receipes_=[]
                        for y in moves:
                            ym=(h_start-y)*-1
                            if moves.index(y)<=(2-h_max):
                                m_l=['','','']
                                for i in range(len(d_l)):m_l[(i+ym)%3]=d_l[i]
                                h_l=['','','']
                                for str_ in m_l:
                                    for i in range(3):h_l[i]+=str_[i]
                                for x in moves:
                                    xm=(w_start-x)*-1
                                    if moves.index(x)<=(2-w_max):
                                        m_l=['','','']
                                        for i in range(len(h_l)):m_l[(i+xm)%3]=h_l[i]
                                        w_l=['','','']
                                        for str_ in m_l:
                                            for i in range(3):w_l[i]+=str_[i]
                                        for str_ in w_l:print(f"\t{str_.replace(' ','-')}")
                                        print('')
                                        receipes_.append(''.join(w_l))
                        for k in list(used_keys.keys()):print(f'{k}-->{used_keys[k]}')
                    if str(input('Retry?')).lower().startswith('n'):retry=False
                receipes.extend(receipes_)
                if str(input('Add receipe?')).lower().startswith('n'):finish=True
            all_['receipe']=receipes
            all_['key']={used_keys[itm]:itm for itm in list(used_keys.keys())}
            all_['reward']={'id':name,'count':int(input('Reward count?'))}
        else:
            all_={'type':'furnace'}
            all_['input']=input('Input?')
            all_['reward']={'id':name,'count':int(input('Reward count?'))}
    with open(f'data\\receipes\\{name}.json','w') as f:f.write(json.dumps(all_,indent=4))
mode=1#0-all,1-all not defined,2-custom
if mode==0:
    print('\'*\'->Receipe for this item already exists.')
    for itm in all_items:
        txt=''
        if os.path.isfile(f'data\\receipes\\{itm}.json'):txt+='*'
        txt+=f'Add receipe for item \'{itm}\'?'
        if str(input(txt)).lower().startswith('y'):receipe(itm)
elif mode==1:
    for itm in all_items:
        if not os.path.isfile(f'data\\receipes\\{itm}.json'):
            if str(input(f'Add receipe for item \'{itm}\'?')).lower().startswith('y'):receipe(itm)
elif mode==2:
    while True:receipe(input('Receipe name?'))
        
