from tetris_class_constant import Tetris,BOARD_WIDTH, BOARD_HEIGHT

import numpy as np
import keras

# ゲーム開始
if __name__ == "__main__":
    argv,size = input().split()
    size = int(size)
    model = keras.models.load_model(f'model_gen/gen_{int(argv)-1}.keras')
    score = 0
    #for i in range(1):
    for i in range(1,size+1):
        game = Tetris([[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)],model)
        score += game.run(False,gen = argv)
        if(i%10 == 0):
            print(i)
    with open(f"score.csv","a") as f:
        f.write(f'model_gen/gen_{int(argv)-1}.keras'+" , "+str(score/size)+"\n")



# import keras
# import multiprocessing
# from tqdm import tqdm

# def run_game(args):
#     """個々のゲームを実行する関数 (並列処理で実行)"""
#     game_index, argv, model = args
#     game = Tetris([[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)], model)
#     print(game_index)
#     game.run(False)
#     if game_index % 10 == 0:
#         print(game_index)


# if __name__ == "__main__":
#     argv, size_str = input().split()
#     size = int(size_str)
#     model = keras.models.load_model(f'model_gen/gen_{argv}.keras')

#     # 並列処理を行う
#     with multiprocessing.Pool() as pool:
#         list(tqdm(pool.imap(run_game, [(i, argv, model) for i in range(1, size + 1)]), total=size))

#     print("全てのゲームが終了しました")