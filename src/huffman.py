import heapq
from collections import Counter, defaultdict

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_table(data):
    # Count frequency of each byte in the binary data
    return Counter(data)

def build_huffman_tree(freq_table):
    heap = [HuffmanNode(char, freq) for char, freq in freq_table.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

def generate_codes(root, code="", code_dict=None):
    if code_dict is None:
        code_dict = {}
    if root:
        if root.char is not None:
            code_dict[root.char] = code
        generate_codes(root.left, code + "0", code_dict)
        generate_codes(root.right, code + "1", code_dict)
    return code_dict

def encode(data, code_dict):
    # Encode binary data using the Huffman codes
    return ''.join(code_dict[char] for char in data)

def decode(encoded_data, root):
    decoded_data = []
    current = root
    for bit in encoded_data:
        if bit == '0':
            current = current.left
        else:
            current = current.right
        if current.char is not None:
            decoded_data.append(current.char)
            current = root
    return bytes(decoded_data)  # Return bytes for binary data

def build_frequency_table(data):
    return Counter(data)

def build_huffman_tree(freq_table):
    if not freq_table:
        raise ValueError("Error: The file appears to be empty or invalid for Huffman Encoding.")

    heap = [HuffmanNode(char, freq) for char, freq in freq_table.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0] if heap else None

def generate_codes(root, code="", code_dict=None):
    if code_dict is None:
        code_dict = {}
    if root:
        if root.char is not None:
            code_dict[root.char] = code
        generate_codes(root.left, code + "0", code_dict)
        generate_codes(root.right, code + "1", code_dict)
    return code_dict

def encode(data, code_dict):
    if not data:
        return ""  # Return empty string for empty files
    return ''.join(code_dict[char] for char in data)

def decode(encoded_data, root):
    if not root:
        return b""  # Return empty bytes for invalid tree
    decoded_data = []
    current = root
    for bit in encoded_data:
        if bit == '0':
            current = current.left
        else:
            current = current.right
        if current.char is not None:
            decoded_data.append(current.char)
            current = root
    return bytes(decoded_data)