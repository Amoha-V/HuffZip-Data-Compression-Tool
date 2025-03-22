# HuffZip: Advanced Data Compression Tool

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://huffzip-data-compression-tool-6qxfzdfd9n2fu8trvblnpr.streamlit.app/)

HuffZip is a powerful data compression tool that uses state-of-the-art algorithms to efficiently compress your files. It provides an intuitive web interface built with Streamlit that allows users to compress and decompress files with just a few clicks.

![HuffZip Screenshot](https://raw.githubusercontent.com/Amoha-V/HuffZip-Data-Compression-Tool/master/data/screenshot.png)

## Inspiration

I got inspired from the lossless compression techniques, particularly the Huffman compression algorithm that I learned in my Data Structures and Algorithms course. For anyone interested in understanding how this works, there are great explanations of the Huffman coding algorithm available at:
- https://en.wikipedia.org/wiki/Huffman_coding
- https://www.mathworks.com/help/comm/ug/huffman-coding.html

The elegance of this algorithm in assigning variable-length codes based on character frequency really fascinated me, which led to the development of HuffZip as a practical implementation.

## Live Demo
Try the live application: [HuffZip Data Compression Tool](https://huffzip-data-compression-tool-6qxfzdfd9n2fu8trvblnpr.streamlit.app/)

## Features

- **Multiple Compression Algorithms**:
  - Huffman Encoding for optimal text compression
  - Bzip2 Compression for complex data types
  
- **User-Friendly Interface**:
  - Clean, intuitive design
  - Real-time compression progress
  - Immediate result visualization
  
- **File Support**:
  - Text files (.txt)
  - Image files (.png, .jpg, .jpeg)
  
- **Comprehensive Analytics**:
  - Original file size
  - Compressed file size
  - Space saved percentage
  
- **Interactive Workflow**:
  - Upload → Compress → Download → Decompress
  - Preview of original and decompressed content

## How It Works

### Huffman Encoding
Huffman coding is a lossless data compression algorithm that assigns variable-length codes to input characters, with shorter codes for more frequent characters:

1. Builds a frequency table for all characters in the input
2. Constructs a Huffman tree based on character frequencies
3. Generates optimal prefix codes for each character
4. Encodes the data using the generated codes
5. Stores both the compressed data and the Huffman tree for decompression

### Bzip2 Compression
Bzip2 is a high-quality compression algorithm that combines several techniques:

1. Applies the Burrows-Wheeler transform to rearrange character strings
2. Uses Move-To-Front transform and Huffman coding
3. Provides excellent compression ratio for most file types
4. Works well with both text and binary data

## Project Structure
```
├── data/                  # Directory for storing temporary files
├── models/                # Store for compression models
├── src/                   # Source code
│   ├── huffman.py         # Huffman encoding implementation
│   ├── bzip2.py           # Simplified bzip2 implementation
│   └── utils.py           # Utility functions
├── app.py                 # Main Streamlit application
├── requirements.txt       # Dependencies
├── README.md              # Documentation
└── LICENSE                # MIT License
```

## Installation

### Prerequisites
- Python 3.7+
- pip

### Setup
```bash
# Clone the repository
git clone https://github.com/Amoha-V/HuffZip-Data-Compression-Tool.git
cd HuffZip-Data-Compression-Tool

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Usage

1. **Launch the application**:
   - Run `streamlit run app.py` or visit the [live demo](https://huffzip-data-compression-tool-6qxfzdfd9n2fu8trvblnpr.streamlit.app/)

2. **Select compression method**:
   - Choose between Huffman Encoding or Bzip2 Compression

3. **Upload a file**:
   - Drag and drop or browse for a file (.txt, .png, .jpg, .jpeg)

4. **Compress the file**:
   - Click "Compress File" and wait for the process to complete

5. **View the results**:
   - See original size, compressed size, and space saved

6. **Download the compressed file**:
   - Click "Download Compressed File"

7. **Decompress (optional)**:
   - Click "Decompress File" to restore the original file

## Implementation Details

### Huffman Encoding
```python
def build_frequency_table(data):
    """Builds a frequency table from input data"""
    freq = {}
    for byte in data:
        if byte in freq:
            freq[byte] += 1
        else:
            freq[byte] = 1
    return freq

def build_huffman_tree(freq):
    """Builds a Huffman tree from a frequency table"""
    # Implementation details...
```

### Compression Metrics
The application calculates the following metrics:
- Original file size in bytes
- Compressed file size in bytes
- Space saved as a percentage: `(1 - (compressed_size / original_size)) * 100`

## Performance Analysis

HuffZip's performance varies depending on the type of data being compressed:

| File Type | Size      | Huffman Compression | Bzip2 Compression |
|-----------|-----------|---------------------|-------------------|
| Text      | Small     | 40-60% reduction    | 60-80% reduction  |
| Text      | Large     | 30-50% reduction    | 70-85% reduction  |
| Images    | PNG/JPEG  | 5-15% reduction     | 10-20% reduction  |

*Note: Images are already compressed, so further compression yields less dramatic results.*

## Future Improvements

- Add support for more file types
- Implement additional compression algorithms (LZ77, LZMA)
- Batch processing of multiple files
- Progressive compression with quality options for images
- Command-line interface for automation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch 
3. Commit your changes 
4. Push to the branch 
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Inspired by classic compression techniques and modern implementations
- Special thanks to the Data Structures and Algorithms community for their educational resources on compression algorithms
