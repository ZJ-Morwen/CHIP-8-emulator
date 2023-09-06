#键盘控制部分
class Keyboard:
    def __init__(self):
        self.keyboard = [0] * 16
        self.keylist = ['1' , '2' , '3', '4' , 'q' , 'w' , 'e' , 'r' , 'a' , 's' , 'd' , 'f' , 'z' , 'x' , 'c' , 'v']
        self.chip8_keylist = [1 , 2 , 3 , 0xc , 4 , 5 , 6 , 0xd , 7 , 8 , 9 , 0xe , 0xa , 0 , 0xb , 0xf]
        self.keynum = 0
        self.key = 0

    def set_keyboard(self , key):
        self.keynum = self.keylist.index(key)
        self.key = self.chip8_keylist[self.keynum]
        self.keyboard[self.key] = 1