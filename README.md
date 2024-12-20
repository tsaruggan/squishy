# Squishy
Squishy uses a [Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding) algorithm and the [Pillow](https://pillow.readthedocs.io/en/stable/) library to compress (and decompress) image files into a binary format. The technique works by creating a binary tree of nodes based on the colour information of pixels and how frequently they appear in the image. A binary encoding is efficiently generated for each unique pixel so the image can be expressed using fewer bits. Information about how to restore the tree is also included in the header of the binary file so the image can be reconstructed without losing any detail.

> C++ implementation & speed comparison [here](https://github.com/tsaruggan/squishy-cpp)

### Demo:
For example, we have this image we want to compress:

<img src="https://github.com/tsaruggan/squishy/blob/main/demo/octopus.png" alt="octopus" width="400px">

&nbsp;

We write the following code to compress it into a .bin file:
```Python
from squishy import *

squishy = Squishy()
squishy.compress('octopus.png')
```
```
Compressing "octopus.png" -> "octopus.bin"
Image dimensions: 1536 x 1024px
RAW size: 4718596 bytes
Compressed size: 3943812 bytes
Writing...
* Header: 4 bytes
* Tree: 320 bytes
* Pixels: 3943488 bytes
Compressed 3943812 bytes.
Memory reduced by 16.42 %.
```

The resulting binary code looks something like this:
```
  Offset: 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 	
00000000: 04 00 06 00 00 59 A0 17 02 81 51 5A CF C7 DD F4    .....Y....QZOG]t
00000010: F9 A6 F7 82 D3 15 18 3B 13 0F 14 27 B1 3B 04 80    y&w.S..;...'1;..
00000020: 92 82 0F 89 9D D9 30 97 39 30 94 11 BA B1 67 29    .....Y0.90..:1g)
00000030: 90 93 E5 F1 84 5B C0 66 F3 34 A3 2D 9A AE 63 44    ..eq.[@fs4#-..cD
00000040: 2A 9C 7B F3 0C BE 7A A0 9B 5E D2 26 48 3E 19 D6    *.{s.>z..^R&H>.V
00000050: 73 41 8A AC 92 72 C3 32 96 8A 6A FC 3D DA 18 62    sA.,.rC2..j|=Z.b
00000060: 16 CF E8 E4 72 40 15 29 7E 00 5D AC 6C 2E 30 34    .Ohdr@.)~.],l.04
...
```
Later, we can decompress the binary code and confirm the images are identical:
```Python
squishy.decompress('octopus.bin', 'octopus_new.png')
print('Images equal = %s' % images_equal('octopus.png', 'octopus_new.png'))
```
```
Decompressing "octopus.bin" -> "octopus_new.png"
Reading...
* Header: 4 bytes
* Tree: 320 bytes
* Pixels: 3943488 bytes
Decompressed 3943812 bytes.
Image dimensions: 1536 x 1024px
RAW size: 4718596 bytes
Memory expanded by 19.65 %.
Images equal = True
```
