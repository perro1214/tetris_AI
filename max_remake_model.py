import pprint
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from tensorflow import keras
from tensorflow.keras import layers

number = int(input())

if number != 0:
    with open('score.csv', 'r') as file:
        score_lis = []
        for i,line in enumerate(file):
            if i%5 == 0:
                score_lis.append([line.strip().split(',')[0],float(line.strip().split(',')[1])])
            else:
                score_lis[i//5][1] += float(line.strip().split(',')[1])
    score_lis = list(map(lambda x: [x[0],x[1]/5], score_lis))
    #score_lis = sorted(score_lis, key=lambda x: x[1], reverse=True)
    result = score_lis[0][0].replace("model_gen/gen_", "").replace(".keras", "")

with open(f'./data_gen/data_{number[0]}.csv', 'r') as f:
    lis = f.read().split()
for i in range(len(lis)):
    lis[i] = list(map(int,(lis[i].split(","))))
arr=np.array(lis)


# 1. データの生成 (サンプルデータ)
num_samples = arr.shape[0]
num_features = arr.shape[1]

# 入力データ
X = arr[:,:-3]
y = arr[:,-3:]

# 2. データの分割 (訓練データとテストデータ)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#print(len(X_train[0]),len(y_test[0]))

# 3. モデルの構築
model = keras.models.load_model(f'model_gen/gen_{number - 1}.keras')

# 5. モデルの学習
model.fit(X_train, y_train, epochs=5, batch_size=32, validation_split=0.1, verbose=1)

# 6. モデルの評価
y_pred = model.predict(X_test)

# 評価指標の計算
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"R2 Score: {r2:.4f}")

# 7. (オプション) 予測結果の確認
print("最初の5つの予測結果:")
for i in range(5):
    formatted_y_pred = [f"{val:.5f}" for val in y_pred[i]]
    formatted_y_test = [f"{val:.5f}" for val in y_test[i]]
    print(f"予測: {formatted_y_pred}, 実際: {formatted_y_test}")


model.save(f"model_gen/gen_{number}.keras")