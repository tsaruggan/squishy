from PIL import Image, ImageChops
import sys, string
import copy

from IO import Input, Output
from codec import Encoder, Decoder
from huffman import *

class Squishy:
    def compress(self,in_file_name, out_file_name = ''):
        if (out_file_name == ''):
            out_file_name = in_file_name.split('.')[0] + ".bin"
        print('Compressing "%s" -> "%s"' % (in_file_name, out_file_name))
        image = Image.open(in_file_name)
        print('Image shape: (height=%d, width=%d)' % (image.height, image.width))
        size_raw = raw_size(image.height, image.width)
        print('RAW image size: %d bytes' % size_raw)

        counts = count_symbols(image)
        tree = build_tree(counts)
        trimmed_tree = trim_tree(tree)
        codes = assign_codes(trimmed_tree)
        size_estimate = compressed_size(counts, codes)
        print('Estimated size: %d bytes' % size_estimate)

        print('Writing...')
        stream = Output(out_file_name)
        encoder = Encoder(stream)
        print('* Header offset: %d' % stream.bytes_written)
        encoder.encode_header(image)
        stream.flush() # Ensure next chunk is byte-aligned
        print('* Tree offset: %d' % stream.bytes_written)
        encoder.encode_tree(trimmed_tree)
        stream.flush() # Ensure next chunk is byte-aligned
        print('* Pixel offset: %d' % stream.bytes_written)
        encoder.encode_pixels(image, codes)
        stream.close()

        size_real = stream.bytes_written
        print('Wrote %d bytes.' % size_real)
        print('Compression ratio: %0.2f' % (float(size_raw) / size_real))
    
    def decompress(self,in_file_name, out_file_name = ''):
        if (out_file_name == ''):
            out_file_name = in_file_name.split('.')[0] + ".png"
        else:
            out_file_name = out_file_name.split('.')[0] + ".png"

        print('Decompressing "%s" -> "%s"' % (in_file_name, out_file_name))

        print('Reading...')
        stream = Input(in_file_name)
        decoder = Decoder(stream)
        print('* Header offset: %d' % stream.bytes_read)
        height, width = decoder.decode_header()
        stream.flush() # Ensure next chunk is byte-aligned
        print('* Tree offset: %d' % stream.bytes_read)    
        trimmed_tree = decoder.decode_tree()
        stream.flush() # Ensure next chunk is byte-aligned
        print('* Pixel offset: %d' % stream.bytes_read)
        image = decoder.decode_pixels(height, width, trimmed_tree)
        stream.close()

        print('Read %d bytes.' % stream.bytes_read)
        print('Image size: (height=%d, width=%d)' % (height, width))
        image.save(out_file_name)

def compressed_size(counts, codes):
    header_size = 2 * 16 # height and width as 16 bit values
    tree_size = len(counts) * (1 + 8) # Leafs: 1 bit flag, 8 bit symbol each
    tree_size += len(counts) - 1 # Nodes: 1 bit flag each
    if tree_size % 8 > 0: # Padding to next full byte
        tree_size += 8 - (tree_size % 8)
    # Sum for each symbol of count * code length
    pixels_size = sum([count * len(codes[symbol]) for symbol, count in counts])
    if pixels_size % 8 > 0: # Padding to next full byte
        pixels_size += 8 - (pixels_size % 8)
    return (header_size + tree_size + pixels_size) / 8

def raw_size(width, height):
    header_size = 2 * 16 # height and width as 16 bit values
    pixels_size = 3 * 8 * width * height # 3 channels, 8 bits per channel
    return (header_size + pixels_size) / 8

def images_equal(file_name_a, file_name_b):
    image_a = Image.open(file_name_a)
    image_b = Image.open(file_name_b)
    diff = ImageChops.difference(image_a, image_b)
    return diff.getbbox() is None