# Squishy
Squishy uses a [Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding) algorithm and the [Pillow](https://pillow.readthedocs.io/en/stable/) library to compress (and decompress) image files into a binary format. The technique works by creating a binary tree of nodes based on the colour information of pixels and how frequently they appear in the image. A binary encoding is efficiently generated for each unique pixel so the image can be expressed using fewer bits. Information about how to restore the tree is also included in the header of the binary file so the image can be reconstructed without losing any detail.

### Demo:
For example, we have this image we want to compress:

<img src="https://github.com/tsaruggan/squishy/blob/main/demo/octopus.jpg" alt="octopus" width="400px">

&nbsp;

We write the following code to compress it into a .bin file:
```Python
from squishy import *

squishy = Squishy()
squishy.compress('octopus.jpg')
```
```
Compressing "octopus.jpg" -> "octopus.bin"
Image shape: (height=1024, width=1536)
RAW image size: 4718596 bytes
Estimated size: 3944984 bytes
Writing...
* Header offset: 0
* Tree offset: 4
* Pixel offset: 324
Wrote 3944984 bytes.
Compression ratio: 1.20
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
print('Images equal = %s' % images_equal('octopus.jpg', 'octopus_new.png'))
```
```
Decompressing "octopus.bin" -> "octopus_new.png"
Reading...
* Header offset: 0
* Tree offset: 4
* Pixel offset: 324
Read 3944984 bytes.
Image size: (height=1024, width=1536)
Images equal = True
```
