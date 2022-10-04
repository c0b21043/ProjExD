import tkinter as tk
import tkinter.messagebox as tkm

root = tk.Tk()
root.title("電卓")
root.geometry("300x500")#練習1

def button_crick(event):
    button = event.widget
    num = int(button["text"])
    tkm.showinfo(f"{num}", f"{num}のボタンが押されました")#練習3

r = 0
c = 0
for i, num in enumerate(range(9, -1, -1), 1):
    button = tk.Button(root, text = f"{num}", font=("Times New Roman", 30), width=4, height=2)
    button.bind("<1>", button_crick)
    button.grid(row = r, column = c)
    c += 1
    if i%3==0:
        r += 1
        c = 0 #練習2



root.mainloop()