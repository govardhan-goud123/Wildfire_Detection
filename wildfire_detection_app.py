"""Streamlit interface for TensorFlow wildfire detection."""

import time
import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image

from model_utils import (
    CLASS_NAMES, IMAGE_SIZE, MODEL_PATH, build_model, train_and_save,
)

st.set_page_config(
    page_title="Wildfire Detection AI",
    page_icon="🔥",
    layout="wide",
)

st.title("🔥 AI-Powered Wildfire Detection")
st.write(
    "Upload an image to check whether it appears to contain a wildfire. "
    "This demo is an image classifier, so results should be reviewed by a person."
)

with st.sidebar:
    st.header("Model")
    st.write("Framework: TensorFlow / Keras")
    st.write("Architecture: MobileNetV2 transfer learning")
    st.write(f"Image size: {IMAGE_SIZE[0]} × {IMAGE_SIZE[1]}")
    st.divider()
    epochs = st.slider("Training epochs", min_value=1, max_value=15, value=5)
    if st.button("Train / retrain model", type="primary", use_container_width=True):
        try:
            with st.spinner(
                "Training model. The first run may download MobileNetV2 weights."
            ):
                model, history, test_results = train_and_save(epochs=epochs)
            st.success("Training finished and model saved.")
            st.write("Test results")
            st.json({key: round(float(value), 4) for key, value in test_results.items()})
        except Exception as exc:
            st.error(f"Training failed: {exc}")

@st.cache_resource
def load_saved_model(model_path, modified_time):
    del modified_time
    return tf.keras.models.load_model(model_path)

if not MODEL_PATH.exists():
    st.info(
        "No trained TensorFlow model was found yet. Use **Train / retrain model** "
        "in the sidebar first. The old PyTorch .pth model is not used."
    )
    st.stop()

try:
    model = load_saved_model(str(MODEL_PATH), MODEL_PATH.stat().st_mtime)
except Exception as exc:
    st.error(f"Could not load the saved model: {exc}")
    st.stop()

uploaded_file = st.file_uploader(
    "Choose a forest or aerial image",
    type=["jpg", "jpeg", "png", "webp"],
)

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file).convert("RGB")
        left, right = st.columns([1, 1])
        with left:
            st.image(image, caption="Uploaded image", use_container_width=True)

        resized = image.resize(IMAGE_SIZE)
        image_array = np.asarray(resized, dtype=np.float32)
        batch = np.expand_dims(image_array, axis=0)

        start = time.perf_counter()
        fire_probability = float(model.predict(batch, verbose=0)[0][0])
        elapsed = time.perf_counter() - start
        nofire_probability = 1.0 - fire_probability

        with right:
            st.subheader("Prediction")
            if fire_probability >= 0.5:
                st.error("🔥 Possible fire detected")
            else:
                st.success("🌿 No fire detected")
            st.metric("Fire probability", f"{fire_probability:.1%}")
            st.metric("No-fire probability", f"{nofire_probability:.1%}")
            st.caption(f"Inference time: {elapsed:.2f} seconds")
            st.progress(min(max(fire_probability, 0.0), 1.0))
            st.warning(
                "This prediction is not an emergency alert or proof of safety. "
                "Verify suspicious images with reliable sources."
            )
    except Exception as exc:
        st.error(f"Could not analyze this image: {exc}")
