import requests
import PathAlgo
import ast


# Detect if person is in paths or not
def checkpath(cam,path):
    find=True
    for cameras in path:
        for camera in cameras:
            if cam==camera:
                find= False
    return find     
# print(detectCam('cam7'))

def saveAlerts(name,status,cam):
    requests.post("http://127.0.0.1:5000/saveAlerts/"+name+"/"+str(status)+"/"+(cam))
    
def updatetime(name):
    requests.post("http://127.0.0.1:5000/updatetimeout/"+name)


def cameralist():
    response=requests.get("http://127.0.0.1:5000/getAllCameras")
    response=response.json()
    return response

def cameratime():
    response=requests.get("http://127.0.0.1:5000/camtocamtime")
    response=response.json()
    return response

def DestinationCam(des):
    response=requests.get("http://127.0.0.1:5000/getDescam/"+des)
    response=response.json()
    a=response
    remove = str.maketrans("","","{}")
    a = [x.translate(remove) for x in a]  
    return a[0]
 

def DestinationName(name):
    response=requests.get("http://127.0.0.1:5000/getDesbyname/"+name)
    response=response.json()
    a=response
    remove = str.maketrans("","","{}")
    a = [x.translate(remove) for x in a]  
    return a[0]
 
# DestinationCamName
# a=DestinationCam('admin')
# remove = str.maketrans("","","{}")
# a = [x.translate(remove) for x in a]    
# print(DestinationName('saud'))
cameras=[['a', 'd', 'g', 'h'], ['a', 'c', 'd', 'g', 'h']]

if  (checkpath(path=cameras,cam='k')):
    print("f")
else:
    print('b')
# Edges
# edges=(cameratime())
# edges = [ast.literal_eval(i) for i in edges]               
# print(edges)

# nodes
# nodes=(cameralist())
# remove = str.maketrans("","","{}'")
# nodes = [x.translate(remove) for x in nodes]                
# print(nodes)

def getPath(e):
    nodes=(cameralist())
    remove = str.maketrans("","","{}'")
    nodes = [x.translate(remove) for x in nodes] 
    edges=(cameratime())
    edges = [ast.literal_eval(i) for i in edges]                 
    initg=PathAlgo.create_init_graph(nodes,edges)
    g=PathAlgo.Graph(nodes,initg)
    paths=g.printAllPaths("cam1",e)
    paths=PathAlgo.truncate_list(paths,4)
    return paths
# Path Algo Input
# end=PathAlgo.d="h"
# nodes=PathAlgo.nodes=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
# edges=PathAlgo.edges=[
#     ('a', 'b', 2), 
#     ('a', 'c', 3), 
#     ('a', 'd', 1), 
#     ('b', 'd', 4), 
#     ('b', 'e', 5), 
#     ('c', 'd', 2), 
#     ('c', 'f', 7), 
#     ('d', 'g', 1),
#     ('e', 'h', 3),
#     ('f', 'h', 8),
#     ('g', 'h', 2)
# ]
# initg=PathAlgo.create_init_graph(nodes,edges)
# g=PathAlgo.Graph(nodes,initg)
# paths=g.printAllPaths("a","c")
# paths=PathAlgo.truncate_list(paths,4)
# print(paths)
#
# for counter
# dict={'ali':{'a':0,'d':0,'g':0....}}
data={}
cameras=[['a', 'd', 'g', 'h'], ['a', 'c', 'd', 'g', 'h']]
names=['ali']
name=['saud']
result = {name: {camera: 0 for camera_list in cameras for 
                 camera in camera_list} for name in names}
result2 = {name: {camera: 0 for camera_list in cameras for 
                 camera in camera_list} for name in name}


# result
# print(result)
# result.update(result2)
# print(result)

countdata={
    'ali':[('a', 'b', 2), 
    ('a', 'c', 3), 
    ('a', 'd', 1)]
}
def checkcount(name,cam,countdata):
    c=countdata[name][cam]
    if c>=10:
        return True
    else:
        countdata[name][cam]+=1
        return False
    
a=[]
a.append('b')
print(a)
a.append('b')
print(a.__contains__('b'))