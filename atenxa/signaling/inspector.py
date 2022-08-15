# -*- coding: utf-8 -*-
"""ATENXA信号システム - 信号検測車

編成に組み込むと，走行しながら信号関係のセンサーの設置状況を検測し，
ATENXA信号システムのセットアップに必要な情報を収集・保存します。
"""
from atenxa.signaling import *


def activate_inspector(obj, ev, param):
    """編成で検測機能を有効にする"""
    return NotImplemented
    if ev == 'broadcast':
        if param['broadcast'] == 'atenxa.atscallback':
            sensorid = param['sensorid']
            

