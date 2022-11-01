import pygame as pg
import sys
from random import randint
import random
import os

key_delta = {
    pg.K_UP:    [0, -1],
    pg.K_DOWN:  [0, +1],
    pg.K_LEFT:  [-1, 0],
    pg.K_RIGHT: [+1, 0],
}

main_dir = os.path.split(os.path.abspath(__file__))[0]


class Screen:
    def __init__(self, title, wh, bgimg):
        pg.display.set_caption(title)#にげろこうかとん
        self.sfc = pg.display.set_mode(wh)#1600, 900
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(bgimg)#"fig/pg_bg.jpg"
        self.bgi_rct = self.bgi_sfc.get_rect()
    
    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)


class Bird:
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
        }

    def __init__(self, img, zoom, xy):
        sfc = pg.image.load(img)#"fig/6.png"
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)#2.0
        self.rct = self.sfc.get_rect()
        self.rct.center = xy #900, 400

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        key_states = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_states[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]
                if check_bound(self.rct, scr.rct) != (+1, +1):
                    self.rct.centerx -= delta[0]
                    self.rct.centery -= delta[1]
        self.blit(scr)
        

#触れるとしんでしまう爆弾のクラス
class Bombsaikyou:
    def __init__(self, color, radius, vxy, scr:Screen):
        self.sfc = pg.Surface((radius*2, radius*2)) # 空のSurface
        self.sfc.set_colorkey((0, 0, 0)) # 四隅の黒い部分を透過させる
        pg.draw.circle(self.sfc, color, (radius, radius), radius) # 爆弾用の円を描く
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(0, scr.rct.width)
        self.rct.centery = randint(0, scr.rct.height)
        self.vx, self.vy = vxy # 練習6

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        self.rct.move_ip(self.vx, self.vy) # 練習6
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)


#倒せる爆弾のクラス
class Bombyowai:
    def __init__(self, color, radius, vxy, scr:Screen):
        self.sfc = pg.Surface((radius*2, radius*2)) # 空のSurface
        self.sfc.set_colorkey((0, 0, 0)) # 四隅の黒い部分を透過させる
        pg.draw.circle(self.sfc, color, (radius, radius), radius) # 爆弾用の円を描く
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(0, scr.rct.width/2)
        self.rct.centery = randint(0, scr.rct.height/2)
        self.vx, self.vy = vxy # 練習6

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        self.rct.move_ip(self.vx, self.vy) # 練習6
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)


#ゲームオーバーと表示するクラス
class Gameover:
    def __init__(self, text, color, basho,scr:Screen):
        font = pg.font.SysFont(None, 100)
        text = font.render(text, False, color) # "GAME OVER", False, (255, 0, 0)
        scr.sfc.blit(text, basho) # 300, 450


#画像チェンジのクラス
class Change:
    def __init__(self,zoom, kkt:Bird):
        kkt.sfc = pg.image.load('fig/7.png')
        kkt.sfc = pg.transform.rotozoom(kkt.sfc, 0, zoom) # 2.0


#タックルして倒すクラス
class Tackle:
    def __init__(self, color, bkd2:Bombyowai, scr:Screen):
        pg.draw.circle(bkd2.sfc, color, (50, 50), 50)


#爆弾の効果音のクラス
class Music:
    def load_sound(file):
        if not pg.mixer:
            return None
        file = os.path.join(main_dir, "data", file)
        try:
            sound = pg.mixer.Sound(file)
            return sound
        except pg.error:
            print("Warning, unable to load, %s" % file)
        return None


def check_bound(obj_rct, scr_rct):
    """
    obj_rct：こうかとんrct，または，爆弾rct
    scr_rct：スクリーンrct
    領域内：+1／領域外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right: 
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom: 
        tate = -1
    return yoko, tate


def main():
    scr = Screen("逃げろ！！こうかとん", (1600, 900), "fig/pg_bg.jpg")

    kkt = Bird("fig/6.png", 2.0, (900, 400))

    bkd = Bombsaikyou((255, 0, 0), 10, (+1, +1), scr)
    bkd2 = Bombyowai((255, 0, 0), 50, (+1, +1), scr)

    boom_sound = pg.mixer.Sound("fig/boom.wav")

    clock = pg.time.Clock() 
    while True:
        scr.blit()
        
        for event in pg.event.get(): 
            if event.type == pg.QUIT:
                return

        kkt.update(scr)

        bkd.update(scr)
        bkd2.update(scr)

        if kkt.rct.colliderect(bkd.rct): # こうかとんrctが爆弾rctと重なったら
            Gameover("GameOver", (255, 0, 0), (300, 450), scr)
            Change(2.0, kkt)
            if pg.mixer:
                boom_sound.play()
            pg.display.update()
            clock.tick(1)
            return
            
        elif kkt.rct.colliderect(bkd2.rct):
            Tackle((175, 228, 227), bkd2, scr)
            pg.display.update()
            
        pg.display.update() 
        clock.tick(1000)


if __name__ == "__main__":
    pg.init() # 初期化
    main()    # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()