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
(([a-g]|[a-g][!#])[0-9])\*[ihqox]|[.\*]

a-fは音階を表します．

!はフラット，#はシャープを表します．

0-9はオクターブを表します．

ihqoxは以下の通りです．

- i:1分音符（*i*dentical）
- h:2分音符（*h*alf）
- q:4分音符（*q*uarter）
- o:8分音符（*o*cta）
- x:16分音符（he*x*）

音階・オクターブは省略可能です．省略した場合は最後に設定した音階・オクターブが設定されます．

.は16分休符，\*は4分休符です．

```
| f3a3c3qqoo.xo |
```

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
