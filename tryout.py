
xr=2
yr=3

v1=[1,2]
v2=[3,4]
v3=[4,5]
v4=[6,7]

v1,v2,v3,v4=[[x*xr,y*yr] for x,y in [v1,v2,v3,v4]]
print(v1,v2,v3,v4,sep='\n')