from tetris_class_constant import Tetris,get_ai_generation_status,BOARD_WIDTH, BOARD_HEIGHT

import numpy as np
import keras

# ゲーム開始

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

if __name__ == "__main__":
    max_score_AI,generation_count=get_ai_generation_status()
    print(max_score_AI,generation_count)
    print(f'model_gen/gen_{generation_count - 1}.keras')
    model = keras.models.load_model(f'model_gen/gen_{generation_count - 1}.keras')
    for i in range(1):
        import datetime
        now = datetime.datetime.now()
        print(now)
        game = Tetris([[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)],model)
        game.run(False,print_flag="print")
        if(i%10 == 0):
            print(i)