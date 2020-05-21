from mesh_to_sdf import mesh_to_voxels, sample_sdf_near_surface
from numba import jit

import trimesh
import pyrender
import numpy as np
import pyglet
import skimage



@jit
def func2():
    mesh = trimesh.load('C1_vertebra.stl')

    voxels = mesh_to_voxels(mesh, 64, pad=True)

    vertices, faces, normals, _ = skimage.measure.marching_cubes_lewiner(voxels, level=0)
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, vertex_normals=normals)
    mesh.show()


if __name__ == "__main__":
    func2()
