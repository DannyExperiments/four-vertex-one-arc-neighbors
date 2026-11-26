#!/usr/bin/env python3
"""Rotate both four-vertex graphs with their original directed arcs."""
from math import atan2, cos, hypot, pi, sin, tau
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W,H=664,434
COLORS=["#0d1723","#162638","#2f475c","#eef6fa","#b1c7d8","#80e2cb","#ffc27d","#6f94b0"]
NODES={0:(0,.22,.43),1:(-1,-.72,-.27),2:(1,-.72,-.27),3:(0,1,-.44)}
D=[(0,1),(0,2),(0,3),(1,2)]
OTHER=[(1,0),(2,0),(0,3)]


def font(size,bold=False):
    names=("Arial Bold.ttf","DejaVuSans-Bold.ttf") if bold else ("Arial.ttf","DejaVuSans.ttf")
    for name in names:
        for dirpath in (Path("/System/Library/Fonts/Supplemental"),Path("/usr/share/fonts/truetype/dejavu")):
            path=dirpath/name
            if path.is_file():
                return ImageFont.truetype(str(path),size)
    raise RuntimeError("Arial or DejaVu Sans is required")


FONTS=[font(32,True),font(19),font(22,True),font(18),font(19,True)]


def project(x,y,z,angle,center):
    x,z=x*cos(angle)+z*sin(angle),-x*sin(angle)+z*cos(angle)
    y,z=y*cos(.34)-z*sin(.34),y*sin(.34)+z*cos(.34)
    scale=59*6/(6-z)
    return center+x*scale,217-y*scale,z


def arrow(d,a,b,highlight):
    ax,ay,_=a
    bx,by,_=b
    dist=hypot(bx-ax,by-ay)
    if dist<22:
        return
    theta=atan2(by-ay,bx-ax)
    dx,dy=cos(theta),sin(theta)
    pad=min(20,dist/4)
    end=bx-pad*dx,by-pad*dy
    color=COLORS[6 if highlight else 7]
    d.line((ax+pad*dx,ay+pad*dy,*end),fill=color,width=4 if highlight else 3)
    d.polygon([end,(end[0]-12*cos(theta+.5),end[1]-12*sin(theta+.5)),
               (end[0]-12*cos(theta-.5),end[1]-12*sin(theta-.5))],fill=color)


def graph(d,center,angle,edges):
    p={node:project(*xyz,angle,center) for node,xyz in NODES.items()}
    for a,b in sorted(edges,key=lambda e:p[e[0]][2]+p[e[1]][2]):
        arrow(d,p[a],p[b],(a,b)==(1,2))
    for node,(x,y,z) in sorted(p.items(),key=lambda item:item[1][2]):
        r=16+1.5*z
        color=COLORS[5 if node==0 else 7]
        d.ellipse((x-r,y-r,x+r,y+r),fill=COLORS[2],outline=color,width=2)
        d.text((x,y),str(node),font=FONTS[4],fill=COLORS[3],anchor="mm")


def frame(angle):
    image=Image.new("RGB",(W,H),COLORS[0])
    d=ImageDraw.Draw(image)
    d.text((24,18),"A nearer DAG takes more than one edit",font=FONTS[0],fill=COLORS[3])
    d.text((24,59),"Four vertices  ·  Distance counts d-separation disagreements",font=FONTS[1],fill=COLORS[4])
    for x,edges,title,cap in (
        (24,D,"D  ·  Fixed input","Best positive one-edit distance 2"),
        (344,OTHER,"H  ·  Nearest alternative","Global positive distance 1"),
    ):
        d.rounded_rectangle((x,102,x+296,337),radius=18,fill=COLORS[1],outline=COLORS[2])
        d.text((x+14,116),title,font=FONTS[2],fill=COLORS[3])
        graph(d,x+148,angle,edges)
        d.text((x+14,300),cap,font=FONTS[3],fill=COLORS[5])
    d.text((24,362),"Only new separation in H: vertices 1 and 2, unconditioned.",font=FONTS[4],fill=COLORS[3])
    d.text((24,397),"After free reorientation of D, one deletion reaches H.",font=FONTS[3],fill=COLORS[4])
    return image


def main():
    palette=Image.new("P",(1,1))
    palette.putpalette([int(c[i:i+2],16) for c in COLORS for i in (1,3,5)]+[0,0,0]*(256-len(COLORS)))
    frames=[frame(tau*i/48+pi/8).quantize(palette=palette,dither=Image.Dither.NONE) for i in range(48)]
    frames[0].save(Path(__file__).with_name("fixed-dag-neighbors.gif"),save_all=True,append_images=frames[1:],
                   loop=0,duration=130,optimize=True,disposal=1)


if __name__=="__main__":
    main()
