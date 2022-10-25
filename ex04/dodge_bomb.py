import pygame as pg
import sys
from random import randint
import random

def check_bound(obj_rct, scr_rct): #はみ出さないように
    #obj_rct: こうかとんrct または 爆弾rct
    #scr_rct: スクリーンrct
    #領域内: +1, 領域外: -1
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom: 
        tate = -1
    return yoko, tate


def main():
    #練習1
    pg.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = pg.display.set_mode((1600, 900))
    scrn_rct = scrn_sfc.get_rect()
    bg_sfc = pg.image.load("fig/pg_bg.jpg")
    bg_rct = bg_sfc.get_rect()

    #練習3
    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 900, 400

    #練習5
    bomb_sfc = pg.Surface((50, 50)) #空のサーフェイス
    bomb_sfc.set_colorkey((0,0,0)) #四隅の黒の部分を透明にする
    pg.draw.circle(bomb_sfc, (255, 0, 0), (25, 25), 25) #円を描く
    bomb_rct = bomb_sfc.get_rect()
    bomb_rct.centerx = randint(0, scrn_rct.width/2)
    bomb_rct.centery = randint(0, scrn_rct.height/2)

    #大きい爆弾の作成
    bigbomb_sfc = pg.Surface((150, 150)) #空のサーフェイス
    bigbomb_sfc.set_colorkey((0,0,0)) #四隅の黒の部分を透明にする
    pg.draw.circle(bigbomb_sfc, (255, 0, 0), (75, 75), 75) #円を描く
    bigbomb_rct = bigbomb_sfc.get_rect()
    bigbomb_rct.centerx = randint(0, scrn_rct.width/2)
    bigbomb_rct.centery = randint(0, scrn_rct.height/2)

    #練習6
    vx, vy, big_vx, big_vy = +1, +1, +1, +1

    clock = pg.time.Clock() #時間計測用のオフジェクト
    while True:
        scrn_sfc.blit(bg_sfc, bg_rct) #練習2
    
        for event in pg.event.get(): #練習2
            if event.type == pg.QUIT:
                return
        
        #練習4
        key_state = pg.key.get_pressed()
        if key_state[pg.K_UP]: tori_rct.centery -= 1 #こうかとんの縦座標を-1
        if key_state[pg.K_DOWN]: tori_rct.centery += 1 #こうかとんの縦座標を+1
        if key_state[pg.K_LEFT]: tori_rct.centerx -= 1#こうかとんの横座標を-1
        if key_state[pg.K_RIGHT]: tori_rct.centerx += 1 #こうかとんの横座標を+1
        #練習7
        yoko, tate = check_bound(tori_rct, scrn_rct)
        if yoko == -1:
            if key_state[pg.K_LEFT]:
                tori_rct.centerx += 1
            if key_state[pg.K_RIGHT]:
                tori_rct.centerx -= 1
        if tate == -1:
            if key_state[pg.K_UP]:
                tori_rct.centery += 1
            if key_state[pg.K_DOWN]:
                tori_rct.centery -= 1

        scrn_sfc.blit(tori_sfc, tori_rct) #練習3
        
        #小さい爆弾の動き方
        yoko, tate = check_bound(bomb_rct, scrn_rct)
        vx *= yoko
        vy *= tate
        bomb_rct.move_ip(vx, vy) #練習6
        scrn_sfc.blit(bomb_sfc, bomb_rct) #練習5

        #大きい爆弾の動き方
        yoko, tate = check_bound(bigbomb_rct, scrn_rct)
        big_vx *= yoko
        big_vy *= tate
        bigbomb_rct.move_ip(big_vx, big_vy) #練習6
        scrn_sfc.blit(bigbomb_sfc, bigbomb_rct) #練習5

        #練習8
        if tori_rct.colliderect(bomb_rct) or tori_rct.colliderect(bigbomb_rct): #こうかとんrctが爆弾rctと重なったら
            #ゲームオーバーの文字を表示
            bomb_rct.move_ip(0, 0)
            font = pg.font.SysFont(None, 100)
            text = font.render("GAME OVER", False, (255, 0, 0))
            scrn_sfc.blit(text, (300, 450))
            #怒りのこうかとんに画像が変わる
            koukaton = [f"fig/{i}.png" for i in range(10)]
            tori_sfc = pg.image.load(random.choice(koukaton))
            tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
            #ぶつかると、画面全体が少し赤色に
            red_scr = pg.Surface((1600, 900), flags=pg.SRCALPHA)
            red_scr.fill((255, 0, 0, 128))
            scrn_sfc.blit(red_scr, (0, 0))

        pg.display.update() #練習2
        clock.tick(1000) #1000fpsを刻む


if __name__ == "__main__":
    pg.init() #初期化
    main() #ゲームの本体
    pg.quit() #初期化の解除
    sys.exit() #プログラムの終了