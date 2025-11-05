# GUI Module

The `GUI` folder is a Python module containing a collection of visual widgets for your dashboard project. It is structured for modularity and easy testing of each widget.

---

## Folder Structure
```
GUI/
├── init.py # Makes GUI a Python module
├── bar.py # Bar widget class
├── knob.py # Knob widget class
├── label.py # Label widget class
├── logbox.py # Log box widget class
├── panel.py # Panel class
├── plotter.py # Plotter widget class
├── slider.py # Slider widget class
├── widget.py # Base Widget class and global colors
├── demo.py # run_widget_demo() for running widget demos
```

---

## What This Module Contains

- **`widget.py`**  
  Defines the base `Widget` class and global colors used by all widgets.  

- **Widget Classes (`bar.py`, `knob.py`, `label.py`, etc.)**  
  Each file defines a specific visual widget class inheriting from `Widget`.  

- **`demo.py`**  
  Contains a reusable `run_widget_demo()` function to run any widget in a Pygame window.  

- **`__init__.py`**  
  Allows `GUI` to be imported as a Python module.

---

## How to Run Widgets

Each widget file includes a **demo section** that can be run directly. 

```python
if __name__ == "__main__":
    from dash_pygame.GUI import demo

    ...

    demo.run_widget_demo(...)

```

To run the demos:
```bash
python -m dash_pygame.GUI.knob
python -m dash_pygame.GUI.bar
python -m dash_pygame.GUI.plotter
...
```