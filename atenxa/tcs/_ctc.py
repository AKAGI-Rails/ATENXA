# -*- coding: utf-8 -*-
""" ATENXA.TCS CTC """

from types import MappingProxyType

class CTC:
    """CTC クラスオブジェクト
    
    実際の機能は、いわゆるCTC (Central Traffic Control: 中央運行指令)というよりは、
    レイアウト内で定義された駅 (Station)、閉塞 (Block)などのオブジェクト参照を保存するコンテナです。

    CTCはレイアウト全体で1つだけ存在することを想定しており、
    インスタンスを生成せずに、クラスオブジェクトに直接アクセスして使用します。
    """
    _stations = {}  #: 内部で保持する駅オブジェクトの辞書
    _blocks = {}  #: 内部で保持する閉塞オブジェクトの辞書

    stations = MappingProxyType(_stations)  #: 駅オブジェクトの読み取り専用辞書 {station_name: station_object, ...}
    blocks = MappingProxyType(_blocks)  #: 閉塞オブジェクトの読み取り専用辞書 {block_name: block_object, ...}

    @classmethod
    def assign_station(cls, station) -> None:
        """駅オブジェクトをCTCに登録します。
        
        Args:
            station (BaseBlock): 駅オブジェクト
        """
        name = station.name
        if name in cls._stations:
            raise ValueError(f"駅 '{name}' はすでに登録されています。")
        cls._stations[name] = station

    @classmethod
    def assign_block(cls, block) -> None:
        """閉塞オブジェクトをCTCに登録します。
        
        Args:
            block (BaseBlock): 閉塞オブジェクト
        """
        name = block.name
        if name in cls._blocks:
            raise ValueError(f"閉塞 '{name}' はすでに登録されています。")
        cls._blocks[name] = block
        print(cls._blocks.keys())
