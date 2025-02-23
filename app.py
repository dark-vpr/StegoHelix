# import os
import streamlit as st
import cv2
import numpy as np
from io import BytesIO

from src.encoder import StegoEncoder
from src.decoder import StegoDecoder

# Page configuration
st.set_page_config(
    page_title="StegoHelix",
    page_icon="🧬",
    layout="wide"
)

# Custom CSS for file uploader styling
st.markdown("""
<style>
[data-testid="stFileUploader"] {
    border: 2px dashed #4B89DC;
    border-radius: 10px;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)

class StegoHelixGUI:
    def __init__(self):
        self.encoder = StegoEncoder()
        self.decoder = StegoDecoder()
        
    def _process_image(self, uploaded_file):
        """Convert uploaded file bytes into an OpenCV image."""
        file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Invalid image file.")
        return img

    def _image_to_bytes(self, image):
        """
        Encode the NumPy image array to bytes.
        We force PNG output (lossless) to preserve the LSB-embedded payload.
        """
        success, buffer = cv2.imencode(".png", image)
        if not success:
            raise ValueError("Image encoding failed.")
        return BytesIO(buffer)
        
    def run(self):
        st.title("🧬 StegoHelix - Secure Binary Steganography")
        st.markdown("### Hide your secret message in a cover image (losslessly)")
        
        tab1, tab2 = st.tabs(["🔒 Encode Message", "🔓 Decode Message"])
        
        with tab1:
            col1, col2 = st.columns([2, 1])
            with col1:
                img_file = st.file_uploader(
                    "Upload Cover Image (preferably PNG)", 
                    type=["png", "jpg", "jpeg"],
                    key="encoder_upload"
                )
                if img_file:
                    try:
                        img = self._process_image(img_file)
                        st.image(img, caption="Original Image", channels="BGR", use_container_width=True)
                    except Exception as e:
                        st.error(f"Failed to read image: {str(e)}")
            
            with col2:
                secret = st.text_area("Secret Message", height=150, placeholder="Enter message to encode...")
                password = st.text_input("Encryption Key", type="password")
                if st.button("🔒 Encode Secret", type="primary"):
                    if not img_file:
                        st.error("Please upload an image.")
                    elif not secret:
                        st.error("Please enter a secret message.")
                    elif not password:
                        st.error("Please provide an encryption key.")
                    else:
                        try:
                            with st.spinner("Encoding secret message..."):
                                encoded_img = self.encoder.encode(img, secret, password)
                                download_bytes = self._image_to_bytes(encoded_img)
                                st.success("Encoding successful!")
                                st.download_button(
                                    label="📥 Download Protected Image (PNG)",
                                    data=download_bytes,
                                    file_name="protected.png",
                                    mime="image/png"
                                )
                        except Exception as e:
                            st.error(f"Encoding failed: {str(e)}")

        with tab2:
            secret_file = st.file_uploader(
                "Upload Protected Image (PNG)", 
                type=["png"],
                key="decoder_upload"
            )
            decode_pass = st.text_input("Decryption Key", type="password", key="decoder_pass")
            
            if st.button("🔍 Decode Secret Message", type="primary"):
                if not secret_file:
                    st.error("Please upload the protected image.")
                elif not decode_pass:
                    st.error("Please provide the decryption key.")
                else:
                    try:
                        with st.spinner("Decoding secret message..."):
                            secret_img = self._process_image(secret_file)
                            message = self.decoder.decode(secret_img, decode_pass)
                            st.success("Message successfully extracted!")
                            st.text_area("Hidden Message", value=message, height=150, disabled=True)
                    except Exception as e:
                        st.error(f"Decryption failed: {str(e)}")

if __name__ == "__main__":
    gui = StegoHelixGUI()
    gui.run()
