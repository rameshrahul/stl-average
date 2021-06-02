from mesh_to_sdf import get_surface_point_cloud
import trimesh
import skimage, skimage.measure
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

from trimesh.voxel import creation

#from mayavi import mlab


def get_scale_factor(mesh):
    if isinstance(mesh, trimesh.Scene):
        mesh = mesh.dump().sum()

    vertices = mesh.vertices - mesh.bounding_box.centroid
    distances = np.linalg.norm(vertices, axis=1)
    return np.max(distances)


def center_and_scale(mesh, scale_factor):
    if isinstance(mesh, trimesh.Scene):
        mesh = mesh.dump().sum()
    vertices = mesh.vertices - mesh.bounding_box.centroid
    new_mesh = trimesh.Trimesh(vertices=vertices, faces=mesh.faces)
    new_mesh.apply_scale(scale_factor)
    return new_mesh

def scale_to_unit_sphere_ret_transform(mesh, transform=0):
    if isinstance(mesh, trimesh.Scene):
        mesh = mesh.dump().sum()

    vertices = mesh.vertices - mesh.bounding_box.centroid
    distances = np.linalg.norm(vertices, axis=1)
    if transform == 0:
        vertices /= np.max(distances)
    else:
        vertices /= transform
    return trimesh.Trimesh(vertices=vertices, faces=mesh.faces), np.max(distances)


inputs = ['cubes/25 mm cube.stl']
mesh = trimesh.load(inputs[0])
print(mesh)
voxels = trimesh.voxel.creation.voxelize(mesh, 0.1)
mesh = voxels.marching_cubes
mesh.export('cube_voxel.stl')


scale_factors = []


#mesh = trimesh.load('C1 80% Scale.stl')
#mesh = trimesh.load('chair.obj')
#mesh = trimesh.load('Bone1.stl')
#mesh = trimesh.load('cubes/25 mm cube.stl')
mesh = trimesh.load('bones/Bone1.stl')
print(mesh.volume, "mesh 1 volume before converting")
mesh.convert_units('mm', guess=True)
print(mesh.volume, "mesh 1 volume after converting")
mesh.apply_scale(1/25.4)
print(mesh.volume, "mesh 1 volume after converting and scaling")

scale_factors.append(get_scale_factor(mesh))

mesh2 = trimesh.load('bones/Bone2.stl')
#mesh2 = trimesh.load('cubes/Test Cube 15mm.stl')
mesh2.convert_units('mm', guess=True)
mesh2.apply_scale(1/25.4)
scale_factors.append(get_scale_factor(mesh2))



mesh3 = trimesh.load('bones/Bone5.stl')
#mesh3 = trimesh.load('cubes/Test Cube 50 mm.stl')
mesh3.convert_units('mm', guess=True)
mesh3.apply_scale(1/25.4)
scale_factors.append(get_scale_factor(mesh3))


mesh4 = trimesh.load('bones/Bone3.stl')
mesh4.convert_units('mm', guess=True)
mesh4.apply_scale(1/25.4)
scale_factors.append(get_scale_factor(mesh4))



mesh5 = trimesh.load('bones/Bone4.stl')
mesh5.convert_units('mm', guess=True)
mesh5.apply_scale(1/25.4)
scale_factors.append(get_scale_factor(mesh4))

#print(scale_factors)

max_transform = 1/max(scale_factors)
print("scaling by factor of", max_transform)

mesh = center_and_scale(mesh, max_transform)
#mesh, tf = scale_to_unit_sphere_ret_transform(mesh)
cloud = get_surface_point_cloud(mesh, surface_point_method='scan', scan_count=20, scan_resolution=400)
#cloud.show()
print("volume of mesh 1 after scaling", mesh.volume)

#mesh2, transform_2 = scale_to_unit_sphere_ret_transform(mesh2, transform=max_transform)
mesh2 = center_and_scale(mesh2, max_transform)
cloud2 = get_surface_point_cloud(mesh2, surface_point_method='scan', scan_count=20, scan_resolution=400)
#cloud2.show()


#mesh3, transform_3 = scale_to_unit_sphere_ret_transform(mesh3, transform=max_transform)
mesh3 = center_and_scale(mesh3, max_transform)
cloud3 = get_surface_point_cloud(mesh3, surface_point_method='scan', scan_count=20, scan_resolution=400)
#cloud3.show()

#mesh4, transform_4 = scale_to_unit_sphere_ret_transform(mesh4, transform=max_transform)
mesh4 = center_and_scale(mesh4, max_transform)
cloud4 = get_surface_point_cloud(mesh4, surface_point_method='scan', scan_count=20, scan_resolution=400)
#cloud4.show()

#cloud5 = get_surface_point_cloud(mesh5, surface_point_method='scan', scan_count=20, scan_resolution=400)
mesh5 = center_and_scale(mesh5, max_transform)
cloud5 = get_surface_point_cloud(mesh5, surface_point_method='scan', scan_count=20, scan_resolution=400)
#cloud5.show()



print("Voxelizing...")
voxels = cloud.get_voxels(128, use_depth_buffer=True)
voxels2 = cloud2.get_voxels(128, use_depth_buffer=True)
voxels3 = cloud3.get_voxels(128, use_depth_buffer=True)
voxels4 = cloud4.get_voxels(128, use_depth_buffer=True)
voxels5 = cloud5.get_voxels(128, use_depth_buffer=True)


#print(voxels[0])

voxels_avg = 0.2*voxels + 0.2*voxels2 + 0.2*voxels3 + 0.2*voxels4 + 0.2*voxels5
#voxels_avg = 0.333*voxels + 0.333*voxels2 + 0.333*voxels3
#voxels_avg = 0.5*voxels + 0.5*voxels2
#voxels_avg = 0.25*voxels + 0.25*voxels2 + 0.25*voxels3 + 0.25*voxels4 
#voxels_avg = voxels

print("Creating a mesh using Marching Cubes...")
vertices, faces, normals, _ = skimage.measure.marching_cubes_lewiner(voxels_avg, level=0)


#average_mesh = mlab.triangular_mesh([vert[0] for vert in vertices],
#                     [vert[1] for vert in vertices],
#                     [vert[2] for vert in vertices], faces)

average_mesh_trimesh = trimesh.Trimesh(vertices=vertices, faces=faces, vertex_normals=normals)
print(average_mesh_trimesh.volume, "volume before conversion")
average_mesh_trimesh.convert_units('mm', guess=True)
print(average_mesh_trimesh.volume, "volume afer conversion")
average_mesh_trimesh.apply_scale(1/max_transform / get_scale_factor(average_mesh_trimesh))
print(average_mesh_trimesh.volume, "volume afer scaling")

#average_mesh_trimesh, tf = scale_to_unit_sphere_ret_transform(average_mesh_trimesh, transform=1/max_transform)


 

#average_mesh_trimesh.convert_units('mm', guess=True)



#average_mesh_trimesh.apply_scale(1/max_transform)
#average_mesh_trimesh, _ = scale_to_unit_sphere_ret_transform(average_mesh_trimesh, 
#                                                          transform=1)

print("Saving to file")
average_mesh_trimesh.export("avg_cube_trimesh.stl")


#if isinstance(average_mesh_trimesh, trimesh.Scene):
#        average_mesh_trimesh = average_mesh_trimesh.dump().sum()
#trimesh_verts = average_mesh_trimesh.vertices
#trimesh_faces = average_mesh_trimesh.faces

#average_mesh = mlab.triangular_mesh([vert[0] for vert in trimesh_verts],
#                     [vert[1] for vert in trimesh_verts],
#                     [vert[2] for vert in trimesh_verts], trimesh_faces)

#mlab.show()



#mlab.savefig('avg_cube_mlab.obj')

print("finished")
# fig = plt.figure(figsize=(10, 10))
# ax = fig.add_subplot(111, projection='3d')

# # Fancy indexing: `verts[faces]` to generate a collection of triangles
# mesh = Poly3DCollection(vertices[faces])
# mesh.set_edgecolor('k')
# ax.add_collection3d(mesh)

# ax.set_xlabel("x-axis: a = 6 per ellipsoid")
# ax.set_ylabel("y-axis: b = 10")
# ax.set_zlabel("z-axis: c = 16")

# ax.set_xlim(0, 24)  # a = 6 (times two for 2nd ellipsoid)
# ax.set_ylim(0, 20)  # b = 10
# ax.set_zlim(0, 32)  # c = 16

# plt.tight_layout()
# plt.show()

# mesh = trimesh.Trimesh(vertices=vertices, faces=faces, vertex_normals=normals)
# mesh.show()
