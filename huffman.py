from collections import Counter

# count the frequency of each channel intensity of pixels in the image
def count_symbols(image):
    pixels = image.getdata() # get the RGB values for each pixel
    intensities = get_intensities(pixels) # get list of intensity values in RGB channels
    frequencies = count_frequencies(intensities) # count frequency of each intensity value
    return frequencies

# create a iterable of (flattened) intensity values (R G B)
def get_intensities(pixels):
    for pixel in pixels:
        for channel in pixel:
            yield channel

# count how frequent each intensity value appears
def count_frequencies(intensities):
    frequencies = Counter(intensities).items()
    return sorted(frequencies, key=lambda x:x[::-1])

# generate an optimal huffman tree
def build_tree(counts) :
    nodes = [entry[::-1] for entry in counts] # reverse each (symbol,count) tuple
    while len(nodes) > 1 :
        least_two = tuple(nodes[0:2]) # get the 2 nodes to combine
        sum_freq = least_two[0][0] + least_two[1][0]
        branch = [(sum_freq, least_two)] # combine least two nodes
        nodes = nodes[2:] + branch # add combined node (branch) back into nodes
        nodes.sort(key=lambda t: t[0]) # sort nodes again
    tree = trim_tree(nodes[0]) # remove frequency values from tree
    return tree 

# remove the frequency values from each node
def trim_tree(tree) :
    t = tree[1] # ignore freq count in [0]
    if type(t) is tuple: # if branch
        trim_left = trim_tree(t[0]) # trim left branch
        trim_right = trim_tree(t[1]) # trim right branch
        return (trim_left, trim_right) # recombine tree
    return t # else, return leaf

# assign a unique binary pattern to each leaf in the tree
def assign_binary_patterns(tree):
    codes = {}
    pattern = []
    assign_binary_patterns_rec(codes, tree, pattern)
    return codes

def assign_binary_patterns_rec(codes, node, pattern):
    if type(node) == tuple: # if branch,
        assign_binary_patterns_rec(codes, node[0], pattern + [0]) # assign pattern to left branch
        assign_binary_patterns_rec(codes, node[1], pattern + [1]) # assign pattern to left branch
    else:
        codes[node] = pattern # else, assign pattern to leaf

# convert integer into a binary pattern
def int_to_binary(n):
    if (n <= 1):
        return [n]
    else:
        return int_to_binary(n >> 1) + [n & 1]

# convert binary pattern into an integer
def binary_to_int(pattern):
    result = 0
    for bit in pattern:
        result = (result << 1) | bit
    return result

# zero extend binary pattern (to allow fixed length encoding)
def pad_bits(pattern, num):
    assert(num >= len(pattern))
    return ([0] * (num - len(pattern)) + pattern)