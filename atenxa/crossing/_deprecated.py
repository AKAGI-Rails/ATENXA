# -*- coding: utf-8 -*-
"""ATENXA踏切システムのコア"""
import vrmapi
from atenxa.basis import printLOG

crossing_group = dict()

def setup_control(group):
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
    print("[atenxa.crossing] Group {} setup OK.".format(group))

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
        self.approach = {1:0, 0:0}  #: 方向別の接近中列車数
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

    def register_sensor(self, sensor, direc, passed=False):
        """センサーを踏切制御専用に引当て
        
        引当てられたセンサーはATENXA側でイベントハンドラを上書きするので、
        デフォルトのイベントハンドラは無効となり、
        他の制御との兼用はできなくなります。
        他の踏切の制御センサーと兼用させることもできません。

        Args:
            sensor: センサーオブジェクトまたはそのID
            dir (int): 踏切に対するセンサーの向き(1 or 2)
            passed (bool): 通過後センサーに対してTrue
        """
        if type(sensor) == vrmapi.VRMATS:
            pass
        elif type(sensor) == type(0):
            sensor = vrmapi.LAYOUT().GetATS(sensor)
        else:
            raise TypeError('objは自動センサーオブジェクトかそのID(int)でなければなりません。')

        if type(direc) != type(0):
            raise TypeError('direc')
        elif direc not in {1,2}:
            raise ValueError("'direc'が{}でしたが正しくは1か2です。".format(direc))

        atsmd = sensor.GetDict()
        atsmd['atenxa.crossing.target'] = self
        atsmd['atenxa.crossing.direction'] = direc
        printLOG('UserEventFunction:')
        sensor.SetUserEventFunction('atenxa.crossing.sensor_approach')
        printLOG('Set OK?')

    def register_sensors(self, sensors, direc, passed=False):
        raise NotImplementedError('register_sensors is not implemented yet.')

def sensor_approach(obj, ev, param):
    """接近センサー用イベントハンドラ"""
    if ev == 'catch':
        md = obj.GetDict()
        crs = md['atenxa.crossing.target']
        direc = md['atenxa.crossing.direction']
        crs.approach(direc)
        printLOG('Test: Catched Train')
    elif ev == 'init':
        printLOG('Test: UserEventFunction set OK.')

def sensor_passed(obj, ev, param):
    """通過センサー用イベントハンドラ"""
    if ev == 'catch':
        md = obj.GetDict()
        crs = md['atenxa.crossing.target']
        direc = md['atenxa.crossing.direction']
        crs.passed(direc)
