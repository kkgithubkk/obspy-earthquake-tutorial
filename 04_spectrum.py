"""04: 周波数を調べる（FFT・スペクトログラム）"""

# ---------------------------------------------------------------
# ライブラリの読み込み
# ---------------------------------------------------------------
import matplotlib.pyplot as plt  # グラフを描くライブラリ
import numpy as np  # 数値計算ライブラリ（FFT に使う）
from obspy import read, read_events  # 波形・震源情報を読み込む関数

# ---------------------------------------------------------------
# データを読み込む
# ---------------------------------------------------------------
st_vel = read("data/noto_IU.MAJO_vel.mseed")  # 03 で保存した速度 [m/s] の波形
events = read_events("data/noto_event.xml")   # 震源情報の一覧（今回は 1 件）
origin = events[0].preferred_origin()          # 1 件目の地震の震源（発生時刻など）

tr = st_vel.select(channel="BHZ")[0]   # 上下方向（Z）の波形を 1 本取り出す
fs = tr.stats.sampling_rate            # サンプリング周波数（1 秒あたりのデータ数。今回は 40）

# ---------------------------------------------------------------
# 1. FFT で「地震前」と「地震後」の周波数の成分を比べる
# ---------------------------------------------------------------
# 比べる 2 つの区間を切り出す（どちらも 100 秒間）
noise = tr.slice(origin.time - 110, origin.time - 10)   # 地震前: 発生の 110 秒前 〜 10 秒前
signal = tr.slice(origin.time + 10, origin.time + 110)  # 地震後: 発生の 10 秒後 〜 110 秒後

fig1 = plt.figure(figsize=(7, 4.5))   # 図を用意する

for w, label in [(noise, "before earthquake"), (signal, "after earthquake")]:  # 2 つの区間を順に
    amp = np.abs(np.fft.rfft(w.data)) / fs                # FFT して、各周波数の振幅を求める
    freq = np.fft.rfftfreq(w.stats.npts, d=1 / fs)        # 振幅の配列に対応する周波数 [Hz] の配列
    plt.loglog(freq[1:], amp[1:], label=label)            # 両対数グラフで描く（0 Hz は除く）

plt.xlabel("Frequency [Hz]")        # 横軸のラベル: 周波数
plt.ylabel("Amplitude")             # 縦軸のラベル: 振幅
plt.legend()                        # 凡例（地震前 / 地震後）を表示する
plt.tight_layout()                  # 文字が見切れないように余白を調整する
fig1.savefig("fig/04_fft.png", dpi=150)  # 画像ファイルとして保存する

# ---------------------------------------------------------------
# 2. スペクトログラムで「いつ・どの周波数が強いか」を見る
# ---------------------------------------------------------------
fig2, ax = plt.subplots(figsize=(10, 4))   # 図と、描画する領域（ax）を用意する

# 地震発生の 60 秒前 〜 600 秒後 を切り出す
tr_part = tr.slice(origin.time - 60, origin.time + 600)

# スペクトログラムを描く
tr_part.spectrogram(
    log=True,       # 縦軸（周波数）を対数目盛にする
    wlen=20,        # 20 秒ずつの区間に分けて FFT する
    per_lap=0.9,    # 区間を 90% ずつ重ねながらずらす（なめらかな図になる）
    dbscale=True,   # 色の強さをデシベル（対数）で表す
    axes=ax,        # 用意した領域に描く
)

ax.set_ylim(0.05, 20)             # 縦軸の範囲: 0.05〜20 Hz
ax.set_xlabel("Time [s]")          # 横軸のラベル: 切り出した区間の先頭からの秒数
ax.set_ylabel("Frequency [Hz]")    # 縦軸のラベル: 周波数
fig2.savefig("fig/04_spectrogram.png", dpi=150)  # 画像ファイルとして保存する

# ---------------------------------------------------------------
# 作った図をウィンドウで表示する（すべて閉じるとスクリプトが終わる）
# ---------------------------------------------------------------
plt.show()
