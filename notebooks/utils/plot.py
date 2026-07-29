'''
This file contains all of the utility functions for plotting data in the Jupyter notebooks. 
It is separated from the main notebook to avoid circular imports and to keep the notebook clean and organized.
'''


import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np

def plot_spectrogram(data : np.ndarray, samp_rate: int, center_feq: int):
    '''
    Plot the spectrogram of the given IQ data.
    
    Args:
        data (np.ndarray): The IQ data to plot.
        samp_rate (int): The sample rate of the IQ data.
        center_feq (int): The center frequency of the IQ data.
    '''

    plt.figure(figsize=(10, 6))
    Pxx, freqs, bins = mlab.specgram(x=data, NFFT=4096, Fs=samp_rate, noverlap=2048)

    # Transpose the axes (switch time and frequency)
    plt.pcolormesh(freqs, bins, 10 * np.log10(Pxx.T), shading='auto')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Time [sec]')
    plt.colorbar(label='Intensity [dB]')
    plt.show()
