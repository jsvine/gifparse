import struct
from core import Block, SubBlock

class Header(Block):
    pass

class LogicalScreenDescriptor(Block):
    def parse(self):
        packed_field = '{0:08b}'.format(int(self.raw[4].encode("hex"), 16))
        self.global_color_flag = int(packed_field[0], 2)
        self.color_resolution = int(packed_field[1:4], 2)
        self.color_table_length = pow(2, self.color_resolution + 1)

class GlobalColorTable(Block):
    pass

class Trailer(Block):
    pass

class Extension(Block):
    pass

class ApplicationExtension(Extension):
    @classmethod
    def extract(cls, io):
        ext_bytes = "\x21\xff"
        block_size_bytes = io.read(1)
        block_size = int(block_size_bytes.encode("hex"), 16)
        ext_info = io.read(block_size)
        ext_bytes += block_size_bytes + ext_info
        while True:
            subblock = SubBlock.extract(io)
            ext_bytes += subblock.raw
            if subblock.raw[0] == "\x00": break
        return cls(ext_bytes)

class GraphicsControlExtension(Extension):
    @classmethod
    def extract(cls, io):
        ext_bytes = "\x21\xf9"
        block_size_bytes = io.read(1)
        block_size = int(block_size_bytes.encode("hex"), 16)
        packed_byte = io.read(1)
        unpacked_bits = '{0:08b}'.format(int(packed_byte.encode("hex"), 16))
        delay_bytes = io.read(2)
        delay = struct.unpack('H', delay_bytes)[0]
        transparent_color_index = io.read(1)
        terminator = io.read(1)
        ext_bytes += block_size_bytes + packed_byte + delay_bytes + transparent_color_index + terminator
        ext = cls(ext_bytes)
        ext.delay = delay
        return ext

class ImageBlock(Block):
    @classmethod
    def extract(cls, io):
        img_bytes = "\x2c"
        left = io.read(2)
        top = io.read(2)
        width = io.read(2)
        height = io.read(2)
        packed_byte = io.read(1)
        unpacked_bits = '{0:08b}'.format(int(packed_byte.encode("hex"), 16))
        local_color_table_len = int(unpacked_bits[0]) * pow(2, int(unpacked_bits[4:], 2) + 1)
        local_color_table = io.read(3*local_color_table_len)
        lzw_min = io.read(1)
        img_bytes += left + top + width + height + packed_byte + local_color_table + lzw_min
        while True:
            subblock = SubBlock.extract(io)
            img_bytes += subblock.raw
            if subblock.raw[0] == "\x00": break
        img = cls(img_bytes)
        return img
