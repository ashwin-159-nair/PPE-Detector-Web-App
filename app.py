import streamlit as st
from ultralytics import YOLO
import tempfile
import os
import gdown # Used to download files from Google Drive share links

# --- Configuration ---
# CRITICAL: This is the direct download link for your best.pt file.
DOWNLOAD_URL = "https://drive.google.com/uc?export=download&id=1_gFEBNMVvOAQWQTF7J__kEbHOJJEPviK"

# Path where the model will be saved locally on the Streamlit server
MODEL_PATH = "best.pt" 

st.set_page_config(layout="wide")
st.title("👷 Real-Time PPE (Personal Protective Equipment) Detector")

# --- Model Loading (Cached for Speed and Download) ---
# @st.cache_resource ensures the model is only downloaded and loaded once.
@st.cache_resource
def load_model():
    """Downloads model from Drive and loads it using YOLO."""
    try:
        if not os.path.exists(MODEL_PATH):
            st.info("Downloading model weights from Google Drive...")
            # gdown will download the file to the Streamlit server's storage
            gdown.download(DOWNLOAD_URL, MODEL_PATH, quiet=False)
            st.success("Download complete!")
            
        model = YOLO(MODEL_PATH)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()
        
model = load_model()

# --- File Uploader ---
uploaded_file = st.file_uploader(
    "Upload an Image or Video of a Worksite", 
    type=["jpg", "jpeg", "png", "mp4", "mov", "avi"]
)

# --- Prediction Logic ---
if uploaded_file is not None and model:
    # 1. Determine file type and get user settings
    file_type = uploaded_file.type.split('/')[0]

    st.sidebar.header("Prediction Settings")
    
    conf_threshold = st.sidebar.slider(
        "Confidence Threshold", 
        0.0, 1.0, 0.25, 0.05
    )

    # 2. Save the uploaded file to a temporary location
    file_extension = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_file_path = tmp_file.name

    if file_type == 'image':
        st.subheader("Processing Image...")
        
        # Run inference
        results = model.predict(
            source=temp_file_path, 
            conf=conf_threshold, 
            save=True, 
            project='runs/detect', 
            name='predict', 
            exist_ok=True
        )
        
        # Get the path to the annotated image
        annotated_image_path = os.path.join('runs', 'detect', 'predict', os.path.basename(temp_file_path))

        # Display the results
        st.image(annotated_image_path, caption='PPE Detection Results', use_column_width=True)
        st.success("Detection Complete!")

    elif file_type == 'video':
        st.subheader("Processing Video...")
        st.info("Video processing can take several minutes. Please wait...")

        # Run inference
        results = model.predict(
            source=temp_file_path, 
            conf=conf_threshold, 
            save=True,
            project='runs/detect', 
            name='predict_video', 
            exist_ok=True
        )
        
        # Find the actual output video file name saved by YOLO
        output_folder = os.path.join('runs', 'detect', 'predict_video')
        # YOLO renames the file during prediction, so we search the output folder for the predicted video
        saved_video_path = next((os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.startswith('results') and f.endswith(('.mp4', '.avi'))), None)
        
        if saved_video_path:
            st.video(saved_video_path)
            st.success("Video Processing Complete!")
        else:
            st.error("Could not find the processed video file.")

    # Clean up the temporary input file
    os.remove(temp_file_path)
