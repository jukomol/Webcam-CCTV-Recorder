from flask import Flask, render_template, Response, send_from_directory, redirect, url_for
import cv2
import os
import time
from datetime import datetime, timedelta
from threading import Thread, Lock

app = Flask(__name__)
RECORDINGS_DIR = "static/recordings"
os.makedirs(RECORDINGS_DIR, exist_ok=True)

frame_buffer = None
recording_active = True
buffer_lock = Lock()

# ✅ Global VideoCapture initialized once
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FPS, 30)

def capture_and_record():
    global frame_buffer, recording_active
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = None
    end_time = None  # Initially None to detect fresh start
    is_recording = False  # To track state transition

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("⚠️ Failed to capture frame.")
            time.sleep(0.1)
            continue

        with buffer_lock:
            frame_buffer = frame.copy()

        if recording_active:
            if not is_recording:
                # Transition from stopped -> started
                start_time = datetime.now()
                timestamp = start_time.strftime("%Y-%m-%d_%H-%M-%S")
                filepath = os.path.join(RECORDINGS_DIR, f"{timestamp}.mp4")
                height, width = frame.shape[:2]
                out = cv2.VideoWriter(filepath, fourcc, 30.0, (width, height))
                if not out.isOpened():
                    print(f"❌ Failed to open VideoWriter for {filepath}")
                    out = None
                    continue
                end_time = start_time + timedelta(hours=1)
                is_recording = True
                print(f"🎥 Started recording: {filepath}")

            if datetime.now() >= end_time:
                out.release()
                is_recording = False
                out = None
                print("⏳ Hour completed. Next file will start on new activation.")

            if out:
                try:
                    out.write(frame)
                except Exception as e:
                    print(f"❌ Error writing frame: {e}")
                    out.release()
                    out = None
                    is_recording = False
        else:
            if is_recording:
                out.release()
                out = None
                is_recording = False
                print("🛑 Recording stopped.")
            time.sleep(0.1)


def gen_frames():
    while True:
        with buffer_lock:
            frame = frame_buffer.copy() if frame_buffer is not None else None
        if frame is not None:
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        else:
            time.sleep(0.1)

@app.route('/')
def index():
    files = sorted(os.listdir(RECORDINGS_DIR), reverse=True)
    msg = "✅ Recording is ON" if recording_active else "🛑 Recording is OFF"
    return render_template("index.html", files=files, message=msg)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_recording')
def start_recording():
    global recording_active
    recording_active = True
    return redirect(url_for('index'))


@app.route('/stop_recording')
def stop_recording():
    global recording_active
    recording_active = False
    return redirect(url_for('index'))

@app.route('/recordings/<filename>')
def download_file(filename):
    return send_from_directory(RECORDINGS_DIR, filename)

if __name__ == '__main__':
    Thread(target=capture_and_record, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
