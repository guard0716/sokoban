import pyxel

class Sokoban:
    def __init__(self):
        pyxel.init(160, 160, title="ひよころぷっしゅ")  # 10x10マスを16x16ピクセルで表示
        pyxel.load("my_resource.pyxres")
        self.TILE_SIZE = 16
        self.GRID_SIZE = 10
        # マップ: 0=空, 1=壁, 2=プレイヤー, 3=障害物, 4=ゴール, 5=ボール
        self.map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 3, 3, 3, 3, 3, 3, 0, 3, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 5, 0, 0, 0, 1],
            [1, 0, 3, 3, 3, 3, 3, 3, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 3, 3, 3, 3, 3, 3, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 4, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.player_x, self.player_y = 1, 1  # プレイヤーの初期位置
        self.game_cleared = False
        self.player_news = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_cleared:
            return

        # プレイヤー移動
        dx, dy = 0, 0
        if pyxel.btnp(pyxel.KEY_UP):
            dy = -1
            self.player_news = 1
        elif pyxel.btnp(pyxel.KEY_DOWN):
            dy = 1
            self.player_news = 0
        elif pyxel.btnp(pyxel.KEY_LEFT):
            dx = -1
            self.player_news = 2
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            dx = 1
            self.player_news = 3

        if dx != 0 or dy != 0:
            new_x, new_y = self.player_x + dx, self.player_y + dy
            # マップ範囲内かチェック
            if 0 <= new_x < self.GRID_SIZE and 0 <= new_y < self.GRID_SIZE:
                # 移動先が空(0)またはゴール(4)の場合
                if self.map[new_y][new_x] in [0, 4]:
                    self.map[self.player_y][self.player_x] = 0
                    self.player_x, self.player_y = new_x, new_y
                    self.map[new_y][new_x] = 2
                # 移動先が障害物(3)の場合
                elif self.map[new_y][new_x] == 3:
                    # 障害物の先の座標
                    next_x, next_y = new_x + dx, new_y + dy
                    # 先が範囲内で空(0)またはゴール(4)の場合、障害物を押す
                    if (0 <= next_x < self.GRID_SIZE and 0 <= next_y < self.GRID_SIZE and
                        self.map[next_y][next_x] in [0, 4]):
                        self.map[self.player_y][self.player_x] = 0
                        self.map[new_y][new_x] = 2
                        self.map[next_y][next_x] = 3
                        self.player_x, self.player_y = new_x, new_y
                elif self.map[new_y][new_x] == 5:
                    # 障害物の先の座標
                    next_x, next_y = new_x + dx, new_y + dy
                    # 先が範囲内で空(0)またはゴール(4)の場合、障害物を押す
                    if (0 <= next_x < self.GRID_SIZE and 0 <= next_y < self.GRID_SIZE and
                        self.map[next_y][next_x] in [0, 4]):
                        self.map[self.player_y][self.player_x] = 0
                        self.map[new_y][new_x] = 2
                        self.map[next_y][next_x] = 5
                        self.player_x, self.player_y = new_x, new_y


        # ゴール判定
        if self.map[8][8] == 5:
            self.game_cleared = True

    def draw(self):
        pyxel.cls(pyxel.COLOR_GREEN)  # 画面クリア
        for y in range(self.GRID_SIZE):
            for x in range(self.GRID_SIZE):
                tile = self.map[y][x]
                pixel_x, pixel_y = x * self.TILE_SIZE, y * self.TILE_SIZE
                if tile == 0:  # 空
                    pyxel.rect(pixel_x, pixel_y, self.TILE_SIZE, self.TILE_SIZE, pyxel.COLOR_GREEN)
                elif tile == 1:  # 壁
                    pyxel.blt(pixel_x, pixel_y, 0, 0, 48, 16, 16, pyxel.COLOR_BLACK)
                elif tile == 2:  # プレイヤー
                    if self.player_news == 1:#上向き
                        pyxel.blt(pixel_x, pixel_y, 0, 16, 32, 16, 16, pyxel.COLOR_BLACK)
                    elif self.player_news == 2:#左向き
                        pyxel.blt(pixel_x, pixel_y, 0, 0, 32, 16, 16, pyxel.COLOR_BLACK)
                    elif self.player_news == 3:#右向き
                        pyxel.blt(pixel_x, pixel_y, 0, 48, 32, 16, 16, pyxel.COLOR_BLACK)
                    else :#下向き
                        pyxel.blt(pixel_x, pixel_y, 0, 32, 32, 16, 16, pyxel.COLOR_BLACK)
                elif tile == 3:  # 障害物
                    pyxel.blt(pixel_x, pixel_y, 0, 48, 16, 16, 16, pyxel.COLOR_BLACK)
                elif tile == 4:  # ゴール
                    pyxel.blt(pixel_x, pixel_y, 0, 32, 16, 16, 16, pyxel.COLOR_BLACK)
                elif tile == 5:  # ボール
                    pyxel.blt(pixel_x, pixel_y, 0, 0, 16, 16, 16, pyxel.COLOR_BLACK)

        if self.game_cleared:
            pyxel.text(50, 80, "Game Cleared!", 10)

Sokoban()