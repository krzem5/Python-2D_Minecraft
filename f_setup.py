import random



text=''
with open('saves/test.world','w') as f:
    for _ in range(21):
        text+='air:-,'*37
        text=text[:len(text)-1]
        if _<20:text+=';'
    text+=';;0,0;;0,0;;air,0;;1;;10.0,10.0;;-;;-;;-'
    key=random.randint(round(len(text)/3),round(len(text)/3*2))
    txt,text_=['']*key,''
    for c in range(key):
        p=c
        while p<len(text):
            txt[c]+=text[p]
            p+=key
    for chr_ in str(key):text_+=chr(ord(chr_)+2)
    for i in str(''.join(txt)):text_+=f' {chr(ord(i)+2)}'
    f.write(text_)
t=''
with open('saves/test(2x).txt','w') as f:
    for _ in range(10):
        t+='air,'*18
        t=t[:len(t)-1]
        if _<9:t+=';'
    t+=';;0,0;;'
    t+='stone,10;'*9
    t=t[:len(t)-1]
    f.write(t)
