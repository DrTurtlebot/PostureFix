class PostureEvaluator:
    def __init__(self, angle_threshold=160, distance_threshold_ratio=0.05):
        self.angle_threshold = angle_threshold
        self.distance_threshold_ratio = distance_threshold_ratio

    def evaluate_posture(self, angle, horizontal_distance, frame_width):
        distance_threshold = frame_width * self.distance_threshold_ratio  # Calculate threshold
        return angle < self.angle_threshold or horizontal_distance > distance_threshold