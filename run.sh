#!/bin/bash

# 仮想環境のセットアップ
if [ ! -d "venv" ]; then
    echo "仮想環境を作成します..."
    python3.10 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

size1=5000
size2=100
mkdir -p gen
mkdir -p model_gen
mkdir -p data_gen
touch score.csv
if [ $# -eq 0 ]; then
    echo "引数が指定されていません。デフォルトの5回繰り返し動作を実行します。"
    start=0
    count=5
elif [ $# -eq 1 ];then
    start=0
    count=$1
else
  echo "エラー: 引数の数は1つである必要があります。"
  exit 1
fi

for ((i=start; i<count; i++));
do
    current_datetime=$(date)
    echo "gen_test: $current_datetime $i/$count"
    (echo $(expr $size2 / 5)| ./venv/bin/python3 make_dates.py)&
    (echo $(expr $size2 / 5)| ./venv/bin/python3 make_dates.py)& 
    (echo $(expr $size2 / 5)| ./venv/bin/python3 make_dates.py)& 
    (echo $(expr $size2 / 5)| ./venv/bin/python3 make_dates.py)& 
    (echo $(expr $size2 / 5)| ./venv/bin/python3 make_dates.py)&
    wait
    ./venv/bin/python3 make_model.py 2> error.txt
    ./venv/bin/python3 tetris-one.py 2> error.txt
done

current_datetime=$(date)
echo "gen_test: $current_datetime $count/$count"