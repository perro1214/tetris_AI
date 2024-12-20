from tetris_class_constant import Tetris,BOARD_WIDTH, BOARD_HEIGHT



# # ゲーム開始
# if __name__ == "__main__":
#     argv,size = input().split()
#     size = int(size)
#     for i in range(1,size):
#     #for i in range(1,11):
#         game = Tetris([[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)],"_")
#         game.run(True)
#         if(i%10 == 0):
#             print(i)


import keras
import multiprocessing
from tqdm import tqdm

def run_game(args):
    """個々のゲームを実行する関数 (並列処理で実行)"""
    game_index, argv, model = args
    game = Tetris([[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)],"_")
    game.run(True)
    if game_index % 10 == 0:
      print(game_index)


if __name__ == "__main__":
    argv, size_str = input().split()
    size = int(size_str)

    # 並列処理を行う
    with multiprocessing.Pool() as pool:
        list(tqdm(pool.imap(run_game, [(i, argv,"_") for i in range(1, size + 1)]), total=size))

    print("全てのゲームが終了しました")