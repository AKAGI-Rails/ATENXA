.. ATENXA documentation master file, created by
   sphinx-quickstart on Sun Sep 20 17:57:09 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ATENXA for VRMNX
================

ATENXA - Advanced Tools for Enhancing VRMNX by Akagi は
VRMNXのPythonスクリプトに便利な機能を提供するパッケージです。

主要な機能
----------

* 汎用の便利なログ出力
* 便利な時間系イベントシステム
* 簡単に組み込め、リアルに動作する踏切
* 表示順入れ替えに対応するスプライトのラッパ
* スプライトで動作する速度計

計画中の機能

* 自動運転
* 閉塞・ATS

Download and Install
====================

ATENXAは下記のリンクからGitHubリポジトリの中身をZipで配布しています。

`ATENXAのダウンロード(zip) <https://github.com/AKAGI-Rails/ATENXA/archive/refs/heads/master.zip>`_


アーカイブ内の``atenxa``フォルダを、そのままお使いのレイアウトと同じフォルダ内にコピーしてください。

::

   (root)
    ├─ atenxa
    │  ├ __init__.py
    │  └ ...
    └─ YourLayout.vrmnx


ATENXAのバージョンが競合しないよう，レイアウトスクリプトで以下のようにセットアップすることを推奨します。::

   #LAYOUT
   import vrmapi

   # レイアウトと同じディレクトリのpythonスクリプトを優先的にインポートする
   import os, sys
   sys.path.insert(0, os.path.abspath(vrmapi.SYSTEM().GetLayoutDir()))

   import atenxa

   def vrmevent(obj,ev,param):
      pass

これでお使いのレイアウトから ``import atenxa`` できるようになります。

もくじ
==================

.. toctree::
   :maxdepth: 2
   
   quickstart
   tutorial/index
   reference
   history


.. toctree::
   :caption: 外部リンク

   Python 3.7 <https://docs.python.org/ja/3.7/index.html>
   VRMNX Scriptマニュアル<https://vrmcloud.net/nx/script/>

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
