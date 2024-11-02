from PIL import Image
from huffman import *

class Encoder:
    def __init__(self, output_stream):
        self.bitstream = output_stream

    # convert and store image height and width 
    def encode_header(self, image):
        width_bits = pad_bits(int_to_binary(image.width), 16)
        self.bitstream.write_bits(width_bits)
        height_bits = pad_bits(int_to_binary(image.height), 16)
        self.bitstream.write_bits(height_bits)    

    # convert and store Huffman table (information to recreate tree)
    def encode_tree(self, tree):
        if type(tree) == tuple: # if not leaf, write 0 and encode branches
            self.bitstream.write_bit(0)
            self.encode_tree(tree[0])
            self.encode_tree(tree[1])
        else: # if leaf, write 1 followed by 8-bit pattern
            self.bitstream.write_bit(1)
            pattern = pad_bits(int_to_binary(tree), 8)
            self.bitstream.write_bits(pattern)

    # convert and store pixel channel intensity values 
    def encode_pixels(self, image, codes):
        for pixel in image.getdata(): # for each pixel in image,
            for channel in pixel: # for each channel in pixel (RGB),
                binary = codes[channel] # convert intensity value to binary
                self.bitstream.write_bits(binary)

class Decoder:
    def __init__(self, input_stream):
        self.bitstream = input_stream

    # read and return image height and width
    def decode_header(self):
        width = binary_to_int(self.bitstream.read_bits(16))
        height = binary_to_int(self.bitstream.read_bits(16))
        return (width, height)

    # read and return Huffman table (information to recreate tree)
    def decode_tree(self):
        flag = self.bitstream.read_bits(1)[0]
        if flag == 1: # if 1, then leaf; return 8-bit pattern
            return binary_to_int(self.bitstream.read_bits(8))
        else: # else if 0 then not leaf; decode left and right branches
            left = self.decode_tree()
            right = self.decode_tree()
            return (left, right)

    # read and return pixel channel intensity values 
    def decode_pixels(self, width, height, tree):
        pixels = bytearray()
        for i in range(height * width * 3):
            pixels.append(self.decode_value(tree))
        return Image.frombytes('RGB', (width, height), bytes(pixels))

    def decode_value(self, tree):
        bit = self.bitstream.read_bit()
        node = tree[bit]
        if type(node) == tuple:
            return self.decode_value(node)
        return node