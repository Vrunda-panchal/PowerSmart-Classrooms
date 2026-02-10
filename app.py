import streamlit as st
import cv2
from ultralytics import YOLO

# Load model
model = YOLO("yolov8n.pt")

st.title("⚡ PowerSmart Classrooms")
st.subheader("Smart Energy Management System")

light_intensity = st.slider("Ambient Light Intensity (Lux)", 0, 1000, 300)

# Initialize session state
if "camera_on" not in st.session_state:
    st.session_state.camera_on = False

# Buttons
start = st.button("▶ Start Camera")
stop = st.button("⏹ Stop Camera")

if start:
    st.session_state.camera_on = True

if stop:
    st.session_state.camera_on = False

frame_window = st.image([])

if st.session_state.camera_on:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    ret, frame = cap.read()
    if ret:
        results = model(frame)
        person_count = 0

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                if model.names[cls] == "person":
                    person_count += 1

        # Classification
        status = "Occupied" if person_count > 0 else "Empty"

        # Decision Logic
        if status == "Occupied":
            lights = "ON" if light_intensity < 300 else "OFF"
            fans = "ON"
        else:
            lights = "OFF"
            fans = "OFF"

        # Display
        st.markdown(f"### Classroom Status: **{status}**")
        st.markdown(f"💡 Lights: **{lights}**")
        st.markdown(f"🌀 Fans: **{fans}**")

        frame_window.image(frame, channels="BGR")

    cap.release()
