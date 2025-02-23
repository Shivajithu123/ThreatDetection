"""from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import threading
import os
from Threatdetection import ThreatDetector  # Import corrected class

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

# Load KV files
Builder.load_file(r"home_screen.kv")
Builder.load_file(r"notifications_screen.kv")
Builder.load_file(r"logs_screen.kv")

class HomeScreen(Screen):
    pass

class NotificationsScreen(Screen):
    pass

class LogsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log_list = BoxLayout(orientation="vertical", size_hint_y=None)
        self.add_widget(self.log_list)

    def add_log_entry(self, image_path):
        
        Clock.schedule_once(lambda dt: self._update_ui(image_path), 0)

    def _update_ui(self, image_path):
       
        incident_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=100)
        incident_text = Label(text=f"Threat detected at {time.strftime('%H:%M:%S')}", size_hint_x=0.7)
        incident_img = Image(source=image_path, size_hint_x=0.3)

        incident_box.add_widget(incident_text)
        incident_box.add_widget(incident_img)
        self.log_list.add_widget(incident_box)

class MainApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(NotificationsScreen(name='notifications'))
        self.sm.add_widget(LogsScreen(name='logs'))
        return self.sm

    def view_live_detections(self):
        
        print("🔴 Starting live threat detection...")

        log_screen = self.sm.get_screen('logs')

        def callback(image_path):
            log_screen.add_log_entry(image_path)

        # Start threat detection in a separate thread
        threat_detector = ThreatDetector(callback)
        detection_thread = threading.Thread(
            target=threat_detector.process_video, 
            args=(r"D:\\python_project\\Test\\fighttest.mp4",),
            daemon=True
        )
        detection_thread.start()

    def show_notifications(self):
        self.sm.current = "notifications"

    def show_logs(self):
        self.sm.current = "logs"

    def back_to_home(self):
        self.sm.current = "home"

if __name__ == "__main__":
    MainApp().run()"""


import os
import time
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.popup import Popup
import threading
from Threatdetection import ThreatDetector

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

# Load KV files
Builder.load_file(r"home_screen.kv")
Builder.load_file(r"notifications_screen.kv")
Builder.load_file(r"logs_screen.kv")

class HomeScreen(Screen):
    pass

class NotificationsScreen(Screen):
    pass

class LogsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.log_list = BoxLayout(orientation="vertical", size_hint_y=None)
        self.add_widget(self.log_list)

    def add_log_entry(self, image_path):
        """Updates UI with detected threats and shows notification."""
        absolute_path = os.path.abspath(image_path)  # ✅ Fix incorrect path issues
        Clock.schedule_once(lambda dt: self._update_ui(absolute_path), 0)

    def _update_ui(self, image_path):
        """Adds an image and timestamp to the logs UI and displays an alert."""
        print(f"🖼️ Loading Image: {image_path}")

        incident_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=100)
        incident_text = Label(text=f"⚠️ Threat detected at {time.strftime('%H:%M:%S')}", size_hint_x=0.7)
        incident_img = Image(source=image_path, size_hint_x=0.3)

        incident_box.add_widget(incident_text)
        incident_box.add_widget(incident_img)
        self.log_list.add_widget(incident_box)

        # Show notification popup
        self.show_notification(image_path)

    def show_notification(self, image_path):
        """Displays an alert with the detected threat image."""
        popup_layout = BoxLayout(orientation='vertical')
        notif_img = Image(source=image_path, size_hint=(1, 0.7))
        notif_text = Label(text="🚨 Threat Detected! Check logs.", size_hint=(1, 0.3))

        popup_layout.add_widget(notif_img)
        popup_layout.add_widget(notif_text)

        popup = Popup(title="🔴 Alert!", content=popup_layout, size_hint=(0.7, 0.7))
        popup.open()

class MainApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(NotificationsScreen(name='notifications'))
        self.sm.add_widget(LogsScreen(name='logs'))
        return self.sm

    def view_live_detections(self):
        """Start real-time detection and show alerts in Kivy."""
        print("🔴 Starting live threat detection...")

        log_screen = self.sm.get_screen('logs')

        def callback(image_path):
            log_screen.add_log_entry(image_path)

        # Start detection in a separate thread
        threat_detector = ThreatDetector(callback)
        detection_thread = threading.Thread(
            target=threat_detector.process_video, 
            args=(r"D:\\python_project\\RealTimeThreatDetectionApp\\frontend\\video\\dance.mp4",),
            daemon=True
        )
        detection_thread.start()

    def show_notifications(self):
        self.sm.current = "notifications"

    def show_logs(self):
        self.sm.current = "logs"

    def back_to_home(self):
        self.sm.current = "home"

if __name__ == "__main__":
    MainApp().run()
