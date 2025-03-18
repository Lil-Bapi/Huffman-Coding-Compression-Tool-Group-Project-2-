import os
import sys
from bitarray import bitarray

def read_huffman_codes(code_file_path):
    """Read Huffman codes from the provided text file. 
      
       Arguments: 
            code_file_path (str): The path to the file containing the Huffman codes.
        
        Returns: 
            a dictionary where keys are huffman codes, or strings, and the values are
            corresponding characters (strings).
            In case that an error occurs while reading the file, it will return error.

        File Format: each line in the file should follow the format:
           'char' : code
    """
    codes = {}
    try:
        with open(code_file_path, 'r') as file:
            for line in file:
                if not line.strip():
                    continue
                # Split character and code (expected format "'x': 30")    
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
                # Add to the dictionary (code -> char)
                codes[code] = char
        return codes
    except Exception as e:
        print(f"Error reading code file: {e}")
        return None

def decode_from_huffman_codes(encoded_bits, code_map):
    """Decode a bit string using the Huffman code map
       
       Arguments:
            encoded_bits : is an encoded string of bits to be decoded
            code_map (dict): A dictionary where keys  are Huffman codes
            and values are characters.

        Returns:
             str : decoded text
    """
    decoded_text = ""
    current_code = ""
    
    # Iterates through the encoded bits to form valid codes
    for bit in encoded_bits:
        current_code += bit
        if current_code in code_map:
            # Map the code to the corresponding character
            decoded_text += code_map[current_code]
            current_code = ""
            
    return decoded_text

def read_original_text(file_path):
    """Read the original text file .

        Arguments:
            file_path (str): The path to the file containing the original text.

        Returns:
           None if an error occurs while the file is being read.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading original file: {e}")
        return None

def encode_with_huffman(text, codes_reverse):
    """Encode text using the provided Huffman codes
       
        Args:
            text (string) : The original text to be encoded
            codes_reverse (dictionary) : Dictionary where keys are Huffman codes
            values are characters.

        Returns:
            string : The encoded binary string    
    """
    # Reverse the code map for encoding
    codes = {v: k for k, v in codes_reverse.items()}
    
    encoded = ""
    # This encodes each character in the text
    for char in text:
        if char in codes:
            encoded += codes[char]
        else:
            print(f"Warning: Character '{char}' not found in Huffman codes")
     
    return encoded

def main():
    """ 
        Main function :
            * Reads Huffman codes and original text from its corresponding files
            * Encodes original text using HUffman codes
            * Decodes the encoded text back to the original
            * For accuracy, it compares the original and decoded text
    """
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