class Block(object):
    def __init__(self, raw_bytes):
        self.raw = raw_bytes
        self.parse()
    def parse(self):
        pass


class SubBlock(object):
    @classmethod
    def extract(cls, io):
        subblock_size_bytes = io.read(1)
        subblock_size = int(subblock_size_bytes.encode("hex"), 16)
        subblock_data = io.read(subblock_size)
        subblock = cls(subblock_size_bytes + subblock_data)
        subblock.data = subblock_data
        subblock.size = subblock_size
        return subblock
    def __init__(self, raw_bytes):
        self.raw = raw_bytes
