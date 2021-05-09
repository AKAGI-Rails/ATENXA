# -*- coding: utf-8 -*-
"""ATENXA踏切システム

簡単な組み込みとリアルな動作が特長の踏切制御パッケージです。

踏切を構成する部品とセンサーのイベントハンドラに1行ずつ記述するとセットアップ完了です。
"""
# import vrmapi
from atenxa.basis import printLOG, pprintLOG, ATENXAError
from atenxa.richevent import richevent as _richevent

from ._core import crossing_group as _crossing_group
from ._core import setup_hub as _setup_hub

def activate(obj, ev, param, group, rev=False, delay=0.0):
    """踏切部品をアクティベート
    
    踏切部品をatenxa踏切システムで有効化します。
    踏切部品のイベントハンドラに書き込みます。

    Args:
        obj: 踏切オブジェクトまたはそのID
        ev: イベントハンドラに渡されたイベント種別
        param: イベントハンドラに渡されたイベントパラメータ
        group (int or str): 踏切のグループ番号 or 名前
        rev (default=False): 方向表示機を逆転するならTrue
        delay (default=0.0): 遮断機の動作遅延時間(秒)

    グループ番号またはグループ名は，

    Example:
        「ねこ踏切」の遮断機部品で，警報機の鳴動から1.5秒後に遮断を開始します。

        >>> import atenxa.crossing as atx
        >>> def vrmevent_xx(obj,ev,param):
        ...     atx.activate(obj,ev,param, group='nekofumikiri', delay=1.5)

    """
    # ATENXA式イベントシステムを有効化
    _richevent(obj,ev,param)

    if ev == 'init':
        try:
            _crossing_group[group].addmember(obj,rev,delay)
        except KeyError:
            _setup_hub(group)
            _crossing_group[group].addmember(obj,rev,delay)

def activate_close(obj, ev, param, group, direction):
    """センサー通過で踏切を閉じる

    atenxa踏切システムの踏切を閉じる指令を送ります。
    センサー部品のイベントハンドラに書き込みます。

    Args:
        obj: センサーオブジェクト
        ev: イベントハンドラに渡されたイベント種別
        param: イベントハンドラに渡されたイベントパラメータ
        group (int or str): 踏切のグループ番号 or 名前
        direction: 踏切に対するセンサーの向き(1 or 2)
    
    Example: 
        「ねこ踏切」を閉じます。

        >>> import atenxa.crossing as atx
        >>> def vrmevent_xx(obj,ev,param):
        ...     atx.activate(obj,ev,param, group='nekofumikiri', delay=1.5)

    """
    if ev == 'catch':
        if param['dir'] == 1:
            try:
                g = _crossing_group[group]
            except KeyError:
                raise ValueError("group名が不正です ({}).".format(group))
            g.approach(direction)

def activate_open(obj, ev, param, group, direction):
    """センサー通過で踏切を閉じる

    atenxa踏切システムの踏切を閉じる指令を送ります。
    センサー部品のイベントハンドラに書き込みます。

    Args:
        obj: センサーオブジェクト
        ev: イベントハンドラに渡されたイベント種別
        param: イベントハンドラに渡されたイベントパラメータ
        group (int or str): 踏切のグループ番号 or 名前
        direction: 踏切に対するセンサーの向き(1 or 2)
    
    Example: 
        「ねこ踏切」を閉じます。

        >>> import atenxa.crossing as atx
        >>> def vrmevent_xx(obj,ev,param):
        ...     atx.activate(obj,ev,param, group='nekofumikiri', delay=1.5)

    """
    if ev == 'catch':
        if param['dir'] == 1:
            try:
                g = _crossing_group[group]
            except KeyError:
                raise ValueError("group名が不正です ({}).".format(group))
            g.passed(direction)
