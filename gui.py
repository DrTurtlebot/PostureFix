import tkinter as tk
from tkinter import ttk, StringVar
import os
import json

class PostureGUI:
    SETTINGS_FILE = "settings.txt"

    def __init__(self, root, default_angle=160, default_distance_ratio=0.05, default_alert_method="GUI", default_timeout=3):
        """
        Initialize the GUI for posture settings.
        """
        self.root = root
        self.root.title("Posture Detection Settings")
        self.root.geometry("400x600")
        self.is_dark_mode = False  # Default to light mode

        # Load settings or use defaults
        self.settings = self.load_settings(default_angle, default_distance_ratio, default_alert_method, default_timeout)
        self.angle_threshold = tk.DoubleVar(value=self.settings["angle_threshold"])
        self.distance_threshold_ratio = tk.DoubleVar(value=self.settings["distance_threshold_ratio"])
        self.alert_method = StringVar(value=self.settings["alert_method"])
        self.timeout = tk.IntVar(value=self.settings["timeout"])

        # Configure styles
        self.style = ttk.Style()
        self.configure_styles()

        # Create GUI elements
        self.create_widgets()
        self.apply_theme()  # Apply the initial theme

    def create_widgets(self):
        """Create the GUI widgets."""
        # Dark Mode Toggle
        self.dark_mode_button = ttk.Button(
            self.root, text="🌞 Light Mode", command=self.toggle_dark_mode, style="TButton"
        )
        self.dark_mode_button.pack(pady=10)

        # Angle Threshold
        ttk.Label(self.root, text="Angle Threshold (degrees):", style="TLabel").pack(pady=10)
        self.angle_slider = tk.Scale(
            self.root, from_=90, to=180, resolution=1, variable=self.angle_threshold, orient=tk.HORIZONTAL
        )
        self.angle_slider.pack(fill=tk.X, padx=20)

        # Distance Threshold Ratio
        ttk.Label(self.root, text="Distance Threshold Ratio:", style="TLabel").pack(pady=10)
        self.distance_slider = tk.Scale(
            self.root, from_=0.01, to=0.5, resolution=0.01, variable=self.distance_threshold_ratio, orient=tk.HORIZONTAL
        )
        self.distance_slider.pack(fill=tk.X, padx=20)

        # Alert Method
        ttk.Label(self.root, text="Alert Method:", style="TLabel").pack(pady=10)
        self.alert_dropdown = ttk.OptionMenu(
            self.root, self.alert_method, self.alert_method.get(), "GUI", "Sound", "StreamDeck"
        )
        self.alert_dropdown.pack()

        # Timeout Setting
        ttk.Label(self.root, text="Timeout (seconds):", style="TLabel").pack(pady=10)
        self.timeout_slider = tk.Scale(
            self.root, from_=0, to=10, resolution=1, variable=self.timeout, orient=tk.HORIZONTAL
        )
        self.timeout_slider.pack(fill=tk.X, padx=20)

        # Show Camera Feed Toggle
        self.show_camera = tk.BooleanVar(value=False)  # Default: show camera feed
        ttk.Checkbutton(
            self.root, text="Show Camera Feed", variable=self.show_camera, style="TCheckbutton"
        ).pack(pady=10)

        # Exit Button
        ttk.Button(self.root, text="Exit", command=self.exit_gui, style="TButton").pack(pady=10)

        # Warning Box for GUI Alert
        self.warning_box = tk.Frame(self.root, width=200, height=50, bg="green")
        self.warning_box.pack(pady=10)

    def configure_styles(self):
        """Define styles for light and dark modes."""
        # Light Mode Styles
        self.style.configure("TButton", background="white", foreground="black", font=("Arial", 12))
        self.style.configure("TLabel", background="white", foreground="black", font=("Arial", 12))

        # Dark Mode Styles
        self.style.map("TButton", background=[("active", "gray"), ("!active", "black")])
        self.style.map("TLabel", background=[("active", "black"), ("!active", "black")])

    def toggle_dark_mode(self):
        """Toggle between light and dark mode."""
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def apply_theme(self):
        """Apply the current theme to the GUI."""
        if self.is_dark_mode:
            # Dark Mode
            self.root.configure(bg="black")
            self.dark_mode_button.configure(text="🌙 Dark Mode")
            self.style.configure("TButton", background="black", foreground="black")
            self.style.configure("TLabel", background="black", foreground="white")
            self.style.configure("TOptionMenu", background="black", foreground="white")
            self.angle_slider.configure(bg="black", fg="white", highlightbackground="white")
            self.distance_slider.configure(bg="black", fg="white", highlightbackground="white")
        else:
            # Light Mode
            self.root.configure(bg="white")
            self.dark_mode_button.configure(text="🌞 Light Mode")
            self.style.configure("TButton", background="white", foreground="black")
            self.style.configure("TLabel", background="white", foreground="black")
            self.style.configure("TOptionMenu", background="white", foreground="black")
            self.angle_slider.configure(bg="white", fg="black", highlightbackground="black")
            self.distance_slider.configure(bg="white", fg="black", highlightbackground="black")

        # Force-update all existing labels' backgrounds
        for child in self.root.winfo_children():
            if isinstance(child, ttk.Label):
                child.configure(background=self.root["bg"])

    def load_settings(self, default_angle, default_distance_ratio, default_alert_method, default_timeout):
        """Load settings from the settings file or use defaults."""
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, "r") as file:
                    settings = json.load(file)
                
                # Ensure all keys exist; add missing keys with default values
                settings.setdefault("angle_threshold", default_angle)
                settings.setdefault("distance_threshold_ratio", default_distance_ratio)
                settings.setdefault("alert_method", default_alert_method)
                settings.setdefault("timeout", default_timeout)

                return settings
            except Exception as e:
                print(f"Error reading settings file: {e}")

        # Return default settings if file doesn't exist or is corrupted
        return {
            "angle_threshold": default_angle,
            "distance_threshold_ratio": default_distance_ratio,
            "alert_method": default_alert_method,
            "timeout": default_timeout,
        }

    def save_settings(self):
        """Save the current settings to the settings file."""
        settings = {
            "angle_threshold": self.angle_threshold.get(),
            "distance_threshold_ratio": self.distance_threshold_ratio.get(),
            "alert_method": self.alert_method.get(),
            "timeout": self.timeout.get(),
        }
        try:
            with open(self.SETTINGS_FILE, "w") as file:
                json.dump(settings, file)
        except Exception as e:
            print(f"Error saving settings file: {e}")

    def exit_gui(self):
        """Exit the GUI and save settings."""
        self.save_settings()
        self.root.destroy()

    def get_angle_threshold(self):
        """Return the current angle threshold."""
        return self.angle_threshold.get()

    def get_distance_threshold_ratio(self):
        """Return the current distance threshold ratio."""
        return self.distance_threshold_ratio.get()

    def get_alert_method(self):
        """Return the selected alert method."""
        return self.alert_method.get()

    def get_timeout(self):
        """Return the timeout setting."""
        return self.timeout.get()

    def is_camera_enabled(self):
        """Return whether the camera feed should be displayed."""
        return self.show_camera.get()

    def set_gui_alert(self, color):
        """Update the warning box color."""
        self.warning_box.configure(bg=color)
