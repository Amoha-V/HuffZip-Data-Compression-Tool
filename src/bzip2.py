def burrows_wheeler_transform(data):
    # Generate all rotations of the input data
    rotations = [data[i:] + data[:i] for i in range(len(data))]
    # Sort the rotations lexicographically
    rotations.sort()
    # Return the last column of the sorted rotations
    return ''.join(rotation[-1] for rotation in rotations)

def move_to_front_encode(data):
    # Initialize the MTF alphabet
    alphabet = list(set(data))
    alphabet.sort()
    encoded_data = []
    for char in data:
        index = alphabet.index(char)
        encoded_data.append(index)
        # Move the character to the front of the alphabet
        alphabet.pop(index)
        alphabet.insert(0, char)
    return encoded_data

def run_length_encode(data):
    encoded_data = []
    count = 1
    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            count += 1
        else:
            encoded_data.append((data[i - 1], count))
            count = 1
    encoded_data.append((data[-1], count))
    return encoded_data

def simplified_bzip2_compress(data):
    # Apply BWT
    bwt_data = burrows_wheeler_transform(data)
    # Apply MTF encoding
    mtf_data = move_to_front_encode(bwt_data)
    # Apply RLE
    rle_data = run_length_encode(mtf_data)
    return rle_data

def simplified_bzip2_decompress(rle_data):
    # Reverse RLE
    mtf_data = []
    for char, count in rle_data:
        mtf_data.extend([char] * count)
    # Reverse MTF encoding
    alphabet = list(set(mtf_data))
    alphabet.sort()
    bwt_data = []
    for index in mtf_data:
        char = alphabet[index]
        bwt_data.append(char)
        alphabet.pop(index)
        alphabet.insert(0, char)
    # Reverse BWT
    # (This step is complex and omitted for simplicity)
    return ''.join(bwt_data)