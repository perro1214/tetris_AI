#!/usr/bin/env python
# coding: utf-8

# In[24]:


import pprint
import pprint
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from tensorflow import keras
from tensorflow.keras import layers


# In[26]:


with open('data.csv', 'r') as f:
    lis = f.read().split()
for i in range(len(lis)):
    lis[i] = list(map(int,(lis[i].split(","))))
arr=np.array(lis)


# In[27]:


arr.shape


# In[28]:


# 1. データの生成 (サンプルデータ)
num_samples = arr.shape[0]
num_features = arr.shape[1]

# 入力データ: 220次元の正規分布に従う乱数を1000サンプル生成
X = arr[:,:-3]
y = arr[:,-3:]
# 目的変数: 2次元の正規分布に従う乱数を1000サンプル生成
# 例として、出力1は入力の最初の100個の和 + ノイズ, 出力2は入力の最後の120個の和 + ノイズ


# In[29]:


# 2. データの分割 (訓練データとテストデータ)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# In[30]:


# 3. モデルの構築
model = keras.Sequential(
    [
        layers.Dense(128, activation="relu", input_shape=(224,)),  # ここを修正
        layers.Dense(64, activation="relu"),
        layers.Dense(32, activation="relu"),
        layers.Dense(16, activation="relu"),
        layers.Dense(3),
    ]
)
# 4. モデルのコンパイル
model.compile(optimizer="adam", loss="mse", metrics=["mae"])

# 5. モデルの学習
model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.1, verbose=1)

# 6. モデルの評価
y_pred = model.predict(X_test)

# 評価指標の計算
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# print(f"Mean Squared Error (MSE): {mse:.4f}")
# print(f"Mean Absolute Error (MAE): {mae:.4f}")
# print(f"R2 Score: {r2:.4f}")

# # 7. (オプション) 予測結果の確認
# print("最初の5つの予測結果:")
# for i in range(5):
#     print(f"予測: {y_pred[i]}, 実際: {y_test[i]}")


# In[33]:


# print("最初の5つの予測結果:")
# for i in range(5):
#     print("予測: {:.3f}, 実際: {:.3f}".format(y_pred[i][0],y_test[i][0]))


# In[36]:

argv = int(input())
model.save(f"model_gen/model_{argv}.h5")

