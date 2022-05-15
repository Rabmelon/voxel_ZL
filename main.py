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
scene.set_directional_light((1, 1, -1), 0.2, (1, 0.8, 0.6))     # direction and color of light

@ti.func
def create_block(pos, size, color, color_noise):
    for I in ti.grouped(ti.ndrange((pos[0], pos[0] + size[0]), (pos[1], pos[1] + size[1]), (pos[2], pos[2] + size[2]))):
        scene.set_voxel(I, 1, color + color_noise * ti.random())

@ti.func
def create_line_centroid(start, direction, length, width, color, color_noise):
    pass

@ti.func
def create_cubic_frame(center, d, w, color, color_noise):
    # 先根据中心点、边长、厚度，确定12个边的起点、方向、尺寸
    pass

@ti.func
def create_cubic_edge(start, direction, length, width):
    # 根据中心起点、方向、长度、厚度，构造体素边（不包含角点）
    pass

@ti.func
def create_cubic_corner(center, d, w):
    pass

@ti.func
def create_cubic_face():
    pass

@ti.func
def create_arrow(start, direction, length, color):
    pass


@ti.kernel
def initialize_voxels():
    # scene.set_voxel(vec3(0, 0, 0), 1, vec3(1))  # Add a white(1,1,1) voxel at (0,0,0), property is 1 solid voxel or 2 light source voxel
    create_block(ivec3(-64, 63, -64), ivec3(128, 1, 1), vec3(1.0, 0.0, 0.0), vec3(0.1))
    create_block(ivec3(-64, -64, -64), ivec3(128, 1, 1), vec3(1.0, 0.0, 0.0), vec3(0.1))
    create_block(ivec3(-64, -64, 63), ivec3(128, 1, 1), vec3(1.0, 0.0, 0.0), vec3(0.1))
    create_block(ivec3(-64, -64, -64), ivec3(1, 128, 1), vec3(0.0, 1.0, 0.0), vec3(0.1))
    create_block(ivec3(-64, 63, -64), ivec3(1, 1, 128), vec3(0.0, 0.0, 1.0), vec3(0.1))
    create_block(ivec3(-64, -64, -64), ivec3(1, 1, 128), vec3(0.0, 0.0, 1.0), vec3(0.1))
    create_block(ivec3(63, -64, -64), ivec3(1, 1, 128), vec3(0.0, 0.0, 1.0), vec3(0.1))

initialize_voxels()

scene.finish()
