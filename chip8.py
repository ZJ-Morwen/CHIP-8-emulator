import time

from computer import Computer


def main():
    rompath = '.\\rom\\TETRIS'
    computer = Computer()
    computer.import_fontset()      # 加载字体到内存
    computer.import_file(rompath)  # 加载运行程序
    computer.run()
    computer.display.screen.mainloop()


main()
