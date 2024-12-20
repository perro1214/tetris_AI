import pprint
import pprint
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from tensorflow import keras
from tensorflow.keras import layers


# In[2]:


print("a")


# In[55]:

number = int(input())
with open(f'./data_gen/data_{number}.csv', 'r') as f:
    lis = f.read().split()
for i in range(len(lis)):
    lis[i] = list(map(int,(lis[i].split(","))))
arr=np.array(lis)
#pprint.pprint(arr,width=4000)


# In[56]:


# 1. データの生成 (サンプルデータ)
num_samples = arr.shape[0]
num_features = arr.shape[1]

# 入力データ: 220次元の正規分布に従う乱数を1000サンプル生成
X = arr[:,:-3]
y = arr[:,-3:]
# 目的変数: 2次元の正規分布に従う乱数を1000サンプル生成
# 例として、出力1は入力の最初の100個の和 + ノイズ, 出力2は入力の最後の120個の和 + ノイズ
#print(X,len(X[0]))
#print(y,len(y[0]))


# In[57]:


# 2. データの分割 (訓練データとテストデータ)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#print(len(X_train[0]),len(y_test[0]))


# In[58]:


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


# In[60]:


model.save(f"model_gen/gen_{number}.keras")
