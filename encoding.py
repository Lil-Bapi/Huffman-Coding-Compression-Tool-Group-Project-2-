import heapq
import os
import sys
from collections import Counter, namedtuple
from bitarray import bitarray

#Im lazy
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

# Build Huffman Tree
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

# Generate Huffman Codes
def generate_codes(node, prefix="", code_dict=None):
    if code_dict is None:
        code_dict = {}
    if node:
        if node.char is not None:
            code_dict[node.char] = prefix
        generate_codes(node.left, prefix + "0", code_dict)
        generate_codes(node.right, prefix + "1", code_dict)
    return code_dict

# Encode text using Huffman Codes
def encode_text(text, codes):
    return bitarray("".join(codes[char] for char in text))

# Save compressed data to a binary file
def save_compressed_file(text, output_path):
    huffman_tree = build_huffman_tree(text)
    codes = generate_codes(huffman_tree)

    encoded_text = encode_text(text, codes)
    with open(output_path, "wb") as file:
        file.write(len(text).to_bytes(4, "big"))  # Store original length
        file.write(encoded_text.tobytes())       # Store compressed data

    return output_path

# Decode Huffman encoded binary data
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

# Read compressed file and decompress it
def decompress_file(input_path, huffman_tree):
    with open(input_path, "rb") as file:
        original_length = int.from_bytes(file.read(4), "big")  # Read original length
        encoded_data = file.read()  # Read compressed data

    decoded_text = decode_text(encoded_data, huffman_tree, original_length)

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "decompressed.txt")
    with open(output_path, "w") as file:
        file.write(decoded_text)

    return decoded_text

# Save Huffman codes to a text file
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

#get huffman codes from text
def getHFFMCodes(text):

    #im really lazy
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


# Display Huffman codes from a text file
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
