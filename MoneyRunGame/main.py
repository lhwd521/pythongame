import cocos
from cocos import scene
from cocos.scene import Scene
from cocos.scenes import SplitColsTransition
from cocos.director import director
from cocos.layer import Layer
from cocos.text import Label
from cocos.sprite import Sprite
from cocos.menu import *
from cocos.actions import *
from pyglet.window.key import symbol_string
import pyglet
import random

# 方块死亡时的坐标记录
rect_x = 0
rect_y = 0
# 选择角色
role = [
    "images/husband.png",
    "images/father.png",
    "images/grandfather.png"
]
role_choose = [
    "images/husband.jpg",
    "images/father.jpg",
    "images/grandfather.jpg"
]
# 选择场景
scene_choose = [
    ["images/ground.png", "images/sky.jpg"],
    ["images/ground1.png", "images/sky1.png"],
    ["images/ground2.png", "images/sky2.png"]
]
# 角色选择序号
choose_i = 1
# 场景选择序号
choose_j = 0


# 游戏开始菜单
class GameStart(Menu):
    def __init__(self):
        super(GameStart, self).__init__("爸爸向钱冲!")
        items = [
            (MenuItem('开始游戏', self.play_game)),
            (MenuItem('游戏帮助', self.help)),
            (MenuItem('退出', self.quit)),
        ]
        self.font_title['font_size'] = 100
        self.font_title['color'] = (250, 0, 0, 255)
        self.font_title['bold'] = True
        self.font_title['italic'] = True
        self.create_menu(items, selected_effect=self.rotate_effect(),
                         unselected_effect=self.rotate_effect_back(),
                         layout_strategy=fixedPositionMenuLayout([(500, 400), (500, 300), (500, 200)]))

    # 开始游戏
    def play_game(self):
        scene = Scene(Choose())
        director.replace(SplitColsTransition(scene))

    # 游戏说明
    def help(self):
        scene1 = Scene(HelpLayer())
        director.replace(SplitColsTransition(scene1))

    # 退出
    def quit(self):
        pyglet.app.exit()

    # 选择菜单后的翻转效果
    def rotate_effect(self):
        angle = 360
        duration = 0.5
        return Accelerate(RotateBy(angle, duration), 0.15)

    # 取消选择后的效果
    def rotate_effect_back(self):
        self.font_item['font_size'] = 35
        return RotateTo(0, 0)


class HelpLayer(Layer):
    is_event_handler = True

    def __init__(self):
        super(HelpLayer, self).__init__()
        self.label_show = Label("方向键控制小方块,空格键跳跃,可以进行两段式跳跃", font_size=28, color=(255, 255, 255, 255))
        self.label_show.position = (30, 400)
        self.add(self.label_show)
        self.show = Label("（按空格键返回）", font_size=30, color=(255, 255, 255, 255))
        self.show.position = (330, 300)
        self.add(self.show)

    def on_key_press(self, key, modifiers):
        k = symbol_string(key)
        if k == "SPACE":
            scene = Scene(GameStart())
            director.replace(SplitColsTransition(scene))

class Choose(Layer):
    is_event_handler = True
    global role_choose, choose_i

    def __init__(self):
        super(Choose, self).__init__()
        self.i = 1
        self.j = 0
        self.sprite = Sprite(role_choose[self.i])
        self.sprite.position = (500, 450)
        self.add(self.sprite)
        self.label = Label("爸爸", font_size=40, color=(255, 0, 0, 255), bold=1)
        self.label.position = (450, 180)
        self.add(self.label)
        self.label1 = Label("金钱崇拜", font_size=40, color=(0, 255, 0, 255), bold=1)
        self.label1.position = (390, 110)
        self.add(self.label1)
        self.label2 = Label("左右键选人，上下键换场景，空格键确认", font_size=30, color=(255, 255, 255, 255))
        self.label2.position = (100, 60)
        self.add(self.label2)

    def on_key_press(self, key, modifiers):
        k = symbol_string(key)
        if k == "UP":
            self.j -= 1
            if self.j < 0:
                self.j = 0
            if self.j == 2:
                self.label1.element.text = "纸醉金迷"
            elif self.j == 1:
                self.label1.element.text = "交易赌局"
            elif self.j == 0:
                self.label1.element.text = "金钱崇拜"
        elif k == "DOWN":
            self.j += 1
            if self.j > 2:
                self.j = 2
            if self.j == 2:
                self.label1.element.text = "纸醉金迷"
            elif self.j == 1:
                self.label1.element.text = "交易赌局"
            elif self.j == 0:
                self.label1.element.text = "金钱崇拜"
        elif k == "LEFT":
            self.i -= 1
            if self.i < 0:
                self.i = 0
            if self.i == 2:
                self.label.element.text = "爷爷"
            elif self.i == 1:
                self.label.element.text = "爸爸"
            elif self.i == 0:
                self.label.element.text = "老公"
            self.remove(self.sprite)
            self.sprite = Sprite(role_choose[self.i])
            self.sprite.position = (500, 450)
            self.add(self.sprite)
        elif k == "RIGHT":
            self.i += 1
            if self.i > 2:
                self.i = 2
            if self.i == 2:
                self.label.element.text = "爷爷"
            elif self.i == 1:
                self.label.element.text = "爸爸"
            elif self.i == 0:
                self.label.element.text = "老公"
            self.remove(self.sprite)
            self.sprite = Sprite(role_choose[self.i])
            self.sprite.position = (500, 450)
            self.add(self.sprite)
        elif k == "SPACE":
            global choose_i, choose_j
            choose_i = self.i
            choose_j = self.j
            print(choose_i)
            scene = Scene(GameLayer())
            director.replace(SplitColsTransition(scene))


# 障碍物生成
class Black(object):
    def __init__(self):
        super(Black, self).__init__()
        # 障碍物初始速度
        self.speed = 4
        w, h = self.random_black()
        # 生成一个障碍物
        self.black = cocos.layer.ColorLayer(210, 210, 0, 255, width=w, height=h)
        self.reset_status()

    # 随机生成宽高
    def random_black(self):
        width = random.randint(100, 200)
        height = random.randint(100, 300)
        return width, height

    # 重置障碍物坐标状态
    def reset_status(self):
        x = 1000
        y = 165
        self.black.position = (x, y)

    # 移动x坐标
    def move(self):
        x, y = self.black.position
        x -= self.speed
        self.black.position = (x, y)


# 主游戏界面
class GameLayer(Layer):
    is_event_handler = True

    def __init__(self):
        super(GameLayer, self).__init__()
        global role, choose_i, choose_j, scene_choose
        self.i = choose_i
        self.j = choose_j
        print(choose_i)
        # 3张图片导入
        self.sky = Sprite(scene_choose[self.j][1])
        self.sky.position = (500, 350)
        self.add(self.sky)
        self.sprite = Sprite(role[self.i])
        self.sprite.position = (10, 200)
        self.add(self.sprite)
        self.ground = Sprite(scene_choose[self.j][0])
        self.ground.position = (500, 60)
        self.add(self.ground)
        # 显示得分
        self.label_show = Label("财富：   亿", font_size=40, color=(255, 0, 0, 255))
        self.label_show.position = (720, 630)
        self.add(self.label_show)
        self.show = Label("0", font_size=40, color=(255, 0, 0, 255))
        self.show.position = (880, 630)
        self.add(self.show)
        # 生命
        self.life = 1
        # 前后移动速度
        self.speed = 6
        # 跳高速度
        self.jump_speed = 20
        # 重力速度
        self.g_speed = 5
        # 跳跃高度
        self.jump_high = 185
        # 按键状态
        status = False
        self.key_pressed_left = status
        self.key_pressed_right = status
        self.key_pressed_up = status
        self.key_pressed_down = status
        # 跳跃次数
        self.jump_count = 2
        # 跳跃到空中的坐标
        self.jump_y = 268
        # 生成障碍物
        self.black = Black()
        self.add(self.black.black)
        self.schedule(self.update)

    # 2次跳跃
    def jump(self):
        jump_high = self.jump_high
        x, y = self.sprite.position
        if y > self.jump_y + jump_high:
            self.key_pressed_up = False
        elif y > self.jump_y + jump_high * 0.8:
            self.g_speed = 3
        elif y > self.jump_y + jump_high * 0.5:
            self.g_speed = 6
        else:
            self.g_speed = 9

    # 判断矩形是否相撞
    def collision(self, rect1, rect2):
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        if x2 < x1 < x2 + w2:
            if y2 < y1 < y2 + h2:
                return True
        if x2 < x1 + w1 < x2 + w2:
            if y2 < y1 < y2 + h2:
                return True
        return False

    # 得到矩形的坐标与宽高
    def rect_of_sprite(self, sprite):
        x, y = sprite.position
        w, h = sprite.width, sprite.height
        rect1 = x, y, w, h
        return rect1

    # 得到图片矩形的坐标与宽高
    def rect_of_sprite1(self, sprite):
        x, y = sprite.position
        w, h = sprite.width, sprite.height
        easy = 20
        x -= sprite.width / 2
        y -= sprite.height / 2 - easy
        rect1 = x, y, w, h
        return rect1

    def on_mouse_press(self, x, y, buttons, modifiers):
        print('mouse press', x, y, buttons)
        print('size', self.sprite.width, self.sprite.height)

    # 实时更新
    def update(self, dt):
        x, y = self.sprite.position
        y -= self.g_speed
        if self.key_pressed_left:
            x -= self.speed
        if self.key_pressed_right:
            x += self.speed
        if self.key_pressed_up:
            y += self.jump_speed
        # 固定移动边界
        if y < 268:
            y = 268
        if x < 50:
            x = 50
        if x > 950:
            x = 950
        self.jump()
        self.sprite.position = x, y
        if y == 268:
            try:
                self.remove(self.jump1)
            except:
                pass
            self.jump_count = 2
            self.jump_speed = 20
            self.jump_y = 180
        self.black.move()
        if self.black.black.position[0] < -100:
            num = int(self.show.element.text) + 1
            self.show.element.text = str(num)
            self.remove(self.black.black)
            self.black = Black()
            self.add_speed()
            self.add(self.black.black)
        rect1 = self.rect_of_sprite1(self.sprite)
        rect2 = self.rect_of_sprite(self.black.black)
        if self.collision(rect1, rect2):
            self.game_over()

    # 障碍物速度变快
    def add_speed(self):
        num = int(self.show.element.text)
        level = 1
        value = 4
        for i in range(35):
            if level <= num < level + 1:
                self.black.speed = value
            level += 1
            value += 1

    # 游戏结束
    def game_over(self):
        self.life = 0
        try:
            self.remove(self.jump1)
        except:
            pass
        self.unschedule(self.update)
        global rect_x, rect_y
        rect_x, rect_y = self.sprite.position
        self.remove(self.sprite)
        self.stars = [Star() for i in range(100)]
        for s in self.stars:
            self.add(s.rect)
        self.schedule(self.baozha)
        self.label = Label("游戏结束", font_size=60, color=(0, 0, 0, 255), bold=1)
        self.label.position = (300, 400)
        self.label1 = Label("(按空格键重新开始)", font_size=30, color=(0, 128, 255, 255), bold=1)
        self.label1.position = (280, 300)
        self.add(self.label)
        self.add(self.label1)

    # 爆炸碎片移动
    def baozha(self, dt):
        for s in self.stars:
            s.move()

    # 按键控制
    def on_key_press(self, key, modifiers):
        k = symbol_string(key)
        status = True
        if k == "LEFT":
            self.key_pressed_left = status
        elif k == "RIGHT":
            self.key_pressed_right = status
        elif k == "SPACE" and self.life == 1:
            if self.jump_count > 0:
                x, y = self.sprite.position
                try:
                    self.remove(self.jump1)
                except:
                    pass
                # jump效果图
                self.jump1 = Sprite("images/jump.png")
                self.jump1.opacity = 250
                self.jump1.position = (x, y-100)
                self.add(self.jump1)
                self.jump_speed = 20
                self.jump_y = y
                self.key_pressed_up = True
                self.jump_count -= 1
        elif k == "DOWN":
            self.key_pressed_down = status
        elif k == "SPACE" and self.life == 0:
            scene = Scene(GameLayer())
            director.replace(SplitColsTransition(scene))

    # 松键控制
    def on_key_release(self, key, modifiers):
        k = symbol_string(key)
        status = False
        if k == "LEFT":
            self.key_pressed_left = status
        elif k == "RIGHT":
            self.key_pressed_right = status
        # elif k == "DOWN":
        #     self.key_pressed_down = status


# 爆炸碎片生成
class Star(object):
    def __init__(self):
        super(Star, self).__init__()
        global rect_x, rect_y
        self.speed = random.randint(2, 15)
        self.rect = cocos.layer.ColorLayer(34, 177, 76, 255, width=8, height=8)
        self.rect.position = rect_x, rect_y
        self.l_x = random.choice(['+', '-', ' '])
        self.l_y = random.choice(['+', '-', ' '])

    def move(self):
        x, y = self.rect.position
        if self.l_x == ' ' and self.l_y == ' ':
            self.l_y = '+'
        if self.l_x == '+':
            x += self.speed
        elif self.l_x == '-':
            x -= self.speed
        elif self.l_x == ' ':
            pass
        if self.l_y == '+':
            y += self.speed
        elif self.l_y == '-':
            y -= self.speed
        elif self.l_y == ' ':
            pass
        self.rect.position = (x, y)

if __name__ == '__main__':
    director.init(1000, 700)
    main_layer = GameStart()
    scene = scene.Scene(main_layer)
    director.set_show_FPS(main_layer)
    director.run(scene)
