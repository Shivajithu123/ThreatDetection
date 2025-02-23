"""import cv2
import os
import time
from ultralytics import YOLO

class ThreatDetector:
    def __init__(self, callback):
        
        
        
        
    
        self.model = YOLO('best(7).pt')
        self.frames_folder = "frames"
        self.violence_folder = "violence_frames"
        os.makedirs(self.frames_folder, exist_ok=True)
        os.makedirs(self.violence_folder, exist_ok=True)
        self.callback = callback  # Kivy callback function to update UI

    def process_video(self, video_path):
    
      

        
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Could not open video.")
            return

        frame_count = 0
        last_save_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if time.time() - last_save_time >= 0.2:  # Process frame every 0.2 sec
                last_save_time = time.time()
                frame_count += 1

                # Run YOLOv8 inference
                results = self.model(frame, device="cpu")

                detected_violence = False
                image_path = None

                for result in results:
                    for box in result.boxes:
                        class_id = int(box.cls[0].item())
                        confidence = box.conf[0].item()

                        if class_id == 1 and confidence >= 0.8:  # Violence detected
                            detected_violence = True
                            image_path = os.path.join(self.violence_folder, f"violence_{frame_count}.jpg")
                            cv2.imwrite(image_path, frame)
                            print(f"📸 Threat detected: {image_path}")

                            if self.callback:
                                self.callback(image_path)  # Send image path to Kivy UI

                if detected_violence:
                    continue  # Skip non-violence cases

            # Show real-time detection
            cv2.imshow('YOLOv8 Threat Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        print("🔄 Video Processing Complete")"""


import cv2
import os
import time
from ultralytics import YOLO
from PIL import Image as PILImage

class ThreatDetector:
    def __init__(self, callback):
        """Initializes YOLOv8 model for real-time threat detection."""
        self.model = YOLO('best(7).pt')
        self.violence_folder = "violence_frames"
        os.makedirs(self.violence_folder, exist_ok=True)
        self.callback = callback  # Kivy callback function

    def process_video(self, video_path):
        """Processes video, detects threats, and updates UI via callback."""
        print(f"📂 Loading video: {video_path}")

        if not os.path.exists(video_path):
            print(f"❌ Error: Video file not found - {video_path}")
            return

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"❌ Error: Could not open video file - {video_path}")
            return

        print("✅ Video loaded successfully!")

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                print("🚫 End of video reached or error reading frame.")
                break

            results = self.model(frame, device="cpu")
            detected_violence = False

            for result in results:
                for box in result.boxes:
                    class_id = int(box.cls[0].item())
                    confidence = box.conf[0].item()

                    if class_id == 1 and confidence >= 0.8:
                        detected_violence = True
                        image_path = os.path.join(self.violence_folder, f"violence_{frame_count}.jpg")
                        cv2.imwrite(image_path, frame)

                        # ✅ Ensure the image is completely saved
                        time.sleep(0.2)  # Short delay before calling callback

                        print(f"📸 Threat detected: {image_path}")

                        if self.callback:
                            self.callback(image_path)  # Send image path to Kivy UI

            frame_count += 1

        cap.release()
        print("✅ Video processing complete!")
