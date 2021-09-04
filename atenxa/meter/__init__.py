# -*- coding: utf-8 -*-
"""ATENXA 速度計パッケージ

スプライトを使用した速度計表示機能を提供するパッケージです。
MeterBaseのサブクラスを自作して異なるデザインの速度計を作ることもできます。
実用上は，MeterSimpleクラスを継承して作るのが便利でしょう。

Example:
    シンプルなサンプル速度計を表示するサンプルです。
    編成スクリプトのイベントハンドラ直下にactivate関数を書き込みます。
    リソース画像は別途登録しておいてください。
    
    >>> def vrmevent_xx(obj, ev, param):
    ...     atenxa.meter.activate(obj, ev, param, atenxa.meter.MeterSimple, 1)

"""

from atenxa.sprite import Sprite

__all__ = ['activate', 'MeterBase', 'MeterSimple']

_trainmeter = {} #: key=trainid, value=MeterClassオブジェクト

def activate(train, ev, param, MeterClass, res, layoutres=False):
    """対象の編成で速度計スプライトを有効にします。

    Args:
        train: 対象の編成オブジェクト
        ev: 編成のイベントハンドラに来るイベントコード
        param: 編成のイベントハンドラに来るパラメータ
        MeterClass: 使用する速度計のクラス
        res: 速度計テクスチャのリソースID
        layoutres (optional): Trueでレイアウトのリソースを参照します。デフォルト(False)は編成のリソースを参照します。 
    """
    if ev == 'init':
        #td = train.GetDict()
        tid = train.GetID()
        train.SetEventFrame()
        meter = MeterClass(train, res, layoutres)
        #td['ATENXA.Meter'] = meter
        _trainmeter[tid] = meter
        #return meter
    elif ev == 'frame':
        #td = train.GetDict()
        #meter = td['ATENXA.Meter']
        tid = train.GetID()
        meter = _trainmeter[tid]
        #meter._frame()
        pass


class MeterBase(object):
    """速度計のためのベースクラス。

    このクラス自体が速度計として機能するわけではありませんが，
    これのサブクラスを作り，setupメソッドとdisplayメソッドをオーバーライドして
    オリジナルデザインの速度計を作ってください。

    Args:
        train: 対象の編成オブジェクト
        res: 速度計テクスチャのリソースID
        layoutres (optional): 
            Trueでレイアウトのリソースを参照します。
            デフォルト(False)は編成のリソースを参照します。 
    """

    def __init__(self, train, res, layoutres):
        self._train = train
        self._res = res
        self._layoutres = layoutres
        self.setup()

    def new_sprite(self):
        """スプライトオブジェクトを生成
        
        atenxa.Spriteスプライトオブジェクトを生成し，
        クラスで設定されたリソースIDと読込先から
        テクスチャをロードします。
    
        Returns:
            テクスチャをロード済みのatenxa.Spriteオブジェクト
        """
        return Sprite(self._res, self._train.GetID())

    def setup(self):
        """スプライトのパーツを設定します。
        
        initイベント内でコールされます。
        """
        pass

    def _frame(self):
        if not self._train.IsActive():
            return
        if not self._train.IsView():
            return        
        # 表示対象かつ操作対象のときのみ
        self.display()

    def display(self):
        """各フレームでスプライトを表示します。
        
        対象の編成が操作対象かつ表示対象のときのみframeイベント内でコールされます。
        """
        pass

from .simple import MeterSimple
