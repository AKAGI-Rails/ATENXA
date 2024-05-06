# -*- coding: utf-8 -*-
"""
vrmapi.VRMSpriteのラッパとユーティリティ
"""
import vrmapi

class Sprite(object):
    """vrmapi.VRMSpriteクラスのラッパ。

    SetUV(), SetPos()をした後，frameイベント内でSetSprite()してください。(直接指定モード)

    SetUV(), SetOrg(), SetZoom(), SetRotate(), SetTranslate()を設定しておき，
    スプライト座標をVRMNXシステム内部で処理してからSetSprite()で表示することもできます。（演算指定モード）

    SetPos()かSetOrg()を呼び出すと，SetSprite()での描画モードが相応に切り替わります。
    各属性値をを直接いじってSetSprite()も可能です。その際，描画モードはdispdirect属性に従います。

    Note:
        コンストラクタはリソース画像読み込み済みのSpriteオブジェクトを返します。
    
    Args:
        res: リソース画像の番号。
        src: リソースの読み込み先となる編成オブジェクトのID。デフォルトではレイアウトのリソースから読み込みます。

    Attributes:
        uv: UV座標のタプル (u0, v0, u1, v1)
        pos: 表示座標のタプル (sx0,sy0, sx1,sy1, sx2,sy2, sx3,sy3)
        org: 演算指定モードでの基準サイズ (dx, dy)
        trans: 移動量(x,y)
        color: 表示色(r,g,b,a)
        pivot: 回転中心(x,y)
        rot: 回転角度(deg)のfloat。
        dispdirect: Trueで直接指定モード。Falseで演算指定モード。

    Examples:
        >>> sp1 = Sprite(1) #Layoutからリソース1番の画像を読み込み，スプライトオブジェクトを生成
        >>> sp1.SetUV(0,0,256,256)
        >>> sp1.SetPos(10,10,200,10,10,300,200,300)

        frameイベントでスプライトを表示させます。

        >>> if ev == 'frame':
        >>>     sp1.SetSprite()
    
    """

    def __init__(self, res, src=0):
        vrmsprite = vrmapi.LAYOUT().CreateSprite()
        if src:
            vrmsprite.LoadTrainTexture(src, res)
        else:
            vrmsprite.LoadSystemTexture(res)
        self.vrmsprite = vrmsprite

        self.uv = None          #: UV座標のタプル (u0, v0, u1, v1)
        self.pos = None         #: 表示座標のタプル (sx0,sy0, sx1,sy1, sx2,sy2, sx3,sy3)
        self.org = None         #: 演算指定モードでの基準サイズ (dx, dy)
        self.zoom = (1.0, 1.0)  #: 拡大縮小の倍率 (rx, ry)
        self.pivot = (0.0, 0.0) #: 回転中心(x,y)
        self.rot = 0.0          #: 回転角
        self.trans = (0.0, 0.0) #: 移動量(x,y)
        self.color = None       #: スプライトのカラー(r,g,b,a). 0.0<=r,g,b,a<=1.0.
        self.dispdirect = True  #: Trueで直接指定モード

    def GetTextureDX(self):
        """スプライトにロードしたテクスチャー画像のXサイズを取得する。"""
        return self.vrmsprite.GetTextureDX()

    def GetTextureDY(self):
        """スプライトにロードしたテクスチャー画像のYサイズを取得する。"""
        return self.vrmsprite.GetTextureDY()

    def SetUV(self, u0,v0, u1,v1):
        """スプライトパターンを設定。

        u0,v0がスプライトパターンの左上座標。u1,v1は右下の座標。

        Note:
            vrmapi.VRMSpriteと違い，毎フレームでSetUVを実行する必要はありません。
        """
        self.uv = (u0, v0, u1, v1)

    def SetPos(self, sx0,sy0, sx1,sy1, sx2,sy2, sx3,sy3):
        """スプライトの表示座標を設定
        
        四角形スプライトの画面上の座標を設定します。
        このメソッドを実行すると，それ以降は直接指定モードでスプライトを描画します。

        Args:
            sx0
            sy0: 左上座標
            sx1
            sy1: 右上座標
            sx2
            sy2: 左下座標
            sx3
            sy3: 右下座標

        Note:
            vrmapi.VRMSpriteと違い，毎フレームでSetPosを実行する必要はありません。
        """
        self.pos = (sx0,sy0, sx1,sy1, sx2,sy2, sx3,sy3)
        self.dispdirect = True

    def SetOrg(self, orgdx, orgdy):
        """ スプライトの基準サイズを設定します。

        このメソッドを実行して以降は，演算指定モードでスプライトを描画します。
        基準サイズをもとに、拡大縮小、回転、移動の演算を順番に行い、
        結果をSetSprite()で表示します。

        Args:
            orgdx
            orgdy: 基準サイズ
        """
        self.org = (orgdx, orgdy)
        self.dispdirect = False

    def SetZoom(self, zoomx, zoomy):
        """スプライトの拡大縮小率を設定します。

        描画モードが演算指定モードのときに使用されます。

        Args:
            zoomx
            zoomy: 1.0で等倍。
        """
        self.zoom = (zoomx, zoomy)
        self.dispdirect = False

    def SetRotate(self, pivotx, pivoty, rot):
        """スプライトの回転を設定します。

        描画モードが演算指定モードのときに使用されます。

        Args:
            pivotx
            pivoty: 回転中心座標。0.0で原点。
            rot: 回転角度(deg)
        """
        self.pivot = (pivotx, pivoty)
        self.rot = rot
        self.dispdirect = False

    def SetTranslate(self, x,y):
        """スプライトの移動を設定します。
        
        描画モードが演算指定モードのときに使用されます。
        """
        self.trans = (x,y)
        self.dispdirect = False

    def SetColor(self, r,g,b,a):
        """スプライトの色を指定します。
        
        r,g,b,a: 0.0～1.0の数値を設定します。
        """
        self.color = (r,g,b,a)

    def SetSprite(self):
        """スプライトを画面に表示。
        
        直接指定モードか演算指定モードを自動で選択して表示します。
        """
        self.vrmsprite.SetUV(self.uv[0], self.uv[1], self.uv[2], self.uv[3])
        if self.dispdirect:
            # 直接指定モード
            self.vrmsprite.SetPos(self.pos[0], self.pos[1], self.pos[2], self.pos[3], self.pos[4], self.pos[5], self.pos[6], self.pos[7])
        else:
            # 演算指定モード
            if self.org:
                self.vrmsprite.SetOrg(self.org[0], self.org[1])
            self.vrmsprite.SetZoom(self.zoom[0], self.zoom[1])
            self.vrmsprite.SetRotate(self.pivot[0], self.pivot[1], self.rot)
            self.vrmsprite.SetTranslate(self.trans[0], self.trans[1])
        if self.color is not None:
            self.vrmsprite.SetColor(self.color[0], self.color[1], self.color[2], self.color[3])
        self.vrmsprite.SetSprite()

