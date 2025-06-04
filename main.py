import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
CHICK_INTERVAL = 15
FRAME_RATE = 30

#ひよころ生成クラス
class Chick:
    def __init__(self, x, y, life):
        self.x = x
        self.y = y
        self.life = life
        self.frame = 0
        self.isAnim = False
    
    def update(self):
        self.frame+=1

        if self.frame % CHICK_INTERVAL == 0:
            self.isAnim ^= True


    def draw(self):
        if self.isAnim:
            pyxel.blt(self.x, self.y, 0, 32, 0, 16, 16, pyxel.COLOR_BLACK)
        else:
            pyxel.blt(self.x, self.y, 0, 48, 0, 16, 16, pyxel.COLOR_BLACK)
        
        pyxel.text(self.x + 8, self.y + 8, f"{self.life}", pyxel.COLOR_RED)

    def isLifeCycle(self):
        if self.frame > 90:#生存
            return 1       
        elif self.life == 0:#死亡
            return 2
        else:
            return 0
        
    def damage(self):
        self.life -= 1


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="ひよころくりっく")
        pyxel.load("my_resource.pyxres")
        self.chicks = []
        self.score = 0
        self.level = 1
        self.time = 50
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            for chick in self.chicks:
                if chick.x <= pyxel.mouse_x <= chick.x + 16 and chick.y <= pyxel.mouse_y <= chick.y + 16:
                    chick.damage()

        if pyxel.frame_count % FRAME_RATE == 0:
            self.chicks.append(Chick(pyxel.rndi(0, SCREEN_WIDTH - 16), pyxel.rndi(20, SCREEN_HEIGHT - 16), 2 + self.level))
            self.time -= 1

        for chick in self.chicks.copy():
            chick.update()
            if chick.isLifeCycle() == 1:
                self.chicks.remove(chick)
            elif chick.isLifeCycle() == 2:
                self.score += 1
                self.chicks.remove(chick)

        self.level = 1 + (self.score // 10)

    def draw(self):
        pyxel.cls(pyxel.COLOR_DARK_BLUE)
        if self.time <= 0:
            pyxel.text(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT // 2, "Game Over", pyxel.COLOR_YELLOW)
            pyxel.text(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT // 2 + 10, f"score:{self.score}", pyxel.COLOR_WHITE)

        elif self.time > 0:
            #ひよころ
            for chick in self.chicks:
                chick.draw()

            #スコア
            pyxel.text(10, 0, f"score:{self.score}", pyxel.COLOR_WHITE)
            #レベル
            pyxel.text(60, 0, f"level:{self.level}", pyxel.COLOR_WHITE)
            #タイム
            pyxel.text(120, 0, f"time:{self.time}", pyxel.COLOR_WHITE)

            #ひなころ
            #pyxel.blt(pyxel.mouse_x - 8, SCREEN_HEIGHT - 16, 0, 16, 0, 16, 16, pyxel.COLOR_BLACK)

App()