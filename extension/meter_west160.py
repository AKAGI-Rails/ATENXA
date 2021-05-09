# -*- coding: utf-8 -*-
"""速度計　西の特急風 (Texture by Dilexer)

西日本特急車両風のデジタル速度計(160km/h)のための
ATENXAの速度計パッケージに対応した，拡張モジュールです。
テクスチャはDilexerさん(@dilexer223)のものです。
"""
from threading import Timer
from atenxa import LAYOUT, NXSYS
from atenxa.meter import *

class MeterWest160(MeterBase):
    """速度計　西の特急風 (160km/h)
    
    西日本特急車両風のデジタル速度計(160km/h)です。
    テクスチャはDilexerさん(@dilexer223)のものです。
    Example:
        編成スクリプトのイベントハンドラ直下にactivate関数を書き込みます。
        編成リソースのID=1のテクスチャーを使用する例です。
        >>> def vrmevent_xx(obj,ev,param):
        ...     meter_west160.activate(obj,ev,param, meter_west160.MeterWest160, 1)
    """
    def setup(self):
        # ここでnew_sprite()して基本的な設定をしておくとよい。
        # Spriteのインスタンスは好きな名前のクラス属性に突っ込んでください。

        # デジタル表示 (3桁分)
        self.digit = [self.new_sprite() for i in range(3)]
        for e, dsp in enumerate(self.digit):
            dsp.SetUV(512,240, 512+90,360)
            dsp.SetZoom(0.5, 0.5)
            dsp.SetTranslate(16+45*e, 1016)
        # digit[0]:100の位

        self.cover = self.new_sprite()
        self.cover.SetUV(0,0,512,512)
        self.cover.SetZoom(0.5, 0.5)
        self.cover.SetTranslate(0, 824)

        self.gauge = [self.new_sprite() for i in range(3)]
        for i, gsp in enumerate(self.gauge):
            gsp.SetUV(512,360, 512+180,363+180)
            gsp.SetZoom(0.5, 0.5)
            gsp.SetRotate(0,0, 45)
            gsp.SetTranslate(128, 952)

        self.meterbase = self.new_sprite()
        self.meterbase.SetUV(580, 551, 581, 552)
        self.meterbase.SetOrg(360,360)
        self.meterbase.SetZoom(0.5,0.5)
        self.meterbase.SetTranslate(39,861)

        # デジタル表示の更新インターバル
        self.nextflash = 0.1
        self.interval = 0.2
        self.gauge_update()

    def display(self):
        t = NXSYS.GetSystemTime()
        if t > self.nextflash:
            self.gauge_update()
            self.nextflash += self.interval
        for dsp in self.digit:
            dsp.SetSprite()
        for gsp in self.gauge:
            gsp.SetSprite()
        self.cover.SetSprite()
        self.meterbase.SetSprite()

    def gauge_update(self):
        spd = self._train.GetSpeed()

        for e,dsp in enumerate(self.digit):
            c = "{:03.0f}".format(spd)[e]
            #LOG(c)
            n = int(c)
            if spd >= 10.0**(2-e) or e == 2:
                u0,v0,u1,v1 = self.digituv(n)
                dsp.SetUV(u0,v0,u1,v1)
            else:
                dsp.SetUV(512,240, 512+90,360)
            #dsp.SetSprite()

        rot = 1.5 * (spd//2)*2 + 60
        for i,gsp in enumerate(self.gauge):
            gsp.rot = min(rot, 1.5 * 60 * (i+1) + 60)
            #gsp.SetSprite()

    def digituv(self, n):
        """数字に対応するテクスチャのuvを取得
        
        Args:
            n: 数字 (一桁のint)
            
        Returns:
            (u0, v0, u1, v1) タプル型。

        Note:
            nに不正な値を入れてもValueErrorを送出しません。結果は不定になります。
        """
        u0 = 512 + 90*n
        v0 = 0
        if n >= 5:
            u0 -= 450
            v0 = 120
        return u0,v0, u0+90, v0+120
