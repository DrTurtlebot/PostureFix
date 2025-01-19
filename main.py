import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
from gui import PostureGUI
import threading
import tkinter as tk

#Custom Imports
from components.camera import Camera
from components.pose_detection import PoseDetector
from components.posture_evaluation import PostureEvaluator
from components.warnings.alert_manager import PostureAlertManager
from components.warnings.gui_warning import GUIWarning
from components.warnings.sound_warning import SoundWarning
from components.warnings.stream_deck_warning import StreamDeckWarning


def load_dlls():
    dll_folder = os.path.abspath("./dlls")
    if not os.path.exists(dll_folder):
        raise FileNotFoundError(f"DLL folder not found: {dll_folder}")
    os.environ["PATH"] = dll_folder + os.pathsep + os.environ["PATH"]


def start_posture_detection(gui):
    """Run posture detection while dynamically fetching settings from the GUI."""
    print("Turning on camera")
    camera = Camera(width=640, height=480, desired_fps=10)
    print("Camera is on")
    pose_detector = PoseDetector()
    alert_manager = PostureAlertManager()
    gui_warning = GUIWarning(gui, alert_manager)
    sound_warning = SoundWarning(alert_manager)
    stream_deck_warning = StreamDeckWarning(alert_manager)

    bad_posture_start_time = None  # Track when bad posture starts
    is_camera_displayed = False  # Track the state of the OpenCV window

    while camera.is_opened():
        frame = camera.get_frame()
        if frame is None:
            continue

        # Fetch current thresholds and settings
        angle_threshold = gui.get_angle_threshold()
        distance_threshold_ratio = gui.get_distance_threshold_ratio()
        alert_method = gui.get_alert_method()
        timeout = gui.get_timeout()  # Fetch timeout value
        show_camera = gui.is_camera_enabled()  # Check if the camera feed should be shown
        posture_evaluator = PostureEvaluator(angle_threshold, distance_threshold_ratio)

        # Initialize variables for drawing
        current_angle = None

        # Get pose landmarks and calculate metrics
        landmarks = pose_detector.get_pose_landmarks(frame)
        if landmarks:
            angle, horizontal_distance = pose_detector.calculate_metrics(landmarks, frame)
            current_angle = angle  # Update the current angle
            is_bad_posture = posture_evaluator.evaluate_posture(angle, horizontal_distance, frame.shape[1])

            if is_bad_posture:
                if bad_posture_start_time is None:
                    bad_posture_start_time = cv2.getTickCount()  # Start the timer
                elapsed_time = (cv2.getTickCount() - bad_posture_start_time) / cv2.getTickFrequency()
                if elapsed_time >= timeout:  # Trigger alerts after timeout
                    gui_warning.update(is_bad_posture, alert_method)
                    if alert_method == "Sound":
                        sound_warning.update(is_bad_posture)
                    elif alert_method == "StreamDeck":
                        stream_deck_warning.update_warnings(is_bad_posture, frame, angle, horizontal_distance)
            else:
                bad_posture_start_time = None  # Reset timer if posture improves
                gui_warning.update(False, alert_method)  # Reset GUI warning box to green
                sound_warning.update(False)
                stream_deck_warning.update_warnings(False, frame, angle, horizontal_distance)

            pose_detector.visualize_pose(frame, landmarks)
        else:
            bad_posture_start_time = None  # Reset timer if no landmarks detected
            gui_warning.update(False, alert_method)  # Reset GUI warning box to green
            sound_warning.update(False)
            stream_deck_warning.update_warnings(False, frame, None, None)

        # Draw the current angle on the frame
        if current_angle is not None:
            current_angle_text = f"Current Angle: {int(current_angle)}°"
            cv2.putText(
                frame,
                current_angle_text,
                (10, 30),  # Position on the frame (x, y)
                cv2.FONT_HERSHEY_SIMPLEX,
                1,  # Font scale
                (255, 255, 255),  # Font color (white)
                2,  # Line thickness
                cv2.LINE_AA,
            )

        # Manage camera feed display
        if show_camera:
            if not is_camera_displayed:  # Open the window if not already displayed
                is_camera_displayed = True
            cv2.imshow("Posture Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            if is_camera_displayed:  # Close the window when the toggle is off
                cv2.destroyWindow("Posture Detection")
                is_camera_displayed = False

    # Clean up resources
    camera.release()
    cv2.destroyAllWindows()
    stream_deck_warning.close()


def run_gui():
    """Launch the GUI and handle real-time posture detection."""
    root = tk.Tk()
    gui = PostureGUI(root)

    # Start posture detection in a separate thread
    threading.Thread(
        target=start_posture_detection,
        args=(gui,),
        daemon=True
    ).start()

    root.mainloop()


if __name__ == "__main__":
    load_dlls()
    run_gui()
