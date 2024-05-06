# ATENXA - simple & powerful toolkit for VRMNX

VRMNXpyの，シンプル・使いやすい・リアルな拡張です。
使いやすいイベントシステムや踏切制御などを提供します。

ATENXAの詳細は，下記ページをチェックしてください。

[https://akagi-rails.github.io/ATENXA/](https://akagi-rails.github.io/ATENXA/)

## VRMNXについて

VRMNX（鉄道模型シミュレーターNX）は，I.MAGIC社開発の3DCG鉄道模型です。
Pythonスクリプトによりさまざまなギミックをユーザーが組み込むことができます。

VRMNX (Virtual Railroad Models System NX) is developed by I.MAGIC. Japanese-only.

[VRMNX Official](http://www.imagic.co.jp/hobby/)

## ダウンロード & インストール

このリポジトリのZipは以下リンクからダウンロードできます。

[リポジトリをZipでダウンロード](https://github.com/AKAGI-Rails/ATENXA/archive/refs/heads/master.zip)

ATENXAを使用するレイアウトと同じディレクトリに，
atenxaフォルダをそのままコピーするのが典型的な方法です。

```text
(somedirectory)
├ atenxa
│ ├ __init__.py
│ └ (略)
└ yourlayout.vrmnx
```

ATENXAのバージョンが競合しないよう，レイアウトスクリプトで以下のようにセットアップすることを推奨します。

```python
#LAYOUT
import vrmapi

# レイアウトと同じディレクトリのpythonスクリプトを優先的にインポートする
import sys
sys.path.insert(0, vrmapi.SYSTEM().GetLayoutDir())

import atenxa

def vrmevent(obj,ev,param):
    # (省略)
    pass
```

## サンプル

exampleフォルダにサンプルがあります。
相対パスで `atenxa` パッケージをインポートしている関係で，

- ATENXA/atenxa
- ATENXA/example

以上2つのディレクトリは移動せず，そのままの位置関係でごらんください。
