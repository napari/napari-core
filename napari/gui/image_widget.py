
from OpenGL import GL
from PyQt5 import QtWidgets, QtCore, QtGui, QtOpenGL
from OpenGL.GL.ARB.texture_rg import GL_R32F

import numpy as np
import ctypes
import time

class ImageWidget(QtOpenGL.QGLWidget):

    def __init__(self, image, dimx=0, dimy=1):

        self.brightness = 1
        self.image = image
        self.image_width = image.shape[dimx]
        self.image_height = image.shape[dimy]
        self.image_aspect_ratio = self.image_height/self.image_width

        QtOpenGL.QGLWidget.__init__(self)
        self.resize(self.image_width, self.image_height)
        #self.sizePolicy().setHeightForWidth(True)
        #self.setScaledContents(True)

        #self.t = time.time()
        #self._update_timer = QtCore.QTimer()
        #self._update_timer.timeout.connect(self.update)
        #self._update_timer.start(1e3 / 60.)



    def setBrightness(self, brightness):
        print("brightess = %f" % brightness)
        self.brightness = brightness
        self.update()

    def initializeGL(self):

        w = self.image_width
        h = self.image_height

        # create pixel buffer object for transferring textures
        self._buffer_id = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_PIXEL_UNPACK_BUFFER, self._buffer_id)
        GL.glBufferData(GL.GL_PIXEL_UNPACK_BUFFER, w * h * 4, None, GL.GL_STREAM_DRAW)
        GL.glBindBuffer(GL.GL_PIXEL_UNPACK_BUFFER, 0)

        # map and modify pixel buffer
        GL.glBindBuffer(GL.GL_PIXEL_UNPACK_BUFFER, self._buffer_id)
        pbo_addr = GL.glMapBuffer(GL.GL_PIXEL_UNPACK_BUFFER, GL.GL_WRITE_ONLY)
        # write to PBO using ctypes memmove
        ctypes.memmove(pbo_addr, self.image.ctypes.data, (w * h * self.image.itemsize))
        # write to PBO using numpy interface
        #pbo_ptr = ctypes.cast(pbo_addr, ctypes.POINTER(ctypes.c_float))
        #pbo_np = np.ctypeslib.as_array(pbo_ptr, shape=(h, w))
        #pbo_np[:] = self.image
        GL.glUnmapBuffer(GL.GL_PIXEL_UNPACK_BUFFER)
        GL.glBindBuffer(GL.GL_PIXEL_UNPACK_BUFFER, 0)

        # create texture from pixel buffer object
        self._texture_id = GL.glGenTextures(1)
        GL.glBindBuffer(GL.GL_PIXEL_UNPACK_BUFFER, self._buffer_id)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture_id)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL_R32F, w, h, 0, GL.GL_RED, GL.GL_FLOAT, None)
        GL.glBindBuffer(GL.GL_PIXEL_UNPACK_BUFFER, 0)

        # create a shader for coloring the texture
        shader_program = QtGui.QOpenGLShaderProgram()
        vertex_src = """
        void main() {
            gl_TexCoord[0] = gl_MultiTexCoord0;
            gl_Position = gl_Vertex;
        }
        """
        fragment_src = """
        uniform highp sampler2D tex;
        uniform float brightness;

        void main() {
            float val = texture2D(tex, gl_TexCoord[0].xy).r;
            vec4 color = vec4(val, val, val, 1.)*brightness;
            gl_FragColor = color;
        }
        """
        shader_program.addShaderFromSourceCode(QtGui.QOpenGLShader.Vertex,   vertex_src)
        shader_program.addShaderFromSourceCode(QtGui.QOpenGLShader.Fragment, fragment_src)
        shader_program.link()
        self._shader_program = shader_program
        self.brightness_uniform = shader_program.uniformLocation("brightness")

    def paintGL(self):
        target = QtCore.QRectF(-1, -1, 2, 2)
        self._shader_program.bind()
        self._shader_program.setUniformValue(self.brightness_uniform, self.brightness)
        self.drawTexture(target, self._texture_id)

    def resizeGL(self, width, height):
        pass
        # new_ratio = height / width
        # if new_ratio > self.image_aspect_ratio:
        #     height = width * self.image_aspect_ratio
        # else:
        #     width = height / self.image_aspect_ratio
        # self._viewport_width  = width
        #self._viewport_height = height
        #print("w=%d h=%d \n" % (w,h) )
        #GL.glViewport(0, 0, 2*width, 2*height)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, w):
        return int(w * (self.image_height / self.image_width))