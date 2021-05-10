# -*- coding: utf-8 -*-
"""ATENXA基幹部分"""
import vrmapi

def printLOG(*objects, sep=' ', end=''):
    """すこし賢いログ出力
    
    Python標準のprint()とほぼ同じ形式でVRMNXのスクリプトLOGに出力します。
    objectsのすべてにstr()を引っかけて，sepで区切りながらつなげて出力します。
    sep, endを設定する場合キーワード引数で設定してください。

    スクリプトLOGではString型と表示されますが、objectsの実体とは無関係です。
    そのかわり、任意の型のオブジェクトを与えれば、
    TypeErrorとならずに、オブジェクトの ``__str__`` 属性を利用して
    何らかの形で出力することができます。
    
    Args:
        *objects: LOGに出したいオブジェクト。str()した上で出力します。
        sep (str, optional): objectどうしの区切り。
        end: 行末。

    Return:
        str: ログへの出力内容。

    Example:
        出力するオブジェクトは複数並べることができます。::

            >>> atenxa.printLOG(obj1, obj2, obj3)

    Note:
        vrmapi.LOG() が受け付けるのは、ただ一つの
        int, float, str オブジェクトに限定されています。
    """
    output = sep.join(map(str, objects)) + end
    vrmapi.LOG(output)
    return output

def pprintLOG(object):
    """書式化したログ出力
    
    Pythonの構造的なデータを書式化して、'pretty-print'します。
    リストや辞書を、見やすくきれいに出力できます。
    
    Args:
        object: LOGに出したいオブジェクト。

    Return:
        str: ログへの出力内容。

    Example:
        センサーのイベントハンドラで、受け取った params(辞書)を表示。::

            >>> def vrmevent_xx(obj,ev,param):
            ...     if ev == 'catch':
            ...         pprintLOG(param)
            [2020/9/21 1:18:58][6.820493ns : ID 0] : string : 
            {'dir': 1,
            'eventUID': 0,
            'eventid': 8,
            'eventtime': 6.8204931000000215,
            'tire': 1,
            'trainid': 18}
    
    """
    from pprint import pformat

    output = pformat(object)
    printLOG("\n"+output)
    return output

class ATENXAError(Exception):
    """ATENXAシステムのエラー。"""
    pass