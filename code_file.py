import math
import random



def decode(txt):
    text,key,txt='',int(txt.split(' ')[0]),txt.split(' ')[1:]
    for i in txt:
        if i!='':text+=chr(int(i))
    col,row=math.ceil(len(text)/key),key
    eb,txt,c,r=(col*row)-len(text),['']*col,0,0
    for symbol in text:
        txt[c],c=txt[c]+symbol,c+1
        if(c==col)or(c==col-1 and r>=row-eb):c,r=0,r+1
    return ''.join(txt)
def code(key,text):
    txt,text_=['']*key,f'{key} '
    for c in range(key):
        p=c
        while p<len(text):
            txt[c]+=text[p]
            p+=key
    for i in str(''.join(txt)):text_+=str(ord(i))+' '
    return text_
with open('saves/test.txt','r') as f:
    text=f.read()
    print(decode(text))
