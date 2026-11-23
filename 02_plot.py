"""02: 波形をグラフにして、P 波・S 波の到着時刻を重ねる"""

# ---------------------------------------------------------------
# ライブラリの読み込み
# ---------------------------------------------------------------
from pathlib import Path  # フォルダやファイルのパスを扱う標準ライブラリ

import matplotlib.pyplot as plt  # グラフを描くライブラリ
from obspy import read, read_events, read_inventory  # 波形・震源情報・観測点情報を読み込む関数
from obspy.geodetics import gps2dist_azimuth, kilometers2degrees  # 2 点間の距離を計算する関数
from obspy.taup import TauPyModel  # 地震波が届く時刻（走時）を計算するクラス

# 図を保存する fig フォルダを作る（すでにあれば何もしない）
Path("fig").mkdir(exist_ok=True)

# ---------------------------------------------------------------
# 01 で保存したデータを読み込む
# ---------------------------------------------------------------
st = read("data/noto_IU.MAJO.mseed")        # 波形（Stream: 3 本の Trace が入っている）
inv = read_inventory("data/IU.MAJO.xml")    # 観測点情報（位置・地震計の特性）
events = read_events("data/noto_event.xml")  # 震源情報の一覧（今回は 1 件）
origin = events[0].preferred_origin()        # 1 件目の地震の震源（発生時刻・緯度・経度・深さ）

# ---------------------------------------------------------------
# 1. plot() で 3 方向の波形をまとめて描く
# ---------------------------------------------------------------
fig1 = plt.figure(figsize=(8, 6))     # 横 8 × 縦 6 インチの図を用意する
st.plot(fig=fig1)                     # その図に、3 本の波形を上下に並べて描く
fig1.savefig("fig/01_raw_stream.png")  # 図を画像ファイルとして保存する

# ---------------------------------------------------------------
# 2. 震源から観測点までの距離を計算する
# ---------------------------------------------------------------
# 観測点の緯度・経度を取り出す
coords = inv.get_coordinates(st[0].id, origin.time)

# 震源（緯度・経度）と観測点（緯度・経度）の距離を計算する
dist_m, _, _ = gps2dist_azimuth(
    origin.latitude,       # 震源の緯度
    origin.longitude,      # 震源の経度
    coords["latitude"],    # 観測点の緯度
    coords["longitude"],   # 観測点の経度
)  # 戻り値は (距離[m], 方位角, 逆方位角)。今回は距離だけ使う

# ---------------------------------------------------------------
# 3. P 波・S 波が届く時刻を計算する
# ---------------------------------------------------------------
# 地球内部の標準的な速度構造モデル「iasp91」を使う
model = TauPyModel("iasp91")

# 震源の深さと距離から、各地震波が届くまでの時間を計算する
arrivals = model.get_travel_times(
    source_depth_in_km=origin.depth / 1000,                 # 震源の深さ（m → km に変換）
    distance_in_degree=kilometers2degrees(dist_m / 1000),   # 距離（m → km → 角度[°] に変換）
    phase_list=["p", "P", "s", "S"],                        # 計算する波の種類（小文字は浅い経路の波）
)

# 「P 系」「S 系」それぞれで、いちばん早く届く時刻だけを辞書に入れる
first = {}                                         # 例: {"P": 22.8, "S": 39.5}
for arr in arrivals:                               # 計算結果を早く届く順に 1 つずつ見る
    first.setdefault(arr.name.upper(), arr.time)   # 名前を大文字にそろえ、まだ無ければ登録する

# 計算結果を表示する（地震発生から何秒後に届くか）
for name, sec in first.items():                      # P 波・S 波それぞれについて
    print(f"{name} 波: 地震発生から {sec:.1f} 秒後")  # 小数第 1 位まで表示する

# ---------------------------------------------------------------
# 4. 上下方向の波形に、P 波・S 波の時刻を重ねて描く
# ---------------------------------------------------------------
tr = st.select(channel="BHZ")[0]      # 3 本の中から上下方向（Z）の波形を 1 本取り出す
t = tr.times(reftime=origin.time)     # 横軸用の時刻: 地震発生を 0 秒とした経過時間の配列

fig2 = plt.figure(figsize=(10, 3.5))   # 横長の図を用意する
plt.plot(t, tr.data, "k-", lw=0.5)     # 波形を黒い細線で描く（tr.data は振幅の NumPy 配列）

for name, sec in first.items():                   # P 波・S 波それぞれについて
    color = "red" if name == "P" else "blue"      # P 波は赤、S 波は青にする
    plt.axvline(sec, color=color, ls="--", label=name)  # 届く時刻に縦の点線を引く

plt.xlim(-30, 300)                        # 横軸の範囲: 地震発生の 30 秒前 〜 300 秒後
plt.xlabel("Time since origin [s]")       # 横軸のラベル: 地震発生からの経過時間
plt.ylabel("Counts")                      # 縦軸のラベル: 地震計の生の出力値
plt.legend()                              # 凡例（P / S）を表示する
plt.tight_layout()                        # 文字が見切れないように余白を調整する
fig2.savefig("fig/02_bhz_with_taup.png", dpi=150)  # 画像ファイルとして保存する

# ---------------------------------------------------------------
# 作った図をウィンドウで表示する（すべて閉じるとスクリプトが終わる）
# ---------------------------------------------------------------
plt.show()
