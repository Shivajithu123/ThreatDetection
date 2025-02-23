import cv2
import os
import time
from collections import deque
from ultralytics import YOLO

class ThreatDetector:
    def __init__(self, callback):
        """
        Initializes the YOLOv8 model and sets up video processing.
        
        :param callback: Function to update Kivy UI with detected threats.
        """
        self.model = YOLO('best(7).pt')
        self.frames_folder = "frames"
        self.violence_folder = "violence_frames"
        os.makedirs(self.frames_folder, exist_ok=True)
        os.makedirs(self.violence_folder, exist_ok=True)
        self.callback = callback  # Kivy callback function to update UI

    def process_video(self, video_path):
        """
        Processes the video, detects threats, and sends results to Kivy UI.
        
        :param video_path: Path to the input video file.
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Could not open video.")
            return

        frame_buffer = deque(maxlen=15)  # Stores last 15 frames
        frame_count = 0
        last_save_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                break  # Stop if no frame is captured

            current_time = time.time()

            if current_time - last_save_time >= 0.2:  # Process frame every 0.2 sec
                last_save_time = current_time
                frame_count += 1

                # Run YOLOv8 inference
                results = self.model(frame, device="cpu")

                detected_violence = False
                frame_path = os.path.join(self.frames_folder, f"frame_{frame_count}.jpg")

                for result in results:
                    for box in result.boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box coordinates
                        confidence = box.conf[0].item()
                        class_id = int(box.cls[0].item())

                        confidence_threshold = 0.8
                        if confidence >= confidence_threshold:
                            label = f"{self.model.names[class_id]}: {confidence:.2f}"
                            color = (0, 255, 0)  # Green (Non-Violence)

                            if class_id == 1:  # Assuming Class ID 1 = Violence
                                detected_violence = True
                                frame_path = os.path.join(self.violence_folder, f"violence_{frame_count}.jpg")
                                color = (0, 0, 255)  # Red for Violence

                            # Draw bounding box
                            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                if detected_violence:
                    cv2.imwrite(frame_path, frame)
                    print(f"📸 Threat detected! Screenshot saved: {frame_path}")

                    # Send detected frame to Kivy UI
                    if self.callback:
                        self.callback(frame_path)  # Call Kivy function to update UI

                frame_buffer.append(frame_path)

            # Show real-time detection
            cv2.imshow('YOLOv8 Video Threat Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break  # Press 'q' to exit

        cap.release()
        cv2.destroyAllWindows()
        print("Processing complete. All frames saved in 'frames/' and detected violence in 'violence_frames/'.")

