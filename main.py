from scene import Scene
import taichi as ti
from taichi.math import *

# 想法：
# 1，柯西应力张量（立方体边框+箭头+坐标轴+面），每个边厚一点，有一些随机缺损，中空加光源；面可设计为砖墙样式
#       maybe a cauchy stress tensor lantern! with light face around
# 2，湖南电视台大楼羊驼（底座+楼身+连廊+logo+楼顶），可+新楼（阶梯地面+八个独立部分）
# 3，亚琛大教堂

scene = Scene(voxel_edges=0, exposure=2)    # create a scene, set the width of voxel edge line and exposure value
scene.set_floor(-1, (0.5, 0.5, 0.4))     # height and color of floor
scene.set_background_color((0.5, 0.5, 0.4))     # color of sky
scene.set_directional_light((1, 1, 1), 0.2, (1, 0.8, 0.6))     # direction and color of light

dir_face = (vec3(1,0,0), vec3(0,1,0), vec3(0,0,1), vec3(-1,0,0), vec3(0,-1,0), vec3(0,0,-1))
dir_corner = (vec3(1,1,1), vec3(1,1,-1), vec3(1,-1,1), vec3(1,-1,-1), vec3(-1,1,1), vec3(-1,1,-1), vec3(-1,-1,1), vec3(-1,-1,-1))
dir_edge = (vec3(1,1,0), vec3(1,-1,0), vec3(-1,1,0), vec3(-1,-1,0), vec3(1,0,1), vec3(1,0,-1), vec3(-1,0,1), vec3(-1,0,-1), vec3(0,1,1), vec3(0,1,-1), vec3(0,-1,1), vec3(0,-1,-1))

@ti.func
def create_block(pos, size, mat, color, color_noise):
    for I in ti.grouped(ti.ndrange((pos[0], pos[0] + size[0]), (pos[1], pos[1] + size[1]), (pos[2], pos[2] + size[2]))):
        scene.set_voxel(I, mat, color + color_noise * ti.random())

@ti.func
def extend_center(cpos, direction, length, width, mat, color, color_noise):
    begin_pos = cpos - direction * length / 2 - (vec3(1) - direction) * width // 2
    size = direction * length + (vec3(1) - direction) * width
    create_block(begin_pos, size, mat, color, color_noise)

@ti.func
def isequal_vec3(a, b):
    flag = 0
    for i in ti.static(range(3)):
        if a[i] == b[i]:
            flag += 1
    return 1 if flag == 3 else 0

@ti.func
def center_square(cpos, direction, width, mat, color, color_noise):
    for n1 in range(-width, width + 1):
        n2 = width - ti.abs(n1)
        if isequal_vec3(direction, vec3(1,0,0)) or isequal_vec3(direction, vec3(-1,0,0)):
            scene.set_voxel(vec3(cpos[0], cpos[1]+n1, cpos[2]+n2), mat, color+color_noise * ti.random())
            scene.set_voxel(vec3(cpos[0], cpos[1]+n1, cpos[2]-n2), mat, color+color_noise * ti.random())
        elif isequal_vec3(direction, vec3(0,1,0)) or isequal_vec3(direction, vec3(0,-1,0)):
            scene.set_voxel(vec3(cpos[0]+n1, cpos[1], cpos[2]+n2), mat, color+color_noise * ti.random())
            scene.set_voxel(vec3(cpos[0]+n1, cpos[1], cpos[2]-n2), mat, color+color_noise * ti.random())
        elif isequal_vec3(direction, vec3(0,0,1)) or isequal_vec3(direction, vec3(0,0,-1)):
            scene.set_voxel(vec3(cpos[0]+n1, cpos[1]+n2, cpos[2]), mat, color+color_noise * ti.random())
            scene.set_voxel(vec3(cpos[0]+n1, cpos[1]-n2, cpos[2]), mat, color+color_noise * ti.random())

@ti.func
def create_arrow(dir_a, start, direction, length, arrwidth, mat, color, color_noise):
    if dir_a == -1:
        start = start + length*direction
        direction = -direction
    for i in range(length+1):
        scene.set_voxel(start+i*direction, mat, color+color_noise * ti.random())
    for i in range(arrwidth):
        center_square(start+(length - i - 1)*direction, direction, i + 1, mat, color, color_noise)

@ti.func
def create_arrows(cpos, l_cub, l_arr, w_arr, mat, color, color_noise):
    for i in ti.static(range(6)):
        create_arrow(-1, cpos+(l_cub/2+1)*dir_face[i], dir_face[i], l_arr, w_arr, mat, color, color_noise)
    create_arrow(1, cpos+(w_arr+l_cub/2+1)*dir_face[0], dir_face[1], l_arr, w_arr, mat, color, color_noise)
    create_arrow(1, cpos+(w_arr+l_cub/2+1)*dir_face[0], dir_face[2], l_arr, w_arr, mat, color, color_noise)
    create_arrow(1, cpos+(w_arr+l_cub/2+1)*dir_face[1], dir_face[2], l_arr, w_arr, mat, color, color_noise)
    create_arrow(1, cpos+(w_arr+l_cub/2+1)*dir_face[1], dir_face[0], l_arr, w_arr, mat, color, color_noise)
    create_arrow(1, cpos+(w_arr+l_cub/2+1)*dir_face[2], dir_face[0], l_arr, w_arr, mat, color, color_noise)
    create_arrow(1, cpos+(w_arr+l_cub/2+1)*dir_face[2], dir_face[1], l_arr, w_arr, mat, color, color_noise)
    create_arrow(1, cpos+(w_arr+l_cub/2+1)*dir_face[3], dir_face[4], l_arr, w_arr, mat, color, color_noise)
    create_arrow(1, cpos+(w_arr+l_cub/2+1)*dir_face[3], dir_face[5], l_arr, w_arr, mat, color, color_noise)
    create_arrow(1, cpos+(w_arr+l_cub/2+1)*dir_face[4], dir_face[5], l_arr, w_arr, mat, color, color_noise)
    create_arrow(1, cpos+(w_arr+l_cub/2+1)*dir_face[4], dir_face[3], l_arr, w_arr, mat, color, color_noise)
    create_arrow(1, cpos+(w_arr+l_cub/2+1)*dir_face[5], dir_face[3], l_arr, w_arr, mat, color, color_noise)
    create_arrow(1, cpos+(w_arr+l_cub/2+1)*dir_face[5], dir_face[4], l_arr, w_arr, mat, color, color_noise)

@ti.kernel
def initialize_voxels():
    create_block(ivec3(-64, -64, -64), ivec3(128, 1, 1), 2, vec3(1.0, 0.0, 0.0), vec3(0.1))
    create_block(ivec3(-64, -64, -64), ivec3(1, 128, 1), 2, vec3(0.0, 1.0, 0.0), vec3(0.1))
    create_block(ivec3(-64, -64, -64), ivec3(1, 1, 128), 2, vec3(0.0, 0.0, 1.0), vec3(0.1))


    center = vec3(0, 0, 0)
    l_cubic = 40
    w_face = 2
    w_edge = 6
    color_face = vec3(0.2, 0.4, 0.6)
    color_edge = vec3(0.2, 0.2, 0.2)
    color_corner = vec3(0.4, 0.4, 0.4)
    for i in ti.static(range(len(dir_face))):
        extend_center(center + dir_face[i] * l_cubic // 2, vec3(1)-ti.abs(dir_face[i]), l_cubic - w_edge, w_face, 2, color_face, vec3(0.1))
    for i in ti.static(range(len(dir_edge))):
        extend_center(center + dir_edge[i] * l_cubic // 2, vec3(1)-ti.abs(dir_edge[i]), l_cubic - w_edge, w_edge, 1, color_edge, vec3(0.1))
    for i in ti.static(range(len(dir_corner))):
        extend_center(center + dir_corner[i] * l_cubic // 2, vec3(1)-ti.abs(dir_corner[i]), w_edge, w_edge, 2, color_corner, vec3(0.1))

    create_arrows(center, l_cubic, 16, 4, 1, color_edge, vec3(0.1))

    scene.set_voxel(vec3(0,35,0), 2, vec3(1))

initialize_voxels()

scene.finish()
