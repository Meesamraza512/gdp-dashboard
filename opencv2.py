

import streamlit as st
import cv2
from PIL import Image
import numpy as np
from fer import FER


def process_image(image):
    # Convert the image to a format suitable for FER
    img_array = np.array(image)
    face_detector = FER()
    result = face_detector.detect_emotions(img_array)
    colors = {'happy': (0, 255, 0), 'sad': (0, 0, 255), 'neutral': (255, 255, 255)}

    if result:
        for face in result:
            emotions = face['emotions']
            emotion = max(emotions, key=emotions.get)
            color = colors.get(emotion, (255, 255, 255))
            x, y, w, h = face['box']
            cv2.rectangle(img_array, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img_array, emotion.capitalize(), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    return Image.fromarray(img_array)


def main():
    st.title("Real-Time Emotion Detection")

    # Create placeholders for the camera feed and uploaded image
    frame_placeholder = st.empty()
    uploaded_image_placeholder = st.empty()

    # Button to open the camera
    if st.button("Open Camera", key="open_camera"):
        cap = cv2.VideoCapture(1)
        face_detector = FER()
        colors = {'happy': (0, 255, 0), 'sad': (0, 0, 255), 'neutral': (255, 255, 255)}

        # Create a stop button
        stop_button = st.button("Stop Camera", key="stop_camera")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.write("Failed to capture image")
                break

            result = face_detector.detect_emotions(frame)
            if result:
                for face in result:
                    emotions = face['emotions']
                    emotion = max(emotions, key=emotions.get)
                    color = colors.get(emotion, (255, 255, 255))
                    x, y, w, h = face['box']
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, emotion.capitalize(), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            # Convert the frame to RGB (Streamlit expects RGB images)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Update the placeholder with the current frame
            frame_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)

            # Check if the "Stop Camera" button is pressed
            if stop_button:
                break

        cap.release()
        cv2.destroyAllWindows()

    # Image upload functionality
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        processed_image = process_image(image)
        uploaded_image_placeholder.image(processed_image, caption='Uploaded Image with Emotion Detection',
                                         use_column_width=True)


if __name__ == "__main__":
    main()

