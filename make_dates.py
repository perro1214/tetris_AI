from tetris_class_constant import Tetris,get_ai_generation_status,BOARD_WIDTH, BOARD_HEIGHT

import numpy as np
import keras
import keras
import multiprocessing
from tqdm import tqdm

# def get_ai_generation_status():
#     with open("score.csv","r") as f:
#         generation_count = sum(1 for line in f)
#     if generation_count != 0:
#         generation_count = generation_count//5
#         with open('score.csv', 'r') as file:
#             Y = []
#             for i,line in enumerate(file):
#                 if i%5 == 0:
#                     Y.append([line.strip().split(',')[0],float(line.strip().split(',')[1])])
#                 else:
#                     Y[i//5][1] += float(line.strip().split(',')[1])
#         Y = list(map(lambda x: [x[0],x[1]/5], Y))
#         Y = sorted(Y, key=lambda x: x[1], reverse=True)
#         max_score_AI = Y[0][0].replace("model_gen/gen_", "").replace(".keras", "").replace(" ","")
#     else:
#         max_score_AI = -1
#     return max_score_AI,generation_count

def run_game(args):
    """個々のゲームを実行する関数 (並列処理で実行)"""
    game_index = args
    game = Tetris([[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)],"_")
    game.run(not_use_AI=True)
    if game_index % 10 == 0:
      print(game_index)

# ゲーム開始
if __name__ == "__main__":
    max_score_AI,generation_count=get_ai_generation_status()
    size = int(input()) # 試行回数
    if generation_count == 0:
        # 並列処理を行う
        with multiprocessing.Pool() as pool:
            list(tqdm(pool.imap(run_game, [(i) for i in range(1, size + 1)]), total=size))
        with open(f"score.csv","a") as f:
            f.write(f'model_gen/gen_{generation_count}.keras'+" , "+str(0)+"\n")
        print("全てのゲームが終了しました")
    else:
        model = keras.models.load_model(f'model_gen/gen_{int(max_score_AI)}.keras')
        score = 0
        for i in range(1,size+1):
            game = Tetris([[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)],model)
            score += game.run(not_use_AI=False,gen = generation_count,make_scv_mame=generation_count)
            if(i%10 == 0):
                print(i)
        with open(f"score.csv","a") as f:
            if(score == 0):
                f.write(f'model_gen/gen_{generation_count}.keras'+" , "+str(0)+"\n")
            else:
                f.write(f'model_gen/gen_{generation_count}.keras'+" , "+str(score/size)+"\n")