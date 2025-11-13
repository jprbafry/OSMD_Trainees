import pyqtgraph as pg
import logging

from dash_pyqtgraph.GUI.widget import WHITE, BLACK


def run_widget_demo(draw_callback, update_callback = None, extra_arg = None):
    logger = logging.getLogger("Demo")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    logger.addHandler(ch)
    try:
        # basic pyqtgraph setups
        pg.setConfigOptions(antialias=True)
        pg.setConfigOption('background', WHITE)   # white background
        pg.setConfigOption('foreground', BLACK)   # black axes/text
        app = pg.mkQApp("Dashboard")
        view = pg.GraphicsView()
        scene = pg.GraphicsScene()
        if extra_arg is not None:
            draw_callback(scene, extra_arg)
        else:
            draw_callback(scene)
        if update_callback is not None:
            update_callback(True)

        view.setScene(scene)
        view.setWindowTitle("Demo")
        view.resize(400, 300)

        if extra_arg is not None:
            logging.getLogger("log_window").info("No sensor data received.")

        view.show()
        app.exec()

    except KeyboardInterrupt:
        view.close()
        app.quit()
