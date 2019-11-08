# Mutelang

Mutelangは音楽作成用の言語です．ソースコードからmidiファイルを生成することができます．

## セットアップとサンプル実行

```python
pip install -r requirements.txt
python mutec.py test.mu
```

# Muteファイルの書き方

## 非ドラムパートの書き方

### 曲のスピード（bpm）を設定する

`bpm = <num>`と書いてbpmを設定します．

```
bpm = 80
```

### 楽器（instrument）を設定する

`instrument = <name>`と書いてinstrumentを設定します．

```
instrument = AcousticBass
```

### 音の大きさ（velocity）を設定する

`velocity = <num>`と書いてvelocityを設定します．

```
velocity = 80
```

### 楽譜を書く
TODO

## ドラムパートの書き方

### ドラムモードに切り替える

`drum`と書いた行以降はドラムモードになります．

```
drum
```

### 打楽器のリストを設定する

ドラムモードでは楽器を複数設定できます．

```
instrument = {BassDrum1, AcousticSnare, SplashCymbal}
```

### 音の大きさ（velocity）を設定する

`velocity = <num>`と書いてvelocityを設定します．

```
velocity = 80
```

### 楽譜を書く

TODO

# mutecの処理フロー

1. mutecがmuteファイルをパースして通常はinstrumentごとに`chord_bass_seq`を呼び出す．drumモード時には`drum_seq`を呼び出す．
1. `chord_bass_seq`と`drum_seq`はmidiファイルを生成する．
1. 最後にmutecは`stack_midi`を呼び出す．
1. `stack_midi`はmidiファイルを束ねてひとつのmidiファイルを生成する．
