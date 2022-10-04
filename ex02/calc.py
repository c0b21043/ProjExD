import tkinter as tk
import tkinter.messagebox as tkm

root = tk.Tk()
root.title("電卓")
root.geometry("300x500")#練習1

def button_crick(event):
    button = event.widget
    num = int(button["text"])
    tkm.showinfo(f"{num}", f"{num}のボタンが押されました")#練習3

takasa = 1
yoko = 0
for i, num in enumerate(range(9, -1, -1), 1):
    button = tk.Button(root, text = f"{num}", font=("Times New Roman", 30), width=4, height=2)
    button.bind("<1>", button_crick)
    button.grid(row = takasa, column = yoko)
    yoko += 1
    if i % 3 == 0:
        takasa += 1
        yoko = 0 #練習2

entry = tk.Entry(root, justify="right", width=10, font=("Times New Roman", 40))
entry.grid(row = 0, column =0, columnspan = 3)#練習4

root.mainloop()