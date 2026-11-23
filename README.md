# obspy-earthquake-tutorial

ObsPyを用いて地震波データを操作するチュートリアルです。

Qiita の記事「Pythonで地震を解析するならObsPy。地震波形の取得から可視化・周波数解析まで」のサンプルコードです。
2024年1月1日の能登半島地震（M7.5）を、長野県・松代の観測点（IU.MAJO）で記録した波形を使います。

![spectrogram](fig/04_spectrogram.png)

## 必要なもの

- **Apple Silicon（M1 以降）の Mac**
- **Homebrew でインストールした Python 3.14**
- インターネット接続（地震データのダウンロードに使います）

> [!NOTE]
> 上の環境で動作を確認しています。ObsPy は今のところ、Intel Mac 向けと Python 3.15 向けのインストール済みパッケージ（wheel）を配布していません。

## 準備（macOS）

以下のコマンドは **ターミナル**（`⌘ + スペース` →「ターミナル」）で実行します。

### 1. Homebrew をインストールする

すでに入っている場合は 2 へ。[Homebrew 公式サイト](https://brew.sh/ja/) のコマンドを実行します。

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

終了時に表示される **Next steps** のコマンドも実行して、`brew` を使えるようにします。

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### 2. Python 3.14 をインストールする

最新版（3.15）ではなく、バージョンを指定して 3.14 を入れます。

```bash
brew install python@3.14
python3.14 --version   # Python 3.14.x と出ればOK
```

> [!TIP]
> python.org のインストーラ版 Python は未検証です。使う場合は、インストール後に `アプリケーション > Python 3.14` の `Install Certificates.command` を実行してください（しないとデータのダウンロードで `SSL: CERTIFICATE_VERIFY_FAILED` になります）。

### 3. このリポジトリをダウンロードする

緑色の「Code」ボタン →「Download ZIP」でダウンロードして解凍し、そのフォルダに移動します。

```bash
cd ~/Downloads/obspy-earthquake-tutorial-main
```

（Git を使う場合は `git clone https://github.com/kkgithubkk/obspy-earthquake-tutorial.git` でも OK）

### 4. 仮想環境を作って ObsPy をインストールする

```bash
python3.14 -m venv .venv          # 仮想環境を作る（最初の 1 回だけ）
source .venv/bin/activate         # 仮想環境に入る（行頭に (.venv) と出ればOK）
pip install -r requirements.txt   # ObsPy をインストール
```

ターミナルを開き直したときは、フォルダに移動して `source .venv/bin/activate` からやり直してください。

## 実行

このフォルダで、番号の順に実行してください。

```bash
python 01_fetch_data.py   # 地震の情報と波形をダウンロード → data/
python 02_plot.py         # 波形をグラフにして、P波・S波の到着時刻を重ねる
python 03_preprocess.py   # 揺れの大きさを速度 [m/s] に直す・フィルタ
python 04_spectrum.py     # FFT とスペクトログラムで周波数を調べる
```

`02`〜`04` は図をウィンドウで表示します。**ウィンドウをすべて閉じるとスクリプトが終わります。** 図は `fig/` にも保存されます。

| スクリプト | 出力される図 |
| --- | --- |
| `02_plot.py` | `01_raw_stream.png`, `02_bhz_with_taup.png` |
| `03_preprocess.py` | `03_velocity.png`, `03_bandpass.png` |
| `04_spectrum.py` | `04_fft.png`, `04_spectrogram.png` |

## データについて

- 震源情報: [USGS](https://earthquake.usgs.gov/)
- 波形・観測点情報: [EarthScope](https://www.earthscope.org/)（旧 IRIS）の FDSN Web Service

データはスクリプトの実行時にダウンロードするため、リポジトリには含めていません。

## 動作確認環境

- macOS（Apple Silicon）
- Python 3.14.10（Homebrew の python@3.14）
- ObsPy 1.5.2
