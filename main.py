from svgpathtools import svg2paths2
from math import ceil
import numpy as np
import turtle
import re

svg_file = r'all_svgs\mandalas\Mandala5.svg'

paths, attrs, svg_attr = svg2paths2(svg_file)
svg_size = int(float(svg_attr['viewBox'].split()[-2])), int(float(svg_attr['viewBox'].split()[-1]))
mx = max(svg_size)

with open(svg_file, 'r') as svg:
    svg_text = str(svg.read())

styles_text = re.findall("{.*}", svg_text)
styles_dicts = [{items.split(':')[0]: items.split(':')[1] for items in texts[1:-2].split(';')} for texts in styles_text]

seg_res = 5
polys = []
for path in paths:
    poly = []
    for subpaths in path.continuous_subpaths():
        points = []
        for seg in subpaths:
            interp_num = ceil(seg.length()/seg_res)
            points.append(seg.point(np.arange(interp_num)/interp_num))
        points = np.concatenate(points)
        points = np.append(points, points[0])
        poly.append(points)
    polys.append([[(p.real, p.imag) for p in pl] for pl in poly])


turtle_window = turtle.Screen()
t = turtle

def head_to(t, x, y, draw=True):
    wasdown = t.isdown()
    heading = t.towards(x,y)
    t.pen(pendown=draw)
    t.seth(heading)
    t.clearstamps()
    t.stamp()
    t.goto(x,y)
    t.pen(pendown=wasdown)

def draw_polygon(t, poly, fill='black'):
    t.color(fill,fill)
    p = poly[0]
    head_to(t,p[0],-(p[1]), False)
    for p in poly[1:]: 
        head_to(t,p[0],-(p[1]))
    t.up()

def draw_multipolygon(t, mpoly, fill='black'):
    p = mpoly[0][0]
    head_to(t,p[0],-(p[1]), False)
    t.begin_fill()
    for i, poly in enumerate(mpoly):
        draw_polygon(t, poly, fill)
        if i!=0:
            head_to(t,p[0],-(p[1]), False)
    t.end_fill()

t.reset()
t.setworldcoordinates(-50, -(mx+50), mx+50, 50)
t.mode(mode='world')
t.tracer(n=100, delay=0)

for poly, attr in zip(polys, attrs):
    draw_multipolygon(t, poly)

head_to(t,mx/2,-(mx+40), False)

t.hideturtle()
t.clearstamps()
turtle.done()