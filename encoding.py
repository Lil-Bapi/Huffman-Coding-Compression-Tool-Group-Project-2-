import heapq
import os
import sys
from collections import Counter, namedtuple
from bitarray import bitarray


global compression_percentage
compression_percentage = 0
global comrpessed_bytes
compressed_bytes = 0
global original_size
original_size = 0



# Huffman Tree Node
class Node(namedtuple("Node", ["char", "freq", "left", "right"])):
    def __lt__(self, other):
        return self.freq < other.freq

"""
     Builds a Huffman tree based on the frequency of characters in the input text.
     This function creates a priority queue of nodes based on character frequencies.
     A binary tree where each leaf node represents a character. The inner nodes will
     represent the mereged character frequencies.

     Args: 
        text (string) : This is the input text from which frequencies are calculated. 
                        This text can be any character, for insatance (letters, numbers, spaces, ect.)
    Returns:
        Node: The node to be returned is the root node of our Huffman tree. This node will contain
        the "merged frequency" of all the characters in the input text.This tree allows you to assign 
        shorter codes to more frequent characters, which is the essence of Huffman coding.
"""
def build_huffman_tree(text):
    frequency = Counter(text)
    priority_queue = [Node(char, freq, None, None) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = Node(None, left.freq + right.freq, left, right)
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]  # Root of Huffman Tree

"""
    Generates Huffman codes for each characters by recursively traversing the Huffman tree.

    This function assigns a binary string to each character position in Huffman tree. Left 
    traversal adds a '0' and right traversal adds a '1'. This results in binary strings or the
    codes themselves, which represent the compressed version of the input text.

    Args:
        node : The current node in the Huffman tree. This node may be a character (leaf node), or a 
               combined frequency (internal node)

        prefix (string) : By default this is an empty string. This is an accumulated binary string representing 
                          the path to the current code. 

        code_dict (dictionary) : A dictionary to store the Huffman codes for each character. Empty dictionary
                                by default.
    Returns: 
        dict: A dictionary where keys are characters and values are corresponding Huffman codes as binary strings.
"""
def generate_codes(node, prefix="", code_dict=None):
    if code_dict is None:
        code_dict = {}
    if node:
        if node.char is not None:
        # adds an entry to the code_dict dictionary, key being char
        # the value is the Huffman code (prefix) which is assigned to that character
            code_dict[node.char] = prefix
        generate_codes(node.left, prefix + "0", code_dict)
        generate_codes(node.right, prefix + "1", code_dict)
    return code_dict

"""
 Encodes the input text into a compressed binary format based on provided Huffman codes.

 This function will iterate over each character in the input text, and retrieve the Huffman
 code from the provided dictionary. It will append the binary string to form the encoded text.
  The result is stored as a bitarray to perform bit-level operations on it.

  Args:
      text (string): The input text to be encoded. Each character in the text must have 
                an entry in the 'codes' dictionary.
      codes (dictionary): A dictionary mapping each character to its corresponding Huffman code.

  Returns:
       bitarray: A bitarray representing the compressed binary encoding of the input text

"""
def encode_text(text, codes):
    return bitarray("".join(codes[char] for char in text))

"""
 Compresses the input text using Huffman coding and saves the compressed data to a file.

 This function builds a Huffman tree for the input text, it generates the Huffman codes, it encodes the 
 text using the codes, then writes the resulting compressed data to a binary file. The length
 of the original text is also stored for later decompression.

 Args:
    text (string): The text to be compressed.
    output_path (string): The file path where the compressed binary data will be saved.

 Returns:
    output_path (string): The path to the saved compressed binary file containing the encoded text 
         and the original text length.
"""

def save_compressed_file(text, output_path):
    huffman_tree = build_huffman_tree(text)
    codes = generate_codes(huffman_tree)

    encoded_text = encode_text(text, codes)
    with open(output_path, "wb") as file:
        file.write(len(text).to_bytes(4, "big"))  # Store original length
        file.write(encoded_text.tobytes())       # Store compressed data

    return output_path

"""
    Decodes the given binary data back to the original text using the given Huffman tree.

    This function goes through the copmressed binary data , following the paths in the Huffman 
    tree (left for '0' and right for '1') to decode each character. The decoding stops once the
    original length of the text is reached. 

    Args:
         encoded_text (bytes): The binary-encoded data to be decoded, typically read 
                           from a compressed file.

         huffman_tree (Node): The root of the Huffman tree used for decoding.

         original_length (int): The original length of the text before it was compressed.

    Returns:
         (string): The decoded text, restored from the compressed binary data.

"""
def decode_text(encoded_text, huffman_tree, original_length):
    decoded_text = []
    node = huffman_tree
    bit_string = bitarray()
    bit_string.frombytes(encoded_text)

    for bit in bit_string:
        node = node.left if bit == 0 else node.right
        if node.char is not None:
            decoded_text.append(node.char)
            node = huffman_tree
        if len(decoded_text) == original_length:
            break

    return "".join(decoded_text)
"""
 Decompresses the binary data from the specified file and saves the decompressed text.
 This function reads a compressed binary file, decodes the binary data using the 
 provided Huffman tree, and writes the resulting decoded text to a new file.

 Args:
    input_path (string): The path to the compressed binary file to be decompressed.

    huffman_tree (node): The root of the Huffman tree used to decode the data.

 Returns:
    decoded_text (string): The decompressed text that was restored from the binary file
"""
def decompress_file(input_path, huffman_tree):
    with open(input_path, "rb") as file:
        original_length = int.from_bytes(file.read(4), "big")  # Read original length
        encoded_data = file.read()  # Read compressed data

    decoded_text = decode_text(encoded_data, huffman_tree, original_length)

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "decompressed.txt")
    with open(output_path, "w") as file:
        file.write(decoded_text)

    return decoded_text

"""
    Saves the generated Huffman codes to a textfile.

    This function creates a human-readable file where each linemaps a character  to
    its corrresponding Huffman code.

    Args:
        codes (dictionary): A dictionary mapping characters to their corresponding Huffman codes.

    Returns:
         output_path (string) : The path to the file where the Huffman codes are saved.
"""
def save_huffman_codes_to_file(codes):
    # Create output filename based on input filename
    #base_name = os.path.basename(file_path)
    #name_without_ext = os.path.splitext(base_name)[0]
    #output_file = f"{name_without_ext}_huffman_codes.txt"
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "huffmanCodes.txt")
    
    with open(output_path, 'w') as out_file:
        
        # Sort by character for better readability
        for char, code in sorted(codes.items()):
            # Handle special characters for display
            if char == ' ':
                display_char = "SPACE"
            elif char == '\n':
                display_char = "NEWLINE"
            elif char == '\t':
                display_char = "TAB"
            elif char == '\r':
                display_char = "RETURN"
            else:
                display_char = char
            out_file.write(f"'{display_char}': {code}\n")
    
    return output_path

"""
 This function gets huffman codes from text, it calculates the necessary
 compression information and saves both the Huffman codes and compressed data 
 to files.

    Args:
       text (string): The input text to be compressed.

  Returns:
       output_path(string): The path to the saved compressed binary file.

"""
def getHFFMCodes(text):

    
    global compression_percentage
    global compressed_bytes
    global original_size


    # Original file size (in bytes)
    original_size = len(text.encode('utf-8'))
    
    # Build huffman tree and generate codes
    huffman_tree = build_huffman_tree(text)
    codes = generate_codes(huffman_tree)
    
    # Calculate compressed size (in bits, then convert to bytes)
    compressed_bits = sum(len(codes[char]) for char in text)
    compressed_bytes = (compressed_bits + 7) // 8  # Round up to nearest byte
    
    # Calculate compression percentage
    if original_size > 0:
        compression_percentage = (1 - (compressed_bytes / original_size)) * 100
    else:
        compression_percentage = 0
    
    #print(f"Huffman codes for '{file_path}':")
    print(f"Original size: {original_size} bytes")
    print(f"Compressed size: {compressed_bytes} bytes")
    print(f"Compression: {compression_percentage:.2f}%")
    print("-" * 30)
    
    # Sort by character for better readability
    for char, code in sorted(codes.items()):
        # Handle special characters for display
        if char == ' ':
            display_char = "SPACE"
        elif char == '\n':
            display_char = "NEWLINE"
        elif char == '\t':
            display_char = "TAB"
        elif char == '\r':
            display_char = "RETURN"
        else:
            display_char = char
        print(f"'{display_char}': {code}")
    
    # Save the Huffman codes to a file
    output_path = save_huffman_codes_to_file(codes)
    print(f"\nHuffman codes saved to: {output_path}")

    
    output_path = save_compressed_file(text, os.path.join(os.path.dirname(os.path.abspath(__file__)), "compressedBinary.txt"))
    print(f"\nHuffman binary was saved to {output_path}")

    return output_path


"""
Reads a text file , generates Huffman codes for the content, and outputs the 
codes and compression "statistics" to the console.

"""
def display_huffman_codes_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    if not text:
        print("Error: File is empty.")
        return
    
    getHFFMCodes(text)


# Example Usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python huff.py <text_file.txt>")
        print("Please provide a .txt file path as an argument")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if file_path.endswith('.txt'):
        display_huffman_codes_from_file(file_path)
    else:
        print("Error: Please provide a .txt file")
        print("Usage: python huff.py <text_file.txt>")
        sys.exit(1)
