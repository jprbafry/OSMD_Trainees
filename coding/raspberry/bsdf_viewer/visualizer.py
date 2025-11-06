import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ------------------------------
# Utilities for color conversion
# ------------------------------
def xyz_to_srgb(X, Y, Z):
    """Convert XYZ to sRGB (0-1 range)."""
    M = np.array([
        [3.2406, -1.5372, -0.4986],
        [-0.9689, 1.8758, 0.0415],
        [0.0557, -0.2040, 1.0570]
    ])
    rgb_linear = np.dot(M, np.array([X, Y, Z]))
    rgb_linear = np.clip(rgb_linear, 0, None)
    rgb = np.where(
        rgb_linear <= 0.0031308,
        12.92 * rgb_linear,
        1.055 * (rgb_linear ** (1/2.4)) - 0.055
    )
    return np.clip(rgb, 0, 1)


def read_numbers(lines, start_index, n):
    """Read n floats starting from lines[start_index]."""
    numbers = []
    i = start_index
    while len(numbers) < n and i < len(lines):
        line = lines[i].strip()
        if not line or any(c.isalpha() for c in line):  # stop at header or empty line
            break
        numbers.extend([float(x) for x in line.split()])
        i += 1
    return numbers[:n], i


# ------------------------------
# Data Parsing
# ------------------------------

def read_numbers(lines, start_index, n):
    """
    Safely read n floats starting from lines[start_index].
    Stops if it hits a non-number line (like headers) or end of file.
    Returns the numbers read and the next line index.
    """
    numbers = []
    i = start_index
    while len(numbers) < n and i < len(lines):
        line = lines[i].strip()
        if not line or any(c.isalpha() for c in line):  # stop at header or empty line
            break
        numbers.extend([float(x) for x in line.split()])
        i += 1
    return numbers[:n], i


import numpy as np

def parse_radiant_file(file_path):
    """
    Parse a Radiant Imaging .bsdf file.
    Returns a dict with:
        - sample_rotations: array of rotations
        - incidence_angles: array of incidence angles
        - azimuths: array of azimuths
        - radials: array of radial scatter angles
        - spectral_content: "XYZ" or "Monochrome"
        - data: either a dict with 'X','Y','Z' 4D arrays (rot, inc, az, rad) if XYZ,
                or a single 4D array (rot, inc, az, rad) if Monochrome
    """
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()

    i = 0
    sample_rotations = []
    incidence_angles = []
    azimuths = []
    radials = []
    spectral_content = None
    data = None

    reading_data = False
    current_matrix = None
    current_values = []

    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("#"):
            i += 1
            continue

        # Spectral content determines parser branch
        if line.startswith("SpectralContent"):
            spectral_content = line.split()[1]
            if spectral_content == "XYZ":
                data = {'X': [], 'Y': [], 'Z': []}
            else:
                data = {'M': []}  # will be 4D array later

        elif line.startswith("SampleRotation"):
            numbers_line = lines[i + 1].strip()
            numbers = [float(x) for x in numbers_line.split()]
            sample_rotations = np.array(numbers)
            i += 1

        elif line.startswith("AngleOfIncidence"):
            numbers_line = lines[i + 1].strip()
            numbers = [float(x) for x in numbers_line.split()]
            incidence_angles = np.array(numbers)
            i += 1

        elif line.startswith("ScatterAzimuth"):
            numbers_line = lines[i + 1].strip()
            numbers = [float(x) for x in numbers_line.split()]
            azimuths = np.array(numbers)
            i += 1

        elif line.startswith("ScatterRadial"):
            numbers_line = lines[i + 1].strip()
            numbers = [float(x) for x in numbers_line.split()]
            radials = np.array(numbers)
            i += 1

        # Data sections
        elif spectral_content == "XYZ" and line.startswith("Tristimulus"):
            current_matrix = line[-1]  # 'X','Y','Z'
            current_values = []
            
        elif spectral_content == "Monochrome" and line.startswith("Monochrome"):
            current_matrix = 'M'  # 'X','Y','Z'
            current_values = []

        elif line == "DataBegin":
            reading_data = True

        elif line == "DataEnd":
            reading_data = False
            flat = np.array(current_values).flatten()
            n_rot = len(sample_rotations)
            n_inc = len(incidence_angles)
            n_az = len(azimuths)
            n_rad = len(radials)
            expected_size = n_rot * n_inc * n_az * n_rad

            # pad/truncate if needed
            if flat.size < expected_size:
                flat = np.pad(flat, (0, expected_size - flat.size))
            elif flat.size > expected_size:
                flat = flat[:expected_size]

            reshaped = flat.reshape((n_rot, n_inc, n_az, n_rad))
            
            data[current_matrix] = reshaped

        elif reading_data:
            # Skip TIS lines
            if line.startswith("TIS"):
                pass
            else:
                numbers = [float(x) for x in line.split()]
            current_values.append(numbers)

        i += 1

    return {
        'sample_rotations': np.array(sample_rotations),
        'incidence_angles': np.array(incidence_angles),
        'azimuths': np.array(azimuths),
        'radials': np.array(radials),
        'spectral_content': spectral_content,
        'spectral_data': data
    }


# ------------------------------
# Main
# ------------------------------
if __name__ == "__main__":
    file_path = "bsdf_mon.bsdf"  # Replace with your filename
    data = parse_radiant_file(file_path)

    sample_rotations = data ['sample_rotations']
    incidence_angles = data['incidence_angles']
    azimuths = data['azimuths']
    radials = data['radials']
    spectral_data = data['spectral_data']


    # ---------------------------
    # 1. Normalize data
    # ---------------------------

    spectral_data = spectral_data['M']    
    spectral_data = spectral_data / np.max(spectral_data)



    # -----------------------------
    # Interactive plot setup
    # -----------------------------
    fig = plt.figure(figsize=(10, 8))

    # Axes positions: [left, bottom, width, height]
    ax_slider_v = fig.add_axes([0.05, 0.2, 0.02, 0.6])  # vertical slider, 5× thinner
    ax_slider_h = fig.add_axes([0.15, 0.05, 0.7, 0.02]) # horizontal slider, 5× thinner
    ax_polar = fig.add_axes([0.15, 0.2, 0.7, 0.6], polar=True)
    cax = fig.add_axes([0.88, 0.2, 0.03, 0.6])  # colorbar aligned with vertical slider

    # Initial indices
    idx_rot = 0
    idx_inc = 0

    # -----------------------------
    # Create initial polar plot
    # -----------------------------
    theta = np.radians(azimuths)
    data_to_plot = spectral_data[idx_rot, idx_inc, :, :]
    im = ax_polar.pcolormesh(theta, radials, data_to_plot.T, shading='auto', cmap='inferno')

    # White lines and ticks
    ax_polar.set_facecolor('black')
    ax_polar.grid(color='white', linestyle='--', linewidth=0.5)
    ax_polar.tick_params(colors='white')
    ax_polar.set_yticklabels([])  # hides the labels but keeps the tick marks/circles
    theta_ticks = np.arange(0, 360, 10)
    ax_polar.set_xticks(np.radians(theta_ticks))
    ax_polar.set_xticklabels([str(t) for t in theta_ticks], color='black')



    # Colorbar
    cb = plt.colorbar(im, cax=cax)
    cb.set_label('Normalized intensity')

    # -----------------------------
    # Sliders
    # -----------------------------
    slider_v = Slider(
        ax_slider_v,
        'Angle\nOf\nIncidence',
        0,
        len(incidence_angles) - 1,
        valinit=idx_inc,
        valstep=1,
        orientation='vertical'
    )

    slider_h = Slider(
        ax_slider_h,
        'Sample\nRotation',
        0,
        len(sample_rotations) - 1,
        valinit=idx_rot,
        valstep=1,
        orientation='horizontal'
    )

    # -----------------------------
    # Update function
    # -----------------------------
    def update(val):
        idx_inc = int(slider_v.val)
        idx_rot = int(slider_h.val)

        # Update data
        new_data = spectral_data[idx_rot, idx_inc, :, :]
        im.set_array(new_data.T.ravel())

        # Update slider labels to show actual values
        slider_v.valtext.set_text(f"{incidence_angles[idx_inc]}")
        slider_h.valtext.set_text(f"{sample_rotations[idx_rot]}")

        fig.canvas.draw_idle()

    slider_v.on_changed(update)
    slider_h.on_changed(update)

    plt.show()
