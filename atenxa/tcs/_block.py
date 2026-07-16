# -*- coding: utf-8 -*-
""" ATENXA.TCS 閉そくシステムユーティリティ

Block statusは、閉塞 (Block) またはSectionの鎖錠・在線状態を表します。
int型の値を持ち、以下の意味を持ちます。
    - 0 : 在線・鎖錠なし (unlocked)
    - 1 : 鎖錠中 (locked)
    - 2 : 在線中 (occupied)
    - -1 or less : 異常 (error)
鎖錠中 (status=1) は、駅構内のSectionでのみ有効です。
Blockでは、在線なし (status=0) または在線中 (status=2) のみが有効です。

"""
import vrmapi

import atenxa
from atenxa.richevent import AfterEvent
from ._ctc import CTC
from ._config import tcsconfig

LAYOUT = vrmapi.LAYOUT()

POST_INIT_TIME = float(tcsconfig["ATENXA.TCS"]["POST_INIT_TIME"])

class BaseBlock(object):
    """閉そくシステムの基底クラス
    
    ATS, ATCに共通する閉そくの基本構造を提供します。
    """
    def __init__(
            self, 
            parent: object, 
            name: str, 
            sensor: int|str, 
            next: str|list[str], 
            aspectchain: dict = None
            ):
        """閉そくオブジェクトを初期化します。
        
        Args:
            name (str): 閉そく区間の名前
            sensor (int | str): センサーのID or 名前
            next (str | list[str]): 次の閉そく区間の名前。
                編成が本閉そくの1つ後に進入する閉そくに設定したnameと同じ文字列を指定します。
                本閉そくが第1閉そくで、次が駅の場内信号機の場合は、・・・
        """
        self.parent = parent  #: 親オブジェクト（通常はsensorと一致）
        self.name = str(name)  #: 閉そく区間の名前
        try:
            self.sensor = LAYOUT.GetATS(sensor)  #: センサー部品のオブジェクト
        except Exception as e:
            raise ValueError(f"センサー '{sensor}' が見つかりません。") from e
        self.next_ = next if isinstance(next, list) else [next]  #: 次の閉そく区間の名前のリスト
        self.next: list[BaseBlock] = []  #: 次の閉そく区間のオブジェクトのリスト
        self.prev: list[BaseBlock] = []  #: 前の閉そく区間のオブジェクトのリスト
        self.status = 0  #: 閉そく区間の状態 (0:在線・鎖錠なし, 1:鎖錠中, 2:在線中, -1:異常)
        self._aspect = 1  #: 信号機の現示コード

        # センサーの初期化
        self.sensor.SetSNSMode(2)  #: 最初と最後の車輪の両方に反応

        # 現示チェーンの初期化
        if aspectchain is None:
            aspectchain = {}
        self.aspectchain = sorted(aspectchain)

        # ポスト処理の予約
        AfterEvent(POST_INIT_TIME, self._post_init, userid=1851001, obj=self.sensor)

    def _post_init(self) -> None:
        """初期化後の処理
        
        前の閉そく区間の情報を更新します。
        """
        # 次の閉そく区間の名前をオブジェクトに更新
        for name in self.next_:
            next_block = CTC.blocks.get(name)
            if next_block is not None:
                self.next.append(next_block)
        # 次の閉そくオブジェクトに自分を前の閉そく区間として登録
        for next_block in self.next:
            next_block.prev.append(self)
        atenxa.printLOG(f"{self.name} {self.next=}")
        atenxa.printLOG(f"{self.name} {self.prev=}")

    @property
    def aspect(self) -> int:
        """信号機の現示コードを取得します。"""
        return self._aspect

    def checkin(self, trainid: int) -> int:
        """閉そくへのチェックイン処理
        
        Args:
            trainid (int): 編成ID
        """
        if self.status == 0:  # 在線なし
            # 編成が進入したので在線中にする
            self.status = 2
        elif self.status == 2:
            # 在線中のチェックイン＝閉そく違反
            atenxa.printLOG(
                f"[ATENXA.TCS ATSBlock] Check-in violation: {self.name} is already occupied by another train."
                )
        return

    def checkout(self, trainid: int) -> int:
        """閉そくからのチェックアウト処理

        このメソッドは、列車最後尾が次の閉そく信号機の直下センサで検出されたときに呼び出されます。
        
        Args:
            trainid (int): 編成ID
        """
        # 編成が退出したので在線なしにする
        self.status = 0
        return

    def prev_checkout(self, trainid: int) -> int:
        """前閉そくのチェックアウト処理を呼ぶ

        Args:
            trainid (int): 編成ID
        """
        for block in self.prev:
            block.checkout(trainid)

    def refresh_aspect(self) -> int:
        """閉そくの状態に応じて信号機の現示を更新する
        
        Returns:
            int: 現示コード
        """
        raise NotImplementedError("refresh_aspect() must be implemented in subclasses.")
    