from mesh_to_sdf import get_surface_point_cloud, scale_to_unit_sphere
import trimesh
import skimage, skimage.measure
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from mayavi import mlab

#mesh = trimesh.load('C1 80% Scale.stl')
#mesh = trimesh.load('chair.obj')
mesh = trimesh.load('Bone1.stl')
#mesh = trimesh.load('bone_avg.obj')
mesh = scale_to_unit_sphere(mesh)
#mesh.apply_scale(1.3)
print("Scanning...")
cloud = get_surface_point_cloud(mesh, surface_point_method='scan', scan_count=20, scan_resolution=400)

#cloud.show()



mesh2 = trimesh.load('Bone2.stl')
mesh2 = scale_to_unit_sphere(mesh2)
cloud2 = get_surface_point_cloud(mesh2, surface_point_method='scan', scan_count=20, scan_resolution=400)
#cloud2.show()


mesh3 = trimesh.load('Bone5.stl')
mesh3 = scale_to_unit_sphere(mesh3)
cloud3 = get_surface_point_cloud(mesh3, surface_point_method='scan', scan_count=20, scan_resolution=400)
#cloud3.show()


mesh4 = trimesh.load('Bone3.stl')
mesh4 = scale_to_unit_sphere(mesh4)
cloud4 = get_surface_point_cloud(mesh4, surface_point_method='scan', scan_count=20, scan_resolution=400)
#cloud4.show()


mesh5 = trimesh.load('Bone4.stl')
mesh5 = scale_to_unit_sphere(mesh5)
cloud5 = get_surface_point_cloud(mesh5, surface_point_method='scan', scan_count=20, scan_resolution=400)
#cloud5.show()

print("Voxelizing...")
voxels = cloud.get_voxels(128, use_depth_buffer=True)
voxels2 = cloud2.get_voxels(128, use_depth_buffer=True)
voxels3 = cloud3.get_voxels(128, use_depth_buffer=True)
voxels4 = cloud4.get_voxels(128, use_depth_buffer=True)
voxels5 = cloud5.get_voxels(128, use_depth_buffer=True)


voxels_avg = 0.2*voxels + 0.2*voxels2 + 0.2*voxels3 + 0.2*voxels4 + 0.2*voxels5
#voxels_avg = 0.333*voxels + 0.333*voxels2 + 0.333*voxels3
#voxels_avg = 0.5*voxels2 + 0.5*voxels3


print("Creating a mesh using Marching Cubes...")
vertices, faces, normals, _ = skimage.measure.marching_cubes_lewiner(voxels_avg, level=0)

#print ("figuring out ranges")
#print(min([vert[0] for vert in vertices]))
#print(max([vert[0] for vert in vertices]))
#print()
#print(min([vert[1] for vert in vertices]))
#print(max([vert[1] for vert in vertices]))
#print()
#print(min([vert[2] for vert in vertices]))
#print(max([vert[2] for vert in vertices]))

scale_factor = 1

average_mesh = mlab.triangular_mesh([vert[0]*scale_factor for vert in vertices],
                     [vert[1]*scale_factor for vert in vertices],
                     [vert[2]*scale_factor for vert in vertices], faces)
#mlab.show()

#print("Saving to file")

mlab.savefig('bone_avg_five.obj')

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
