import OpenGL.GL as GL              # standard Python OpenGL wrapper
from PIL import Image               # load texture maps
import OpenGL.GL as GL              # standard Python OpenGL wrapper
from PIL import Image               # load texture maps


# -------------- OpenGL Texture Wrapper ---------------------------------------
class Texture:
    """ Helper class to create and automatically destroy textures """
    def __init__(self, tex_file, #Filename that will be loaded
                 wrap_mode=GL.GL_REPEAT, #Repeat, Mirror, Clamp_to_border, Clamp_to_edge
                 mag_filter=GL.GL_LINEAR, #Linear, Nearest
                 min_filter=GL.GL_LINEAR_MIPMAP_LINEAR, # Linear, Nearest, Nearest_Mipmap_Nearest, Nearest_Mipmap_Linear, Linear_Mipmap_Nearest, Linear_Mipmap_Linear
                 tex_type=GL.GL_TEXTURE_2D):
        self.glid = GL.glGenTextures(1)
        self.type = tex_type
        try:
            # imports image as a numpy array in exactly right format
            tex = Image.open(tex_file).convert('RGBA') #load the file in the GPU
            GL.glBindTexture(tex_type, self.glid)
            GL.glTexImage2D(tex_type, 0, GL.GL_RGBA, tex.width, tex.height,
                            0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, tex.tobytes())
            GL.glTexParameteri(tex_type, GL.GL_TEXTURE_WRAP_S, wrap_mode) #What we do wehen we out of bound (Horizontally)
            GL.glTexParameteri(tex_type, GL.GL_TEXTURE_WRAP_T, wrap_mode) #What we do wehen we out of bound (Vertically)
            GL.glTexParameteri(tex_type, GL.GL_TEXTURE_MIN_FILTER, min_filter) #What we do in minification
            GL.glTexParameteri(tex_type, GL.GL_TEXTURE_MAG_FILTER, mag_filter) #what we do in magnigication
            GL.glGenerateMipmap(tex_type)
            print(f'Loaded texture {tex_file} ({tex.width}x{tex.height}'
                  f' wrap={str(wrap_mode).split()[0]}'
                  f' min={str(min_filter).split()[0]}'
                  f' mag={str(mag_filter).split()[0]})')
        except FileNotFoundError:
            print("ERROR: unable to load texture file %s" % tex_file)

    def __del__(self):  # delete GL texture from GPU when object dies
        GL.glDeleteTextures(self.glid)


# -------------- Textured mesh decorator --------------------------------------
class Textured:
    """ Drawable mesh decorator that activates and binds OpenGL textures """
    def __init__(self, drawable, **textures):
        self.drawable = drawable
        self.textures = textures

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        for index, (name, texture) in enumerate(self.textures.items()):
            GL.glActiveTexture(GL.GL_TEXTURE0 + index)
            GL.glBindTexture(texture.type, texture.glid)
            uniforms[name] = index
        self.drawable.draw(primitives=primitives, **uniforms)

class SkyBoxMaterial:
    def __init__(self, filepath):
        tex_type=GL.GL_TEXTURE_CUBE_MAP
        wrap_mode=GL.GL_CLAMP_TO_EDGE #Repeat, Mirror, Clamp_to_border, Clamp_to_edge
        min_filter=GL.GL_NEAREST # Linear, Nearest, Nearest_Mipmap_Nearest, Nearest_Mipmap_Linear, Linear_Mipmap_Nearest, Linear_Mipmap_Linear
        mag_filter=GL.GL_LINEAR #Linear, Nearest
        
        self.glid = GL.glGenTextures(1)
        self.type = tex_type
        try:
            GL.glBindTexture(tex_type, self.glid)
            GL.glTexParameteri(tex_type, GL.GL_TEXTURE_WRAP_S, wrap_mode) #What we do wehen we out of bound (Horizontally)
            GL.glTexParameteri(tex_type, GL.GL_TEXTURE_WRAP_T, wrap_mode) #What we do wehen we out of bound (Vertically)
            GL.glTexParameteri(tex_type, GL.GL_TEXTURE_WRAP_R, wrap_mode) #What we do wehen we out of bound (Vertically)
            GL.glTexParameteri(tex_type, GL.GL_TEXTURE_MIN_FILTER, min_filter) #What we do in minification
            GL.glTexParameteri(tex_type, GL.GL_TEXTURE_MAG_FILTER, mag_filter) #what we do in magnigication

            # imports image as a numpy array in exactly right format
            tex = Image.open("{filepath}/negx.jpg").convert('RGBA') #load the file in the GPU
            GL.glTexImage2D(GL.GL_TEXTURE_CUBE_MAP_NEGATIVE_X, 0, GL.GL_RGBA, tex.width, tex.height,
                            0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, tex.tobytes())

            tex = Image.open("{filepath}/negy.jpg").convert('RGBA') #load the file in the GPU
            GL.glTexImage2D(GL.GL_TEXTURE_CUBE_MAP_NEGATIVE_Y, 0, GL.GL_RGBA, tex.width, tex.height,
                            0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, tex.tobytes())

            tex = Image.open("{filepath}/negz.jpg").convert('RGBA') #load the file in the GPU
            GL.glTexImage2D(GL.GL_TEXTURE_CUBE_MAP_NEGATIVE_Z, 0, GL.GL_RGBA, tex.width, tex.height,
                            0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, tex.tobytes())

            tex = Image.open("{filepath}/posx.jpg").convert('RGBA') #load the file in the GPU
            GL.glTexImage2D(GL.GL_TEXTURE_CUBE_MAP_POSITIVE_X, 0, GL.GL_RGBA, tex.width, tex.height,
                            0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, tex.tobytes())

            tex = Image.open("{filepath}/posy.jpg").convert('RGBA') #load the file in the GPU
            GL.glTexImage2D(GL.GL_TEXTURE_CUBE_MAP_POSITIVE_Y, 0, GL.GL_RGBA, tex.width, tex.height,
                            0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, tex.tobytes())

            tex = Image.open("{filepath}/posz.jpg").convert('RGBA') #load the file in the GPU
            GL.glTexImage2D(GL.GL_TEXTURE_CUBE_MAP_POSITIVE_Z, 0, GL.GL_RGBA, tex.width, tex.height,
                            0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, tex.tobytes())

            print(f'Loaded texture from {filepath} ({tex.width}x{tex.height}'
                  f' wrap={str(wrap_mode).split()[0]}'
                  f' min={str(min_filter).split()[0]}'
                  f' mag={str(mag_filter).split()[0]})')
        except FileNotFoundError:
            print("ERROR: unable to load texture file %s" % filepath)

    def __del__(self):  # delete GL texture from GPU when object dies
        GL.glDeleteTextures(self.glid)