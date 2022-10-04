import tkinter as tk
import tkinter.messagebox as tkm

root = tk.Tk()
root.title("電卓")
root.geometry("300x600")#練習1

def button_crick(event):
    button = event.widget
    num = button["text"]
    #tkm.showinfo(f"{num}", f"{num}のボタンが押されました")#練習3
    entry.insert(tk.END, num)#練習5

takasa = 1
yoko = 0
numbers = list(range(9, -1, -1))
hugo = ["+"]
for i, num in enumerate(numbers+hugo, 1):
    button = tk.Button(root, text = f"{num}", font=("Times New Roman", 30), width=4, height=2)
    button.bind("<1>", button_crick)
    button.grid(row = takasa, column = yoko)
    yoko += 1
    if i % 3 == 0:
        takasa += 1
        yoko = 0 #練習2

#plus_button = tk.Button(root, text="+", font=("", 30), #width=4, height = 2)
#plus_button.grid(row = 4, column = 1)

entry = tk.Entry(root, justify="right", width=10, font=("Times New Roman", 40))
entry.grid(row = 0, column =0, columnspan = 3)#練習4

root.mainloop()