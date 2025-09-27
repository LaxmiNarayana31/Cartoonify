import streamlit as st 
import cv2 
import numpy as np 
from PIL import Image 
import mediapipe as mp 
import os 
import logging 
import warnings 
from absl import logging as absl_logging 
 
# Suppress TensorFlow, Mediapipe, Protobuf logs 
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3" 
logging.getLogger("absl").setLevel(logging.ERROR) 
absl_logging.set_verbosity(absl_logging.ERROR) 
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf") 
 
st.title("Cartoonify: Avatar Generator")
 
# Make directories 
os.makedirs("uploads", exist_ok=True) 
os.makedirs("avatars", exist_ok=True) 
 
# --- Mediapipe Face Detection --- 
mp_face = mp.solutions.face_detection 
face_detection = mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.6) 
 
uploaded_file = st.file_uploader("Upload a face image...", type=["jpg", "jpeg", "png"]) 
 
if uploaded_file is not None: 
    uploaded_path = os.path.join("uploads", uploaded_file.name) 
    with open(uploaded_path, "wb") as f: 
        f.write(uploaded_file.getbuffer()) 
 
    # Load image with OpenCV 
    file_bytes = np.asarray(bytearray(open(uploaded_path, "rb").read()), dtype=np.uint8) 
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR) 
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    h, w, _ = img.shape 
 
    # Check minimum resolution --- 
    if h < 512 or w < 512: 
        st.error("Image resolution too low. Please upload an image at least 512x512.") 
        st.stop() 
 
    # Face detection  
    results = face_detection.process(img) 
    if not results.detections: 
        st.error("No clear face detected. Please upload another image.") 
        st.stop() 
 
    # Apply bilateral filter to smooth colors while preserving edges
    color = cv2.bilateralFilter(img, d=9, sigmaColor=180, sigmaSpace=180)
    color = cv2.bilateralFilter(color, d=7, sigmaColor=120, sigmaSpace=120)
    
    # Create clean edges
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) 
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold( 
        gray, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 
        blockSize=9, 
        C=7
    ) 
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB) 
    edges = cv2.GaussianBlur(edges, (3,3), 0)
 
    # Combine for cartoon effect
    cartoon = cv2.addWeighted(color, 0.88, edges, 0.12, 0)
    
    # Subtle enhancement without over-blurring
    gaussian = cv2.GaussianBlur(cartoon, (0,0), 1.5)
    cartoon = cv2.addWeighted(cartoon, 1.4, gaussian, -0.4, 0)
 
    # Background removal  
    rgba = cv2.cvtColor(cartoon, cv2.COLOR_RGB2RGBA) 
    mp_selfie = mp.solutions.selfie_segmentation 
    with mp_selfie.SelfieSegmentation(model_selection=1) as segment: 
        seg = segment.process(img) 
        mask = seg.segmentation_mask 
        mask = (mask > 0.5).astype(np.uint8) * 255 
        rgba[:, :, 3] = mask 
 
    # Save output  
    base_name, ext = os.path.splitext(uploaded_file.name) 
    avatar_filename = f"{base_name}_cartoon.png" 
    avatar_path = os.path.join("avatars", avatar_filename) 
 
    avatar_pil = Image.fromarray(rgba) 
    avatar_pil.save(avatar_path, format="PNG") 
 
    # Display  
    st.image(img, caption="Original Image") 
    st.image(rgba, caption="Avatar with Transparent Background") 
 
    with open(avatar_path, "rb") as file: 
        st.download_button( 
            label="Download Avatar (PNG)", 
            data=file, 
            file_name=avatar_filename, 
            mime="image/png" 
        )