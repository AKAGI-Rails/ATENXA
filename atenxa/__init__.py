# -*- coding: utf-8 -*-
"""ATENXA - Advanced Tools for Enhancing VRMNX by Akagi

VRMNXpyの，シンプル・使いやすい・リアルな拡張です。
使いやすいイベントシステムや閉塞制御などを提供します。
"""

__version__ = '0.1.0-alpha'
__date__ =    '2020/9/20'
__author__ =  'AKAGI Rails'

_DEBUG = True # デバッグモード

from .basis import *
from .richevent import *
#from sprite import *

#__all__ = ['basis', 'richevent']

def sensor_approach(obj,ev,param):
    printLOG('Tmp User Handler.')