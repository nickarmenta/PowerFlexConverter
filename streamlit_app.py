import streamlit as st
from pathlib import Path
import tempfile
from app.utils import convert_pf5_to_frc2
import shutil

# Page config to remove hamburger menu and footer
st.set_page_config(
    page_title="PowerFlexConverter",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide streamlit elements
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"][aria-expanded="true"] {display: none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Center all content
st.markdown("""
<style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .uploadedFile {
        max-width: 400px;
        margin: 0 auto;
    }
    div[data-testid="stDownloadButton"] {
        text-align: center;
    }
    h1, h2, h3, p {
        text-align: center;
    }
    .stMarkdown {
        text-align: center;
    }
    div.stMarkdown > div {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Disclaimer
st.markdown("""
# 🚧 FOR TEST USE ONLY 🚧
""")

# Logo/Header
col1, col2, col3 = st.columns([1,2,1])  # Creates three columns with middle one being larger
with col2:
    st.image("docs/logo.png", use_container_width=True)
st.title("PowerFlex Converter")
st.markdown("Convert PowerFlex (.pf5) files to Mitsubishi (.frc2) format in seconds.")

# File uploaders
col1, col2 = st.columns(2)
with col1:
    pf5_file = st.file_uploader("Upload PowerFlex (.pf5) file", type=['pf5'])
with col2:
    template_file = st.file_uploader("Upload template (.frc2) file", type=['frc2'])

if pf5_file and template_file:
    # Create temporary directory to work with files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        
        # Save uploaded files to temp directory
        input_path = temp_dir / pf5_file.name
        template_path = temp_dir / template_file.name
        output_path = temp_dir / input_path.with_suffix('.frc2').name
        
        with open(input_path, 'wb') as f:
            f.write(pf5_file.getvalue())
        with open(template_path, 'wb') as f:
            f.write(template_file.getvalue())
            
        # Copy template to correct filename format
        template_copy = temp_dir / (input_path.stem + ".template.frc2")
        shutil.copy2(template_path, template_copy)
        
        try:
            # Convert file
            convert_pf5_to_frc2(input_path, output_path)
            
            # Provide download button if conversion successful
            with open(output_path, 'rb') as f:
                st.download_button(
                    label="Download converted file",
                    data=f,
                    file_name=output_path.name,
                    mime='application/xml'
                )
                
        except Exception as e:
            st.error(f"Error during conversion: {str(e)}")