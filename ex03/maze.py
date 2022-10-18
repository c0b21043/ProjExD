import imghdr
import tkinter as tk
from typing import TYPE_CHECKING
import maze_maker as mm
import tkinter.messagebox as tkm


def key_down(event):
    global key
    key = event.keysym


def key_up(event):
    global key
    key = ""


#ボタンクリックによってindexを増やし、古い画像を消して新しい画像を作り直している
index = 0 #画像のindexをグローバルで管理する
def btn_click(event):
    global index
    index = (index+1) % len(photos)
    canv.delete("tori")
    canv.create_image(cx, cy, image=photos[index], tag="tori")
    tkm.showinfo("画像変更", "こうかとんの画像が変更されました！\nかわいいですね^^")


def main_proc():
    global mx, my
    global cx, cy
    if key == "Up":
        my -= 1
    if key == "Down":
        my += 1
    if key == "Left":
        mx -= 1
    if key == "Right":
        mx += 1 

    if maze_lst[my][mx] == 0:
        cx, cy = mx*100+50, my*100+50
    else: #もし壁なら動かないようにする
        if key == "Up":
            my += 1
        if key == "Down":
            my -= 1
        if key == "Left":
            mx += 1
        if key == "Right":
            mx -= 1 

    canv.coords("tori", cx, cy)
    root.after(100, main_proc)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん")

    canv = tk.Canvas(root, width=1500, height=900, bg="black")
    canv.pack()
    
    maze_lst = mm.make_maze(15, 9) #1：壁、0：床
    mm.show_maze(canv, maze_lst)

    #こうかとんの写真のリスト
    photos=[tk.PhotoImage(file=f'fig/{i}.png') for i in range(1, 10)]

    mx, my = 1, 1
    cx, cy = mx*100+50, my*100+50
    canv.create_image(cx, cy, image=photos[index], tag="tori")

    key = ""

    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)

    btn = tk.Button(root, text="好きなこうかとんを選ぼう！", font=("", 20), width=50, height=50)
    btn.pack(ipadx=10, ipady=5)
    btn.bind("<1>", btn_click)

    main_proc()

    root.mainloop()