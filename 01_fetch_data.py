"""01: 地震の情報と波形をダウンロードして保存する"""
from pathlib import Path

from obspy import UTCDateTime
from obspy.clients.fdsn import Client

Path("data").mkdir(exist_ok=True)

# 震源情報を検索（時刻は UTC）
t = UTCDateTime("2024-01-01T07:10:00")
cat = Client("USGS").get_events(starttime=t - 300, endtime=t + 300, minmagnitude=7.0)
origin = cat[0].preferred_origin()
print(cat)

# 波形と観測点の情報をダウンロード
client = Client("EARTHSCOPE")
t1, t2 = origin.time - 120, origin.time + 30 * 60
st = client.get_waveforms("IU", "MAJO", "00", "BH?", t1, t2)
inv = client.get_stations(network="IU", station="MAJO", location="00", channel="BH?",
                          starttime=t1, endtime=t2, level="response")
print(st)

# 保存しておく
cat.write("data/noto_event.xml", format="QUAKEML")
st.write("data/noto_IU.MAJO.mseed", format="MSEED")
inv.write("data/IU.MAJO.xml", format="STATIONXML")
