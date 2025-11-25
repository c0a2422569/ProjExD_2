import os
import sys
import random
import time
import pygame as pg



WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0

    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))

    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = 5, 5

    DELTA = {pg.K_UP:    (0, -5),
             pg.K_DOWN:  (0, +5),
             pg.K_LEFT:  (-5, 0),
             pg.K_RIGHT: (+5, 0)}

    bb_imgs, bb_accs = init_bb_imgs()
    kk_imgs = get_kk_imgs()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])

        screen.blit(bb_img, bb_rct)
        avx = vx * bb_accs[min(tmr//500, 9)]
        avy = vy * bb_accs[min(tmr//500, 9)]
        bb_rct.move_ip(avx, avy)
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        bb_img.set_colorkey((0, 0, 0))
        

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        #if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5

        for k, mv in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        print(sum_mv)

        kk_rct.move_ip(sum_mv)
        kk_img = kk_imgs[tuple(sum_mv)]
        screen.blit(kk_img, kk_rct)

        if not check_bound(kk_rct):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        if not check_bound(bb_rct):
            if bb_rct.left < 0 or bb_rct.right > WIDTH:
                vx *= -1
            if bb_rct.top < 0 or bb_rct.bottom > HEIGHT:
                vy *= -1

        pg.display.update()
        if kk_rct.colliderect(bb_rct):
            gameover(pg.display.get_surface())
            return
        tmr += 1
        #print(tmr)
        clock.tick(50)

def check_bound(rct):
    if rct.left < 0 or rct.right > WIDTH:
        return False
    if rct.top < 0 or rct.bottom > HEIGHT:
        return False
    return True

def gameover(screen: pg.Surface) -> None:
    """
    gameover の Docstring
    
    :param screen: こうかとんと赤い球が衝突した際にgameover画面を表示するための関数
    :type screen: pg.Surface
    """
    bl_png = pg.Surface((WIDTH, HEIGHT))
    bl_png.set_alpha(200)
    text = pg.font.Font(None, 100).render("GAME OVER", True, (255, 255, 255))
    bl_png.blit(text, [WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2])
    kt_png = pg.image.load("fig/0.png")
    bl_png.blit(kt_png, [250, HEIGHT/2 - text.get_height()/2])
    bl_png.blit(kt_png, [850 - kt_png.get_width(), HEIGHT/2 - text.get_height()/2])
    screen.blit(bl_png, [0, 0])
    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    bb_accs = [i for i in range(1, 11)]
    return bb_imgs, bb_accs


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    img = pg.image.load("fig/3.png")
    reverse_img = pg.transform.flip(img, True, False)
    kk_dict = {
        (0, 0): pg.transform.rotozoom(reverse_img, 0, 1),
        (5, 0): pg.transform.rotozoom(reverse_img, 0, 1),
        (5, -5): pg.transform.rotozoom(reverse_img, 45, 1),
        (0, -5): pg.transform.rotozoom(reverse_img, 90, 1),
        (-5, -5): pg.transform.rotozoom(img, -45, 1),
        (-5, 0): pg.transform.rotozoom(img, 0, 1),
        (-5, 5): pg.transform.rotozoom(img, 45, 1),
        (0, 5): pg.transform.rotozoom(reverse_img, -90, 1),
        (5, 5): pg.transform.rotozoom(reverse_img, -45, 1),
    }
    return kk_dict

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
