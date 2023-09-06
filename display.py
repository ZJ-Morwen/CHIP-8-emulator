import turtle
import time
from functools import partial

#显示部分
class Display:
    def __init__(self , keyboard):
        self.screen = turtle.Screen()
        self.turtle = turtle.Turtle()
        self.canvas = [0] * 64 * 32  #取位置：y * 64 + x
        self.keyboard = keyboard
        self.screen.onkey(partial(self.keyboard.set_keyboard,'1') , '1')
        self.screen.onkey(partial(self.keyboard.set_keyboard,'2') , '2')
        self.screen.onkey(partial(self.keyboard.set_keyboard,'3') , '3')
        self.screen.onkey(partial(self.keyboard.set_keyboard,'4') , '4')
        self.screen.onkey(partial(self.keyboard.set_keyboard,'q') , 'q')
        self.screen.onkey(partial(self.keyboard.set_keyboard,'w') , 'w')
        self.screen.onkey(partial(self.keyboard.set_keyboard,'e') , 'e')
        self.screen.onkey(partial(self.keyboard.set_keyboard,'r') , 'r')
        self.screen.onkey(partial(self.keyboard.set_keyboard,'a') , 'a')
        self.screen.onkey(partial(self.keyboard.set_keyboard,'s') , 's')
        self.screen.onkey(partial(self.keyboard.set_keyboard,'d') , 'd')
        self.screen.onkey(partial(self.keyboard.set_keyboard,'f') , 'f')
        self.screen.onkey(partial(self.keyboard.set_keyboard,'z') , 'z')
        self.screen.onkey(partial(self.keyboard.set_keyboard,'x') , 'x')
        self.screen.onkey(partial(self.keyboard.set_keyboard,'c') , 'c')
        self.screen.onkey(partial(self.keyboard.set_keyboard,'v') , 'v')
        self.screen.listen()

    def config_screen(self):  #初始化屏幕
        self.screen.tracer(0)
        self.screen.mode("standard")
        self.screen.setup(640 , 320)
        self.screen.setworldcoordinates(0 , 319 , 639 , 0)
        self.turtle.ht()
        self.turtle.penup()
        self.turtle.speed(0)

    def draw_square(self , x , y):
        zoom = 10  #缩放倍数
        self.turtle.goto(x * zoom , y * zoom)
        self.turtle.pendown()
        if self.canvas[y * 64 + x] == 1:
            self.turtle.color('black' , 'black')
        else:
            self.turtle.color('white' , 'white')
        self.turtle.begin_fill()
        for i in range(0 , 4):
            self.turtle.fd(zoom)
            self.turtle.left(90)
        self.turtle.end_fill()
        self.turtle.penup()