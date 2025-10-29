import Bar
import pygame
import threading
import time
import os
import sys


#print(f"{os.path.dirname(__file__)}")
sys.path.append(os.path.join(os.path.dirname(__file__),  "..",  "demo_fair"))
from mux_tx_rx import SerialManager


class TemperatureReceiver:
    """Handles incoming temperature data from SerialManager."""
    def __init__(self):
        self._value = 16.0
        self.sm = SerialManager(simulate=True, name='B', port="", baud=19200, debug=False)
        self.sm.on_receive = self.on_receive
        self.sm.start()

    def on_receive(self, msg):
        print(msg)
        try:
            if msg.startswith("TEMP:"):
                self._value = float(msg.split(":")[1])
            else:
                self._value = float(msg)
        except Exception as e:
            print(f"Invalid temperature received: {msg} ({e})")

    def get_value(self):
        return self._value


class TemperatureBarApp:
    """Main pygame window for visualizing the temperature bar."""
    def __init__(self):
        pygame.init()
        WIDTH, HEIGHT = 400, 400
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Temperature Bar")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

        # Receiver for temperature data
        self.receiver = TemperatureReceiver()

        # Create the bar
        self.temperature_bar = Bar.Bar(
            x=100, y=100, width=50, height=255,
            min_val=0, max_val=60,
            colors=[(0, 0, 255), (255, 255, 255), (255, 0, 0)],
            label="Temperature",
            font=self.font,
            surface=self.screen
        )

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update bar using latest temperature from receiver
            current_temp = self.receiver.get_value()
            self.temperature_bar.set_value(current_temp)
            self.temperature_bar.draw()

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()


if __name__ == "__main__":
    app = TemperatureBarApp()
    app.run()