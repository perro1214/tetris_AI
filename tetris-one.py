from tetris_class_constant import Tetris,BOARD_WIDTH, BOARD_HEIGHT

import numpy as np
import keras

# ゲーム開始
if __name__ == "__main__":
    argv = int(input())
    model = keras.models.load_model(f'model_gen/gen_{argv}.keras')
    for i in range(1):
        import datetime
        now = datetime.datetime.now()
        print(now)
        game = Tetris([[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)],model)
        game.run(False,print_flag="print")
        if(i%10 == 0):
            print(i)