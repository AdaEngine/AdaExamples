#!/usr/bin/env python3
"""Bake the original deterministic Swift garden into portable GLBs and an Ada scene.

No Blender, network, engine build or application process is needed.
"""
import json
import math
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'Assets'
GENERATED = ASSETS / 'Landscape'
GENERATED.mkdir(exist_ok=True)


def normalize(v):
    length = math.sqrt(sum(x*x for x in v))
    return [x/length for x in v] if length else [0, 1, 0]


def glb(name, positions, indices, colors=None, normals=None, material=None):
    data = bytearray()
    views, accessors = [], []
    def buffer(values, kind, dimensions, component=5126):
        while len(data) % 4: data.append(0)
        offset = len(data)
        flat = [x for row in values for x in row] if dimensions > 1 else values
        data.extend(struct.pack('<' + ('f' if component == 5126 else 'I') * len(flat), *flat))
        views.append({'buffer': 0, 'byteOffset': offset, 'byteLength': len(data)-offset})
        entry = {'bufferView': len(views)-1, 'componentType': component, 'count': len(values), 'type': kind}
        if dimensions == 3:
            entry['min'] = [min(row[i] for row in values) for i in range(3)]
            entry['max'] = [max(row[i] for row in values) for i in range(3)]
        accessors.append(entry)
        return len(accessors)-1
    attrs = {'POSITION': buffer(positions, 'VEC3', 3)}
    if normals: attrs['NORMAL'] = buffer(normals, 'VEC3', 3)
    if colors: attrs['COLOR_0'] = buffer(colors, 'VEC4', 4)
    elements = buffer(indices, 'SCALAR', 1, 5125)
    document = {'asset': {'version': '2.0', 'generator': 'SkeletalGarden portable scene baker'},
                'buffers': [{'byteLength': len(data)}], 'bufferViews': views, 'accessors': accessors,
                'materials': [material or {'pbrMetallicRoughness': {'baseColorFactor': [1,1,1,1], 'metallicFactor': 0, 'roughnessFactor': .95}}],
                'meshes': [{'name': name, 'primitives': [{'attributes': attrs, 'indices': elements, 'material': 0}]}],
                'nodes': [{'name': name, 'mesh': 0}], 'scenes': [{'nodes': [0]}], 'scene': 0}
    encoded = json.dumps(document, separators=(',', ':')).encode()
    encoded += b' ' * (-len(encoded) % 4)
    data += b'\0' * (-len(data) % 4)
    result = struct.pack('<III', 0x46546c67, 2, 12+8+len(encoded)+8+len(data))
    result += struct.pack('<II', len(encoded), 0x4e4f534a)+encoded
    result += struct.pack('<II', len(data), 0x004e4942)+data
    (GENERATED / (name+'.glb')).write_bytes(result)


def trail(z): return 2.2*math.sin(z*.19)


def height(x, z):
    factor = min(max((max(abs(x), abs(z))-6)/3, 0), 1)
    blend = factor*factor*(3-2*factor)
    def bump(cx, cz, spread): return math.exp(-((x-cx)**2+(z-cz)**2)/spread)
    hill = bump(12,11,55)*3.4+bump(-14,12,38)*2.3+bump(14,-14,40)*1.8-bump(-11,-10,15)*.85
    noise = (math.sin(x*.58)*math.cos(z*.41)+math.sin(z*1.1+x*.3)*.25)*.16
    return blend*(hill+noise*min(abs(x-trail(z))/2,1))


vertices = [[-24+c*.75, height(-24+c*.75, -24+r*.75), -24+r*.75] for r in range(65) for c in range(65)]
indices = []
for r in range(64):
    for c in range(64):
        a = r*65+c
        indices.extend([a,a+65,a+66,a,a+66,a+1])


def surface(x,z):
    gx = min(max((x+24)/.75,0),63.9999); gz = min(max((z+24)/.75,0),63.9999)
    c,r = int(gx),int(gz); fx,fz=gx-c,gz-r; i=r*65+c
    a,b,cc,d=[vertices[j][1] for j in [i,i+65,i+66,i+1]]
    return a+(cc-b)*fx+(b-a)*fz if fx<=fz else a+(d-a)*fx+(cc-d)*fz


entities = []
def transform(position=(0,0,0), scale=1, yaw=0, rotation=None):
    return {'position': list(position), 'scale': [scale]*3 if isinstance(scale,(float,int)) else list(scale),
            'rotation': rotation or [0,math.sin(yaw/2),0,math.cos(yaw/2)]}


def entity(name, components):
    item = {'id': f'garden-{len(entities):04d}', 'name': name, 'enabled': True, 'components': components}
    entities.append(item)
    return item


def lod(sources=(), thresholds=(), distance=None, skin=False, animation=False):
    return {'sources': ['@res://'+s+'.glb' for s in sources], 'screenThresholds': list(thresholds),
            'maximumDistance': distance, 'fadeDistance': 5, 'skeletonCompatible': skin, 'animationLOD': animation}


def model(name, asset, position=(0,0,0), scale=1, yaw=0, levels=None, animation='', extras=None):
    source = {'source': '@res://'+asset+'.glb', 'animation': animation, 'autoplay': bool(animation), 'repeats': True}
    if levels is not None: source['lod'] = levels
    comps = {'AdaScene.Model3DSource': source, 'AdaTransform.Transform': transform(position,scale,yaw)}
    comps.update(extras or {})
    return entity(name, comps)


def vector(v): return dict(zip(("x", "y", "z"), v))


def box(size): return {'fixture': {'box': {'_0': {'halfExtents': vector([x/2 for x in size])}}}}

def sphere(radius, center=(0,0,0)): return {'fixture': {'sphere': {'_0': {'radius': radius, 'center': vector(center)}}}}


def body(shapes):
    return {'mode': {'static': {}}, 'shapes': shapes, 'isTrigger': False,
            'material': {'friction': .6, 'restitution': 0, 'density': 1}, 'massProperties': {'mass': 0, 'inertia': vector([0,0,0])}}


def collider(name, position, shapes):
    return entity(name, {'AdaTransform.Transform': transform(position), 'AdaPhysics.PhysicsBody3DComponent': body(shapes)})


def playback(clip, speed=1):
    return {'clip': clip, 'speed': speed, 'repeats': True, 'isPlaying': True, 'transitionDuration': .22, 'synchronizePhase': True}


model('Controlled Robot', 'GardenRobot', (-.7,0,0), .5, math.pi,
      lod(('GardenRobotLOD1','GardenRobotLOD2'),(.18,.07),skin=True), 'Idle',
      {'AdaPhysics.CharacterController3DComponent': {'radius': .4, 'height': 2.15},
       'AdaScene.ModelAnimationPlayback3DComponent': playback('Idle')})
model('Reference Robot', 'GardenRobot', (1.5,0,1.8), .38, math.pi,
      lod(('GardenRobotLOD1','GardenRobotLOD2'),(.18,.07),skin=True,animation=True), 'Walk',
      {'AdaScene.ModelAnimationPlayback3DComponent': playback('Walk',.65)})
for asset,position,scale in [('Courtyard',(0,0,0),1),('Crate',(-2.3,0,-.8),1),('Crate',(2.4,0,-1.5),.8),
                             ('Bench',(-2.8,0,2.5),1),('Plant',(-3.2,0,-2.2),1.2),('Plant',(2.8,0,2.4),1.1),
                             ('Pedestal',(3.1,0,.5),1),('Lantern',(3.1,1,.5),1)]: model(asset,asset,position,scale)
for name,position,size in [('Courtyard floor',(0,-.1,0),(12,.2,12)),('Crate',(-2.3,.4,-.8),(.93,.86,.92)),
                          ('Small crate',(2.4,.32,-1.5),(.744,.688,.736)),('Bench seat',(-2.8,.55,2.5),(1.8,.13,.55)),
                          ('Bench back',(-2.8,.92,2.28),(1.8,.55,.12)),('Bench leg',(-3.45,.25,2.5),(.15,.5,.4)),
                          ('Bench leg',(-2.15,.25,2.5),(.15,.5,.4)),('Pedestal',(3.1,.48,.5),(.9,.96,.9)),
                          ('Lantern',(3.1,1.39,.5),(.48,.78,.48)),('Reference robot',(1.5,.83,1.8),(.85,1.66,.7))]:
    collider(name+' collider',position,[box(size)])
for name,position,radius in [('Chrome sphere',(2.3,.35,-.15),.35),('Plant pot',(-3.2,.3,-2.2),.384),('Plant pot',(2.8,.275,2.4),.352)]:
    collider(name+' collider',position,[sphere(radius)])
collider('Rolling landscape',(0,0,0),[{'fixture': {'triangleMesh': {'_0': {'vertices': [vector(v) for v in vertices],'indices': indices}}}}])

# Preserve the original full-resolution chunk edges at all three LODs.
for row in range(8):
    for column in range(8):
        if column in (3,4) and row in (3,4): continue
        for step in (1,2,4):
            points,normals,colors,elements=[],[],[],[]
            def vertex(x,z):
                cx,rz=column*8+x,row*8+z
                p=vertices[rz*65+cx]
                left,right=vertices[rz*65+max(cx-1,0)],vertices[rz*65+min(cx+1,64)]
                back,front=vertices[max(rz-1,0)*65+cx],vertices[min(rz+1,64)*65+cx]
                dx=(right[1]-left[1])/max(right[0]-left[0],.75)
                dz=(front[1]-back[1])/max(front[2]-back[2],.75)
                variation=.035*math.sin(p[0]*1.3+p[2]*.8)
                base=[.24+variation,.36+variation,.16+variation*.4]
                weight=max(0,1-abs(p[0]-trail(p[2]))/1.4)
                result=len(points); points.append(p); normals.append(normalize([-dx,1,-dz]))
                colors.append([v+(g-v)*weight for v,g in zip(base,[.48,.41,.27])]+[1])
                return result
            for z in range(0,8,step):
                for x in range(0,8,step):
                    if step==1:
                        a,b,c,d=vertex(x,z),vertex(x,z+1),vertex(x+1,z+1),vertex(x+1,z)
                        elements.extend([a,b,c,a,c,d]); continue
                    boundary=[vertex(x,z)]
                    if x==0: boundary += [vertex(x,z+i) for i in range(1,step)]
                    boundary.append(vertex(x,z+step))
                    if z+step==8: boundary += [vertex(x+i,z+step) for i in range(1,step)]
                    boundary.append(vertex(x+step,z+step))
                    if x+step==8: boundary += [vertex(x+step,z+step-i) for i in range(1,step)]
                    boundary.append(vertex(x+step,z))
                    if z==0: boundary += [vertex(x+step-i,z) for i in range(1,step)]
                    center=vertex(x+step//2,z+step//2)
                    for i,a in enumerate(boundary): elements.extend([center,a,boundary[(i+1)%len(boundary)]])
            glb(f'Terrain-{column}-{row}-{step}',points,elements,colors,normals)
        model(f'Terrain {column},{row}',f'Landscape/Terrain-{column}-{row}-1',
              levels=lod((f'Landscape/Terrain-{column}-{row}-2',f'Landscape/Terrain-{column}-{row}-4'),(.65,.3)))

seed = 0xAD_AE3D_2026

def random(lower,upper):
    global seed
    seed = (seed*6364136223846793005+1)&((1<<64)-1)
    return lower+(upper-lower)*(seed>>40)/(1<<24)

counts={'trees':0,'rocks':0,'grass':0}
for row in range(-4,5):
    for column in range(-4,5):
        x,z=column*4.8+random(-1.4,1.4),row*4.8+random(-1.4,1.4)
        if max(abs(x),abs(z))<=8 or abs(x-trail(z))<=2.5: continue
        size=random(.65,1.25); y=surface(x,z)
        model('Tree','Tree',(x,y,z),size,random(0,math.pi*2),lod(('TreeLOD1','TreeLOD2'),(.4,.2)))
        collider('Tree trunk collider',(x,y+1.4*size,z),[box((.45*size,2.8*size,.45*size)),sphere(1.45*size,(0,1.9*size,0))])
        counts['trees']+=1
for _ in range(50):
    x,z=random(-22,22),random(-22,22)
    if max(abs(x),abs(z))<=6.5 or abs(x-trail(z))<=1.8: continue
    size=random(.45,1.35); y=surface(x,z)
    model('Rock','Rock',(x,y,z),size,random(0,math.pi*2),lod(('RockLOD1','RockLOD2'),(.16,.06)))
    collider('Rock collider',(x,y+.5*size,z),[sphere(.72*size)])
    counts['rocks']+=1
for _ in range(220):
    x,z=random(-23,23),random(-23,23)
    if max(abs(x),abs(z))<=6.2 or abs(x-trail(z))<=1.3: continue
    yaw=random(0,math.pi*2); size=random(.8,1.5)
    model('Grass','Grass',(x,surface(x,z),z),size,yaw,lod(distance=30))
    counts['grass']+=1

# Original landmarks, baked once instead of creating GPU meshes at startup.
def block_mesh(name,size,color,roughness=.85,metallic=0):
    points,normals,elements=[],[],[]
    for axis,sign,uv in [(0,1,(1,2)),(0,-1,(1,2)),(1,1,(2,0)),(1,-1,(2,0)),(2,1,(0,1)),(2,-1,(0,1))]:
        start=len(points)
        for a,b in [(-1,-1),(1,-1),(1,1),(-1,1)]:
            p=[0.,0.,0.];p[axis]=size[axis]/2*sign;p[uv[0]]=size[uv[0]]/2*a;p[uv[1]]=size[uv[1]]/2*b
            # Reverse negative faces to keep outward winding.
            points.append(p); n=[0,0,0];n[axis]=sign;normals.append(n)
        order=[0,1,2,0,2,3] if sign>0 else [0,3,2,0,2,1]
        elements.extend(start+i for i in order)
    glb(name,points,elements,normals=normals,material={'pbrMetallicRoughness':{'baseColorFactor':color+[1], 'metallicFactor':metallic,'roughnessFactor':roughness}})

def block(name,position,size,color=None):
    if color:
        asset=f'Block-{len(entities)}';block_mesh(asset,size,color)
        model(name,'Landscape/'+asset,position)
    collider(name+' collider',position,[box(size)])

stone,wood=[.39,.38,.31],[.32,.16,.065]
for i in range(5):
    x,z=7.3+i*1.55,4; h=.35+i*.24
    block('Jump terrace',(x,surface(x,z)+h/2,z),(1.25,h,2.4),stone)
hill=[12,surface(12,11),11]
block('Hill lookout deck',(12,hill[1]+.18,11),(4,.36,3),wood)
for x in (-1.8,1.8):
    for z in (-1.25,1.25): block('Lookout pillar',(12+x,hill[1]+1.9,11+z),(.18,3.6,.18),wood)
block('Lookout canopy',(12,hill[1]+3.8,11),(4.5,.18,3.5),wood)
for x in (-1.5,1.5): block('Garden gateway',(x,1.9,6),(.42,3.8,.42),stone)
block('Gateway lintel',(0,3.9,6),(3.8,.4,.7),stone)
for x,z in [(-13,10),(10,-12),(-8,-6.5)]:
    y=surface(x,z); model('Outer bench','Bench',(x,y,z))
    block('Outer bench',(x,y+.6,z),(1.8,1.2,.55))
    y=surface(x+1.7,z);model('Outer plant','Plant',(x+1.7,y,z))
    block('Outer planter',(x+1.7,y+.6,z),(.7,1.2,.7))
glb('Pond',[[-1.6,0,-1.3],[-1.6,0,1.3],[1.6,0,1.3],[1.6,0,-1.3]],[0,1,2,0,2,3],normals=[[0,1,0]]*4,
    material={'pbrMetallicRoughness':{'baseColorFactor':[.075,.25,.3,1],'metallicFactor':.3,'roughnessFactor':.16}})
model('Shallow garden pond','Landscape/Pond',(-11,-.55,-10))
# UV sphere for the original IBL chrome control.
points,normals,elements=[],[],[]
for r in range(13):
    for c in range(25):
        a,b=math.pi*r/12,math.pi*2*c/24
        n=[math.sin(a)*math.cos(b),math.cos(a),math.sin(a)*math.sin(b)]
        points.append([v*.35 for v in n]);normals.append(n)
for r in range(12):
    for c in range(24):
        a=r*25+c
        if r>0: elements.extend([a,a+1,a+25])
        if r<11: elements.extend([a+1,a+26,a+25])
glb('ChromeSphere',points,elements,normals=normals,material={'pbrMetallicRoughness':{'baseColorFactor':[.85,.9,.95,1],'metallicFactor':1,'roughnessFactor':.12}})
model('IBL Chrome Sphere','Landscape/ChromeSphere',(2.3,.35,-.15))

def light(name,kind,position,color,intensity,rotation=None,**extra):
    component={'radiance':color,'intensity':intensity,'castShadows':True,**extra}
    entity(name,{'AdaScene.'+kind:component,'AdaTransform.Transform':transform(position,rotation=rotation)})

light('Sun','DirectionalLightComponent',(0,0,0),[1,.88,.7],.18,[math.sin(.45),0,0,math.cos(.45)],shadowDistance=60,shadowBias=.002,shadowSlopeBias=.006)
light('Lantern Point Light','PointLightComponent',(3.1,2.4,.5),[1,.35,.08],45,range=9,shadowPriority=2,shadowBias=.002,shadowSlopeBias=.006)
light('Courtyard Cool Point Light','PointLightComponent',(-2.8,2.8,2.5),[.1,.35,1],32,range=8,shadowPriority=0,shadowBias=.002,shadowSlopeBias=.006)
# Aim the +Z spot axis at [0.3,0,0.8].
direction=normalize([1.3,-6,2.3]); yaw=math.atan2(direction[0],direction[2]); pitch=-math.asin(direction[1])
q=[math.sin(pitch/2)*math.cos(yaw/2),math.cos(pitch/2)*math.sin(yaw/2),-math.sin(pitch/2)*math.sin(yaw/2),math.cos(pitch/2)*math.cos(yaw/2)]
light('Garden Spot Light','SpotLightComponent',(-1,6,-1.5),[.3,1,.4],160,q,range=12,innerConeAngle=16,outerConeAngle=28,shadowPriority=5,shadowBias=.002,shadowSlopeBias=.006)
light('Cool Fill Directional','DirectionalLightComponent',(0,0,0),[.3,.4,.8],.2,[-math.sin(.35),0,0,math.cos(.35)],shadowDistance=60,shadowBias=.002,shadowSlopeBias=.006)
entities[-1]['components']['AdaScene.DirectionalLightComponent']['castShadows']=False
entity('Camera', {'AdaRender.Camera': {'projection':'perspective','isActive':True,'renderOrder':0,'backgroundColor':{'red':.12,'green':.2,'blue':.3,'alpha':1}},
                  'AdaTransform.Transform': transform((2.5,3.5,-5.5)),
                  'AdaPhysics.CameraCollision3DComponent': {'origin':vector([0,1.15,0]),'destination':vector([2.5,3.5,-5.5]),'target':vector([0,1.15,0]),'radius':.24,'margin':.08,'recoverySpeed':5,'actualDistance':6.6,'isOccluded':False},
                  'AdaCorePipelines.Environment3D': {'screenSpaceReflection':{'isEnabled':False,'maxDistance':35,'stride':.25,'thickness':.18,'maxSteps':48,'intensity':.7,'edgeFade':.08},
                      'imageBasedLightingSource':'@res://Studio.ibl','imageBasedLightingIntensity':.5,
                      'shadows':{'isEnabled':True,'cascadeCount':3,'splitLambda':.65,'blendFraction':.1},
                      'ambientOcclusion':{'isEnabled':True,'radius':.65,'intensity':1.1,'bias':.025,'sampleCount':16},
                      'antiAliasing':'fxaa','meshVisibility':{'frustumCulling':True,'lod':True,'distanceCulling':True,'gpuOcclusion':False},
                      'localShadows':{'isEnabled':True,'maximumLights':4}}})
scene={'format':'ada.scene','schemaVersion':1,'scene':{'id':'skeletal-garden','name':'Skeletal Garden'},'entities':entities}
(ASSETS/'Scenes'/'Main.ascn').write_text(json.dumps(scene,indent=2)+'\n')
(ROOT/'SourceAssets'/'scene-bake.json').write_text(json.dumps({'entities':len(entities),'terrainVertices':len(vertices),'terrainTriangles':len(indices)//3,**counts},indent=2)+'\n')
print(f'Baked {len(entities)} scene entities; {counts}; 60 terrain chunks with three LODs')
