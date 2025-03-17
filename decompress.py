import os
import sys
from bitarray import bitarray

def read_huffman_codes(code_file_path):
    """Read Huffman codes from the provided text file"""
    codes = {}
    try:
        with open(code_file_path, 'r') as file:
            for line in file:
                if not line.strip():
                    continue
                    
                parts = line.strip().split(': ')
                if len(parts) != 2:
                    continue
                    
                char_str, code = parts
                # Handle special character representations
                if char_str == "'SPACE'":
                    char = ' '
                elif char_str == "'NEWLINE'":
                    char = '\n'
                elif char_str == "'TAB'":
                    char = '\t'
                elif char_str == "'RETURN'":
                    char = '\r'
                else:
                    # Extract character from representation like "'a'"
                    char = char_str.strip("'")
                
                codes[code] = char
        return codes
    except Exception as e:
        print(f"Error reading code file: {e}")
        return None

def decode_from_huffman_codes(encoded_bits, code_map):
    """Decode a bit string using the Huffman code map"""
    decoded_text = ""
    current_code = ""
    
    for bit in encoded_bits:
        current_code += bit
        if current_code in code_map:
            decoded_text += code_map[current_code]
            current_code = ""
            
    return decoded_text

def read_original_text(file_path):
    """Read the original text file"""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading original file: {e}")
        return None

def encode_with_huffman(text, codes_reverse):
    """Encode text using the provided Huffman codes"""
    # Reverse the code map for encoding
    codes = {v: k for k, v in codes_reverse.items()}
    
    encoded = ""
    for char in text:
        if char in codes:
            encoded += codes[char]
        else:
            print(f"Warning: Character '{char}' not found in Huffman codes")
    
    return encoded

def main():
    # Paths
    huffman_codes_path = os.path.join(os.path.dirname(__file__), "test_huffman_codes.txt")
    original_text_path = os.path.join(os.path.dirname(__file__), "test.txt")
    
    # Read the Huffman codes (code -> character)
    codes = read_huffman_codes(huffman_codes_path)
    if not codes:
        print("Failed to read Huffman codes")
        return
    
    # Read original text
    original_text = read_original_text(original_text_path)
    if original_text is None:
        print("Failed to read original text")
        return
    
    # Encode the original text using the codes (to simulate having encoded data)
    encoded_bits = encode_with_huffman(original_text, codes)
    
    # Decode the encoded text
    decoded_text = decode_from_huffman_codes(encoded_bits, codes)
    
    # Print results
    print("Original Text:")
    print(f"'{original_text}'")
    print("\nDecoded Text:")
    print(f"'{decoded_text}'")
    
    # Verify if they match
    if original_text == decoded_text:
        print("\n✓ SUCCESS: Decoded text matches the original!")
    else:
        print("\n✗ ERROR: Decoded text does not match the original.")
        print("Differences:")
        for i, (orig, dec) in enumerate(zip(original_text, decoded_text)):
            if orig != dec:
                print(f"Position {i}: Original '{orig}' vs Decoded '{dec}'")

if __name__ == "__main__":
    main()