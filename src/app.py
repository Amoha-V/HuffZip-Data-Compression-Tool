import streamlit as st
import os
import pickle
import bz2
from huffman import *
from bzip2 import simplified_bzip2_compress, simplified_bzip2_decompress

# Ensure the 'data' directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Set page title and favicon
st.set_page_config(
    page_title="HuffZip Data Compression Tool",
    page_icon="📂",  # Favicon (you can replace this with a custom favicon)
    layout="centered",
)

# Custom CSS styling for a professional and visually appealing look
st.markdown(
    """
    <style>
        /* Main background gradient */
        .main {
            background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
            color: #333333;
            padding: 20px;
        }
        /* Sidebar styling */
        .sidebar .sidebar-content {
            background: #ffffff;
            border-right: 1px solid #e0e0e0;
            padding: 20px;
        }
        /* File uploader styling */
        .stFileUploader > div {
            border: 2px dashed #4a90e2;
            border-radius: 10px;
            padding: 20px;
            background-color: #f9f9f9;
            text-align: center;
        }
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #4a90e2, #357abd);
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            border: none;
            font-size: 16px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        /* Header styling */
        h1 {
            color: #4a90e2;
            font-size: 36px;
            font-weight: bold;
            text-align: center;
        }
        h2 {
            color: #4a90e2;
            font-size: 24px;
            font-weight: bold;
        }
        /* Card styling */
        .card {
            background: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin: 10px 0;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        /* Footer styling */
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #666666;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# App title and caption
st.title("Data Compression Tool")
st.markdown("Compress and decompress your files using Huffman Encoding or Bzip2 Compression.")

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    compression_method = st.selectbox(
        "Choose Compression Method",
        ["Huffman Encoding", "Bzip2 Compression"],
        index=0,
    )
    st.divider()
    st.markdown("### Supported File Types")
    st.markdown(
        """
        - Text Files (.txt)
        - Image Files (.png, .jpg, .jpeg)
        """
    )
    st.divider()
    st.markdown("Built with [Streamlit](https://streamlit.io/)")

# File upload
uploaded_file = st.file_uploader("Upload a file to compress", type=["txt", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Save the uploaded file
    filepath = os.path.join("data", uploaded_file.name)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Read the uploaded file
    with open(filepath, "rb") as f:  # Read in binary mode
        data = f.read()

    # Check if the file is an image
    is_image = uploaded_file.type.startswith("image")

    # Compress the file based on the selected method
    if compression_method == "Huffman Encoding":
        # Build Huffman Tree and Trie
        freq_table = build_frequency_table(data)
        huffman_tree = build_huffman_tree(freq_table)
        huffman_codes = generate_codes(huffman_tree)

        # Compress data
        compressed_data = encode(data, huffman_codes)
        compressed_filepath = os.path.join("data", "compressed.bin")
        with open(compressed_filepath, "wb") as f:
            f.write(compressed_data.encode())  # Encode binary data

        # Save Huffman tree
        huffman_tree_filepath = os.path.join("data", "huffman_tree.pkl")
        with open(huffman_tree_filepath, "wb") as f:
            pickle.dump(huffman_tree, f)

        # Provide download link for compressed file
        st.success("File compressed successfully using Huffman Encoding!")
        with open(compressed_filepath, "rb") as f:
            st.download_button(
                label="Download Compressed File (Huffman)",
                data=f,
                file_name="compressed.bin",
                mime="application/octet-stream",
            )

        # Decompress the file
        if st.button("Decompress File (Huffman)"):
            with open(compressed_filepath, "r") as f:
                compressed_data = f.read()

            with open(huffman_tree_filepath, "rb") as f:
                huffman_tree = pickle.load(f)

            decompressed_data = decode(compressed_data, huffman_tree)
            decompressed_filepath = os.path.join("data", "decompressed" + os.path.splitext(uploaded_file.name)[1])
            with open(decompressed_filepath, "wb") as f:
                f.write(decompressed_data)

            st.success("File decompressed successfully!")
            if is_image:
                st.image(decompressed_filepath, caption="Decompressed Image", use_column_width=True)
            else:
                with open(decompressed_filepath, "r") as f:
                    st.text_area("Decompressed Data", f.read(), height=300)

    elif compression_method == "Bzip2 Compression":
        # Compress data using Bzip2
        compressed_filepath = os.path.join("data", "compressed.bz2")
        with bz2.open(compressed_filepath, "wb") as f:
            f.write(data)  # Write binary data directly

        # Provide download link for compressed file
        st.success("File compressed successfully using Bzip2!")
        with open(compressed_filepath, "rb") as f:
            st.download_button(
                label="Download Compressed File (Bzip2)",
                data=f,
                file_name="compressed.bz2",
                mime="application/x-bzip2",  # Correct MIME type for Bzip2
            )

        # Decompress the file
        if st.button("Decompress File (Bzip2)"):
            with bz2.open(compressed_filepath, "rb") as f:
                decompressed_data = f.read()

            # Save decompressed data to a file
            decompressed_filepath = os.path.join("data", "decompressed" + os.path.splitext(uploaded_file.name)[1])
            with open(decompressed_filepath, "wb") as f:
                f.write(decompressed_data)

            st.success("File decompressed successfully!")
            if is_image:
                st.image(decompressed_filepath, caption="Decompressed Image", use_column_width=True)
            else:
                with open(decompressed_filepath, "r") as f:
                    st.text_area("Decompressed Data", f.read(), height=300)

# Footer
# st.markdown('<div class="footer">© 2023 Data Compression Tool. All rights reserved.</div>', unsafe_allow_html=True)