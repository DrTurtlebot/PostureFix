import mediapipe as mp
import cv2
from components.utils import calculate_angle

class PoseDetector:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

    def get_pose_landmarks(self, frame):
        """Detect pose landmarks in the given frame."""
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)
        return results.pose_landmarks.landmark if results.pose_landmarks else None

    def calculate_metrics(self, landmarks, frame):
        """Calculate angle and horizontal distance for posture analysis."""
        ear = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_EAR.value].x * frame.shape[1],
               landmarks[mp.solutions.pose.PoseLandmark.LEFT_EAR.value].y * frame.shape[0]]
        shoulder = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x * frame.shape[1],
                    landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y * frame.shape[0]]
        hip = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x * frame.shape[1],
               landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y * frame.shape[0]]

        angle = calculate_angle(ear, shoulder, hip)
        horizontal_distance = abs(ear[0] - shoulder[0])
        return angle, horizontal_distance

    def visualize_pose(self, frame, landmarks):
        """Visualize pose landmarks and lines."""
        mp_pose = mp.solutions.pose

        try:
            ear = [int(landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].x * frame.shape[1]),
                   int(landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].y * frame.shape[0])]
            shoulder = [int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * frame.shape[1]),
                        int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * frame.shape[0])]
            hip = [int(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * frame.shape[1]),
                   int(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * frame.shape[0])]

            # Draw points and lines
            cv2.circle(frame, ear, 5, (255, 0, 0), -1)
            cv2.circle(frame, shoulder, 5, (0, 255, 0), -1)
            cv2.circle(frame, hip, 5, (0, 0, 255), -1)
            cv2.line(frame, ear, shoulder, (255, 0, 0), 2)
            cv2.line(frame, shoulder, hip, (0, 255, 0), 2)

        except IndexError:
            print("Landmarks not detected properly for visualization.")
