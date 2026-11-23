"""04: 周波数を調べる（FFT・スペクトログラム）"""
import matplotlib.pyplot as plt
import numpy as np
from obspy import read, read_events

st_vel = read("data/noto_IU.MAJO_vel.mseed")  # 03 で作った速度波形
origin = read_events("data/noto_event.xml")[0].preferred_origin()

tr = st_vel.select(channel="BHZ")[0]
fs = tr.stats.sampling_rate

# FFT で地震前と地震後を比べる
noise = tr.slice(origin.time - 110, origin.time - 10)   # 地震前の 100 秒
signal = tr.slice(origin.time + 10, origin.time + 110)  # 地震後の 100 秒

for w, label in [(noise, "before earthquake"), (signal, "after earthquake")]:
    amp = np.abs(np.fft.rfft(w.data)) / fs
    freq = np.fft.rfftfreq(w.stats.npts, d=1 / fs)
    plt.loglog(freq[1:], amp[1:], label=label)
plt.xlabel("Frequency [Hz]")
plt.legend()
plt.savefig("fig/04_fft.png", dpi=150)

# スペクトログラム
fig, ax = plt.subplots(figsize=(10, 4))
tr.slice(origin.time - 60, origin.time + 600).spectrogram(
    log=True, wlen=20, per_lap=0.9, dbscale=True, axes=ax
)
ax.set_ylim(0.05, 20)
ax.set_xlabel("Time [s]")
ax.set_ylabel("Frequency [Hz]")
fig.savefig("fig/04_spectrogram.png", dpi=150)

plt.show()  # 図をウィンドウで表示（閉じるとスクリプトが終わります）
