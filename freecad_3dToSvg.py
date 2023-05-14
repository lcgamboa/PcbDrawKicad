"""
dirt freecad macro python script to convert all 3dmodels in svg outlines to edit and use in pcbdraw

   Tested with FreeCAD_0.19

   Copyright (c) : 2020  Luis Claudio Gambôa Lopes

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2, or (at your option)
   any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

   For e-mail suggestions :  lcgamboa@yahoo.com
"""
outputpath="/tmp/pcbdraw/"
model3dpath="/usr/share/kicad/modules/packages3d/"

from os import listdir,makedirs,path,system
from os.path import isfile, isdir, join, splitext
import shutil
import sys

import ImportGui
import importSVG
import Draft
           
try:
  shutil.rmtree(outputpath)
except OSError as e:
  print("Error: %s - %s." % (e.filename, e.strerror))

for dir in listdir(model3dpath):
  if isdir(join(model3dpath, dir)):   
    path_in=join(model3dpath, dir)
    path_out=join(outputpath, path.splitext(dir)[0])
    makedirs(path_out)
    for file in listdir(path_in):
       fullname_in= join(path_in, file)
       fullname_out= join(path_out, path.splitext(file)[0]+'.svg')
       if isfile(fullname_in):
         if fullname_in.endswith('.step'):
           print(fullname_in)  
           print(fullname_out)  
           doc = App.newDocument("Unnamed")
           #inport 3d step model and make outline
           ImportGui.insert(fullname_in, doc.Name)
           Draft.makeShape2DView(doc.getObject('Part__Feature'))
           doc.recompute()
           doc.removeObject('Part__Feature')
           #put origin box
           pl = FreeCAD.Placement()
           pl.Base = FreeCAD.Vector(0.0, 0.0, 0.0)
           rec = Draft.makeRectangle(length=1.0, height=1.0, placement=pl, face=False, support=None)
           #rec.Label='origin'
           doc.recompute()
           #save SVG
           __objs__=[]
           __objs__.append(doc.getObject("Shape2DView"))
           __objs__.append(doc.getObject("Rectangle"))
           importSVG.export(__objs__,fullname_out)
           del __objs__
           App.closeDocument("Unnamed")
           Gui.updateGui() 
           #replace origin path by rectangle
           os.system("sed -i 's/<path id=\"Rectangle_w0000\"/<rect fill=\"#ff0000\" id=\"origin\" width=\"1\" height=\"1\" x=\"0\" y=\"0\" \/>\\n<path id=\"Rectangle_w0000\"/g' "+fullname_out)
           #remove path
           os.system("sed -i '/<path id=\"Rectangle_w0000\"/d' "+fullname_out)
           
print("Finished !!!!!!!");
