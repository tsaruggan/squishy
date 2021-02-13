from PIL import Image
from huffman import *

class Encoder:
    def __init__(self, output_stream):
        self.bitstream = output_stream

    def encode_header(self, image):
        height_bits = pad_bits(to_binary_list(image.height), 16)
        self.bitstream.write_bits(height_bits)    
        width_bits = pad_bits(to_binary_list(image.width), 16)
        self.bitstream.write_bits(width_bits)

    def encode_tree(self, tree):
        if type(tree) == tuple: # Note - write 0 and encode children
            self.bitstream.write_bit(0)
            self.encode_tree(tree[0])
            self.encode_tree(tree[1])
        else: # Leaf - write 1, followed by 8 bit symbol
            self.bitstream.write_bit(1)
            symbol_bits = pad_bits(to_binary_list(tree), 8)
            self.bitstream.write_bits(symbol_bits)

    def encode_pixels(self, image, codes):
        for pixel in image.getdata():
            for value in pixel:
                self.bitstream.write_bits(codes[value])

class Decoder:
    def __init__(self, input_stream):
        self.bitstream = input_stream

    def decode_header(self):
        height = from_binary_list(self.bitstream.read_bits(16))
        width = from_binary_list(self.bitstream.read_bits(16))
        return (height, width)

    def decode_tree(self):
        flag = self.bitstream.read_bits(1)[0]
        if flag == 1: # Leaf, read and return symbol
            return from_binary_list(self.bitstream.read_bits(8))
        left = self.decode_tree()
        right = self.decode_tree()
        return (left, right)

    def decode_value(self, tree):
        bit = self.bitstream.read_bits(1)[0]
        node = tree[bit]
        if type(node) == tuple:
            return self.decode_value(node)
        return node

    def decode_pixels(self, height, width, tree):
        pixels = bytearray()
        for i in range(height * width * 3):
            pixels.append(self.decode_value(tree))
        return Image.frombytes('RGB', (width, height), bytes(pixels))