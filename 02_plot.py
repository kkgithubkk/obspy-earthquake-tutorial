"""02: 波形をグラフにして、P 波・S 波の到着時刻を重ねる"""
from pathlib import Path

import matplotlib.pyplot as plt
from obspy import read, read_events, read_inventory
from obspy.geodetics import gps2dist_azimuth, kilometers2degrees
from obspy.taup import TauPyModel

Path("fig").mkdir(exist_ok=True)

st = read("data/noto_IU.MAJO.mseed")
inv = read_inventory("data/IU.MAJO.xml")
origin = read_events("data/noto_event.xml")[0].preferred_origin()

# plot() 一発
st.plot(outfile="fig/01_raw_stream.png")

# 震源から観測点までの距離
coords = inv.get_coordinates(st[0].id, origin.time)
dist_m, _, _ = gps2dist_azimuth(origin.latitude, origin.longitude,
                                coords["latitude"], coords["longitude"])

# P 波・S 波が届く時刻を計算
arrivals = TauPyModel("iasp91").get_travel_times(
    source_depth_in_km=origin.depth / 1000,
    distance_in_degree=kilometers2degrees(dist_m / 1000),
    phase_list=["p", "P", "s", "S"],
)
first = {}
for arr in arrivals:
    first.setdefault(arr.name.upper(), arr.time)
print(first)

# 地震発生からの秒数を横軸にしてプロット
tr = st.select(channel="BHZ")[0]
plt.figure(figsize=(10, 3.5))
plt.plot(tr.times(reftime=origin.time), tr.data, "k-", lw=0.5)
for name, sec in first.items():
    plt.axvline(sec, color="red" if name == "P" else "blue", ls="--", label=name)
plt.xlim(-30, 300)
plt.xlabel("Time since origin [s]")
plt.legend()
plt.tight_layout()
plt.savefig("fig/02_bhz_with_taup.png", dpi=150)
