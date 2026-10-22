"""Inspect uncompressed COCO column-major RLE with 4-foreground/8-background topology."""
from collections import deque

def analyze(data):
    obj(data,['size','counts']);size=sequence(data['size'],2)
    if len(size)!=2:raise ValueError('size is [height,width]')
    h,w=[integer(x,1,512)for x in size];counts=sequence(data['counts'],262145)
    if not counts:raise ValueError('counts must be nonempty')
    for x in counts:integer(x,0,h*w)
    if sum(counts)!=h*w:raise ValueError('run lengths must sum to height*width')
    mask=bytearray(h*w);at=0
    for i,n in enumerate(counts):
        if i%2:
            for q in range(at,at+n):mask[(q%h)*w+q//h]=1
        at+=n
    seen=bytearray(h*w);components=[];holes=0
    four=((1,0),(-1,0),(0,1),(0,-1));eight=four+((1,1),(1,-1),(-1,1),(-1,-1))
    for start in range(h*w):
        if seen[start]:continue
        bit=mask[start];queue=deque([start]);seen[start]=1;area=perimeter=0;edge=False
        minx=w;miny=h;maxx=maxy=-1
        while queue:
            q=queue.popleft();y,x=divmod(q,w);area+=1;edge|=x in (0,w-1)or y in (0,h-1)
            minx=min(minx,x);maxx=max(maxx,x);miny=min(miny,y);maxy=max(maxy,y)
            if bit:
                perimeter+=sum(not(0<=x+dx<w and 0<=y+dy<h)or not mask[(y+dy)*w+x+dx] for dx,dy in four)
            for dx,dy in (four if bit else eight):
                xx=x+dx;yy=y+dy
                if 0<=xx<w and 0<=yy<h:
                    j=yy*w+xx
                    if not seen[j] and mask[j]==bit:seen[j]=1;queue.append(j)
        if bit:
            components.append({'area':area,'bbox':[minx,miny,maxx-minx+1,maxy-miny+1],'perimeter':perimeter})
            if len(components)>4096:raise ValueError('more than 4096 foreground components unsupported')
        elif not edge:holes+=1
    return {'size':[h,w],'area':sum(c['area']for c in components),'component_count':len(components),'holes':holes,
            'euler_characteristic':len(components)-holes,'perimeter':sum(c['perimeter']for c in components),'components':components,
            'connectivity':{'foreground':4,'background':8},'order':'components by first foreground pixel in row-major scan; input is column-major RLE'}
import argparse, json, pathlib, sys

def obj(v, keys, required=None):
    if type(v) is not dict or set(v)-set(keys) or set(required if required is not None else keys)-set(v):
        raise ValueError('invalid object keys: '+str(keys))
    return v

def integer(v, low=-10**12, high=10**12):
    if type(v) is not int or not low<=v<=high: raise ValueError('integer outside supported range')
    return v

def ident(v):
    if type(v) is not str or not 1<=len(v)<=128: raise ValueError('identifier must be 1..128 characters')
    return v

def sequence(v, high):
    if type(v) is not list or len(v)>high: raise ValueError('invalid or oversized list')
    return v

def pairs(xs):
    d={}
    for k,v in xs:
        if k in d: raise ValueError('duplicate JSON key: '+k)
        d[k]=v
    return d

def read(path, limit):
    with open(path,'rb') as f: b=f.read(limit+1)
    if len(b)>limit: raise ValueError('input too large')
    return b

def load(path):
    return json.loads(read(path,1048576).decode('utf8'), object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');a=p.parse_args()
    try: print(json.dumps(analyze(load(a.input)),ensure_ascii=True,indent=2));return 0
    except (ValueError,OSError,UnicodeError,RecursionError) as e:
        print(json.dumps({'error':str(e)}),file=sys.stderr);return 2

if __name__=="__main__": raise SystemExit(main())
