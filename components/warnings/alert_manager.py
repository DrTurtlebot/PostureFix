import time

class PostureAlertManager:
    def __init__(self):
        self.bad_posture_start_time = None

    def should_alert(self, is_bad_posture):
        """
        Add extra logic here just incase it needs to be
        - is_bad_posture: Boolean indicating if the posture is bad.
        """
        if is_bad_posture:
            return True
        else:
            self.bad_posture_start_time = None
            return False  # Reset timer and do not alert
