# -*- coding: utf-8 -*-
"""ATENXA踏切システムのコア"""
import vrmapi
from atenxa.basis import printLOG
from atenxa.richevent import AfterEvent

crossing_group = dict()

def setup_hub(group):
    """ATENXA踏切システムの踏切グループをセットアップ

    Args:
        group (int or str): グループ番号 or 名前
    """
    if type(group) == type(1):
        name = "ATENXA.CROSSING.GROUP{}".format(group)
    elif type(group) == type('str'):
        name = group
    else:
        raise TypeError("groupの型が不正です。 {}".format(group))
    crossing_group[group] = CrossingHub(name)
    printLOG('[atenxa.crossing] Group {} setup OK.'.format(group))

class CrossingHub(object):
    """
    踏切制御装置。

    Args:
        name (str, optional): 踏切グループに付ける名前
    """
    _unique_num = 0

    def __init__(self, name=None):
        if name is None:
            self.name = "crs{}".format(CrossingHub._unique_num)
        else:
            self.name = str(name)
        self.members = []           #: list of tuple (obj, rev, delay)
        self.queue = {1:0, 0:0}  #: 方向別の接近中列車数
        CrossingHub._unique_num += 1

    def addmember(self, obj, rev=False, delay=0.0):
        """踏切部品を追加
        
        Args:
            obj: 踏切オブジェクトまたはそのID
            rev (bool, optional): 方向表示機を逆転するときTrue, デフォルトはFalse
            delay (float, optional): 閉じるときの動作を遅延するときの時間 [秒]
        """
        if type(obj) == vrmapi.VRMCrossing:
            pass
        elif type(obj) == type(0):
            obj = vrmapi.LAYOUT().GetCrossing(obj)
        else:
            raise TypeError('objは踏切オブジェクトかそのID(int)でなければなりません。')
        if delay < 0.0:
            raise ValueError('delay(動作遅延時間)は0以上の実数値でなければなりません。')
        self.members.append((obj, rev, delay))

    def addmembers(self, objects, rev=False, delay=0.0):
        """踏切部品をまとめて追加
        
        Args:
            objects: 踏切オブジェクトまたはそのIDのリスト
            rev (bool, optional): 方向表示機を逆転するときTrue, デフォルトはFalse
            delay (float, optional): 閉じるときの動作を遅延するときの時間 [秒]
        """
        for obj in objects:
            self.addmember(obj, rev=rev, delay=delay)

    def approach(self, d):
        """列車接近時の動作

        Args:
            d: 列車の接近方向 (1 or 2)
        """
        if d in [0,1]:
            self.queue[d] += 1
            if self.queue[0] + self.queue[1] == 1:
                # 接近列車数が0から1になった
                # 踏切閉じる
                for obj, rev, delay in self.members:
                    if delay > 0.0:
                        AfterEvent(delay, obj.SetCrossingStatus, [2], obj=obj)
                    else:
                        obj.SetCrossingStatus(2)
            self._update_sign()
        else:
            raise ValueError('接近方向が不正です({})。'.format(d))

    def passed(self,d):
        """列車通過時の動作

        Args:
            d: 列車の接近方向 (1 or 2)
        """
        if d in [0,1]:
            if self.queue[d] > 0:
                self.queue[d] -= 1
            if self.queue[0] + self.queue[1] == 0:
                # 接近列車数が0になった
                # 踏切開ける
                for obj, rev, delay in self.members:
                    obj.SetCrossingStatus(1)
            self._update_sign()
        else:
            raise ValueError('接近方向が不正です({})。'.format(d))

    def _update_sign(self):
        """方向表示器の更新"""
        sign = 0b00
        if self.queue[0]:
            sign = sign | 0b01
        if self.queue[1]:
            sign = sign | 0b10
        if sign:
            for obj, rev, delay in self.members:
                if rev and sign < 3:
                    obj.SetCrossingSign(sign^3)
                else:
                    obj.SetCrossingSign(sign)
                printLOG(obj.GetID(),rev,delay, "SIGN UPDATED.", sign)
