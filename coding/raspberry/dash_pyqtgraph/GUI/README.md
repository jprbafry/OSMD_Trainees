# GUI Module

The `GUI` folder is a Python module containing a collection of visual widgets and constants for the dashboard. It is structured for modularity.

---

## Folder Structure
```
GUI/
├── init.py # Makes GUI a Python module
├── button.py # button for home switches
├── color_bar.py # color bars for temperature and light intensity
├── detector_window.py # window for detector feed
├── knob.py # knobs for azimuthal rotation
├── log_window.py # window for showing real-time logging
├── sinusoidal.py # sinusoidal graphs for accelerator and gyroscope
├── slider.py # sliders for polar rotations
├── tree.avi # fake video to play for the detector window
└── widget.py # base class
```

---

## What This Module Contains

- **`widget.py`**  
  Defines the base `Widget` class and global colors used by all widgets.  

- **Widget Classes (`button.py`, `color_bar.py`, `knob.py`, etc.)**  
  Each file defines a specific visual widget class inheriting from `Widget`.  

- **`__init__.py`**  
  Allows `GUI` to be imported as a Python module.