# -*- coding: utf-8 -*-
"""ATENXA信号システム - ATS

簡単な組み込みとリアルな動作が特長の信号制御パッケージです。
"""

#from warnings import RuntimeWarning
from collections.abc import Container
from atenxa import ATENXAError
import vrmapi

blocks = {} #: id=センサーのID, value=Blockオブジェクト

LAYOUT = vrmapi.LAYOUT()

class Block(object):
    """閉塞オブジェクト"""
    """
    # 信号の現示速度
    ------------車上でもつこと----------
    speedlimit = {
        0: 0,   # 無灯火
        1: 0,   # 停止
        2: 25,  # 警戒
        3: 55,  # 注意
        4: 75,  # 減速
        5: 105, # 抑速
        6: 130, # 進行
        7: 160,  # 高速進行
        }
    """
    def __init__(self, sensorid, name, signal=None, aspect=3, repeater=None, **kwargs):
        self.sensorid = sensorid
        self.name = name
        

        # signal(信号機)
        if signal is None:
            self.signal = None
        elif not isinstance(signal, vrmapi.VRMSignal):
            self.signal = LAYOUT.GetSignal(signal)
        
        # repeater(中継信号機)は，リスト化
        if repeater is None:
            self.repeater = []
        if isinstance(repeater, Container):
            repeater_ = []
            for rp in repeater[:]:
                if isinstance(rp, vrmapi.VRMSignal):
                    repeater_.append(rp)
                else:
                    repeater_.append(LAYOUT.GetSignal(rp))
            self.repeater = repeater_
        elif isinstance(repeater, vrmapi.VRMSignal):
            self.repeater = [repeater]
        else:
            self.repeater = [LAYOUT.GetSignal(repeater)]

        self.train = []
        self.nextblock = None
        self.prevblock = None
        self.clearedblocks = -1

    @property
    def aspect(self):
        """在線状況から判断される信号現示"""
        return 0

    def onblock(self):
        """信号の内方に在線があるか"""
        if self.clearedblocks == 0:
            return 1
        elif self.clearedblocks > 1:
            return 0
        else:
            # 在線状況が不明の場合
            return -1 

    def checkin(self, trainid):
        """信号内方の閉塞に進入"""
        self.clearedblocks = 0
        self.train.append(trainid)

        d = {'sensorid':self.sensorid}
        LAYOUT.SendBRDObject(trainid, 'atenxa.atscallback', d)

    def checkout(self, trainid):
        """信号外方の閉塞から退出"""
        self.prevblock.clearforward(1)

    def clearforward(self, clearedblocks):
        """前方の閉塞がクリアになったことを受け取る
        
        Arg:
            clearedblocks: この先に進入可能な閉塞の数
        """
        if self.clearedblocks == 0:
            # 内方に在線あり
            pass
        else:
            # 在線なしまたは不明
            self.clearedblocks = clearedblocks
            self.update_indicator()
            # 外方の閉塞に伝達
            self.prevblock.clearforward(clearedblocks+1)

    def update_indicator(self):
        """現在の状況に合わせて信号現示を更新"""
        self.signalobj.SetStat(0, self.aspect)
        for r in self.repeater:
            r.SetStat(0, self.aspect)

def atsbeacon(obj, ev, param, name=None, kind='block', signal=None, aspect=3, repeater=None, **kwargs):
    """ATS地上子の機能を有効化
    
    センサー部品のイベントハンドラ直下に記述します。
    """
    if ev=='catch':
        if param['dir'] == 1:
            blk = blocks[obj.GetID()]
            if param['tire'] ==1:
                #先頭
                blk.checkin()
            else:
                #最後尾
                blk.checkout()

    elif ev=='init':
        # 初期化
        # 入力のチェック
        if name is None:
            name = obj.GetNAME()
        elif not isinstance(name, str):
            raise TypeError("nameが無効な値です。")



        sensorid = obj.GetID()
        if kind=='block':
            # 閉塞信号
            blocks[sensorid] = Block(sensorid, name, signal, aspect, repeater)
        elif kind=='entry':
            # 場内信号
            pass
        elif kind=='exit':
            # 出発信号
            pass
        else:
            raise ATENXAError("kind属性の値が不正です。{}".format(kind))

        obj.SetSNSMode(2)

