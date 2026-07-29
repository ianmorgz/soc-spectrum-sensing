'''
Folder for loading the data from the data folder to avoid circular imports inside of the Jupyter notebooks.
'''

# import sys
# # sys.path.append('../data')
import numpy as np
from pathlib import Path

def load_iq_data(filename: str) -> np.ndarray:
    """
    Load IQ data from a .bin file containing interleaved I and Q samples off of the USRP.

    Args:
        filename (str): The name of the .npy file to load.

    Returns:
        np.ndarray: The loaded IQ data as a NumPy array.
    """
    file_path = Path.joinpath(Path.cwd(), "../data", filename)

    try:
        raw_data = np.fromfile(file_path, dtype=np.float32)
        iq_data = raw_data[::2] + 1j * raw_data[1::2]
    except FileNotFoundError:
        raise FileNotFoundError("Signal file not found.")
    return iq_data