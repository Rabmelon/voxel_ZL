from winreg import SetValue
from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=2)    # create a scene, set the width of voxel edge line and exposure value
scene.set_floor(-1, (1.0, 1.0, 1.0))     # height and color of floor
scene.set_background_color((0.5, 0.5, 0.4))     # color of sky
scene.set_directional_light((1, 1, -1), 0.2, (1, 0.8, 0.6))     # direction and color of light

@ti.func
def create_block(pos, size, color, color_noise):
    endpos = pos + size
    for I in ti.grouped(
            ti.ndrange((pos[0], endpos[0]), (pos[1], endpos[1]), (pos[2], endpos[2]))):
        scene.set_voxel(I, 1, color + color_noise * ti.random())

@ti.func
def create_tree(pos, height, radius, color):
    create_block(pos, ivec3(3, height-radius*0.5, 3), vec3(0.7), vec3(0.3))
    create_leaves(pos + ivec3(0, height, 0), radius, color)
    for i, j in ti.ndrange((-radius, radius), (-radius, radius)):
        prob = max((radius - vec2(i, j).norm()) / radius, 0)
        prob = prob * prob
        if ti.random() < prob * prob:
            scene.set_voxel(pos + ivec3(i, 0, j), 1, color+ti.random() * vec3(0.1))

@ti.func
def create_leaves(pos, radius, color):
    for I in ti.grouped(ti.ndrange((-radius, radius), (-radius, radius), (-radius, radius))):
        f = I / radius
        h = 0.5 - max(f[1], -0.5) * 0.5
        d = vec2(f[0], f[2]).norm()
        prob = max(0, 1-d)**2
        prob *= h
        prob += ti.sin(f[0] * 5 + pos[0]) * 0.02
        prob += ti.sin(f[1] * 9 + pos[1]) * 0.01
        prob += ti.sin(f[2] * 10 + pos[2]) * 0.03
        if prob < 0.1:
            prob = 0.0
        if ti.random() < prob:
            scene.set_voxel(pos + I, 1, color + (ti.random() - 0.5) * 0.2)

@ti.func
def make_fence(start, direction, length):
    color = vec3(0.5, 0.3, 0.2)
    create_block(start, direction * length + ivec3(3, 2, 3), color, vec3(0.1))
    fence_dist = 3
    for i in range(length // fence_dist + 1):
        create_block(start + direction * i * fence_dist + ivec3(1, -3, 1), ivec3(1, 5, 1), color, vec3(0))

@ti.kernel
def initialize_voxels():
    # scene.set_voxel(vec3(0, 0, 0), 1, vec3(1))  # Add a white(1,1,1) voxel at (0,0,0), property is 1 solid voxel or 2 light source voxel
    create_block(ivec3(0, -40, 0), ivec3(1, 40, 1), vec3(0.3, 0.5, 0.3), vec3(0.1))
    create_block(ivec3(0, 0, 0), ivec3(1, 40, 1), vec3(0.5, 0.3, 0.5), vec3(0.1))
    create_block(ivec3(2, 0, 0), ivec3(10, 1, 1), vec3(0.3, 0.5, 0.3), vec3(0.1))
    create_block(ivec3(0, 0, 2), ivec3(1, 1, 10), vec3(0.5, 0.3, 0.5), vec3(0.1))
    for i in range(4):
        create_block(ivec3(-60, -(i + 1)**2 - 41, -60), ivec3(120, 2 * i + 1, 120), vec3(0.5 - i * 0.1) * vec3(1.0, 0.8, 0.6), vec3(0.05 * (3 - i)))
    create_block(ivec3(-60, -41, -60), ivec3(120, 1, 120), vec3(0.3, 0.2, 0.1), vec3(0.01))

    # create_tree(ivec3(-20, -40, 25), 65, 35, vec3(1.0, 0.3, 0.15))
    # create_tree(ivec3(45, -40, -45), 15, 10, vec3(0.8, 0.4, 0.1))
    # create_tree(ivec3(20, -40, 0), 45, 25, vec3(1.0, 0.4, 0.1))
    # create_tree(ivec3(30, -40, -20), 25, 15, vec3(1.0, 0.4, 0.1))
    # create_tree(ivec3(30, -40, 30), 45, 25, vec3(1.0, 0.4, 0.1))

    # make_fence(ivec3(-58, -36, -58), ivec3(1, 0, 0), 115)
    # make_fence(ivec3(-59, -36, 57), ivec3(1, 0, 0), 115)
    # make_fence(ivec3(-59, -36, -58), ivec3(0, 0, 1), 115)
    # make_fence(ivec3(57, -36, -58), ivec3(0, 0, 1), 115)

    create_block(ivec3(-64, 63, -64), ivec3(128, 1, 1), vec3(1.0, 0.0, 0.0), vec3(0.1))
    create_block(ivec3(-64, -64, -64), ivec3(128, 1, 1), vec3(1.0, 0.0, 0.0), vec3(0.1))
    create_block(ivec3(-64, -64, 63), ivec3(128, 1, 1), vec3(1.0, 0.0, 0.0), vec3(0.1))
    create_block(ivec3(-64, -64, -64), ivec3(1, 128, 1), vec3(0.0, 1.0, 0.0), vec3(0.1))
    create_block(ivec3(-64, 63, -64), ivec3(1, 1, 128), vec3(0.0, 0.0, 1.0), vec3(0.1))
    create_block(ivec3(-64, -64, -64), ivec3(1, 1, 128), vec3(0.0, 0.0, 1.0), vec3(0.1))
    create_block(ivec3(63, -64, -64), ivec3(1, 1, 128), vec3(0.0, 0.0, 1.0), vec3(0.1))
    for i in range(-64,64):
        scene.set_voxel(vec3(i), 1, vec3(i/255))

initialize_voxels()

scene.finish()
