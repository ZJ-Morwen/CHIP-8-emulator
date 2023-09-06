import time

from cpu import Cpu
from memory import Memory
from display import Display
from keyboard import Keyboard

#  字库
FONTS = [0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
           0x20, 0x60, 0x20, 0x20, 0x70,  # 1
           0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
           0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
           0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
           0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
           0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
           0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
           0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
           0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
           0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
           0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
           0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
           0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
           0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
           0xF0, 0x80, 0xF0, 0x80, 0x80]  # F


# 总虚拟机部分
class Computer:
    def __init__(self) -> None:
        self.memory = Memory()
        self.keyboard = Keyboard()
        self.display = Display(self.keyboard)
        self.cpu = Cpu(self.memory, self.display, self.keyboard)
        self.display.config_screen()

    def import_fontset(self):  # 将字体存入内存最开始位置
        for i in range(0, len(FONTS)):
            self.memory.ram[i] = FONTS[i]

    def import_file(self, rompath):  # 将游戏文件导入cpu
        with open(rompath, "rb") as f:
            file_bytes = f.read()
            for i in range(len(file_bytes)):
                self.memory.ram[0x200 + i] = int(file_bytes[i])

    def run(self):
        print(time.time())
        self.cpu.cycle()
        self.display.screen.update()
        self.display.screen.ontimer(self.run, int(1000 / self.cpu.cpuhz))