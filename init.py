import bpy
import struct

class SHP0Header:
    def __init__(self):
        self.magic = b"SHP0"
        self.length = 0
        self.version = 4
        self.offset = 0
        self.section_offsets = []
        self.name_offset = 0
    
    def pack(self):
        packed = struct.pack("<4sI4i", self.magic, self.length, self.version, self.offset, len(self.section_offsets))
        packed += struct.pack("<{}i".format(len(self.section_offsets)), *self.section_offsets)
        packed += struct.pack("<I", self.name_offset)
        return packed


header = SHP0Header()
packed_header = header.pack() # Pack the header into binary format

with open("example.shp0", "wb") as f: # Write the binary data to a file
    f.write(packed_header)


def write_animation_entry(f, keyframes, vertex_set_name_idx): #each com is write ...
    
    f.write(struct.pack('<H', len(keyframes)))
    f.write(struct.pack('<H', 0)) #padding
    f.write(struct.pack('<f', 1.0 / len(keyframes))) #inverse number of frames

    for frame, value, slope in key_frames:
        file.write(struct.pack('<fff', frame, value, slope))


#section 0
#section 1

#SHP0 file Loader?


