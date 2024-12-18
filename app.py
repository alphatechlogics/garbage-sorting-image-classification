import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

# Load the saved model and compile
model = load_model('mobilenetv2_waste_classifier.h5')
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Define class names
class_names = ['METAL', 'ORGANIC', 'PAPER', 'PLASTIC']

# Function to load and preprocess the image
def load_and_preprocess_image(uploaded_file):
    img = image.load_img(uploaded_file, target_size=(640, 640))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array /= 255.0  # Rescale to [0, 1]
    return img_array

# Streamlit UI
st.title("Waste Classifier App")
st.write("Upload an image to classify it into one of the following classes:")
st.write(", ".join(class_names))

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    # Load and preprocess the image
    img_array = load_and_preprocess_image(uploaded_file)

    # Predict
    predictions = model.predict(img_array)
    predicted_class = class_names[np.argmax(predictions)]
    confidence = np.max(predictions) * 100

    # Display prediction
    st.write(f"**Prediction:** {predicted_class}")
    st.write(f"**Confidence:** {confidence:.2f}%")
