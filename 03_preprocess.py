"""03: 揺れの大きさを「速度 [m/s]」に直す・フィルタをかける"""
from obspy import read, read_inventory

st = read("data/noto_IU.MAJO.mseed")
inv = read_inventory("data/IU.MAJO.xml")

st_vel = st.copy()            # 元のデータは残しておく
st_vel.detrend("demean")
st_vel.taper(max_percentage=0.05)
st_vel.remove_response(inventory=inv, output="VEL", pre_filt=(0.005, 0.01, 8.0, 10.0))
st_vel.plot(outfile="fig/03_velocity.png")

for tr in st_vel:
    print(f"{tr.id}: 最大 {abs(tr.data).max() * 100:.2f} cm/s")

# 10〜50 秒周期のゆっくりした揺れだけを見る
st_vel.copy().filter("bandpass", freqmin=0.02, freqmax=0.1).plot(outfile="fig/03_bandpass.png")

st_vel.write("data/noto_IU.MAJO_vel.mseed", format="MSEED")
