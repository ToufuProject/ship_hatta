from setting import *

class Map:
    def __init__(self, filename):
        # マップファイルを入れる箱を用意
        self.data = []
        # 第１引数で指定したファイルを、rまたはrt、つまり読み込みモードで開く
        # asの後の後には、任意の名前を使える。その名前をwithの中で使うイメージ。fを使うことが多い。
        with open(filename, "rt") as f:
            for line in f:
                #print(line)
                line = line.rstrip()  # 改行除去
                self.data.append(line)
        # 列が何行あるかをlenで出している
        self.row_num = len(self.data)
        # これがちょっとむずかも。おそらく最初の列（self.data[0]）を取り出して、その中に何文字含まれているかをlenで出している
        self.col_num = len(self.data[0])
        self.width = OBJECT_SIZE * self.col_num
        self.height = OBJECT_SIZE * self.row_num