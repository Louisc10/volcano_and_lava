#!/usr/bin/env python3
"""
Python OpenGL practical application.
"""

import sys                          # for system arguments

# External, non built-in modules
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np                  # all matrix manipulations & OpenGL args
import glfw                         # lean window system wrapper for OpenGL
import random                       # starndard Python random

from core import Shader, Mesh, Viewer, Node, load
from transform import translate, identity, rotate, scale, vec, quaternion, quaternion_matrix, quaternion_from_euler, quaternion_slerp
from animation import KeyFrames, KeyFrameControlNode
from texture import *


class Axis(Mesh):
    """ Axis object useful for debugging coordinate frames """
    def __init__(self, shader):
        pos = ((0, 0, 0), (1, 0, 0), (0, 0, 0), (0, 1, 0), (0, 0, 0), (0, 0, 1))
        col = ((1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0), (0, 0, 1), (0, 0, 1))
        super().__init__(shader, attributes=dict(position=pos, color=col))

    def draw(self, primitives=GL.GL_LINES, **uniforms):
        super().draw(primitives=primitives, **uniforms)


class Triangle(Mesh):
    """Hello triangle object"""
    def __init__(self, shader, positio):
        position = np.array(((0, .5, 0), (-.5, -.5, 0), (.5, -.5, 0)), 'f')
        color = np.array(((1, 0, 0), (0, 1, 0), (0, 0, 1)), 'f')
        self.color = (1, 1, 0)
        attributes = dict(position=position, color=color)
        super().__init__(shader, attributes=attributes)

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        super().draw(primitives=primitives, global_color=self.color, **uniforms)

    def key_handler(self, key):
        if key == glfw.KEY_C:
            self.color = (0, 0, 0)

class Volcano:
    def __init__(self, shader):
        self.shader = shader
        
        top_volcano = np.array((146/255, 104/255, 41/255), 'f')
        bottom_volcano = np.array((146/255, 116/255, 91/255), 'f')

        position = np.array(((0,.2,0), (-.1,.5,-.3), (-.3,.5,-.1), (-.3,.5,.1), (-.1,.5,.3), (.1,.5,.3), (.3,.5,.1), (.3,.5,-.1), (.1,.5,-.3), (-.2,0,-.7), (-.4,0,-.6), (-.6,0,-.4), (-.7,0,-.2), (-.7,0,0), (-.7,0,.2), (-.6,0,.4), (-.4,0,.6), (-.2,0,.7), (0,0,.7), (.2,0,.7), (.4,0,.6), (.6,0,.4), (.7,0,.2), (.7,0,0), (.7,0,-.2), (.6,0,-.4), (.4,0,-.6), (.2,0,-.7), (0,0,-.7)), 'f')
        
        color = np.array(((0, 0, 0), top_volcano, top_volcano, top_volcano, top_volcano, top_volcano, top_volcano, top_volcano, top_volcano, bottom_volcano, bottom_volcano, bottom_volcano, bottom_volcano, bottom_volcano, bottom_volcano, bottom_volcano, bottom_volcano, bottom_volcano, bottom_volcano, bottom_volcano, bottom_volcano, bottom_volcano, bottom_volcano, bottom_volcano, bottom_volcano, bottom_volcano, bottom_volcano, bottom_volcano, bottom_volcano), 'f')
        
        self.index = np.array(((1, 2, 0), (2, 3, 0), (3, 4, 0), (4, 5, 0), (5, 6, 0), (6, 7, 0), (7, 8, 0), (8, 1, 0), (9, 10, 1), (10, 2, 1), (10, 11, 2), (11, 12, 2), (12, 13, 2), (13, 3, 2), (13, 14, 3), (14, 15, 3), (15, 4, 3), (15, 16, 4), (16, 17, 4), (17, 18, 4), (4, 18, 5), (18, 19, 5), (19, 20, 5), (5, 20, 6), (6, 20, 21), (6, 21, 22), (6, 22, 23), (7, 6, 23), (7, 23, 24), (7, 24, 25), (7, 25, 26), (8, 7, 26), (8, 26, 27), (8, 27, 28), (1, 8, 28), (1, 28, 9)), np.uint32)

        self.glid = GL.glGenVertexArrays(1)  # create OpenGL vertex array id
        GL.glBindVertexArray(self.glid)      # activate to receive state below
        self.buffers = GL.glGenBuffers(3)    # create buffer for position attrib

        # create position attribute, send to GPU, declare type & per-vertex size
        loc = GL.glGetAttribLocation(shader.glid, 'position')
        GL.glEnableVertexAttribArray(loc)    # assign to position attribute
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[0])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, position, GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(loc, 3, GL.GL_FLOAT, False, 0, None)

        # create color attribute, send to GPU, declare type & per-vertex size
        loc = GL.glGetAttribLocation(shader.glid, 'color')
        GL.glEnableVertexAttribArray(loc)    # assign to color
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[1])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, color, GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(loc, 3, GL.GL_FLOAT, False, 0, None)

        # create a dedicated index buffer, copy python array to GPU
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.buffers[2])
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.index,
                        GL.GL_STATIC_DRAW)

    def draw(self, projection, view, **_args):
        GL.glUseProgram(self.shader.glid)

        loc = GL.glGetUniformLocation(self.shader.glid, 'view')
        GL.glUniformMatrix4fv(loc, 1, True, view)

        loc = GL.glGetUniformLocation(self.shader.glid, 'projection')
        GL.glUniformMatrix4fv(loc, 1, True, projection)

        # draw triangle as GL_TRIANGLE indexed mode array, pass array size
        GL.glBindVertexArray(self.glid)
        GL.glDrawElements(GL.GL_TRIANGLES, self.index.size,
                          GL.GL_UNSIGNED_INT, None)

    def __del__(self):
        GL.glDeleteVertexArrays(1, [self.glid])
        GL.glDeleteBuffers(3, self.buffers)

class Cylinder(Node):
    """ Very simple cylinder based on provided load function """
    def __init__(self, shader):
        super().__init__()
        self.add(*load('cylinder.obj', shader))  # just load cylinder from file

class TexturedPlane(Textured):
    """ Simple multi-textured object """
    def __init__(self, shader, tex_file):        
        # setup plane mesh to be textured
        base_coords = ((-1, 0, -1), (1, 0, -1), (1, 0, 1), (-1, 0, 1))
        scaled = 10 * np.array(base_coords, np.float32)
        indices = np.array((1, 0, 2, 2, 0, 3), np.uint32) 
        mesh = Mesh(shader, attributes=dict(position=scaled), index=indices)

        # setup & upload two textures to GPU
        texture = Texture(tex_file)
        super().__init__(mesh, diffuse_map=texture)

class GridTerrain:    
    def __init__(self, shader, total_row=500, total_col=500, ratio=1/30):
        self.shader = shader
        
        position = [] #np.array((),'f')
        color = [] #np.array((),'f')
        index = []
        
        #initialize the positon of the node
        for i in range(total_row):
            for j in range(total_col):
                x = ((i-(total_row/2)) * ratio)
                y = 0
                z = ((j-(total_col/2)) * ratio)
                position.append([x, y, z])
                color.append([random.random(),random.random(),random.random()])
                
        #creating the terain
        for i in range(total_row - 1):
            for j in range(total_col - 1):
                index.append([j+(total_col*i), (j+1)+(total_col*i), j+(total_col*(i+1))])
        
        for i in range(total_row - 1):
            for j in range(total_col - 1):
                index.append([j+(total_col*(i+1)), (j+1)+(total_col*i), (j+1)+(total_col*(i+1))])
                
        position = np.array(position, 'f')
        color = np.array(color, 'f')
        self.index = np.array(index,  np.uint32)

        self.glid = GL.glGenVertexArrays(1)  # create OpenGL vertex array id
        GL.glBindVertexArray(self.glid)      # activate to receive state below
        self.buffers = GL.glGenBuffers(3)    # create buffer for position attrib

        # create position attribute, send to GPU, declare type & per-vertex size
        loc = GL.glGetAttribLocation(shader.glid, 'position')
        GL.glEnableVertexAttribArray(loc)    # assign to position attribute
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[0])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, position, GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(loc, 3, GL.GL_FLOAT, False, 0, None)

        # create color attribute, send to GPU, declare type & per-vertex size
        loc = GL.glGetAttribLocation(shader.glid, 'color')
        GL.glEnableVertexAttribArray(loc)    # assign to color
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[1])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, color, GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(loc, 3, GL.GL_FLOAT, False, 0, None)

        # create a dedicated index buffer, copy python array to GPU
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.buffers[2])
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.index,
                        GL.GL_STATIC_DRAW)

    def draw(self, projection, view, **_args):
        GL.glUseProgram(self.shader.glid)

        loc = GL.glGetUniformLocation(self.shader.glid, 'view')
        GL.glUniformMatrix4fv(loc, 1, True, view)

        loc = GL.glGetUniformLocation(self.shader.glid, 'projection')
        GL.glUniformMatrix4fv(loc, 1, True, projection)

        # draw triangle as GL_TRIANGLE indexed mode array, pass array size
        GL.glBindVertexArray(self.glid)
        GL.glDrawElements(GL.GL_TRIANGLES, self.index.size,
                          GL.GL_UNSIGNED_INT, None)

    def __del__(self):
        GL.glDeleteVertexArrays(1, [self.glid])
        GL.glDeleteBuffers(3, self.buffers)
    
    def rand_pos(self, position, range = 50, ratio = 1/100):
        x = random.randrange(-range/2, range/2) * ratio
        return (position + x)
               
      
# -------------- main program and scene setup --------------------------------
def main():    
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()
    shader = Shader("shader/color.vert", "shader/color.frag")
    normal_shadder = Shader("shader/normal.vert", "shader/normal.frag")
    volcano_shadder = Shader("shader/volcano.vert", "shader/volcano.frag")
    terrain_shadder = Shader("shader/terrain.vert", "shader/terrain.frag")
    
    # viewer.add(TexturedPlane(terrain_shadder, "texture/volcano.png"))
    
    # viewer.add(Volcano(normal_shadder))
    viewer.add(GridTerrain(volcano_shadder))
    
    

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped