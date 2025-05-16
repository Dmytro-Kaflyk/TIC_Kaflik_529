import numpy as np
from scipy import signal, fft
import matplotlib.pyplot as plt
import os

n = 500
Fs = 1000
F_max = 17

a = 0
b = 10
signal_raw = np.random.normal(a, b, n)

time = np.arange(n) / Fs

w = F_max / (Fs / 2)
sos = signal.butter(3, w, 'low', output='sos')
filtered_signal = signal.sosfiltfilt(sos, signal_raw)

def plot_signal(x, y, title, xlabel, ylabel):
    if not os.path.exists('./figures'):
        os.makedirs('./figures')

    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.plot(x, y, linewidth=1)
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    plt.title(title, fontsize=14)
    plt.tight_layout()
    filepath = f'./figures/{title}.png'
    fig.savefig(filepath, dpi=600)
    plt.show()

plot_signal(time, filtered_signal, "Відфільтрований_сигнал", "Час (с)", "Амплітуда")

spectrum = fft.fft(filtered_signal)
spectrum_shifted = np.abs(fft.fftshift(spectrum))
freqs = fft.fftshift(fft.fftfreq(n, 1 / Fs))

plot_signal(freqs, spectrum_shifted, "Спектр_сигналу", "Частота (Гц)", "Амплітуда спектру")
