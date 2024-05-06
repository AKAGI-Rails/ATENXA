# -*- coding: utf-8 -*-
"""シンプルなサンプル速度計

atenxa.meter.MeterBaseを継承して速度計に仕立てるサンプルです。
"""
from atenxa.meter import MeterBase

# オリジナルの速度系クラスを作る場合は、このファイルに書き足さずに、
# コピーしたモジュールをatenxaの外のディレクトリに置いて編集してください。
# その際以下のコメントを外して、activateができるようにするといいです。
# from atenxa.meter import activate

class MeterSimple(MeterBase):
    """シンプルなアナログ速度計(120km/h)
    
    211系風のシンプルなアナログ速度計です。
    I.MAGIC Blog & バージョン5公式マニュアルでサンプルとして配布されていた
    テクスチャーを使用します。
    
    http://www.imagic.co.jp/devblog/2008/11/24/%e9%80%9f%e5%ba%a6%e8%a8%88%e3%81%ae%e3%83%86%e3%82%af%e3%82%b9%e3%83%81%e3%83%a3%e3%83%bc/

    Example:
        編成スクリプトのイベントハンドラ直下にactivate関数を書き込みます。
        編成リソースのID=1のテクスチャーを使用する例です。

        >>> def vrmevent_xx(obj,ev,param):
        ...     atenxa.meter.activate(obj,ev,param, atenxa.meter.MeterSimple, 1)
    """
    def setup(self):
        # ここでnew_sprite()して基本的な設定をしておくとよい。
        # Spriteのインスタンスは好きな名前のクラス属性に突っ込んでください。

        self.needle = self.new_sprite()
        self.needle.SetUV(164,252, 256,256)
        self.needle.SetTranslate(504,844)
        # 針の回転角度はdisplayメソッドで速度に基づいて計算。

        self.meterbase = self.new_sprite()
        self.meterbase.SetUV(0,0, 240,240)
        self.meterbase.SetTranslate(384,724)
        #self.meterbase.SetColor(1,1,1,1)
        pass

    def display(self):
        spd = self._train.GetSpeed()
        #LOG(spd)
        if spd < 20.0:
            rot = spd * 1.1 - 202
        else:
            rot = (spd - 20.0) * 2.02 - 180.0
        self.needle.SetRotate(0,2, rot)
        self.needle.SetSprite()

        self.meterbase.SetSprite()
