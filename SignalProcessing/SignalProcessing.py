import numpy as np
from scipy import signal, fft
import matplotlib.pyplot as plt
import os

n = 500
Fs = 1000
F_max = 17
F_filter = 24

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

discrete_signals = []
discrete_spectrums = []
restored_signals = []
variance_diff = []
snr_list = []

w_filter = F_filter / (Fs / 2)

for Dt in [2, 4, 8, 16]:
    discrete_signal = np.zeros(n)
    for i in range(round(n / Dt)):
        discrete_signal[int(i * Dt)] = filtered_signal[int(i * Dt)]
    discrete_signals.append(list(discrete_signal))

    spectrum_ds = fft.fft(discrete_signal)
    discrete_spectrums.append(list(np.abs(fft.fftshift(spectrum_ds))))

    sos_filter = signal.butter(3, w_filter, 'low', output='sos')
    restored = signal.sosfiltfilt(sos_filter, discrete_signal)
    restored_signals.append(restored)

    E1 = restored - filtered_signal
    var_signal = np.var(filtered_signal)
    var_diff = np.var(E1)
    variance_diff.append(var_diff)
    snr_list.append(var_signal / var_diff)

fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(2):
    for j in range(2):
        ax[i][j].plot(time, discrete_signals[s], linewidth=1)
        ax[i][j].set_title(f'Дискретизований сигнал Dt={[2, 4, 8, 16][s]}', fontsize=14)
        s += 1
fig.supxlabel("Час (с)", fontsize=14)
fig.supylabel("Амплітуда", fontsize=14)
fig.suptitle("Дискретизовані сигнали", fontsize=14)
plt.tight_layout()
fig.savefig('./figures/Дискретизовані_сигнали.png', dpi=600)
plt.show()

fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(2):
    for j in range(2):
        ax[i][j].plot(freqs, discrete_spectrums[s], linewidth=1)
        ax[i][j].set_title(f'Спектр Dt={[2, 4, 8, 16][s]}', fontsize=14)
        s += 1
fig.supxlabel("Частота (Гц)", fontsize=14)
fig.supylabel("Амплітуда спектру", fontsize=14)
fig.suptitle("Спектри дискретизованих сигналів", fontsize=14)
plt.tight_layout()
fig.savefig('./figures/Спектри_дискретизованих_сигналів.png', dpi=600)
plt.show()

fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(2):
    for j in range(2):
        ax[i][j].plot(time, restored_signals[s], linewidth=1)
        ax[i][j].set_title(f'Відновлений сигнал Dt={[2, 4, 8, 16][s]}', fontsize=14)
        s += 1
fig.supxlabel("Час (с)", fontsize=14)
fig.supylabel("Амплітуда", fontsize=14)
fig.suptitle("Відновлені аналогові сигнали", fontsize=14)
plt.tight_layout()
fig.savefig('./figures/Відновлені_аналогові_сигнали.png', dpi=600)
plt.show()

plt.figure(figsize=(8, 6))
plt.plot([2, 4, 8, 16], variance_diff, marker='o')
plt.xlabel("Крок дискретизації Dt", fontsize=14)
plt.ylabel("Дисперсія різниці", fontsize=14)
plt.title("Залежність дисперсії різниці від кроку дискретизації", fontsize=14)
plt.grid(True)
plt.tight_layout()
plt.savefig('./figures/Дисперсія_різниці.png', dpi=600)
plt.show()

plt.figure(figsize=(8, 6))
plt.plot([2, 4, 8, 16], snr_list, marker='o')
plt.xlabel("Крок дискретизації Dt", fontsize=14)
plt.ylabel("Співвідношення сигнал-шум", fontsize=14)
plt.title("Залежність співвідношення сигнал-шум від кроку дискретизації", fontsize=14)
plt.grid(True)
plt.tight_layout()
plt.savefig('./figures/Співвідношення_сигнал_шум.png', dpi=600)
plt.show()
