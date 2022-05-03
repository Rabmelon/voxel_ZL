from scene import Scene
import taichi as ti
from taichi.math import *

# scene = Scene(voxel_edges=0, exposure=2)    # create a scene, set the width of voxel edge line and exposure value
# scene.set_floor(0, (1.0, 1.0, 1.0))     # height of floor
# scene.set_background_color((0.5, 0.5, 0.4))     # color of sky
# scene.set_directional_light((1, 1, -1), 0.2, (1, 0.8, 0.6))     # direction and color of light
scene = Scene(voxel_edges=0, exposure=2)
scene.set_floor(-0.85, (1.0, 1.0, 1.0))
scene.set_background_color((0.5, 0.5, 0.4))
scene.set_directional_light((1, 1, -1), 0.2, (1, 0.8, 0.6))

@ti.func
def create_block(pos, size, color, color_noise):
    for I in ti.grouped(
            ti.ndrange((pos[0], pos[0] + size[0]), (pos[1], pos[1] + size[1]),
                       (pos[2], pos[2] + size[2]))):
        scene.set_voxel(I, 1, color + color_noise * ti.random())

@ti.kernel
def initialize_voxels():
    # Your code here! :-)
    # scene.set_voxel(vec3(-1, 0, -1), 1, vec3(1))  # Add a white(1,1,1) voxel at (0,0,0), property is 1 solid voxel or 2 light source voxel
    for i in range(4):
        create_block(ivec3(-60, -(i + 1)**2 - 40, -60),
                     ivec3(120, 2 * i + 1, 120),
                     vec3(0.5 - i * 0.1) * vec3(1.0, 0.8, 0.6),
                     vec3(0.05 * (3 - i)))

initialize_voxels()

scene.finish()
