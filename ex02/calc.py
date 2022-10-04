import tkinter as tk
import tkinter.messagebox as tkm


root = tk.Tk()
root.title("わたしの電卓")
root.geometry("400x700") #練習1


#数字を押すための関数
def button_crick(event):
    button = event.widget
    num = button["text"]
    entry.insert(tk.END, num) #練習5


#イコールボタンのための関数
def equal_click(event):
    shiki = entry.get()
    kekka = eval(shiki)
    entry.delete(0, tk.END)
    entry.insert(tk.END, kekka)


#一文字だけ消すクリアボタンのための関数
def clear_click(event):
    entry.delete(1, tk.END)


#オールクリアボタンのための関数
def ALLclear_click(event):
    entry.delete(0, tk.END)


#電源をオフにするための関数
def OFF(event):
    root.destroy()


takasa = 1
yoko = 0
numbers = list(range(9, -1, -1))
hugo = ["+", "-", "*", "/", "."]
for i, num in enumerate(numbers+hugo, 1):
    button = tk.Button(root, text = f"{num}", font=("Times New Roman", 20), width=8, height=2)
    button.bind("<1>", button_crick)
    button.grid(row = takasa, column = yoko)
    button["activebackground"] = "#CCFFFF"
    yoko += 1
    if i % 3 == 0:
        takasa += 1
        yoko = 0 #練習2


#イコールボタンの作成
equal_button = tk.Button(root, text = f"=", font=("Times New Roman", 20), width=8, height=2)
equal_button["activebackground"] = "#CCFFFF"
equal_button.grid(row = 6, column = 2)
equal_button.bind("<1>", equal_click)



#一文字だけ消すボタンの作成
clear_button = tk.Button(root, text="C", font=("Times New Roman", 20), width=8, height=2)
clear_button["activebackground"] = "#CCFFFF"
clear_button.grid(row = 6, column = 0)
clear_button.bind("<1>", clear_click)


#全部消すボタンの作成
ALLclear_button = tk.Button(root, text="AC", font=("Times New Roman", 20), width=8, height=2)
ALLclear_button["activebackground"] = "#CCFFFF"
ALLclear_button.grid(row = 6, column = 1)
ALLclear_button.bind("<1>", ALLclear_click)


#電源オフボタンの作成
OFF_button = tk.Button(root, text="OFF", font=("Times New Roman", 20), width=8, height=2)
OFF_button.grid(row = 7, column = 2)
OFF_button.bind("<1>", OFF)


entry = tk.Entry(root, justify="right", width=10, font=("Times New Roman", 40))
entry.grid(row = 0, column =0, columnspan = 3) #練習4


root.mainloop()