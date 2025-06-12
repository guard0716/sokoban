import pyxel
import copy

class Sokoban:
    def __init__(self):
        pyxel.init(160, 160, title="ひよころぷっしゅ")  # 10x10マスを16x16ピクセルで表示
        pyxel.load("my_resource.pyxres")
        self.TILE_SIZE = 16
        self.GRID_SIZE = 9
        self.state = "TITLE"  # 初期状態：タイトル画面
        self.game_over_timer = 0  # ゲームオーバー画面のタイマー
        self.stage_change_timer = 0  # ゲームオーバー画面のタイマー
        self.stage = 1
        # マップ: 0=空, 1=壁, 2=プレイヤー, 3=障害物, 4=ゴール, 5=ボール
        self.map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 0, 3, 3, 0, 0, 0, 1],
            [1, 0, 3, 0, 3, 0, 0, 0, 1],
            [1, 0, 0, 0, 5, 0, 0, 0, 1],
            [1, 0, 0, 0, 3, 0, 0, 0, 1],
            [1, 0, 0, 0, 3, 0, 0, 0, 1],
            [1, 0, 3, 3, 3, 3, 3, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 4, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.map_history = [copy.deepcopy(self.map)]  # 初期マップを保存
        self.player_x, self.player_y = 1, 1  # プレイヤーの初期位置
        self.player_news = 0
        pyxel.run(self.update, self.draw)

    def find_player(self):
        #マップからプレイヤーの位置を検索
        for y in range(9):
            for x in range(9):
                if self.map[y][x] == 2:
                    self.player_x = x
                    self.player_y = y
                    return

    def update(self):
        if self.state == "TITLE":
            # タイトル画面：任意のキーでゲーム画面へ
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_LEFT):
                self.initValue("STAGE")

        elif self.state == "GAME_OVER":
            # ゲームオーバー画面：5秒後にタイトル画面へ
            self.game_over_timer += 1
            if self.game_over_timer >= 5 * 30:  # 5秒（30fpsで150フレーム）
                self.initValue("TITLE")

        elif self.state == "STAGE":
            # ステージ画面：3秒後にゲーム画面へ
            self.stage_change_timer += 1
            if self.stage_change_timer >= 3 * 30:  # 5秒（30fpsで150フレーム）
                self.initValue("GAME")

        elif self.state == "GAME":

            # 一手戻る（Zキー）
            if pyxel.btnp(pyxel.KEY_Z) and len(self.map_history) > 1:
                self.map_history.pop()  # 最新の状態を削除
                self.map = copy.deepcopy(self.map_history[-1])  # 直前の状態を復元
                self.find_player()            

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
                self.map_history.append(copy.deepcopy(self.map))  # 状態保存

            # ゴール判定
            if self.map[7][7] == 5:
                self.stage += 1
                self.initValue("STAGE")

    def draw(self):
        pyxel.cls(pyxel.COLOR_GREEN)  # 画面クリア

        if self.state == "TITLE":
            pyxel.text(50, 70, "Hiyokoro Push!", 7)
            pyxel.text(50, 80, "Press Any Arrow", 7)

        elif self.state == "GAME_OVER":
            pyxel.text(50, 70, "Game Cleared!", 10)
            pyxel.text(50, 80, "Back to title in 5s", 7)

        elif self.state == "STAGE":
            pyxel.text(60, 75, F"Stage {self.stage}", 10)

        elif self.state == "GAME":
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


    def initValue(self,state):
        if state == "TITLE":
            self.state = "TITLE"  # 初期状態：タイトル画面
            self.game_over_timer = 0  # ゲームオーバー画面のタイマー
            self.stage_change_timer = 0  # ゲームオーバー画面のタイマー
            self.stage = 1
            self.player_x, self.player_y = 1, 1  # プレイヤーの初期位置
            self.player_news = 0
        elif state == "GAME_OVER":
            self.state = "GAME_OVER"  # 初期状態：タイトル画面

        elif state == "GAME":
            self.state = "GAME"  # 初期状態：タイトル画面
            self.game_over_timer = 0  # ゲームオーバー画面のタイマー
            self.stage_change_timer = 0  # ゲームオーバー画面のタイマー
            self.player_x, self.player_y = 1, 1  # プレイヤーの初期位置
            self.game_cleared = False
            self.player_news = 0

        elif state == "STAGE":
            self.state = "STAGE"
            self.map_history.clear()
            if self.stage == 1:
                self.map = [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 2, 0, 3, 3, 0, 0, 0, 1],
                    [1, 0, 3, 0, 3, 0, 0, 0, 1],
                    [1, 0, 0, 0, 5, 0, 0, 0, 1],
                    [1, 0, 0, 0, 3, 0, 0, 0, 1],
                    [1, 0, 0, 0, 3, 0, 0, 0, 1],
                    [1, 0, 3, 3, 3, 3, 3, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 4, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1]
                ]

            elif self.stage == 2:
                self.map = [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 2, 0, 3, 3, 0, 0, 0, 1],
                    [1, 0, 3, 0, 0, 3, 0, 0, 1],
                    [1, 0, 0, 0, 0, 3, 0, 0, 1],
                    [1, 0, 0, 0, 5, 0, 0, 0, 1],
                    [1, 0, 0, 3, 0, 0, 0, 0, 1],
                    [1, 0, 3, 3, 3, 3, 3, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 4, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1]
                ]

            elif self.stage == 3:
                self.map = [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 2, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 3, 3, 3, 3, 3, 0, 1],
                    [1, 0, 0, 0, 0, 0, 3, 0, 1],
                    [1, 0, 3, 3, 5, 3, 3, 0, 1],
                    [1, 0, 0, 0, 0, 0, 3, 0, 1],
                    [1, 0, 3, 3, 3, 3, 3, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 4, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1]
                ]

            elif self.stage == 4:
                self.map = [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 2, 3, 0, 3, 0, 0, 0, 1],
                    [1, 0, 3, 0, 3, 0, 0, 0, 1],
                    [1, 0, 3, 0, 3, 0, 0, 0, 1],
                    [1, 0, 3, 3, 5, 3, 3, 0, 1],
                    [1, 0, 0, 0, 3, 0, 0, 0, 1],
                    [1, 0, 0, 0, 3, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 4, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1]
                ]    

            elif self.stage == 5:
                self.map = [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 2, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 3, 3, 3, 3, 3, 0, 1],
                    [1, 0, 3, 0, 0, 0, 0, 0, 1],
                    [1, 0, 3, 3, 5, 3, 3, 0, 1],
                    [1, 0, 0, 0, 0, 0, 3, 0, 1],
                    [1, 0, 3, 3, 3, 3, 3, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 4, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1]
                ]

            elif self.stage == 6:
                self.initValue("GAME_OVER")

            self.map_history = [copy.deepcopy(self.map)]  # 初期マップを保存


Sokoban()