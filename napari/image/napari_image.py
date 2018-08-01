from napari.image.image_type_enum import ImageType


class NImage():


    def __init__(self, array, name:str = '', itype:ImageType = ImageType.Mono):

        self.name     = name
        self.array    = array
        self.itype     = itype
        self.metadata = {}


    def data_type(self):
        return self.array.dtype

    def is_rgb(self):
        return self.itype == ImageType.RGB
