"""from flask import Flask, request, jsonify
import threading
import os
from Threatdetection import ThreatDetector
from notifications.fcm_service import send_notification

app = Flask(__name__)

# Store detected threats globally
detected_threats = []

def detection_callback(image_path):
   
    global detected_threats
    detected_threats.append(image_path)
    
    # Send push notification
    send_notification(
        title="🚨 Threat Detected!",
        body="A new threat has been detected. Check the app for details.",
        image_url=image_path
    )

@app.route('/detect', methods=['POST'])
def detect():
  
    data = request.json
    video_path = data.get('video_path')

    if not video_path or not os.path.exists(video_path):
        return jsonify({'error': 'Invalid or missing video path'}), 400

    print(f"🔍 Processing video: {video_path}")

    # Start detection in a separate thread
    threat_detector = ThreatDetector(callback=detection_callback)
    detection_thread = threading.Thread(target=threat_detector.process_video, args=(video_path,), daemon=True)
    detection_thread.start()

    return jsonify({'status': 'Detection started', 'video_path': video_path})

@app.route('/threats', methods=['GET'])
def get_threats():
  
    return jsonify({'detected_threats': detected_threats})

if __name__ == "__main__":
    app.run(debug=True)"""


from flask import Flask, request, jsonify
import threading
import os
from Threatdetection import ThreatDetector

app = Flask(__name__)

# Store detected threats globally for UI updates
detected_threats = []

def detection_callback(image_path):
    """Stores detected threats so Kivy UI can fetch them."""
    global detected_threats
    detected_threats.append(image_path)
    print(f"🚨 New Threat Detected: {image_path}")

@app.route('/detect', methods=['POST'])
def detect():
    """Starts threat detection on a video file and updates Kivy UI."""
    data = request.json
    video_path = data.get('video_path')

    if not video_path or not os.path.exists(video_path):
        return jsonify({'error': 'Invalid or missing video path'}), 400

    print(f"🔍 Processing video: {video_path}")

    # Start detection in a separate thread
    threat_detector = ThreatDetector(callback=detection_callback)
    detection_thread = threading.Thread(target=threat_detector.process_video, args=(video_path,), daemon=True)
    detection_thread.start()

    return jsonify({'status': 'Detection started', 'video_path': video_path})

@app.route('/threats', methods=['GET'])
def get_threats():
    """Returns a list of detected threat images for UI display."""
    return jsonify({'detected_threats': detected_threats})

if __name__ == "__main__":
    app.run(debug=True)
