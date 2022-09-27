import random
import datetime 

all_moji = 26
kesson_num = 2
moji_num = 10
roop_num = 2

def shutudai(alphabet):
    mojisuu = random.sample(alphabet, moji_num)
    print("対象文字:", end="")
    for i in sorted(mojisuu):
        print(i, end=" ")
    print()
    kesson = random.sample(mojisuu, kesson_num)
    print("表示文字:", end="")
    for i in mojisuu:
        if i not in kesson:
            print(i, end=" ")

    print()
    print("デバッグ用欠損文字:", kesson)


def kaito(seikai):
    ans_num = int(input("欠損文字はいくつあるでしょうか?:"))
    if ans_num != kesson_num:
        print("不正解です")
    else:
        print("正解です, それでは具体的に欠損文字を一つずつ入力してください")
        for i in range(ans_num):
            ans_kesson = input(f"{i+1}つ目の文字を入力してください:")
            if ans_kesson not in seikai:
                print("不正解です,やり直せ！")
                return False
            else:
                seikai.remove(ans_kesson)
        
        else:
            print("欠損文字も含めて正解！")
            return True
    return False

if __name__ == "__main__":
    alphabet = [chr(i+65) for i in range(all_moji)]
    shutudai(alphabet)

    for sen in range(roop_num):
        kesson = shutudai(alphabet)
        ret = kaito(kesson)
        if ret:
            break
        else:
            print("-"*20)