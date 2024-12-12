import random
from collections import deque
import time

import csv
import pprint

# ボードサイズ
BOARD_WIDTH = 10
BOARD_HEIGHT = 22

# テトリミノの形状 (数字はブロックの種類を表す)
# SHAPES = [
#     [[0, 0, 0, 0],
#     [1, 1, 1, 1]],  # I

#     [[1, 1],  # O
#      [2, 2]],

#     [[0, 3, 0],  # T
#      [3, 3, 3]],

#     [[0, 4, 4],  # S
#      [4, 4, 0]],

#     [[5, 5, 0],  # Z
#      [0, 5, 5]],

#     [[6, 0, 0],  # J
#      [6, 6, 6]],

#     [[0, 0, 7],  # L
#      [7, 7, 7]]
# ]

SHAPES = [
    [[0, 0, 0, 0],
    [1, 1, 1, 1]],  # I

    [[1, 1],  # O
     [1, 1]],

    [[0, 1, 0],  # T
     [1, 1, 1]],

    [[0, 1, 1],  # S
     [1, 1, 0]],

    [[1, 1, 0],  # Z
     [0, 1, 1]],

    [[1, 0, 0],  # J
     [1, 1, 1]],

    [[0, 0, 1],  # L
     [1, 1, 1]]
]

# テトリミノの初期位置
SPAWN_POSITION = (3, 0)  # 修正: ボードの中央に初期位置を設定

# ブロックを表す文字
BLOCK_CHARS = {
    0: " .",  # 空
    1: "[]",  # I
    2: "[]",  # O
    3: "[]",  # T
    4: "[]",  # S
    5: "[]",  # Z
    6: "[]",  # J
    7: "[]"   # L
}

# ゲームクラス
class Tetris:
    def __init__(self,inpu):
        self.board = inpu
        self.current_piece = self.new_piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.fall_speed = 0  # 落下速度（秒間隔）
        self.last_fall_time = time.time()

    def new_piece(self):
        # ランダムに新しいテトリミノを生成
        shape = random.choice(SHAPES)
        return {
            'shape': shape,
            'color': SHAPES.index(shape) + 1,
            'position': list(SPAWN_POSITION),
            'rotation': 0
        }

    def print_board(self):
        # 操作中のピースを一時的にボードにコピー
        temp_board = [row[:] for row in self.board]
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    piece_x = self.current_piece['position'][0] + x
                    piece_y = self.current_piece['position'][1] + y
                    if 0 <= piece_x < BOARD_WIDTH and 0 <= piece_y < BOARD_HEIGHT:
                        temp_board[piece_y][piece_x] = self.current_piece['color']

        # ボードを描画
        print("+" + "---+" * BOARD_WIDTH + "   ")
        for row_index, row in enumerate(temp_board):
            # スコアなどの情報を各行の先頭に追加
            if row_index == 0:
                row_str = f"| Score: {self.score:5d} | "
            elif row_index == 1:
                row_str = f"| Level: {self.level:5d} | "
            else:
                row_str = " "*16+"|"

            # 各セルの文字を追加
            for cell in row:
                row_str += BLOCK_CHARS[cell]

            # 行の末尾に縦線を追加
            row_str += " |"
            print(row_str)
        print("+" + "---+" * BOARD_WIDTH + "---")

        # 操作説明
        print(" a: 左, d: 右, w: 回転, s: ソフトドロップ, space: ハードドロップ, q: 終了")

    def valid_move(self, piece, x, y, rotation):
        # 指定された位置にテトリミノが移動可能かチェック
        shape = piece['shape']
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col]:
                    new_x, new_y = x + col, y + row
                    # ボードの範囲外チェック
                    if new_x < 0 or new_x >= BOARD_WIDTH or new_y >= BOARD_HEIGHT:
                        return False
                    # 他のブロックとの衝突チェック
                    if new_y >= 0 and self.board[new_y][new_x]:
                        return False
        return True

    def place_piece(self, piece):
        # テトリミノをボードに配置
        shape = piece['shape']
        x, y = piece['position']
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col]:
                    #self.board[y + row][x + col] = piece['color']
                    self.board[y + row][x + col] = 1

    def clear_lines(self):
        # そろったラインを消去し、スコアを更新
        lines_to_clear = [index for index, row in enumerate(self.board) if all(cell != 0 for cell in row)]
        if lines_to_clear:
            for index in lines_to_clear:
                del self.board[index]
                self.board.insert(0, [0] * BOARD_WIDTH)
            self.lines_cleared += len(lines_to_clear)
            self.score += {1: 40, 2: 100, 3: 300, 4: 1200}.get(len(lines_to_clear), 0) * self.level

            # レベルの更新
            if self.lines_cleared >= self.level * 10:
                self.level += 1
                self.fall_speed = max(0.1, self.fall_speed - 0.1)

    def rotate_piece(self, piece):
        # テトリミノを回転
        new_shape = list(zip(*piece['shape'][::-1]))
        new_piece = {
            'shape': new_shape,
            'color': piece['color'],
            'position': piece['position'][:],
            'rotation': (piece['rotation'] + 1) % 4
        }

        if self.valid_move(new_piece, *new_piece['position'], new_piece['rotation']):
            return new_piece
        else:
            return piece

    def move_piece_down(self):
        # テトリミノを1マス下に移動
        x, y = self.current_piece['position']
        if self.valid_move(self.current_piece, x, y + 1, self.current_piece['rotation']):
            self.current_piece['position'][1] += 1
            self.last_fall_time = time.time()
        else:
            self.place_piece(self.current_piece)
            self.clear_lines()
            self.current_piece = self.new_piece()
            if not self.valid_move(self.current_piece, *self.current_piece['position'], self.current_piece['rotation']):
                self.game_over = True

    def move_piece_sideways(self, direction):
        # テトリミノを左右に移動
        x, y = self.current_piece['position']
        new_x = x + direction
        if self.valid_move(self.current_piece, new_x, y, self.current_piece['rotation']):
            self.current_piece['position'][0] = new_x

    def hard_drop(self):
        # テトリミノを一気に下に落とす
        while self.valid_move(self.current_piece, self.current_piece['position'][0], self.current_piece['position'][1] + 1, self.current_piece['rotation']):
            self.current_piece['position'][1] += 1
        self.place_piece(self.current_piece)
        self.clear_lines()
        self.current_piece = self.new_piece()
        if not self.valid_move(self.current_piece, *self.current_piece['position'], self.current_piece['rotation']):
            self.game_over = True
    
    def point(self):
        temp_board = [row[:] for row in self.board]
        for s in range(10):
            ne = deque([[0,s]])
            UD = [(-1,0),(1,0)]
            while(len(ne)!=0):
                x,y = ne.popleft()
                for a,b in UD:
                    if not(0<=(x+a)<BOARD_HEIGHT and 0<=(y+b)<BOARD_WIDTH):
                        continue
                    if temp_board[x][y] == 0:
                        temp_board[x][y] = 1
                    if temp_board[x+a][y+b] == 0:
                        temp_board[x+a][y+b] = 1
                        ne.append([x+a,y+b])
        result = 0
        #for i in temp_board:
            #print(i)
        for i in temp_board:
            for j in i:
                if j == 0:
                    result+=1

        return result
    
    def make_input(self):
        # if(random.randint(0,1) == 0):
        #     return random.randint(0,3),0,random.randint(0,3)
        # else:
        #     return 0,random.randint(0,4),random.randint(0,3)
        aaa import numpy as np
        aaa predictions = model.predict(new_data)
        aaa print(predictions)




    def run(self):
        # メインゲームループ
        while not self.game_over:
        #for i in list(move):
            if(self.game_over):
                break
            ##self.print_board()
            Before = self.point()
            old_board = [row[:] for row in self.board]
            # ユーザー入力を処理 (キー入力を待機)
            #user_input = input(" 操作を入力: ").lower()
            #user_input = i
            
            #user_inputs = move.pop(0)
            user_inputs = self.make_input()
            for user_input in list(user_inputs[2]*"w" + user_inputs[0]*"a" + user_inputs[1]*"d" ):
                if user_input == 'q':
                    self.game_over = True
                elif user_input == 'a':
                    self.move_piece_sideways(-1)
                elif user_input == 'd':
                    self.move_piece_sideways(1)
                elif user_input == 'w':
                    self.current_piece = self.rotate_piece(self.current_piece)
                elif user_input == 's':
                    self.move_piece_down()
                
                if self.game_over:
                    break
            self.hard_drop()

            und = []
            new_board = [row[:] for row in self.board]
            for i in range(len(old_board)):
                for a in range(len(old_board[i])):
                    if new_board[i][a]!=old_board[i][a]:
                        und.append([i,a])
            
            flat = []
            for i in old_board:
                flat += i
            
            
            # 一定時間ごとにテトリミノを下に移動
            # if time.time() - self.last_fall_time > self.fall_speed:
            #     self.move_piece_down()
            After = self.point()
            # print(flat)
            # print(Before - After)
            # print(max([i[0] for i in und]))
            # print()
            m = (list(user_inputs)+ list(map(str,flat)) + [str(Before - After)] + [str(max([i[0] for i in und]))] )
            # print(",".join(m))
            with open('sample_writer_row.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(m)

            # if(not move):
            #     break

        # print("ゲームオーバー！")
        ##self.print_board()

# ゲーム開始
if __name__ == "__main__":
    for i in range(1000):
        game = Tetris([[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)])
        game.run()
        if(i%100 == 0):
            print(i)