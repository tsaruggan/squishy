# Squishy
Squishy uses a [Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding) algorithm and the [Pillow](https://pillow.readthedocs.io/en/stable/) library to compress (and decompress) image files into a binary format. The technique works by creating a binary tree of nodes based on the colour information of pixels and how frequently they appear in the image. A binary encoding is efficiently generated for each unique pixel so the image can be expressed using fewer bits. Information about how to restore the tree is also included in the header of the binary file so the image can be reconstructed without losing any detail.

### Demo:
For example, we have this image we want to compress:

<img src="https://github.com/tsaruggan/squishy/blob/main/demo/octopus.jpg" alt="octopus" width="400px">
