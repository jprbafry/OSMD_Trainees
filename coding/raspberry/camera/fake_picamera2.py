import numpy as np
import cv2
import threading
import time
import math

class FakePicamera2:
    def __init__(self):
        self.resolution = (1088, 1456, 3)
        self._running = False
        self._thread = None
        self._current_frame = np.zeros(self.resolution, dtype=np.uint8)
        self._lock = threading.Lock()
        print("[Stub] Picamera2 initialized (dynamic fake camera).")

    def create_preview_configuration(self, *args, **kwargs):
        return {"type": "preview", "size": (1456, 1088)}

    def configure(self, config):
        print(f"[Stub] configure called: {config}")

    def start(self):
        print("[Stub] Starting fake camera animation thread...")
        self._running = True
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()

    def stop(self):
        print("[Stub] Stopping fake camera thread.")
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)
     
    def _animate(self):
        H, W, _ = self.resolution
        center = (W // 2, H // 2)
        R = 240
        T = 5
        amplitude = 0.7  # how much the ellipse stretches

        while self._running:
            for rot_deg in range(360):
                if not self._running:
                    return
                angle = rot_deg
                for ecc_step in range(360):
                    if not self._running:
                        return
                    ecc_factor = abs(math.cos(math.radians(ecc_step)))
                    width = int(R * (1 + amplitude * max(0, ecc_factor)))   # major axis
                    height = R  # minor axis
                    width = max(width, height)

                    # --- Create noisy background ---
                    base_img = np.random.randint(20, 80, (H, W, 3), dtype=np.uint8)

                    # --- Draw ellipse + ring on separate layer ---
                    ellipse_layer = np.zeros((H, W, 3), dtype=np.uint8)
                    # Filled inner ellipse
                    cv2.ellipse(ellipse_layer, center, (width - T, height - T), angle, 0, 360, (180, 180, 180), -1)
                    # Ring
                    cv2.ellipse(ellipse_layer, center, (width, height), angle, 0, 360, (100, 100, 100), T)

                    # --- Apply Gaussian blur to the whole ellipse layer ---
                    blurred_ellipse = cv2.GaussianBlur(ellipse_layer, (11, 11), sigmaX=5, sigmaY=5)

                    # --- Overlay blurred ellipse onto background ---
                    base_img = cv2.addWeighted(base_img, 1.0, blurred_ellipse, 1.0, 0)

                    # --- Save to current frame ---
                    with self._lock:
                        self._current_frame = base_img

                    time.sleep(0.001)  # 10 ms per frame (~100 fps),




    def capture_array(self, *args, **kwargs):
        with self._lock:
            return self._current_frame.copy()

    def capture_file(self, filename, *args, **kwargs):
        frame = self.capture_array()
        cv2.imwrite(filename, frame)
        print(f"[Stub] Saved current frame to {filename}")

# Optional alias for compatibility
Picamera2 = FakePicamera2
