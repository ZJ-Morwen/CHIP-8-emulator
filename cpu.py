import random
import time

# cpu部分
class Cpu:
    def __init__(self, memory, display, keyboard):
        self.register_v = [0] * 16  # 16个8bit通用寄存器（V0-VF）
        self.register_pc = 0x200  # pc寄存器从位置200开始读取
        self.register_i = 0  # I地址寄存器
        self.register_stack = 0xEA0  # 8bit栈顶寄存器
        self.sound_timer = 0  # 8bit声音定时器
        self.delay_timer = 0  # 8bit延迟定时器
        self.key_pressed = [0] * 16  # 按键缓存。按下为1未按下为0
        self.screen = 0  # 屏幕缓存
        self.memory = memory
        self.display = display
        self.keyboard = keyboard
        self.low_address = 0
        self.high_address = 0
        self.code = 0  # 从内存中读出的指令
        self.cpuhz = 500  # cpu频率
        self.timerhz = 60  # timer频率
        self.timer_cycle = 0

    def debug(self):
        print('code', hex(self.code))
        print('register', self.register_v, self.register_pc, self.register_i, self.register_stack)

    # cpu指令循环
    def cycle(self):
        self.fetch()
        self.decode()
        self.update_timer()
        # self.debug()

    def update_timer(self):
        # if self.timer_cycle >= self.cpuhz / self.timerhz:
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1
        self.timer_cycle = 0
        # else:
        #     self.timer_cycle += 1

    def fetch(self):  # 在对应内存中读取指令
        low_address = self.memory.ram[self.register_pc]
        high_address = self.memory.ram[self.register_pc + 1]
        self.code = (low_address << 8) | high_address  # low_address左移八位与high_address合并指令
        self.register_pc += 2  # 对pc指针进行移动

    def stack_push(self, pc):
        low_address = pc & 0x00FF
        high_address = (pc & 0xFF00) >> 8
        self.memory.ram[self.register_stack] = low_address
        self.register_stack += 1
        self.memory.ram[self.register_stack] = high_address
        self.register_stack += 1

    def stack_pop(self):
        self.register_stack -= 1
        high_address = self.memory.ram[self.register_stack]
        self.register_stack -= 1
        low_address = self.memory.ram[self.register_stack]
        return (high_address << 8) | low_address

    def decode_zero(self):
        if self.code & 0x0F00 == 0x000:  # 如果第二位为0:
            if self.code & 0x00FF == 0xE0:  # 00e0
                self.display.turtle.clear()
            elif self.code & 0x00FF == 0xEE:  # 00ee
                self.register_pc = self.stack_pop()
        else:  # 0nnn
            pass
            print('0nnn')

    def decode_eight(self):
        num = self.code & 0x000F
        x = (self.code & 0x0F00) >> 8
        y = (self.code & 0x00F0) >> 4
        if num == 0:  # 8xy0
            self.register_v[x] = self.register_v[y]
        elif num == 1:  # 8xy1 ###############按位或？
            self.register_v[x] |= self.register_v[y]
        elif num == 2:  # 8xy2
            self.register_v[x] &= self.register_v[y]
        elif num == 3:  # 8xy3
            self.register_v[x] ^= self.register_v[y]
        elif num == 4:  # 8xy4
            self.register_v[x] += self.register_v[y]
            if self.register_v[x] > 255:  # vx进位后vf为1否则为0
                self.register_v[0xF] = 1
            else:
                self.register_v[0xF] = 0
            self.register_v[x] &= 0xFF
        elif num == 5:  # 8xy5
            self.register_v[x] -= self.register_v[y]
            if self.register_v[x] < 0:  # vx负数时vf为0否则为1
                self.register_v[0xF] = 0
            else:
                self.register_v[0xF] = 1
            self.register_v[x] &= 0xFF
        elif num == 6:  # 8xy6
            self.register_v[0xF] = self.register_v[x] & 0x01
            self.register_v[x] >>= 1
        elif num == 7:  # 8xy7
            self.register_v[x] = self.register_v[y] - self.register_v[x]
            if self.register_v[x] < 0:  # vx负数时vf为0否则为1
                self.register_v[0xF] = 0
            else:
                self.register_v[0xF] = 1
            self.register_v[x] &= 0xFF
        elif num == 0xE:  # 8xye
            self.register_v[0xF] = (self.register_v[x] >> 7) & 1
            self.register_v[x] = self.register_v[y] << 1
            self.register_v[x] &= 0xFF

    def decode_F(self):
        x = (self.code & 0x0F00) >> 8
        num1 = (self.code & 0x00F0) >> 4
        num2 = (self.code & 0x000F)
        if num1 == 0:
            if num2 == 7:  # fx07
                self.register_v[x] = self.delay_timer
            elif num2 == 0xA:  # fx0a
                flag = 0
                while flag == 0:
                    print('wait key:')
                    for i in range(16):
                        if self.keyboard.keyboard[i] == 1:
                            self.register_v[x] = i
                            print("get key:", i)
                            self.keyboard.keyboard[i] = 0
                            flag = 1
                            break
        elif num1 == 1:
            if num2 == 5:  # fx15
                self.delay_timer = self.register_v[x]
            elif num2 == 8:  # fx18
                self.sound_timer = self.register_v[x]
            elif num2 == 0xE:  # fx1e
                self.register_i += self.register_v[x]
        elif num1 == 2:  # fx29
            self.register_i = self.register_v[x] * 5
        elif num1 == 3:  # fx33  ######?
            self.memory.ram[self.register_i] = self.register_v[x] // 100
            self.memory.ram[self.register_i + 1] = (self.register_v[x] % 100) // 10
            self.memory.ram[self.register_i + 2] = (self.register_v[x] % 100) % 10
        elif num1 == 5:  # fx55
            address = self.register_i
            for j in range(0, x + 1):  #######内存数字存8bit
                self.memory.ram[address] = self.register_v[j]
                address += 1
        elif num1 == 6:
            address = self.register_i
            for j in range(0, x + 1):
                self.register_v[j] = self.memory.ram[address]
                address += 1

    def decode(self):  # 解析指令
        instruction = self.code & 0xF000
        if instruction == 0x0000:  # 如果指令以0开头
            self.decode_zero()
        elif instruction == 0x1000:  # 1nnn
            address_1 = self.code & 0x0FFF
            self.register_pc = address_1
        elif instruction == 0x2000:  # 2nnn
            address_2 = self.code & 0x0FFF
            self.stack_push(self.register_pc)  # pc指针入栈
            self.register_pc = address_2
        elif instruction == 0x3000:  # 3xnn
            x = (self.code & 0x0F00) >> 8
            nn = self.code & 0x00FF
            if self.register_v[x] == nn:
                self.register_pc += 2
        elif instruction == 0x4000:  # 4xnn
            x = (self.code & 0x0F00) >> 8
            nn = self.code & 0x00FF
            if self.register_v[x] != nn:
                self.register_pc += 2
        elif instruction == 0x5000:  # 5xy0
            x = (self.code & 0x0F00) >> 8
            y = (self.code & 0x00F0) >> 4
            if self.register_v[x] == self.register_v[y]:
                self.register_pc += 2
        elif instruction == 0x6000:  # 6xnn
            x = (self.code & 0x0F00) >> 8
            nn = self.code & 0x00FF
            self.register_v[x] = nn
        elif instruction == 0x7000:  # 7xnn
            x = (self.code & 0x0F00) >> 8
            nn = self.code & 0x00FF
            self.register_v[x] += nn
            self.register_v[x] &= 0xFF
        elif instruction == 0x8000:  # 指令以8开头
            self.decode_eight()
        elif instruction == 0x9000:  # 9xy0
            x = (self.code & 0x0F00) >> 8
            y = (self.code & 0x00F0) >> 4
            if self.register_v[x] != self.register_v[y]:
                self.register_pc += 2
        elif instruction == 0xA000:  # ANNN
            self.register_i = self.code & 0x0FFF
        elif instruction == 0xB000:  # BNNN
            nnn = self.code & 0X0FFF
            self.register_pc = self.register_v[0] + nnn
        elif instruction == 0xC000:  # cxnn
            x = (self.code & 0x0F00) >> 8
            nn = self.code & 0x00FF
            rand = random.randrange(0, 255)
            self.register_v[x] = rand & nn
        elif instruction == 0xD000:  # dxyn
            x = (self.code & 0x0F00) >> 8
            y = (self.code & 0x00F0) >> 4
            n = self.code & 0x000F
            vx = self.register_v[x]
            vy = self.register_v[y]
            self.register_v[0xF] = 0
            for i in range(0, n):
                i_code = self.memory.ram[self.register_i + i]
                for j in range(0, 8):
                    i_decode = (i_code >> (7 - j)) & 0x01
                    canvas_position = (vy + i) * 64 + (vx + j)
                    if 0 <= canvas_position < 2048:
                        if self.display.canvas[canvas_position] & i_decode == 1:
                            self.register_v[0xF] = 1
                        self.display.canvas[canvas_position] ^= i_decode
                        self.display.draw_square(vx + j, vy + i)
        elif instruction == 0xE000:
            num = (self.code & 0x00F0) >> 4
            x = (self.code & 0x0F00) >> 8
            if num == 0x9:  # ex9e
                vx = self.register_v[x]
                if self.keyboard.keyboard[vx] == 1:
                    self.register_pc += 2
                    self.keyboard.keyboard[vx] = 0
            elif num == 0xA:  # exa1
                vx = self.register_v[x]
                if self.keyboard.keyboard[vx] == 0:
                    self.register_pc += 2
                else:
                    self.keyboard.keyboard[vx] = 0
        elif instruction == 0xF000:
            self.decode_F()