from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=2)    # create a scene, set the width of voxel edge line and exposure value
scene.set_floor(0, (1.0, 1.0, 1.0))     # height of floor
scene.set_background_color((0.5, 0.5, 0.4))     # color of sky
scene.set_directional_light((1, 1, -1), 0.2, (1, 0.8, 0.6))     # direction and color of light

@ti.func
def create_block(pos, size, color, color_noise):
    endpos = pos + size
    for I in ti.grouped(ti.ndrange((pos[0], endpos[0]), (pos[1], endpos[1]), (pos[2], endpos[2]))):
        scene.set_voxel(I, 1, color + color_noise * ti.random())


@ti.kernel
def initialize_voxels():
    # Your code here! :-)
    scene.set_voxel(vec3(-1, 0, -1), 1, vec3(1))  # Add a white(1,1,1) voxel at (0,0,0), property is 1 solid voxel or 2 light source voxel
    create_block(pos=ivec3(0), size=ivec3(10,40,20), color=vec3(0.3,0.5,0.3), color_noise=vec3(0.1))

initialize_voxels()

scene.finish()
