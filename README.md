
# PostureFix 

## What is it?

**PostureFix** is a Python-based application designed to help users maintain good posture while working at their desks. It uses a webcam to monitor posture, alerting users when they slouch or adopt bad posture habits. The program is customizable, allowing users to adjust sensitivity thresholds, alert methods, and more, making it a versatile tool for ergonomic improvement.

![PostureFix in action](https://temp)  <!-- Update with an actual image link -->

---

## Why is it?

I've been struggling with bad desk posture, which has started to affect my comfort and productivity. I made **PostureFix** to give myself a bit of a push to get better and build healthier habits while working. If you're in the same boat, I hope this tool helps you too!

---

## Key Features

- 🎥 **Real-time Posture Monitoring**: Uses a webcam to evaluate posture based on body landmarks.
- 🎨 **Customizable Settings**: Adjust angle thresholds, timeout duration, and alert methods to suit your needs.
- 🌓 **Dark/Light Mode**: Switch between light and dark themes for better user experience.
- 🔔 **Multiple Alert Methods**:
  - Visual: On-screen notifications with customizable colors.
  - Audio: Alerts with customizable tones.
  - Stream Deck: Compatible with Elgato Stream Deck for tactile feedback.
- 🖥️ **Camera Feed Toggle**: Choose whether to display the live webcam feed.
- 💾 **Persistent Settings**: Automatically saves your preferences in a settings file.

---

## How to Set It Up

### Prerequisites

- Python 3.8 or higher
- A webcam
- Compatible operating system (Windows, macOS, or Linux)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/posturefix.git
   cd posturefix
   ```

2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

4. **Camera Placement**:
   - Place the camera at a **90-degree angle to your body**, ensuring it is **inline with your shoulders**. This positioning is crucial for accurate posture detection.

---

## Customization Options

- **Angle Threshold**: Adjust the shoulder-to-ear angle that determines good posture.

- **Distance Threshold**: Set the distance ratio for detecting slouching.
- **Timeout**: Choose how long bad posture must persist before triggering an alert.
- **Alert Methods**:
  - GUI notifications (green/red alert box)
  - Sound alerts (beep notifications)
  - Stream Deck integration for tactile feedback
- **Dark/Light Mode**: Switch between modes for better visibility.

---

## System Overview

### Application Components

1. **Camera Module**: Captures webcam input and preprocesses frames.

2. **Pose Detection**: Uses `MediaPipe` to detect body landmarks.
3. **Posture Evaluation**: Determines whether the posture is good or bad based on thresholds.
4. **Alert Manager**: Orchestrates alerts based on the user’s selected methods.
5. **GUI**: Provides an intuitive interface for managing settings.

### Technologies Used

- **Python**
- **Tkinter** for the graphical user interface
- **OpenCV** for video capture and frame processing
- **MediaPipe** for posture detection
- **Elgato Stream Deck SDK** for physical alerts
- **Winsound** and OS-specific tools for sound notifications

---

## Usage Tips

- Use the **timeout slider** to control how long bad posture must persist before alerts are triggered.

- Toggle the **camera feed** on/off to focus on posture feedback without distraction.

- Adjust thresholds to match your seating habits.

---

## A Note from the Author

This project was created very quickly as a beta and is not fully finished. While it works as intended, there are areas that could be improved or optimized. Feel free to explore, test, and share your feedback or suggestions for enhancements. Thank you for checking out PostureFix!

---

## License

```
MIT License

Copyright (c) 2025 Alex Dalton

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, and/or distribute copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

2. Selling this software or its source code is not permitted. Any distribution of the software must be free of charge, and the source code must remain free to download if published.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

---
