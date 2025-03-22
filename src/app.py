import streamlit as st
import os
import pickle
import bz2
import time
from huffman import *
from bzip2 import simplified_bzip2_compress, simplified_bzip2_decompress

# Ensure the 'data' directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Set page title and favicon
st.set_page_config(
    page_title="HuffZip",
    page_icon="📂",
    layout="wide",
)

# CSS styling with the HuffZip header and lighter colors
st.markdown(
    """
    <style>
        /* Basic styling */
        .main {
            padding: 0;
        }
        
        /* Clean header */
        h1 {
            color: #6aa9ff;
            font-size: 36px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        /* Description text */
        .description {
            margin-bottom: 20px;
        }
        
        /* Upload area */
        .upload-section {
            margin-top: 20px;
            margin-bottom: 20px;
        }
        
        /* File uploader with clean design */
        .stFileUploader > div {
            border: 2px dashed #a8d0ff;
            border-radius: 10px;
            padding: 20px;
            background-color: #f9fafb;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #6aa9ff;
            color: white;
            border-radius: 4px;
            padding: 8px 16px;
            border: none;
            font-weight: 600;
        }
        
        /* Better spacing */
        .block-container {
            padding-top: 0;
            padding-bottom: 2rem;
        }
        
        /* Hero section styling */
        .hero-section {
            background: linear-gradient(135deg, #a8d0ff, #6aa9ff);
            padding: 3rem 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
            color: white;
        }
        
        .hero-title {
            font-size: 4rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.5rem;
            font-weight: 400;
            margin-bottom: 1rem;
        }
        
        /* Welcome section styling */
        .welcome-section {
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        
        .welcome-title {
            font-size: 2rem;
            color: #333;
            margin-bottom: 1rem;
        }
        
        .welcome-text {
            font-size: 1.1rem;
            color: #555;
            line-height: 1.6;
        }
        
        .algorithm-highlight {
            font-weight: 600;
            color: #6aa9ff;
        }
        
        /* Hide streamlit's default elements that might show None */
        .stMarkdown p:empty {
            display: none;
        }
        
        /* Additional styling to hide None values */
        .element-container div[data-testid="stText"] p:empty,
        .element-container div[data-testid="stText"] p:contains("None") {
            display: none !important;
        }
        
        /* Hide Streamlit's default footer */
        footer {
            visibility: hidden;
        }
        
        /* Hide any empty paragraphs */
        p:empty {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Improved helper function to simulate progress without returning None values
def show_progress_bar():
    progress_placeholder = st.empty()
    with progress_placeholder:
        progress_bar = st.progress(0)
        for i in range(101):
            progress_bar.progress(i)
            time.sleep(0.005) if i < 100 else time.sleep(0.01)
    progress_placeholder.empty()

# Hero Section (HuffZip Header)
st.markdown(
    """
    <div class="hero-section">
        <h1 class="hero-title">HuffZip</h1>
        <p class="hero-subtitle">Advanced Data Compression Tool</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Welcome Section
st.markdown(
    """
    <div class="welcome-section">
        <h2 class="welcome-title">Welcome to HuffZip</h2>
        <p class="welcome-text">
            A powerful compression tool that uses state-of-the-art algorithms to efficiently compress your files. Choose between 
            <span class="algorithm-highlight">Huffman Encoding</span> for optimal text compression or 
            <span class="algorithm-highlight">Bzip2 Compression</span> for complex data types.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# App layout with two columns (sidebar-like left column)
col1, col2 = st.columns([1, 3])

# Left column (Configuration)
with col1:
    st.header("Configuration")
    
    # Compression method selection
    st.write("Choose Compression Method")
    compression_method = st.selectbox(
        "",
        ["Huffman Encoding", "Bzip2 Compression"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Supported file types
    st.header("Supported File Types")
    st.markdown("- Text Files (.txt)")
    st.markdown("- Image Files (.png, .jpg, .jpeg)")
    
    st.markdown("---")
    
    # Credit
    st.write("Built with [Streamlit](https://streamlit.io)")

# Main content in the right column
with col2:
    # File upload section
    st.header("Compress Your Files")
    st.write("Upload a file to compress")
    uploaded_file = st.file_uploader("Drag and drop file here", type=["txt", "png", "jpg", "jpeg"])
    
    # Create containers for different sections to better control the UI flow
    preview_container = st.container()
    action_container = st.container()
    results_container = st.container()
    download_container = st.container()
    decompress_container = st.container()
    
    if uploaded_file is not None:
        # Save the uploaded file
        filepath = os.path.join("data", uploaded_file.name)
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Read the uploaded file
        with open(filepath, "rb") as f:
            data = f.read()
        
        # Check if the file is an image
        is_image = uploaded_file.type.startswith("image")
        
        # Display file information
        file_size = len(data)
        
        # Show file preview (if text)
        with preview_container:
            if not is_image:
                try:
                    with open(filepath, "r", encoding='utf-8', errors='replace') as f:
                        preview_data = f.read(1000)
                        if not preview_data.strip():
                            st.warning("The file appears to be empty or contains only whitespace.")
                        else:
                            st.text_area("File Preview", preview_data, height=100)
                except Exception as e:
                    st.error(f"Could not read file as text: {str(e)}")
                    st.info("This might be a binary file.")
            else:
                st.image(filepath, caption=uploaded_file.name, width=300)
        
        # Compression action buttons
        with action_container:
            # Store button state in session state to avoid None returns
            if 'compress_clicked' not in st.session_state:
                st.session_state.compress_clicked = False
            
            if st.button("Compress File"):
                st.session_state.compress_clicked = True
            
        # Process compression when button is clicked
        if st.session_state.compress_clicked:
            # Use a container for status updates to avoid None values
            status_container = st.container()
            
            with status_container:
                status_placeholder = st.empty()
                status_placeholder.info("Starting compression...")
                
                # Show progress without returning None values
                show_progress_bar()
                
                # Compress the file based on the selected method
                if compression_method == "Huffman Encoding":
                    try:
                        status_placeholder.info("Building Huffman tree...")
                        
                        # Build Huffman Tree and codes
                        freq_table = build_frequency_table(data)
                        huffman_tree = build_huffman_tree(freq_table)
                        huffman_codes = generate_codes(huffman_tree)
                        
                        status_placeholder.info("Encoding data...")
                        
                        # Compress data
                        compressed_data = encode(data, huffman_codes)
                        compressed_filepath = os.path.join("data", "compressed.bin")
                        
                        # Check if compressed_data is not empty
                        if compressed_data:
                            # Convert binary string to bytes
                            compressed_bytes = int(compressed_data, 2).to_bytes((len(compressed_data) + 7) // 8, byteorder='big')
                            with open(compressed_filepath, "wb") as f:
                                f.write(compressed_bytes)
                            
                            # Save Huffman tree
                            huffman_tree_filepath = os.path.join("data", "huffman_tree.pkl")
                            with open(huffman_tree_filepath, "wb") as f:
                                pickle.dump(huffman_tree, f)
                            
                            # Calculate compression ratio
                            compressed_size = os.path.getsize(compressed_filepath)
                            compression_ratio = (1 - (compressed_size / file_size)) * 100
                            
                            # Clear status
                            status_placeholder.empty()
                            
                            # Display results in their container
                            with results_container:
                                st.markdown("### Compression Results:")
                                metrics_cols = st.columns(3)
                                with metrics_cols[0]:
                                    st.metric("Original Size", f"{file_size} bytes")
                                with metrics_cols[1]:
                                    st.metric("Compressed Size", f"{compressed_size} bytes")
                                with metrics_cols[2]:
                                    st.metric("Space Saved", f"{compression_ratio:.2f}%")
                            
                            # Provide download link in its container
                            with download_container:
                                with open(compressed_filepath, "rb") as f:
                                    compressed_bytes = f.read()
                                    st.download_button(
                                        label="Download Compressed File",
                                        data=compressed_bytes,
                                        file_name="compressed.bin",
                                        mime="application/octet-stream",
                                        key="download_huffman",
                                    )
                            
                            # Store decompress state in session state to avoid None returns
                            if 'decompress_clicked' not in st.session_state:
                                st.session_state.decompress_clicked = False
                            
                            # Decompression option
                            with decompress_container:
                                st.markdown("---")
                                if st.button("Decompress File", key="decompress_huffman"):
                                    st.session_state.decompress_clicked = True
                            
                            # Process decompression when button is clicked
                            if st.session_state.decompress_clicked:
                                decomp_placeholder = st.empty()
                                decomp_placeholder.info("Decompressing file...")
                                
                                with open(compressed_filepath, "rb") as f:
                                    compressed_bytes = f.read()
                                    # Convert bytes to binary string
                                    compressed_data = ''.join(f'{byte:08b}' for byte in compressed_bytes)
                                
                                with open(huffman_tree_filepath, "rb") as f:
                                    huffman_tree = pickle.load(f)
                                
                                decompressed_data = decode(compressed_data, huffman_tree)
                                decompressed_filepath = os.path.join("data", "decompressed" + os.path.splitext(uploaded_file.name)[1])
                                with open(decompressed_filepath, "wb") as f:
                                    f.write(decompressed_data)
                                
                                decomp_placeholder.success("File successfully decompressed!")
                                
                                # Display decompressed content
                                if is_image:
                                    st.image(decompressed_filepath, caption="Decompressed Image", width=300)
                                else:
                                    try:
                                        with open(decompressed_filepath, "r", encoding='utf-8', errors='replace') as f:
                                            decompressed_content = f.read()
                                            st.text_area("Decompressed Data", decompressed_content, height=150)
                                    except Exception as e:
                                        st.error(f"Could not display decompressed data as text: {str(e)}")
                        else:
                            status_placeholder.error("Compression failed: No data to compress or empty result.")
                    except Exception as e:
                        status_placeholder.error(f"Compression failed: {str(e)}")
                        st.info("This might be due to an issue with the file format or content.")
                
                elif compression_method == "Bzip2 Compression":
                    try:
                        status_placeholder.info("Compressing with Bzip2...")
                        
                        # Compress data using Bzip2
                        compressed_filepath = os.path.join("data", "compressed.bz2")
                        with bz2.open(compressed_filepath, "wb") as f:
                            f.write(data)
                        
                        # Calculate compression ratio
                        compressed_size = os.path.getsize(compressed_filepath)
                        compression_ratio = (1 - (compressed_size / file_size)) * 100
                        
                        # Clear status
                        status_placeholder.empty()
                        
                        # Display results in their container
                        with results_container:
                            st.markdown("### Compression Results:")
                            metrics_cols = st.columns(3)
                            with metrics_cols[0]:
                                st.metric("Original Size", f"{file_size} bytes")
                            with metrics_cols[1]:
                                st.metric("Compressed Size", f"{compressed_size} bytes")
                            with metrics_cols[2]:
                                st.metric("Space Saved", f"{compression_ratio:.2f}%")
                        
                        # Provide download link in its container
                        with download_container:
                            with open(compressed_filepath, "rb") as f:
                                compressed_bytes = f.read()
                                st.download_button(
                                    label="Download Compressed File",
                                    data=compressed_bytes,
                                    file_name="compressed.bz2",
                                    mime="application/x-bzip2",
                                    key="download_bzip2",
                                )
                        
                        # Store decompress state in session state to avoid None returns
                        if 'decompress_clicked' not in st.session_state:
                            st.session_state.decompress_clicked = False
                        
                        # Decompression option
                        with decompress_container:
                            st.markdown("---")
                            if st.button("Decompress File", key="decompress_bzip2"):
                                st.session_state.decompress_clicked = True
                        
                        # Process decompression when button is clicked
                        if st.session_state.decompress_clicked:
                            decomp_placeholder = st.empty()
                            decomp_placeholder.info("Decompressing file...")
                            
                            with bz2.open(compressed_filepath, "rb") as f:
                                decompressed_data = f.read()
                            
                            decompressed_filepath = os.path.join("data", "decompressed" + os.path.splitext(uploaded_file.name)[1])
                            with open(decompressed_filepath, "wb") as f:
                                f.write(decompressed_data)
                            
                            decomp_placeholder.success("File successfully decompressed!")
                            
                            # Display decompressed content
                            if is_image:
                                st.image(decompressed_filepath, caption="Decompressed Image", width=300)
                            else:
                                try:
                                    with open(decompressed_filepath, "r", encoding='utf-8', errors='replace') as f:
                                        decompressed_content = f.read()
                                        st.text_area("Decompressed Data", decompressed_content, height=150)
                                except Exception as e:
                                    st.error(f"Could not display decompressed data as text: {str(e)}")
                    except Exception as e:
                        status_placeholder.error(f"Compression failed: {str(e)}")
                        st.info("This might be due to an issue with the file format or content.")