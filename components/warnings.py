from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
import time
import cv2

class PostureWarning:
    def __init__(self):
        """Initialize Stream Deck and posture tracking variables."""
        self.streamdecks = DeviceManager().enumerate()
        if not self.streamdecks:
            raise Exception("No Stream Decks found.")
        self.deck = self.streamdecks[0]
        self.deck.open()
        self.deck.reset()
        self.bad_posture_start_time = None

    def set_all_keys_color(self, color):
        """Set all keys on the Stream Deck to a specified color."""
        for key in range(self.deck.key_count()):
            image = PILHelper.create_image(self.deck, background=color)
            self.deck.set_key_image(key, PILHelper.to_native_format(self.deck, image))

    def update_warnings(self, is_bad_posture, frame, angle=None, horizontal_distance=None):
        """
        Update warnings based on posture evaluation.
        - is_bad_posture: Boolean indicating if the posture is bad.
        - frame: The current video frame (for visualizations).
        - angle: The calculated angle (optional, for displaying on the frame).
        - horizontal_distance: The calculated horizontal distance (optional, for displaying on the frame).
        """
        if is_bad_posture:
            if self.bad_posture_start_time is None:
                self.bad_posture_start_time = time.time()

            bad_posture_duration = time.time() - self.bad_posture_start_time
            if bad_posture_duration >= 3:
                # Trigger warning after 3 seconds of bad posture
                self.set_all_keys_color((255, 0, 0))  # Red for bad posture
                posture_status = "Bad Posture"
            else:
                posture_status = "Bad Posture (Pending)"
        else:
            self.bad_posture_start_time = None
            self.set_all_keys_color((0, 255, 0))  # Green for good posture
            posture_status = "Good Posture"

        # Display information on the frame
        self._display_metrics(frame, posture_status, angle, horizontal_distance)

    def _display_metrics(self, frame, posture_status, angle, horizontal_distance):
        """Display posture metrics (status, angle, distance) on the video frame."""
        color = (0, 255, 0) if posture_status == "Good Posture" else (0, 0, 255)
        cv2.putText(frame, f"Status: {posture_status}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        if angle is not None:
            cv2.putText(frame, f"Angle: {int(angle)} deg", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        if horizontal_distance is not None:
            cv2.putText(frame, f"Distance: {int(horizontal_distance)} px", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    def reset(self):
        """Reset posture warnings and Stream Deck state."""
        self.bad_posture_start_time = None
        self.set_all_keys_color((0, 255, 0))

    def close(self):
        """Close the Stream Deck connection."""
        self.deck.reset()
        self.deck.close()
