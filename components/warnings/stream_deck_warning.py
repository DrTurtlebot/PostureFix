from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

class StreamDeckWarning:
    def __init__(self, alert_manager):
        """Initialize Stream Deck and posture tracking variables."""
        self.streamdecks = DeviceManager().enumerate()
        if not self.streamdecks:
            raise Exception("No Stream Decks found.")
        self.deck = self.streamdecks[0]
        self.deck.open()
        self.deck.reset()
        self.alert_manager = alert_manager

    def set_all_keys_color(self, color):
        """Set all keys on the Stream Deck to a specified color."""
        for key in range(self.deck.key_count()):
            image = PILHelper.create_image(self.deck, background=color)
            self.deck.set_key_image(key, PILHelper.to_native_format(self.deck, image))

    def update_warnings(self, is_bad_posture, frame, angle=None, horizontal_distance=None):
        """
        Update warnings on the Stream Deck after the delay.
        - is_bad_posture: Boolean indicating if the posture is bad.
        """
        if self.alert_manager.should_alert(is_bad_posture):
            self.set_all_keys_color((255, 0, 0))  # Red for bad posture
        else:
            self.set_all_keys_color((0, 255, 0))  # Green for good posture

    def reset(self):
        """Reset posture warnings and Stream Deck state."""
        self.alert_manager.bad_posture_start_time = None
        self.set_all_keys_color((0, 255, 0))

    def close(self):
        """Close the Stream Deck connection."""
        self.deck.reset()
        self.deck.close()
