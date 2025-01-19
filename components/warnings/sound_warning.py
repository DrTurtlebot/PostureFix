try:
    import winsound

    def playsound(frequency, duration):
        winsound.Beep(frequency, duration)

except ImportError:
    import os

    def playsound(frequency, duration):
        os.system('beep -f %s -l %s' % (frequency,duration))



class SoundWarning:
    def __init__(self, alert_manager):
        """Initialize the sound warning system."""
        self.alert_manager = alert_manager

    def update(self, is_bad_posture):
        if self.alert_manager.should_alert(is_bad_posture):
            playsound(1000, 500)  # Frequency: 1000Hz, Duration: 500ms
