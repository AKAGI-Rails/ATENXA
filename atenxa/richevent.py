# -*- coding: utf-8 -*-
"""ATENXA式イベントシステム

vrmapiの時間系イベントのラッパです。
コールバック関数と，実行時に与える引数をセットにしてイベントを定義でき便利です。

:ref:richevent 関数をイベントハンドラ直下に記述するとATENXA式イベントシステムが有効になります。
通常はレイアウトオブジェクトのイベントハンドラに記述すればよいです。

AfterEvent, TimerEventのコンストラクタで `obj` 属性をレイアウト以外に指定する場合は、
当該オブジェクトのイベントハンドラにもrichevent関数を記述する必要があります。
"""
import vrmapi
from . import _DEBUG

_LAYOUT = vrmapi.LAYOUT()
_register = {}

def richevent(obj, ev, param):
    """ATENXA式イベントを有効化。
    
    イベントハンドラの直下で呼び出します。
    通常はレイアウトのイベントハンドラの直下で呼び出してください。
    これを記述すると，対象のオブジェクトで各種のATENXA式イベントが動作するようになります。

    AfterEvent, TimerEventのコンストラクタで `obj` オプションを利用する場合，
    対象オブジェクトのイベントハンドラからもこの関数を呼び出す必要があります。

    Example:

        >>> from atenxa import *
        >>> def vrmevent(obj,ev,param):
        ...     richevent(obj, ev, param)
        ...     if ev == 'init':
        ...         pass    # 以下省略
    """
    evid = param['eventid']
    if evid in _register:
        if _DEBUG:
            #LOG(evid, param)
            pass
        return _register[evid].exec()

def kill_event(evid):
    """ATENXA式イベントをキャンセル。
    
    ATENXA式のイベントのみキャンセルできます。
    
    Args:
        evid: イベントID
    """
    try:
        obj = _register[evid]._obj
        del _register[evid]
    except KeyError:
        vrmapi.LOG('[ATENXA.EVENT WARNING]不正なイベントID (ID {})'.format(evid))
    obj.ResetEvent(evid)

class BaseEvent(object):
    """ATENXA式イベントのベースクラス
    
    このクラス自体はイベントとしての機能はありません。
    """
    def __init__(self, callback, args=None, kwargs=None, userid=0, obj=None):
        self.eventid = -1   # システムのイベントID
        self._callback = callback
        self._args = args if args is not None else []
        self._kwargs = kwargs if kwargs is not None else {}
        self.userid = userid    # ユーザID
        if obj:
            self._obj = obj
        else:
            self._obj = _LAYOUT

    def exec(self):
        """コールバック関数を実行します。
        
        イベントハンドラから呼び出されます。
        """
        return self._callback(*self._args, **self._kwargs)

    def kill(self):
        """このイベントを削除します。"""
        kill_event(self.eventid)

class AfterEvent(BaseEvent):
    """ 指定時間後に実行するATENXA式イベント

    interval秒後に引数args，キーワード引数kwargsでcallbackを実行します。
    args*がNoneなら空のリストが使用されます。
    
    Args:
        interval: 時間(秒)
        callback: 実行する関数名
        args (optional): 関数実行時に与える引数
        kwargs (optional): 関数実行時に与えるキーワード引数
        userid (optional): ユーザID
        obj (optional): イベント発生対象のオブジェクト。 (default=LAYOUT)

    Example:
        1.5秒後に編成オブジェクトtrnでSetTimerVoltage

        >>> AfterEvent(1.5, trn.SetTimerVoltage, args=(5.0, 0.2))

        指定時間になると次が実行されます。

        >>> trn.SetTimerVoltage(5.0, 0.2)

    callbackにはユーザーが定義した関数やクラスメソッドを与えることもできます。
    """
    def __init__(self, interval, callback, args=None, kwargs=None, userid=0, obj=None):
        super().__init__(callback, args, kwargs, userid, obj)
        self._interval = interval
        self.eventid = self._obj.SetEventAfter(interval, userid)    #: システムが発行したイベントID
        _register[self.eventid] = self

    def exec(self):
        """コールバック関数を実行します。
        
        イベントハンドラから呼び出されます。

        Note:
            AfterEventは実行と同時に自動でkill_eventと同等のことを行うため，
            不要になったAfterEventをkill_eventする必要はありません。
        """
        del _register[self.eventid]
        return self._callback(*self._args, **self._kwargs)

class TimerEvent(BaseEvent):
    """ 指定時間毎に実行するATENXA式イベント
    
    Args:
        interval: 時間(秒)
        callback: 実行する関数名。
        args (optional): 関数実行時に与える引数。（タプル）
        kwargs (optional): 関数実行時に与えるキーワード引数。（辞書）
        userid (optional): ユーザID
        obj (optional): イベント発生対象のオブジェクト。 (default=LAYOUT)
    """
    def __init__(self, interval, callback, args=None, kwargs=None, userid=0, obj=None):
        super().__init__(callback, args, kwargs, userid, obj)
        self.eventid = self._obj.SetEventTimer(interval, userid)    #: システムが発行したイベントID
        _register[self.eventid] = self

