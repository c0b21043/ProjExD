import random

def shutudai(mondai_list):
    mondai = random.choice(mondai_list)
    print("問題:"+mondai["q"])
    return mondai["a"]


def kaito(seikai_list):
    ans = input("答えるんだ:")
    if ans in seikai_list:
        print("正解")
    else:
        print("不正解")

if __name__ == "__main__":
    mondai_list =[
        {"q":"サザエの旦那は?", "a":["マスオ", "ますお"]},
        {"q":"カツオの妹は?", "a":["ワカメ", "わかめ"]},
        {"q":"タラオはカツオから見て何?", "a":["おい", "甥っ子", "甥", "おいっこ"]}
        ]
    seikai_list = shutudai(mondai_list)
    kaito(seikai_list)
    