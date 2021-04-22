import json
import os



LETTERS="_ABCDEFGHI"



def receipe(nm):
	t=input("F-furnace C-crafting_table\n>>> ")
	if (t.lower() in ["c","f"]):
		if (t.lower().startswith("c")):
			o={"type":"crafting_table","receipe":[]}
			while (True):
				end=False
				while (not end):
					km={}
					r=""
					lk="_"
					for x in range(3):
						for y in range(3):
							nm=input(f"Item at ({x},{y})?").lower()
							if (nm in list(km.keys())):
								nm=km[nm]
							else:
								if (nm.replace(" ","") not in ["air",""]):
									k=LETTERS[LETTERS.index(lk)+1]
									lk=LETTERS[LETTERS.index(lk)+1]
									km[nm]=k
									nm=k
								else:
									nm=" "
							r+=nm
						if (x<2):
							r+=";"
					if (str(input("Shaped crafting receipe?")).lower().startswith("y")):
						for k in r.split(";"):
							print(f"\t{k.replace(" ","-")}")
						for k in list(km.keys()):
							print(f"{k}-->{km[k]}")
						o["receipe"].append(str(r.replace(";","")))
					else:
						w_min=2
						h_min=2
						w_max=0
						h_max=0
						h_l,w_l,d_l=["","",""],r.split(";"),["","",""]
						for i in range(len(w_l)):
							d_l[i]=w_l[i]
						for k in w_l:
							for i in range(3):
								if ((not k[i]==" ") and w_min>i):
									w_min=int(i)
								if ((not k[i]==" ") and w_max<i):
									w_max=int(i)
								h_l[i]+=k[i]
						for k in h_l:
							for i in range(3):
								if ((not k[i]==" ") and h_min>i):
									h_min=int(i)
								if ((not k[i]==" ") and h_max<i):
									h_max=int(i)
						w_start=w_min+1
						h_start=h_min+1
						w_start=w_start-1
						h_start=h_start-1
						while (w_min>0):
							w_min-=1
							w_max-=1
						while (h_min>0):
							h_min-=1
							h_max-=1
						moves=[0,1,2]
						for y in moves:
							ym=(h_start-y)*-1
							if (moves.index(y)<=(2-h_max)):
								m_l=["","",""]
								for i in range(len(d_l)):
									m_l[(i+ym)%3]=d_l[i]
								h_l=["","",""]
								for str_ in m_l:
									for i in range(3):
										h_l[i]+=str_[i]
								for x in moves:
									xm=(w_start-x)*-1
									if (moves.index(x)<=(2-w_max)):
										m_l=["","",""]
										for i in range(len(h_l)):
											m_l[(i+xm)%3]=h_l[i]
										w_l=["","",""]
										for str_ in m_l:
											for i in range(3):
												w_l[i]+=str_[i]
										for str_ in w_l:
											print(f"\t{str_.replace(" ","-")}")
										print()
										o["receipe"].append("".join(w_l))
						for k in list(km.keys()):
							print(f"{k}-->{km[k]}")
					if (str(input("Retry?")).lower().startswith("n")):
						end=True
				if (str(input("Add receipe?")).lower().startswith("n")):
					break
			o["key"]={km[nm]:nm for nm in list(km.keys())}
			o["reward"]={"id":nm,"count":int(input("Reward count?"))}
		else:
			o={"type":"furnace","input":input("Input?"),"reward":{"id":nm,"count":int(input("Reward count?"))}}
	with open(f"data/receipes/{nm}.json","w") as f:
		f.write(json.dumps(o,separators=(",",":")))
t=3
while (t<0 or t>2):
	t=int(input("0-all,1-all not defined,2-custom\n>>> "))
if (t==0):
	print("'*' -> Receipe for this item already exists.")
	for k in os.listdir("data/img/items"):
		if (k[-4:]==".png"):
			txt=""
			if os.path.isfile(f"data/receipes/{k[:-4]}.json"):
				txt+="*"
			txt+=f"Add receipe for item '{k[:-4]}'? (y/n)\t"
			if (str(input(txt)).lower().startswith("y")):
				receipe(k[:-4])
elif (t==1):
	for k in os.listdir("data/img/items"):
		if (k[-4:]==".png"):
			if (not os.path.exists(f"data/receipes/{k[:-4]}.json")):
				if (str(input(f"Add receipe for item '{k[:-4]}'? (y/n)\t")).lower().startswith("y")):
					receipe(k[:-4])
elif (t==2):
	while (True):
		receipe(input("Receipe name?"))

