import pygame as pg
import sys
from random import randint


# スクリーン全体の作成クラス
class Screen:
    def __init__(self, title, wh, bgimg):
        pg.display.set_caption(title) # 食え！パックとん
        self.sfc = pg.display.set_mode(wh) # 800, 900
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(bgimg) # fig/black.png
        self.bgi_rct = self.bgi_sfc.get_rect()

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)


# こうかとん作成クラス
class Bird:
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
    }

    def __init__(self, img, zoom, xy):
        sfc = pg.image.load(img) # fig/7.png
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom) # 2.0
        self.rct = self.sfc.get_rect()
        self.rct.center = xy # 900, 400

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


# こうかとんをやっつけにくる爆弾クラス
class Bakudan:
    def __init__(self, color, radius, vxy, scr:Screen):
        self.sfc = pg.Surface((radius*2, radius*2))
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (radius, radius), radius)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(0, scr.rct.width/2)
        self.rct.centery = randint(0, scr.rct.height/2)
        self.vx, self.vy = vxy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        self.rct.move_ip(self.vx, self.vy) 
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)


# ドットを作成するクラス
class Dotto:
    def __init__(self, color, radius, scr:Screen):
        self.sfc = pg.Surface((radius*2, radius*2))
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (radius, radius), radius)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(10, scr.rct.width-10)
        self.rct.centery = randint(10, scr.rct.height-10)
    
    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        self.blit(scr)


# こうかとんがドットを食べるクラス
class Eat:
    def __init__(self, color, dot:Dotto, scr:Screen):
        pg.draw.circle(dot.sfc, color, (5, 5), 5)
        # ドットの色を黒にして、食べたようにみせる


# スコアを表示するクラス
class Score:
    def __init__(self, x, y):
        self.font = pg.font.SysFont(None, 40)
        self.score = 0
        (self.x, self.y) = (x, y)

    def draw(self, scr:Screen):
        text = self.font.render("SCORE:"+str(self.score), True, (255, 255, 255))
        scr.sfc.blit(text, (self.x, self.y))
    
    def add_score(self, x):
        self.score += x


# ゲームオーバーと表示するクラス
class Gameover:
    def __init__(self, text, color, basho, scr:Screen):
        font = pg.font.SysFont(None, 100)
        text = font.render(text, False, color)
        scr.sfc.blit(text, basho)


# ゲームクリアと表示するクラス
class Clear:
    def __init__(self, text, color, basho, scr:Screen):
        font = pg.font.SysFont(None, 100)
        text = font.render(text, False, color)
        scr.sfc.blit(text, basho)


# 移動に関する関数
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
    scr = Screen("食え！こうかとん", (800, 800), "fig/black.png")

    kkt = Bird("fig/7.png", 1.0, (750, 50))

    bkd = Bakudan((255, 0, 0), 50, (+1, +1), scr)
    
    dot1 = Dotto((255, 255, 255), 5, scr)
    dot2 = Dotto((255, 255, 255), 5, scr)
    dot3 = Dotto((255, 255, 255), 5, scr)
    dot4 = Dotto((255, 255, 255), 5, scr)
    dot5 = Dotto((255, 255, 255), 5, scr)
    dot6 = Dotto((255, 255, 255), 5, scr)
    dot7 = Dotto((255, 255, 255), 5, scr)
    dot8 = Dotto((255, 255, 255), 5, scr)
    dot9 = Dotto((255, 255, 255), 5, scr)

    score = Score(10, 10)

    clock = pg.time.Clock()
    while True:
        scr.blit()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        kkt.update(scr)
        bkd.update(scr)
        dot1.update(scr)
        dot2.update(scr)
        dot3.update(scr)
        dot4.update(scr)
        dot5.update(scr)
        dot6.update(scr)
        dot7.update(scr)
        dot8.update(scr)
        dot9.update(scr)

        score.draw(scr)
        
        # こうかとんがドットと重なったら
        if kkt.rct.colliderect(dot1.rct):
            Eat((0, 0, 0), dot1, scr)
            # スコアを1足す
            score.score += 1
            pg.display.update()
        
        if kkt.rct.colliderect(dot2.rct):
            Eat((0, 0, 0), dot2, scr)
            score.score += 1
            pg.display.update()

        if kkt.rct.colliderect(dot3.rct):
            Eat((0, 0, 0), dot3, scr)
            score.score += 1
            pg.display.update()

        if kkt.rct.colliderect(dot4.rct):
            Eat((0, 0, 0), dot4, scr)
            score.score += 1
            pg.display.update()

        if kkt.rct.colliderect(dot5.rct):
            Eat((0, 0, 0), dot5, scr)
            score.score += 1
            pg.display.update()

        if kkt.rct.colliderect(dot6.rct):
            Eat((0, 0, 0), dot6, scr)
            score.score += 1
            pg.display.update()

        if kkt.rct.colliderect(dot7.rct):
            Eat((0, 0, 0), dot7, scr)
            score.score += 1
            pg.display.update()

        if kkt.rct.colliderect(dot8.rct):
            Eat((0, 0, 0), dot8, scr)
            score.score += 1
            pg.display.update()
        
        if kkt.rct.colliderect(dot9.rct):
            Eat((0, 0, 0), dot9, scr)
            score.score += 1
            pg.display.update()

        # スコアが500を超えたら
        if score.score >= 500:
            # ゲームクリアと表示
            Clear("GAME CLEAR!", (255, 255, 255), (220, 300), scr)
            pg.display.update()
            clock.tick(1)
            return # ゲームを終わらせる

        # こうかとんが爆弾と重なったら
        if kkt.rct.colliderect(bkd.rct):
            # ゲームオーバーと表示
            Gameover("Gameover", (255, 0, 0), (220, 300), scr)
            pg.display.update()
            clock.tick(1)
            return # ゲームを終わらせる
                
        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()