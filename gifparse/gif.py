import sys
from io import IOBase, BytesIO, SEEK_CUR
from blocks import Header
from blocks import LogicalScreenDescriptor
from blocks import GlobalColorTable
from blocks import ApplicationExtension
from blocks import GraphicsControlExtension
from blocks import ImageBlock
from blocks import Trailer

class GIF(object):
    def __init__(self, raw):
        is_buffered = isinstance(raw, IOBase) or isinstance(raw, file)
        self.io = raw if is_buffered else BytesIO(raw)
        self.header = ""
        self.screen_desc = ""
        self.global_color_table = ""
        self.application_extensions = []
        self.frames = []
        self.trailer = ""
        self.parse()
        
    def parse(self):
        self.header = Header(self.io.read(6))
        if self.header.raw != "GIF89a":
            sys.stderr.write("WARNING: File/bytes don't have GIF89a header. Parsing halted.\n")
            return False
        self.screen_desc = LogicalScreenDescriptor(self.io.read(7))
        if self.screen_desc.global_color_flag:
            self.global_color_table = GlobalColorTable(self.io.read(self.screen_desc.color_table_length*3))
        last_gce = None
        while True:
            next_two_bytes = self.io.read(2)
            if next_two_bytes == "\x21\xff":
                ext = ApplicationExtension.extract(self.io)
                self.application_extensions.append(ext)
            elif next_two_bytes == "\x21\xf9":
                gce = GraphicsControlExtension.extract(self.io)
                last_gce = gce
            elif next_two_bytes[0] == "\x2c":
                self.io.seek(-1, SEEK_CUR)
                img = ImageBlock.extract(self.io)
                self.frames.append(dict(gce=last_gce, image_block=img))
            else:
                self.io.seek(-1 * len(next_two_bytes), SEEK_CUR)
                break
        self.total_delay = sum([ f["gce"].delay for f in self.frames ])
        self.trailer = Trailer(self.io.read(-1))
        return
    
    def reconstruct_bytes(self):
        return self.header.raw + self.screen_desc.raw + self.global_color_table.raw + \
            "".join(a.raw for a in self.application_extensions) + \
            "".join((f["gce"].raw or "") + f["image_block"].raw for f in self.frames) + \
            self.trailer.raw
