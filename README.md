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
