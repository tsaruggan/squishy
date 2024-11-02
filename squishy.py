from PIL import Image, ImageChops
import sys, string
import copy

from IO import Input, Output
from codec import Encoder, Decoder
from huffman import *
 
class Squishy:
    def compress(self,in_file_name, out_file_name = ''):
        # assign output filename
        if (out_file_name == ''):
            out_file_name = in_file_name.split('.')[0] + ".bin"
        
        print('Compressing "%s" -> "%s"' % (in_file_name, out_file_name))
        image = Image.open(in_file_name)
        print('Image dimensions: %d x %dpx' % (image.width, image.height))
        size_raw = raw_size(image.width, image.height)
        print('RAW size: %d bytes' % size_raw)

        counts = count_symbols(image)
        tree = build_tree(counts)
        codes = assign_binary_patterns(tree)
        size_compressed = compressed_size(counts, codes)
        print('Compressed size: %d bytes' % size_compressed)

        print('Writing...')
        stream = Output(out_file_name)
        encoder = Encoder(stream)

        # encode image dimensions
        encoder.encode_header(image)
        stream.flush()
        size_header = stream.bytes_written
        print('* Header: %d bytes' % size_header)

        # encode Huffman table 
        encoder.encode_tree(tree)
        stream.flush()
        size_tree = stream.bytes_written - size_header
        print('* Tree: %d bytes' % size_tree)
        
        # encode image pixel data
        encoder.encode_pixels(image, codes)
        stream.close()
        size_pixels = stream.bytes_written - size_tree - size_header
        print('* Pixels: %d bytes' % size_pixels)
        
        size_wrote = stream.bytes_written
        print('Compressed %d bytes.' % size_wrote)
        space_saving = 100 * float(1 - size_wrote / size_raw)
        print('Memory reduced by %0.2f' % (space_saving), '%.')
    
    def decompress(self,in_file_name, out_file_name = ''):
        # assign output filename
        if (out_file_name == ''):
            out_file_name = in_file_name.split('.')[0] + ".png"
        else:
            out_file_name = out_file_name.split('.')[0] + ".png"

        print('Decompressing "%s" -> "%s"' % (in_file_name, out_file_name))
        print('Reading...')
        stream = Input(in_file_name)
        decoder = Decoder(stream)

        # decode image dimensions
        width, height = decoder.decode_header()
        stream.flush()
        size_header = stream.bytes_read
        print('* Header: %d bytes' % size_header)

        # decode Huffman table
        tree = decoder.decode_tree()
        stream.flush()
        size_tree = stream.bytes_read - size_header
        print('* Tree: %d bytes' % size_tree)    

        # decode image pixel data
        image = decoder.decode_pixels(width, height, tree)
        stream.close()
        size_pixels = stream.bytes_read - size_tree - size_header
        print('* Pixels: %d bytes' % size_pixels)

        size_read = stream.bytes_read
        print('Decompressed %d bytes.' % size_read)
        print('Image dimensions: %d x %dpx' % (width, height))
        image.save(out_file_name)
        size_raw = raw_size(width, height)
        print('RAW size: %d bytes' % size_raw)
        space_expand = 100 * float(size_raw / size_read - 1)
        print('Memory expanded by %0.2f' % (space_expand), '%.')

# estimate number of bytes to be compressed
def compressed_size(counts, codes):
    header_size = 2 * 16 # height and width as 16-bit values
    tree_size = len(counts) * (1 + 8) # Leafs: 1 bit flag + 8 bit symbol each
    tree_size += len(counts) - 1 # Nodes: 1 bit flag each
    if tree_size % 8 > 0: # padding to next full byte
        tree_size += 8 - (tree_size % 8)
    # sum for each symbol of count * code length
    pixels_size = sum([count * len(codes[symbol]) for symbol, count in counts])
    if pixels_size % 8 > 0: # padding to next full byte
        pixels_size += 8 - (pixels_size % 8)
    num_bytes = (header_size + tree_size + pixels_size) / 8 # convert bits to bytes
    return num_bytes

# calculate the number of bytes of the image
def raw_size(width, height):
    header_size = 2 * 16 # height and width as 16 bit values
    pixels_size = 3 * 8 * width * height # 3 channels, 8 bits per channel
    num_bytes = (header_size + pixels_size) / 8 # convert bits to bytes
    return num_bytes

# check if two image files are equivalent
def images_equal(file_name_a, file_name_b):
    image_a = Image.open(file_name_a)
    image_b = Image.open(file_name_b)
    diff = ImageChops.difference(image_a, image_b)
    return diff.getbbox() is None

def main():
    if len(sys.argv) < 4:
        print("Error: Insufficient arguments.")
        display_usage()
        sys.exit(1)

    operation = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    squishy = Squishy()

    if operation == "compress":
        squishy.compress(input_file, output_file)
    elif operation == "decompress":
        squishy.decompress(input_file, output_file)
    else:
        print(f"Error: Invalid operation '{operation}'.")
        display_usage()
        sys.exit(1)

def display_usage():
    print("Usage:")
    print("  To compress:   python3 squishy.py compress <inputImageFile.png> <outputBinaryFile.bin>")
    print("  To decompress: python3 squishy.py decompress <inputBinaryFile.bin> <outputImageFile.png>")

if __name__ == "__main__":
    main()