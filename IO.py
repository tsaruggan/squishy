from huffman import *

# API to read single bit streams from a file
class Input: 
    def __init__(self, file_name): 
        self.file_name = file_name
        self.file = open(self.file_name, 'rb') 
        self.bytes_read = 0
        self.buffer = []

    # read a single bit
    def read_bit(self):
        return self.read_bits(1)[0]

    # load bytes to buffer until bit count is reached
    def read_bits(self, count):
        while len(self.buffer) < count:
            self._load_byte()
        result = self.buffer[:count]
        self.buffer[:] = self.buffer[count:]
        return result

    # clear the buffer (assume only zeros)
    def flush(self):
        assert(not any(self.buffer)) # make sure no ones
        self.buffer[:] = []

    # load byte from buffer to input file
    def _load_byte(self):
        value = ord(self.file.read(1)) # get byte from file
        self.buffer += pad_bits(int_to_binary(value), 8) # convert byte to integer
        self.bytes_read += 1

    # close the file
    def close(self): 
        self.file.close()

# API to write single bit streams to a file
class Output: 
    def __init__(self, file_name): 
        self.file_name = file_name
        self.file = open(self.file_name, 'wb') 
        self.bytes_written = 0
        self.buffer = []

    # write a single bit
    def write_bit(self, value):
        self.write_bits([value])

    # add bits to buffer; when buffer contains 8+ bits, save byte
    def write_bits(self, values):
        self.buffer += values
        while len(self.buffer) >= 8:
            self._save_byte()        

    # add trailing zeros to complete a byte and write it
    def flush(self):
        if len(self.buffer) > 0:
            self.buffer += [0] * (8 - len(self.buffer))
            self._save_byte()
        assert(len(self.buffer) == 0)

    # save byte from buffer to output file
    def _save_byte(self):
        byte = self.buffer[:8] # get byte from front of buffer
        byte_value = binary_to_int(byte) # convert byte to integer
        self.file.write(bytes([byte_value])) # write byte to output file
        self.buffer[:] = self.buffer[8:] # remove byte from buffer
        self.bytes_written += 1
        
    # flush the buffer and close the file
    def close(self): 
        self.flush()
        self.file.close()    