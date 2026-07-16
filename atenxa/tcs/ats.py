# -*- coding: utf-8 -*-
""" ATENXA.TCS ATS閉そく """

import vrmapi

import atenxa
from atenxa.richevent import richevent
from ._block import BaseBlock
from ._ctc import CTC

LAYOUT = vrmapi.LAYOUT()

class ATSBlock(BaseBlock):
    """ATS閉そくオブジェクト
    
    ATS閉そくの機能を提供します。
    """
    def __init__(
            self, 
            parent: object, 
            name: str, 
            sensor: int|str, 
            next: str|list[str], 
            signal: int|str, 
            signal_type: str = '3', 
            aspectchain: dict = None
            ):
        """ATS閉そくオブジェクトを初期化します。"""
        super().__init__(parent, name, sensor, next)
        if isinstance(signal, (int, str)):
            try:
                self.signal = LAYOUT.GetSignal(signal)  #: 信号機部品のオブジェクト
            except Exception as e:
                raise ValueError(f"信号機 '{signal}' が見つかりません。") from e
        else:
            raise TypeError("signalはintまたはstr型で指定してください。")
        
        # aspectchain = {this_aspect: next_aspect, ...} の形式で現示チェーンを定義する
        if aspectchain is None:
            aspectchain = {
                1: -1,
                3: 2,  # Y <- R/YY
                6: 5,  # G <- Y/YG
            }
        self.aspectchain = dict(sorted(aspectchain.items()))  # キーでソートして再定義


    def dispatch_sensor(self, trainid: int, dir: int, tire: int, **kwargs) -> None:
        """センサー検出時のディスパッチャ
        
        センサーのイベントハンドラから呼び出す。

        Args:
            trainid (int): 編成ID
            dir (int): センサーに対する進入方向 -1:逆方向 1:順方向
            tire (int): 検出した車輪 1:先頭 2:最後尾
        """
        atenxa.printLOG("[ATENXA.TCS ATSBlock] Sensor catched:", self.name, trainid, dir, tire)
        if dir == 1:
            # 順方向
            if tire == 1:
                # 先頭
                self.checkin(trainid)
            elif tire == 2:
                # 最後尾
                self.prev_checkout(trainid)

    def checkin(self, trainid: int) -> bool:
        """閉そくへのチェックイン処理
        
        Args:
            trainid (int): 編成ID
        """
        res = super().checkin(trainid)
        aspect = self.refresh_aspect()
        return res
    
    def checkout(self, trainid: int) -> bool:
        """閉そくからのチェックアウト処理
        
        Args:
            trainid (int): 編成ID
        """
        res = super().checkout(trainid)
        aspect = self.refresh_aspect()
        return res
        
    def refresh_aspect(self) -> int:
        """閉そくの状態に応じて信号機の現示を更新する
        
        Returns:
            int: 現示コード
        """
        atenxa.printLOG(f"[ATENXA.TCS ATSBlock] {self.name} refresh signal Aspect. {self.status=}")
        if self.status == 0:
            # 閉そくが在線なしの場合
            # 次の閉そくの状態を確認して現示を決定する

            # 次の信号の最上位現示
            next_aspect = max([block.aspect for block in self.next], default=1)
            for this_aspect, next_ub in self.aspectchain.items():
                if next_aspect <= next_ub:
                    aspect = this_aspect
                    break
            else:
                # 現示アップなし。そのまま終わる。
                return self.aspect
            atenxa.printLOG(f"[ATENXA.TCS ATSBlock] {self.name} {next_aspect=} -> {aspect}")
            self.signal.SetStat(0, aspect)
            self._aspect = aspect

            # 後ろに現示アップを連鎖
            # ここで連鎖する分には、どこかに在線がある限りは無限ループにはならない（はず）
            #TODO: tokenをつける
            for block in self.prev:
                block.refresh_aspect()

            return aspect
        
        elif self.status in [-1, 2]:
            # 閉そくが在線中 or 異常の場合
            aspect = 1  # R
            self.signal.SetStat(0, aspect)
            self._aspect = aspect
            return aspect
        


def ats_block(obj, ev, param, name: str, next: str|list[str], signal: int|str, signal_type: str = '3', aspectchain: dict = None) -> None:
    """信号機直下のセンサーに設定してATS閉そくを定義します。
    
    Args:
        obj: イベントハンドラのobj
        ev: イベントハンドラのev
        param: イベントハンドラのparam
        name (str): 閉そく区間の名前
        signal (int | str): 信号機部品の名前またはID
        next (str | list[str]): 次の閉そく区間の名前。編成が本閉そくの1つ後に進入する閉そくに設定したnameと同じ文字列を指定します。
            本閉そくが第1閉そくで、次が駅の場内信号機の場合は、・・・
        signal_type (str, optional): 信号機の種類。
            - '2' : 2灯式信号機
            - '3' : 3灯式信号機
            - '4YG' : 4灯式信号機（YG現示）
            - '4YY' : 4灯式信号機（YY現示）
            - '5' : 5灯式信号機（YY, YG現示）
        aspectchain (dict, optional): 現示チェーンを記述した辞書。省略時はsignal_typeに応じたデフォルトの現示チェーンが使用されます。

    example:
        信号機直下の自動センサー部品のイベントハンドラで、イベントコードによる分岐の前に記述します。::
        
            # OBJECT: 自動センサー
            import vrmapi
            from atenxa.tcs.ats import ats_block
            def vrmevent_xx(obj, ev, param):
                ats_block(obj, ev, param, name='102L', signal='Signal102L', next='101L', signal_type='3')  # ここに書く！
                if ev == 'init':
                    pass    # 以下省略

    """
    richevent(obj, ev, param)
    if ev == 'catch':
        block = CTC.blocks[name]
        block.dispatch_sensor(**param)

    elif ev == 'init':
        sensor = obj.GetID()
        block = ATSBlock(
            parent=obj, 
            name=name, 
            sensor=sensor, 
            next=next, 
            signal=signal, 
            signal_type=signal_type, 
            aspectchain=aspectchain
        )
        CTC.assign_block(block)
