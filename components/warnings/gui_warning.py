class GUIWarning:
    def __init__(self, gui, alert_manager):
        """Initialize the GUI warning system."""
        self.gui = gui
        self.alert_manager = alert_manager

    def update(self, is_bad_posture, alert_method):
        """
        Update the GUI warning box after the delay.
        - is_bad_posture: Boolean indicating if the posture is bad.
        - alert_method: The currently selected alert method.
        """
        if alert_method == "GUI":
            if self.alert_manager.should_alert(is_bad_posture):
                self.gui.set_gui_alert("red")  # Red for bad posture
            else:
                self.gui.set_gui_alert("green")  # Green for good posture
        else:
            self.gui.set_gui_alert("gray")  # Gray when GUI is not active
