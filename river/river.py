from core import Mesh, Shader
import numpy as np
import OpenGL.GL as GL
from time import time


class River(Mesh):
    def __init__(self, shader, size):
        self.t0 = time()
        self.time = 0.0
        self.size = size
        self.points = 1000

        index = np.empty((self.points - 1) * (self.points - 1) * 6, dtype=float)
        self.pos = np.empty((self.points**2, 2), dtype=float)
        y, x = np.meshgrid(
            np.linspace(0, self.size, self.points),
            np.linspace(0, self.size, self.points),
        )
        self.pos = np.column_stack((x.ravel(), y.ravel()))

        # Compute indices and normals
        idx = np.arange(0, 6 * (self.points - 1) ** 2, 6)
        i = np.arange(0, self.points - 1).reshape(-1, 1) * self.points
        j = np.arange(0, self.points - 1)

        i1 = (i + j).flatten()
        i2 = i1 + 1
        i3 = i1 + self.points
        i4 = i2 + self.points

        index[idx] = i1
        index[idx + 1] = i3
        index[idx + 2] = i2
        index[idx + 3] = i3
        index[idx + 4] = i4
        index[idx + 5] = i2

        super().__init__(
            shader,
            attributes=dict(position=self.pos),
            index=index,
            time=self.time,
            k_d=(0, 1, 0),
            k_a=(.3, .75, 0.89, 1),
            light_dir=(1, 0, 0),
            k_s=(0, 0, 1),
            s=2,
        )

    def draw(self, primitives=GL.GL_TRIANGLES, attributes=None, **uniforms):
        self.time = time() - self.t0
        self.uniforms["time"] = self.time
        super().draw(primitives, attributes, **uniforms)
